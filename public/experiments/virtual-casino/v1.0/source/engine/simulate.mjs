import { hashObject, sha256, stream } from "./random.mjs";
import { calculateStake, chooseBet, chooseGame, scheduleSessions } from "./policies.mjs";
import { settleGame } from "./games.mjs";

const ZERO_HASH = "0".repeat(64);

function initialState(config, policy) {
  return {
    playerId: policy.playerId,
    cohortId: policy.cohortId,
    bankrollCents: config.allocationCents,
    bankrollMonth: 1,
    allocationsUsed: 1,
    cumulativeAllocatedCents: config.allocationCents,
    cumulativeTurnoverCents: 0,
    cumulativePayoutCents: 0,
    cumulativeExpectedPnlCents: 0,
    wagerCount: 0,
    sessionsCompleted: 0,
    ruinCount: 0,
    firstRuinAt: null,
    peakBankrollCents: config.allocationCents,
    maximumDrawdownCents: 0,
    winStreak: 0,
    lossStreak: 0,
    longestWinStreak: 0,
    longestLossStreak: 0,
    cooldownRemaining: 0,
    status: "active",
    gameStats: {},
    stakeSumCents: 0,
    stakes: [],
    allocationWagers: 0,
    allocationTurnoverCents: 0,
    allocationStartedAt: config.calendarStart,
  };
}

function policyStateForHash(state) {
  return {
    bankrollCents: state.bankrollCents,
    bankrollMonth: state.bankrollMonth,
    allocationsUsed: state.allocationsUsed,
    wagerCount: state.wagerCount,
    winStreak: state.winStreak,
    lossStreak: state.lossStreak,
    status: state.status,
  };
}

function serialisableState(state) {
  const sortedStakes = [...state.stakes].sort((a, b) => a - b);
  return {
    playerId: state.playerId,
    cohortId: state.cohortId,
    currentBankrollCents: state.bankrollCents,
    bankrollMonth: state.bankrollMonth,
    allocationsUsed: state.allocationsUsed,
    cumulativeAllocatedCents: state.cumulativeAllocatedCents,
    cumulativeTurnoverCents: state.cumulativeTurnoverCents,
    cumulativePayoutCents: state.cumulativePayoutCents,
    cumulativeExpectedPnlCents: state.cumulativeExpectedPnlCents,
    netPnlCents: state.bankrollCents - state.cumulativeAllocatedCents,
    deviationFromExpectationCents: state.bankrollCents - state.cumulativeAllocatedCents - state.cumulativeExpectedPnlCents,
    wagerCount: state.wagerCount,
    sessionsCompleted: state.sessionsCompleted,
    ruinCount: state.ruinCount,
    firstRuinAt: state.firstRuinAt,
    peakBankrollCents: state.peakBankrollCents,
    maximumDrawdownCents: state.maximumDrawdownCents,
    longestWinStreak: state.longestWinStreak,
    longestLossStreak: state.longestLossStreak,
    averageStakeCents: state.wagerCount ? Math.round(state.stakeSumCents / state.wagerCount) : 0,
    medianStakeCents: sortedStakes.length ? sortedStakes[Math.floor(sortedStakes.length / 2)] : 0,
    realisedRtp: state.cumulativeTurnoverCents ? state.cumulativePayoutCents / state.cumulativeTurnoverCents : 0,
    status: state.status,
    gameStats: state.gameStats,
  };
}

function updateState(state, gameId, stakeCents, settlement) {
  const netPnlCents = settlement.grossPayoutCents - stakeCents;
  state.bankrollCents += netPnlCents;
  state.cumulativeTurnoverCents += stakeCents;
  state.cumulativePayoutCents += settlement.grossPayoutCents;
  state.cumulativeExpectedPnlCents += settlement.expectedGrossCents - stakeCents;
  state.wagerCount += 1;
  state.allocationWagers += 1;
  state.allocationTurnoverCents += stakeCents;
  state.stakeSumCents += stakeCents;
  state.stakes.push(stakeCents);
  state.peakBankrollCents = Math.max(state.peakBankrollCents, state.bankrollCents);
  state.maximumDrawdownCents = Math.max(state.maximumDrawdownCents, state.peakBankrollCents - state.bankrollCents);
  if (netPnlCents > 0) {
    state.winStreak += 1;
    state.lossStreak = 0;
  } else if (netPnlCents < 0) {
    state.lossStreak += 1;
    state.winStreak = 0;
  }
  state.longestWinStreak = Math.max(state.longestWinStreak, state.winStreak);
  state.longestLossStreak = Math.max(state.longestLossStreak, state.lossStreak);
  const game = state.gameStats[gameId] ?? { wagerCount: 0, turnoverCents: 0, payoutCents: 0, expectedPnlCents: 0 };
  game.wagerCount += 1;
  game.turnoverCents += stakeCents;
  game.payoutCents += settlement.grossPayoutCents;
  game.expectedPnlCents += settlement.expectedGrossCents - stakeCents;
  state.gameStats[gameId] = game;
}

function buildRuntime(config, policy, worldSeed) {
  return {
    policy,
    state: initialState(config, policy),
    gameStream: stream(worldSeed, policy.playerId, "game-selection"),
    choiceStream: stream(worldSeed, policy.playerId, "choice"),
    stakeStream: stream(worldSeed, policy.playerId, "stake"),
    outcomeStreams: Object.fromEntries(config.games.map((game) => [game.id, stream(worldSeed, policy.playerId, game.id, "outcome")])),
  };
}

export function advanceAfterRuin(config, policy, state, simulatedAt) {
  if (state.allocationsUsed < config.allocationCap) {
    state.allocationsUsed += 1;
    state.bankrollMonth += 1;
    state.cumulativeAllocatedCents += config.allocationCents;
    state.bankrollCents = config.allocationCents;
    state.allocationWagers = 0;
    state.allocationTurnoverCents = 0;
    state.allocationStartedAt = simulatedAt;
    state.cooldownRemaining = policy.cooldownSessionsAfterRuin;
    return "allocation-started";
  }
  state.status = "inactive-all-six-allocations-used";
  return "player-inactivated";
}

function runSession(config, runtime, session, hooks = {}) {
  const { policy, state } = runtime;
  if (state.status !== "active") return;
  if (state.cooldownRemaining > 0) {
    state.cooldownRemaining -= 1;
    return;
  }
  const sessionId = `${policy.playerId}-S${String(session.sessionIndex).padStart(4, "0")}`;
  const sessionStartBankroll = state.bankrollCents;
  hooks.sessionStart?.({ runtime, session, sessionId });
  for (let betIndex = 0; betIndex < session.scheduledBets; betIndex += 1) {
    if (state.status !== "active") break;
    const eligible = config.games.filter((game) => game.minStakeCents <= state.bankrollCents);
    if (!eligible.length) break;
    const game = chooseGame(policy, eligible, runtime.gameStream);
    const choice = chooseBet(game, policy, runtime.choiceStream);
    const stakeCents = calculateStake(config, policy, state, game, runtime.stakeStream);
    if (stakeCents < game.minStakeCents || stakeCents > state.bankrollCents || stakeCents > game.maxStakeCents) throw new Error(`Invalid generated stake for ${policy.playerId}`);
    const before = policyStateForHash(state);
    const bankrollBeforeCents = state.bankrollCents;
    const outcomeStream = runtime.outcomeStreams[game.id];
    const drawReference = outcomeStream.counter;
    const settlement = settleGame(game.id, choice, stakeCents, outcomeStream);
    updateState(state, game.id, stakeCents, settlement);
    const simulatedAt = new Date(session.simulatedAtMs + betIndex * 30_000).toISOString();
    hooks.wager?.({ runtime, sessionId, simulatedAt, game, choice, stakeCents, bankrollBeforeCents, settlement, drawReference, before, after: policyStateForHash(state) });

    if (state.bankrollCents < config.minimumStakeCents) {
      const exhaustedAllocation = state.bankrollMonth;
      state.ruinCount += 1;
      state.firstRuinAt ??= simulatedAt;
      hooks.ruin?.({ runtime, simulatedAt, sessionId, exhaustedAllocation, finalStakeCents: stakeCents, finalOutcome: settlement.outcome, finalPayoutCents: settlement.grossPayoutCents });
      const transition = advanceAfterRuin(config, policy, state, simulatedAt);
      if (transition === "allocation-started") {
        hooks.allocation?.({ runtime, simulatedAt, reason: "post-ruin-reset" });
      } else {
        hooks.inactive?.({ runtime, simulatedAt });
      }
      break;
    }

    const sessionPnl = state.bankrollCents - sessionStartBankroll;
    const stopLoss = sessionPnl <= -Math.round(sessionStartBankroll * policy.stopLossFractionOfSessionStart);
    const stopWin = sessionPnl >= Math.round(sessionStartBankroll * policy.stopWinFractionOfSessionStart);
    if (stopLoss || stopWin) break;
  }
  state.sessionsCompleted += 1;
  hooks.sessionEnd?.({ runtime, session, sessionId });
}

function scheduleAll(config, manifest, worldSeed) {
  return manifest.flatMap((policy) => scheduleSessions(config, policy, worldSeed).map((session) => ({ ...session, policy })))
    .sort((a, b) => a.simulatedAtMs - b.simulatedAtMs || a.playerId.localeCompare(b.playerId));
}

export function simulateWorldSummary(config, manifest, worldSeed) {
  const runtimes = new Map(manifest.map((policy) => [policy.playerId, buildRuntime(config, policy, worldSeed)]));
  for (const session of scheduleAll(config, manifest, worldSeed)) runSession(config, runtimes.get(session.playerId), session);
  return [...runtimes.values()].map((runtime) => serialisableState(runtime.state));
}

export function simulateVisibleWorld(config, manifest, worldSeed) {
  const runtimes = new Map(manifest.map((policy) => [policy.playerId, buildRuntime(config, policy, worldSeed)]));
  const ledger = [];
  let previousHash = ZERO_HASH;
  let sequenceNumber = 0;
  const append = (body) => {
    sequenceNumber += 1;
    const event = { experimentId: config.experimentId, worldId: "visible-world-0001", sequenceNumber, previousEventHash: previousHash, ...body };
    event.eventHash = sha256(previousHash + hashObject(event));
    previousHash = event.eventHash;
    ledger.push(Object.freeze(event));
  };

  for (const runtime of runtimes.values()) {
    append({ eventType: "allocation_started", playerId: runtime.policy.playerId, cohortId: runtime.policy.cohortId, simulatedAt: config.calendarStart, bankrollMonth: 1, allocationCents: config.allocationCents, reason: "initial-allocation" });
  }

  const hooks = {
    sessionStart: ({ runtime, session, sessionId }) => append({ eventType: "session_started", playerId: runtime.policy.playerId, cohortId: runtime.policy.cohortId, sessionId, simulatedAt: new Date(session.simulatedAtMs).toISOString(), bankrollCents: runtime.state.bankrollCents }),
    wager: ({ runtime, sessionId, simulatedAt, game, choice, stakeCents, bankrollBeforeCents, settlement, drawReference, before, after }) => append({
      eventType: "wager_settled",
      betId: `B${String(sequenceNumber + 1).padStart(9, "0")}`,
      playerId: runtime.policy.playerId,
      cohortId: runtime.policy.cohortId,
      gameId: game.id,
      gameRuleVersion: game.ruleVersion,
      simulatedAt,
      sessionId,
      bankrollMonth: runtime.state.bankrollMonth,
      bankrollBeforeCents,
      stakeCents,
      choice: { betType: choice },
      rngStreamId: `${runtime.policy.playerId}:${game.id}:outcome`,
      rngCounterOrDrawReference: drawReference,
      outcome: settlement.outcome,
      probabilityReference: settlement.probabilityReference,
      grossPayoutCents: settlement.grossPayoutCents,
      netPnlCents: settlement.grossPayoutCents - stakeCents,
      bankrollAfterCents: runtime.state.bankrollCents,
      theoreticalEvCents: settlement.expectedGrossCents - stakeCents,
      policyStateBeforeHash: hashObject(before),
      policyStateAfterHash: hashObject(after),
    }),
    ruin: ({ runtime, simulatedAt, sessionId, exhaustedAllocation, finalStakeCents, finalOutcome, finalPayoutCents }) => append({ eventType: "ruin_recorded", playerId: runtime.policy.playerId, cohortId: runtime.policy.cohortId, sessionId, simulatedAt, bankrollImmediatelyAfterFinalWagerCents: runtime.state.bankrollCents, finalStakeCents, finalOutcome, finalPayoutCents, wagersInAllocation: runtime.state.allocationWagers, turnoverInAllocationCents: runtime.state.allocationTurnoverCents, allocationStartedAt: runtime.state.allocationStartedAt, exhaustedAllocation, cumulativeAllocationsConsumed: runtime.state.allocationsUsed }),
    allocation: ({ runtime, simulatedAt, reason }) => append({ eventType: "allocation_started", playerId: runtime.policy.playerId, cohortId: runtime.policy.cohortId, simulatedAt, bankrollMonth: runtime.state.bankrollMonth, allocationCents: config.allocationCents, reason }),
    inactive: ({ runtime, simulatedAt }) => append({ eventType: "player_inactivated", playerId: runtime.policy.playerId, cohortId: runtime.policy.cohortId, simulatedAt, reason: "used-all-six-allocations", allocationsUsed: runtime.state.allocationsUsed }),
    sessionEnd: ({ runtime, session, sessionId }) => append({ eventType: "session_ended", playerId: runtime.policy.playerId, cohortId: runtime.policy.cohortId, sessionId, simulatedAt: new Date(session.simulatedAtMs + session.scheduledBets * 30_000).toISOString(), bankrollCents: runtime.state.bankrollCents }),
  };

  for (const session of scheduleAll(config, manifest, worldSeed)) runSession(config, runtimes.get(session.playerId), session, hooks);
  const endAt = new Date(Date.parse(config.calendarStart) + config.calendarDays * 86_400_000 - 1).toISOString();
  const players = [...runtimes.values()].map((runtime) => serialisableState(runtime.state));
  const finalStateHash = hashObject(players);
  append({ eventType: "world_completed", simulatedAt: endAt, finalStateHash, wagerCount: players.reduce((sum, player) => sum + player.wagerCount, 0) });
  return { ledger, players, finalEventHash: previousHash, finalStateHash };
}

export function aggregatePlayers(players) {
  const totals = players.reduce((acc, player) => {
    acc.handleCents += player.cumulativeTurnoverCents;
    acc.payoutCents += player.cumulativePayoutCents;
    acc.expectedPnlCents += player.cumulativeExpectedPnlCents;
    acc.allocatedCents += player.cumulativeAllocatedCents;
    acc.wagers += player.wagerCount;
    acc.ruins += player.ruinCount;
    acc.ahead += player.netPnlCents > 0 ? 1 : 0;
    acc.behind += player.netPnlCents < 0 ? 1 : 0;
    acc.ruinedAtLeastOnce += player.ruinCount > 0 ? 1 : 0;
    acc.usedAllAllocations += player.allocationsUsed === 6 && player.status !== "active" ? 1 : 0;
    acc.active += player.status === "active" ? 1 : 0;
    return acc;
  }, { handleCents: 0, payoutCents: 0, expectedPnlCents: 0, allocatedCents: 0, wagers: 0, ruins: 0, ahead: 0, behind: 0, ruinedAtLeastOnce: 0, usedAllAllocations: 0, active: 0 });
  return {
    ...totals,
    ggrCents: totals.handleCents - totals.payoutCents,
    actualRtp: totals.handleCents ? totals.payoutCents / totals.handleCents : 0,
    theoreticalRtp: totals.handleCents ? (totals.handleCents + totals.expectedPnlCents) / totals.handleCents : 0,
    playerWagerPnlCents: totals.payoutCents - totals.handleCents,
  };
}
