import { stream, hashObject } from "./random.mjs";

function round(value, digits = 6) {
  return Number(value.toFixed(digits));
}

function normalise(weights) {
  const total = Object.values(weights).reduce((sum, value) => sum + value, 0);
  return Object.fromEntries(Object.entries(weights).map(([key, value]) => [key, round(value / total)]));
}

function gameWeights(gameIds, cohortId, playerIndex, rng) {
  const weights = Object.fromEntries(gameIds.map((id) => [id, 0.55 + rng.uniform() * 0.9]));
  const affinities = {
    small_frequent: ["three_reel_slot", "european_roulette"],
    small_infrequent: ["baccarat", "lottery"],
    medium_frequent: ["blackjack", "craps"],
    medium_infrequent: ["virtual_sports", "baccarat"],
    large_frequent: ["crash", "high_volatility_slot"],
    large_infrequent: ["lottery", "american_roulette"],
    loss_chasing: ["crash", "american_roulette", "craps"],
    strict_limits: ["european_roulette", "baccarat"],
    variable_staking: ["high_volatility_slot", "virtual_sports"],
    random_control: gameIds,
  };
  for (const id of affinities[cohortId]) weights[id] += 2.25;
  weights[gameIds[playerIndex % gameIds.length]] += 1.75;
  return normalise(weights);
}

function sampleRange(rng, range) {
  return rng.between(range[0], range[1]);
}

export function generateManifest(config) {
  const gameIds = config.games.map((game) => game.id);
  const players = [];
  for (let cohortIndex = 0; cohortIndex < config.cohorts.length; cohortIndex += 1) {
    const cohort = config.cohorts[cohortIndex];
    for (let within = 0; within < config.cohortSize; within += 1) {
      const ordinal = cohortIndex * config.cohortSize + within + 1;
      const playerId = `P${String(ordinal).padStart(4, "0")}`;
      const rng = stream(config.assignmentSeed, "assignment", playerId);
      const policy = {
        playerId,
        cohortId: cohort.id,
        cohortLabel: cohort.label,
        policyVersion: "policy-1.0.0",
        startingAllocationCents: config.allocationCents,
        baseStakeFraction: round(sampleRange(rng, cohort.stakeFraction)),
        sessionsPerWeek: round(sampleRange(rng, cohort.sessionsPerWeek), 3),
        betsPerSessionMean: round(sampleRange(rng, cohort.betsPerSession), 3),
        gameWeights: gameWeights(gameIds, cohort.id, within, rng),
        lossResponse: {
          stakeMultiplierAfterLoss: round(sampleRange(rng, cohort.lossMultiplier), 4),
          maximumConsecutiveEscalations: cohort.id === "loss_chasing" ? 3 + rng.integer(4) : 1 + rng.integer(2),
        },
        winResponse: { stakeMultiplierAfterWin: round(0.88 + rng.uniform() * 0.14, 4) },
        stopLossFractionOfSessionStart: round(sampleRange(rng, cohort.stopLoss), 4),
        stopWinFractionOfSessionStart: round(sampleRange(rng, cohort.stopWin), 4),
        maximumStakeCents: 20_000 + rng.integer(config.maximumStakeCents - 19_999),
        gameSwitchPropensity: round(0.08 + rng.uniform() * 0.62, 4),
        leaveWhileAheadPropensity: round(0.1 + rng.uniform() * 0.75, 4),
        cooldownSessionsAfterRuin: rng.integer(3),
        adaptationStrength: round(rng.uniform(), 4),
        choiceBias: round(rng.uniform(), 4),
        assignmentSeedReference: hashObject({ seed: config.assignmentSeed, playerId }).slice(0, 20),
      };
      players.push(policy);
    }
  }
  return players;
}

export function scheduleSessions(config, policy, worldSeed) {
  const rng = stream(worldSeed, policy.playerId, "session-schedule");
  const sessions = [];
  const base = Math.floor(policy.sessionsPerWeek);
  const fractional = policy.sessionsPerWeek - base;
  for (let week = 0; week < config.sessionModel.weeks; week += 1) {
    const count = base + (rng.uniform() < fractional ? 1 : 0);
    for (let index = 0; index < count; index += 1) {
      const dayOffset = week * 7 + rng.uniform() * 7;
      if (dayOffset >= config.calendarDays) continue;
      const timestampMs = Date.parse(config.calendarStart) + Math.floor(dayOffset * 86_400_000);
      const mean = policy.betsPerSessionMean;
      const bets = Math.max(1, Math.round(mean * (0.65 + rng.uniform() * 0.7)));
      sessions.push({
        playerId: policy.playerId,
        simulatedAtMs: timestampMs,
        scheduledBets: bets,
        sessionIndex: sessions.length + 1,
      });
    }
  }
  return sessions.sort((a, b) => a.simulatedAtMs - b.simulatedAtMs);
}

export function chooseGame(policy, eligibleGames, gameStream) {
  return gameStream.weighted(eligibleGames, eligibleGames.map((game) => policy.gameWeights[game.id] ?? 0));
}

export function chooseBet(game, policy, choiceStream) {
  const choices = game.choices;
  if (game.id === "blackjack") {
    if (policy.cohortId === "strict_limits") return "basic";
    if (policy.cohortId === "random_control") return choiceStream.pick(choices);
    return policy.choiceBias < 0.58 ? "basic" : policy.choiceBias < 0.84 ? "novice" : "random";
  }
  if (game.id === "baccarat") {
    return policy.choiceBias < 0.46 ? "banker" : policy.choiceBias < 0.9 ? "player" : "tie";
  }
  if (game.id === "craps") return policy.choiceBias < 0.56 ? "pass_line" : policy.choiceBias < 0.86 ? "field" : "any_seven";
  if (game.id === "virtual_sports") return policy.choiceBias < 0.72 ? "single" : "parlay";
  if (game.id === "crash") {
    const pool = policy.cohortId === "strict_limits" ? ["1.25", "2"] : choices;
    return choiceStream.pick(pool);
  }
  if (game.id.includes("roulette")) return choiceStream.pick(choices);
  return choices[0];
}

export function calculateStake(config, policy, state, game, stakeStream) {
  const streakDepth = Math.min(state.lossStreak, policy.lossResponse.maximumConsecutiveEscalations);
  let multiplier = streakDepth > 0 ? policy.lossResponse.stakeMultiplierAfterLoss ** streakDepth : policy.winResponse.stakeMultiplierAfterWin ** Math.min(state.winStreak, 2);
  if (policy.cohortId === "variable_staking" || policy.cohortId === "random_control") multiplier *= 0.35 + stakeStream.uniform() * 1.65;
  multiplier = Math.min(5, Math.max(0.2, multiplier));
  const raw = Math.floor(state.bankrollCents * policy.baseStakeFraction * multiplier);
  const cap = Math.min(config.maximumStakeCents, policy.maximumStakeCents, game.maxStakeCents);
  const clamped = Math.min(state.bankrollCents, cap, Math.max(game.minStakeCents, raw));
  return Math.floor(clamped / 100) * 100;
}
