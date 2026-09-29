import { aggregatePlayers } from "./simulate.mjs";
import { gameValidationRows } from "./games.mjs";
import { hashObject } from "./random.mjs";

export function quantile(values, probability) {
  if (!values.length) return 0;
  const sorted = [...values].sort((a, b) => a - b);
  const index = (sorted.length - 1) * probability;
  const lower = Math.floor(index);
  const upper = Math.ceil(index);
  if (lower === upper) return sorted[lower];
  return Math.round(sorted[lower] + (sorted[upper] - sorted[lower]) * (index - lower));
}

function summariseGroup(players, id, label) {
  const pnl = players.map((player) => player.netPnlCents);
  const totals = aggregatePlayers(players);
  return {
    id,
    label,
    players: players.length,
    meanPnlCents: Math.round(pnl.reduce((sum, value) => sum + value, 0) / players.length),
    medianPnlCents: quantile(pnl, 0.5),
    p05PnlCents: quantile(pnl, 0.05),
    p25PnlCents: quantile(pnl, 0.25),
    p75PnlCents: quantile(pnl, 0.75),
    p95PnlCents: quantile(pnl, 0.95),
    probabilityAhead: totals.ahead / players.length,
    ruinRate: totals.ruinedAtLeastOnce / players.length,
    usedAllAllocationsRate: totals.usedAllAllocations / players.length,
    turnoverCents: totals.handleCents,
    allocatedCents: totals.allocatedCents,
    expectedPnlCents: totals.expectedPnlCents,
    actualRtp: totals.actualRtp,
    theoreticalRtp: totals.theoreticalRtp,
  };
}

export function cohortSummaries(config, players) {
  return config.cohorts.map((cohort) => summariseGroup(players.filter((player) => player.cohortId === cohort.id), cohort.id, cohort.label));
}

export function gameSummaries(config, players) {
  const validation = gameValidationRows();
  return config.games.map((game) => {
    const totals = players.reduce((acc, player) => {
      const row = player.gameStats[game.id];
      if (!row) return acc;
      acc.wagerCount += row.wagerCount;
      acc.turnoverCents += row.turnoverCents;
      acc.payoutCents += row.payoutCents;
      acc.expectedPnlCents += row.expectedPnlCents;
      acc.uniquePlayers += 1;
      return acc;
    }, { wagerCount: 0, turnoverCents: 0, payoutCents: 0, expectedPnlCents: 0, uniquePlayers: 0 });
    return {
      id: game.id,
      label: game.label,
      ruleVersion: game.ruleVersion,
      ...totals,
      ggrCents: totals.turnoverCents - totals.payoutCents,
      actualRtp: totals.turnoverCents ? totals.payoutCents / totals.turnoverCents : 0,
      theoreticalRtp: totals.turnoverCents ? (totals.turnoverCents + totals.expectedPnlCents) / totals.turnoverCents : 0,
      choices: validation.filter((row) => row.gameId === game.id),
    };
  });
}

export function ledgerTimeSeries(config, ledger) {
  const wagers = ledger.filter((event) => event.eventType === "wager_settled").sort((a, b) => a.simulatedAt.localeCompare(b.simulatedAt));
  const playerPnl = new Map();
  let cursor = 0;
  let handleCents = 0;
  let payoutCents = 0;
  let expectedPnlCents = 0;
  const rows = [];
  const start = Date.parse(config.calendarStart);
  for (let day = 0; day < config.calendarDays; day += 1) {
    const end = start + (day + 1) * 86_400_000;
    while (cursor < wagers.length && Date.parse(wagers[cursor].simulatedAt) < end) {
      const event = wagers[cursor];
      handleCents += event.stakeCents;
      payoutCents += event.grossPayoutCents;
      expectedPnlCents += event.theoreticalEvCents;
      playerPnl.set(event.playerId, (playerPnl.get(event.playerId) ?? 0) + event.netPnlCents);
      cursor += 1;
    }
    const ahead = [...playerPnl.values()].filter((value) => value > 0).length;
    rows.push({
      day: day + 1,
      simulatedDate: new Date(start + day * 86_400_000).toISOString().slice(0, 10),
      handleCents,
      payoutCents,
      ggrCents: handleCents - payoutCents,
      actualRtp: handleCents ? payoutCents / handleCents : 0,
      theoreticalRtp: handleCents ? (handleCents + expectedPnlCents) / handleCents : 0,
      playersAhead: ahead,
      denominator: config.population,
    });
  }
  return rows;
}

export function playerMonthlyHistory(config, ledger) {
  const wagers = ledger.filter((event) => event.eventType === "wager_settled").sort((a, b) => a.simulatedAt.localeCompare(b.simulatedAt));
  const monthEnds = [31, 59, 90, 120, 151, 181].map((day) => Date.parse(config.calendarStart) + day * 86_400_000);
  const pnl = new Map();
  const result = Object.fromEntries([...new Set(wagers.map((event) => event.playerId))].map((id) => [id, []]));
  let cursor = 0;
  for (let month = 0; month < monthEnds.length; month += 1) {
    while (cursor < wagers.length && Date.parse(wagers[cursor].simulatedAt) < monthEnds[month]) {
      const event = wagers[cursor];
      pnl.set(event.playerId, (pnl.get(event.playerId) ?? 0) + event.netPnlCents);
      cursor += 1;
    }
    for (const playerId of Object.keys(result)) result[playerId].push({ month: month + 1, netPnlCents: pnl.get(playerId) ?? 0 });
  }
  return result;
}

export function pnlHistogram(players, bucketCount = 20) {
  const values = players.map((player) => player.netPnlCents);
  const min = Math.min(...values);
  const max = Math.max(...values);
  const width = Math.max(1, Math.ceil((max - min + 1) / bucketCount));
  const bins = Array.from({ length: bucketCount }, (_, index) => ({ lowerCents: min + index * width, upperCents: min + (index + 1) * width - 1, count: 0 }));
  for (const value of values) bins[Math.min(bucketCount - 1, Math.floor((value - min) / width))].count += 1;
  return bins;
}

export function checkpointRows(config, ledger, players, configHash, manifestHash) {
  const series = ledgerTimeSeries(config, ledger);
  const wagerEvents = ledger.filter((event) => event.eventType === "wager_settled");
  const rows = [{ checkpointType: "initial", simulatedAt: config.calendarStart, lastLedgerEventHash: ledger[config.population - 1]?.eventHash ?? null, handleCents: 0, payoutCents: 0, ggrCents: 0 }];
  for (const day of series) {
    const end = Date.parse(day.simulatedDate) + 86_400_000;
    const prior = wagerEvents.filter((event) => Date.parse(event.simulatedAt) < end).at(-1);
    rows.push({ checkpointType: "daily", simulatedAt: new Date(end - 1).toISOString(), lastLedgerEventHash: prior?.eventHash ?? rows.at(-1).lastLedgerEventHash, handleCents: day.handleCents, payoutCents: day.payoutCents, ggrCents: day.ggrCents });
  }
  const monthDays = new Set([31, 59, 90, 120, 151, 181]);
  for (const day of series.filter((row) => monthDays.has(row.day))) rows.push({ checkpointType: "monthly", simulatedAt: `${day.simulatedDate}T23:59:59.999Z`, lastLedgerEventHash: rows[day.day].lastLedgerEventHash, handleCents: day.handleCents, payoutCents: day.payoutCents, ggrCents: day.ggrCents });
  rows.push({ checkpointType: "final", simulatedAt: new Date(Date.parse(config.calendarStart) + config.calendarDays * 86_400_000 - 1).toISOString(), lastLedgerEventHash: ledger.at(-1).eventHash, handleCents: series.at(-1).handleCents, payoutCents: series.at(-1).payoutCents, ggrCents: series.at(-1).ggrCents, finalPlayerStateHash: hashObject(players) });
  return rows.map((row) => ({ ...row, experimentVersion: config.protocolVersion, configHash, manifestHash, checkpointHash: hashObject({ ...row, experimentVersion: config.protocolVersion, configHash, manifestHash }) }));
}

export function buildReplicationAccumulator(config, manifest) {
  const players = Object.fromEntries(manifest.map((policy) => [policy.playerId, { pnl: [], turnover: [], wagers: [], ranks: [], ahead: 0, ruined: 0, capped: 0 }]));
  const cohorts = Object.fromEntries(config.cohorts.map((cohort) => [cohort.id, { medianPnl: [], ruinRate: [], aheadRate: [] }]));
  return { players, cohorts, worlds: [], selectedWorlds: [] };
}

export function addReplicationWorld(accumulator, config, worldIndex, worldPlayers) {
  const aggregate = aggregatePlayers(worldPlayers);
  const ranked = [...worldPlayers].sort((a, b) => b.netPnlCents - a.netPnlCents);
  const ranks = new Map(ranked.map((player, index) => [player.playerId, index + 1]));
  for (const player of worldPlayers) {
    const acc = accumulator.players[player.playerId];
    acc.pnl.push(player.netPnlCents);
    acc.turnover.push(player.cumulativeTurnoverCents);
    acc.wagers.push(player.wagerCount);
    acc.ranks.push(ranks.get(player.playerId));
    acc.ahead += player.netPnlCents > 0 ? 1 : 0;
    acc.ruined += player.ruinCount > 0 ? 1 : 0;
    acc.capped += player.status !== "active" && player.allocationsUsed === config.allocationCap ? 1 : 0;
  }
  for (const cohort of cohortSummaries(config, worldPlayers)) {
    const acc = accumulator.cohorts[cohort.id];
    acc.medianPnl.push(cohort.medianPnlCents);
    acc.ruinRate.push(cohort.ruinRate);
    acc.aheadRate.push(cohort.probabilityAhead);
  }
  accumulator.worlds.push({
    worldIndex,
    worldId: `replication-${String(worldIndex).padStart(4, "0")}`,
    seedReference: hashObject({ prefix: config.replicationSeedPrefix, worldIndex }).slice(0, 24),
    ggrCents: aggregate.ggrCents,
    actualRtp: aggregate.actualRtp,
    theoreticalRtp: aggregate.theoreticalRtp,
    playersAhead: aggregate.ahead,
    ruinedAtLeastOnce: aggregate.ruinedAtLeastOnce,
    usedAllAllocations: aggregate.usedAllAllocations,
    wagerCount: aggregate.wagers,
  });
}

export function finaliseReplication(accumulator, config, visiblePlayers, visibleAggregate) {
  const count = accumulator.worlds.length;
  const playerRows = Object.entries(accumulator.players).map(([playerId, acc]) => ({
    playerId,
    meanPnlCents: Math.round(acc.pnl.reduce((sum, value) => sum + value, 0) / count),
    medianPnlCents: quantile(acc.pnl, 0.5),
    p01PnlCents: quantile(acc.pnl, 0.01),
    p05PnlCents: quantile(acc.pnl, 0.05),
    p95PnlCents: quantile(acc.pnl, 0.95),
    p99PnlCents: quantile(acc.pnl, 0.99),
    probabilityAhead: acc.ahead / count,
    probabilityRuin: acc.ruined / count,
    probabilityAllAllocations: acc.capped / count,
    medianTurnoverCents: quantile(acc.turnover, 0.5),
    medianWagerCount: quantile(acc.wagers, 0.5),
    medianRank: quantile(acc.ranks, 0.5),
    visiblePnlCents: visiblePlayers.find((player) => player.playerId === playerId).netPnlCents,
    visiblePercentileWithinPolicy: acc.pnl.filter((value) => value <= visiblePlayers.find((player) => player.playerId === playerId).netPnlCents).length / count,
  }));
  const cohortRows = config.cohorts.map((cohort) => {
    const acc = accumulator.cohorts[cohort.id];
    return {
      cohortId: cohort.id,
      label: cohort.label,
      worlds: count,
      medianOfWorldMedianPnlCents: quantile(acc.medianPnl, 0.5),
      p05WorldMedianPnlCents: quantile(acc.medianPnl, 0.05),
      p95WorldMedianPnlCents: quantile(acc.medianPnl, 0.95),
      medianRuinRate: quantile(acc.ruinRate.map((value) => Math.round(value * 1_000_000)), 0.5) / 1_000_000,
      medianAheadRate: quantile(acc.aheadRate.map((value) => Math.round(value * 1_000_000)), 0.5) / 1_000_000,
    };
  });
  const visibleWorldPercentile = accumulator.worlds.filter((world) => world.ggrCents <= visibleAggregate.ggrCents).length / count;
  return { completedWorlds: count, visibleWorldPercentile, worlds: accumulator.worlds, players: playerRows, cohorts: cohortRows };
}
