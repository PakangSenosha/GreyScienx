import { stream } from "../../engine/random.mjs";

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

export function validateProtocol(config) {
  assert(Number.isSafeInteger(config.targetPayoutCents) && config.targetPayoutCents > 0, "targetPayoutCents must be a positive integer");
  assert(Number.isSafeInteger(config.monthlyBudgetCents) && config.monthlyBudgetCents > 0, "monthlyBudgetCents must be a positive integer");
  assert(Number.isSafeInteger(config.entrantsPerCell) && config.entrantsPerCell > 0, "entrantsPerCell must be a positive integer");
  assert(config.horizonsMonths.includes(12) && config.horizonsMonths.includes(36), "The preregistered 12- and 36-month horizons are required");
  for (const strategy of config.strategies) {
    assert(strategy.stakeCents * strategy.betsPerMonth === config.monthlyBudgetCents, `${strategy.id} does not spend exactly the monthly budget`);
    assert(config.targetPayoutCents % strategy.stakeCents === 0, `${strategy.id} does not divide the target exactly`);
  }
  for (const game of config.games) {
    assert(game.replicationClass.startsWith("C"), `${game.id} must remain explicitly labelled as synthetic`);
    if (game.ruleType === "discreteMultipliers") {
      const probability = game.outcomes.reduce((sum, outcome) => sum + outcome.probability, 0);
      const rtp = game.outcomes.reduce((sum, outcome) => sum + outcome.multiplier * outcome.probability, 0);
      assert(Math.abs(probability - 1) < 1e-12, `${game.id} probabilities do not sum to one`);
      assert(Math.abs(rtp - game.theoreticalRtp) < 1e-12, `${game.id} outcome table does not match its RTP`);
    }
  }
  return true;
}

export function targetMultiplier(config, strategy) {
  return config.targetPayoutCents / strategy.stakeCents;
}

export function targetProbability(config, game, strategy) {
  const threshold = targetMultiplier(config, strategy);
  if (game.ruleType === "targetMultiplier") return game.theoreticalRtp / threshold;
  return game.outcomes
    .filter((outcome) => outcome.multiplier >= threshold)
    .reduce((sum, outcome) => sum + outcome.probability, 0);
}

export function exactCumulativeIncidence(probabilityPerBet, bets) {
  return 1 - ((1 - probabilityPerBet) ** bets);
}

function geometricTrialIndex(random, probabilityPerBet) {
  return Math.floor(Math.log1p(-random.uniform()) / Math.log1p(-probabilityPerBet)) + 1;
}

function quantile(sorted, probability) {
  if (!sorted.length) return null;
  const index = (sorted.length - 1) * probability;
  const lower = Math.floor(index);
  const upper = Math.ceil(index);
  if (lower === upper) return sorted[lower];
  return sorted[lower] + (sorted[upper] - sorted[lower]) * (index - lower);
}

function selectWinningMultiplier(random, config, game, strategy) {
  const threshold = targetMultiplier(config, strategy);
  if (game.ruleType === "targetMultiplier") return threshold;
  const eligible = game.outcomes.filter((outcome) => outcome.multiplier >= threshold);
  return random.weighted(eligible, eligible.map((outcome) => outcome.probability)).multiplier;
}

function simulateCell(config, game, strategy) {
  const random = stream(config.simulationSeed, "make-it-big", game.id, strategy.id);
  const probabilityPerBet = targetProbability(config, game, strategy);
  const maximumBets = strategy.betsPerMonth * config.maximumMonths;
  const oneYearBets = strategy.betsPerMonth * 12;
  const winners = [];
  const auditEntrants = [];
  let totalSpendCents = 0;

  for (let entrant = 1; entrant <= config.entrantsPerCell; entrant += 1) {
    const trialIndex = geometricTrialIndex(random, probabilityPerBet);
    const targetHit = trialIndex <= maximumBets;
    const betsObserved = targetHit ? trialIndex : maximumBets;
    const spendCents = betsObserved * strategy.stakeCents;
    totalSpendCents += spendCents;
    let winner = null;

    if (targetHit) {
      const grossMultiplier = selectWinningMultiplier(random, config, game, strategy);
      const grossPayoutCents = grossMultiplier * strategy.stakeCents;
      winner = {
        trialIndex,
        month: Math.ceil(trialIndex / strategy.betsPerMonth),
        spendCents,
        grossMultiplier,
        grossPayoutCents,
        netAfterSpendCents: grossPayoutCents - spendCents,
      };
      winners.push(winner);
    }

    if (entrant <= 25) {
      auditEntrants.push({
        entrantId: `${game.id}-${strategy.id}-${String(entrant).padStart(6, "0")}`,
        gameId: game.id,
        strategyId: strategy.id,
        targetHit,
        terminalOutcome: targetHit ? "target_hit" : "three_year_budget_exhausted",
        betsObserved,
        spendCents,
        hitMonth: winner?.month ?? null,
        grossPayoutCents: winner?.grossPayoutCents ?? 0,
      });
    }
  }

  const winningBets = winners.map((winner) => winner.trialIndex).sort((a, b) => a - b);
  const winningMonths = winners.map((winner) => winner.month).sort((a, b) => a - b);
  const winningSpend = winners.map((winner) => winner.spendCents).sort((a, b) => a - b);
  const winningGross = winners.map((winner) => winner.grossPayoutCents).sort((a, b) => a - b);
  const oneYearWinners = winners.filter((winner) => winner.trialIndex <= oneYearBets).length;
  const exact12 = exactCumulativeIncidence(probabilityPerBet, oneYearBets);
  const exact36 = exactCumulativeIncidence(probabilityPerBet, maximumBets);

  const row = {
    gameId: game.id,
    gameLabel: game.label,
    strategyId: strategy.id,
    strategyLabel: strategy.label,
    stakeCents: strategy.stakeCents,
    betsPerMonth: strategy.betsPerMonth,
    maximumBets,
    targetMultiplier: targetMultiplier(config, strategy),
    theoreticalRtp: game.theoreticalRtp,
    probabilityPerBet,
    exactProbability12Months: exact12,
    exactProbability36Months: exact36,
    simulatedProbability12Months: oneYearWinners / config.entrantsPerCell,
    simulatedProbability36Months: winners.length / config.entrantsPerCell,
    oneYearWinners,
    threeYearWinners: winners.length,
    oneYearBudgetExhaustedWithoutTarget: config.entrantsPerCell - oneYearWinners,
    threeYearBudgetExhaustedWithoutTarget: config.entrantsPerCell - winners.length,
    winnersPer1000Entrants: (winners.length / config.entrantsPerCell) * 1000,
    entrantsPerWinner: winners.length ? config.entrantsPerCell / winners.length : null,
    totalSpendCents,
    spendPerWinnerCents: winners.length ? totalSpendCents / winners.length : null,
    medianBetsBeforeWin: quantile(winningBets, 0.5),
    medianMonthsBeforeWin: quantile(winningMonths, 0.5),
    medianSpendBeforeWinCents: quantile(winningSpend, 0.5),
    medianGrossPayoutCents: quantile(winningGross, 0.5),
    simulationErrorPercentagePoints12Months: ((oneYearWinners / config.entrantsPerCell) - exact12) * 100,
    simulationErrorPercentagePoints36Months: ((winners.length / config.entrantsPerCell) - exact36) * 100,
  };

  const survival = [];
  for (let month = 0; month <= config.maximumMonths; month += 1) {
    const bets = month * strategy.betsPerMonth;
    const simulatedHits = month === 0 ? 0 : winners.filter((winner) => winner.trialIndex <= bets).length;
    survival.push({
      gameId: game.id,
      strategyId: strategy.id,
      month,
      bets,
      exactSurvival: (1 - probabilityPerBet) ** bets,
      exactCumulativeIncidence: exactCumulativeIncidence(probabilityPerBet, bets),
      simulatedCumulativeIncidence: simulatedHits / config.entrantsPerCell,
    });
  }

  return { row, survival, auditEntrants };
}

export function simulateStudy(config) {
  validateProtocol(config);
  const cells = [];
  const survival = [];
  const auditEntrants = [];
  for (const game of config.games) {
    for (const strategy of config.strategies) {
      const result = simulateCell(config, game, strategy);
      cells.push(result.row);
      survival.push(...result.survival);
      auditEntrants.push(...result.auditEntrants);
    }
  }
  const totalEntrants = config.entrantsPerCell * cells.length;
  const totalWinners = cells.reduce((sum, cell) => sum + cell.threeYearWinners, 0);
  const maximumAbsoluteError = Math.max(...cells.flatMap((cell) => [
    Math.abs(cell.simulationErrorPercentagePoints12Months),
    Math.abs(cell.simulationErrorPercentagePoints36Months),
  ]));
  return {
    summary: {
      experimentalCells: cells.length,
      entrantsPerCell: config.entrantsPerCell,
      totalEntrantRuns: totalEntrants,
      totalThreeYearTargetHits: totalWinners,
      maximumAbsoluteSimulationErrorPercentagePoints: maximumAbsoluteError,
    },
    cells,
    survival,
    auditEntrants,
  };
}
