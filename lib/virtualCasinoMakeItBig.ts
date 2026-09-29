import dashboard from "@/research/experiments/virtual-casino/make-it-big/artifacts/v1.0/dashboard.json";

export type MakeItBigStrategy = {
  id: string;
  label: string;
  stakeCents: number;
  betsPerMonth: number;
};

export type MakeItBigGame = {
  id: string;
  label: string;
  rulesVersion: string;
  replicationClass: string;
  ruleType: string;
  theoreticalRtp: number;
  maximumMultiplier: number;
  sourceReference: string;
  assumptions: string;
  outcomes: { multiplier: number; probability: number }[] | null;
};

export type MakeItBigCell = {
  gameId: string;
  gameLabel: string;
  strategyId: string;
  strategyLabel: string;
  stakeCents: number;
  betsPerMonth: number;
  maximumBets: number;
  targetMultiplier: number;
  theoreticalRtp: number;
  probabilityPerBet: number;
  exactProbability12Months: number;
  exactProbability36Months: number;
  simulatedProbability12Months: number;
  simulatedProbability36Months: number;
  oneYearWinners: number;
  threeYearWinners: number;
  oneYearBudgetExhaustedWithoutTarget: number;
  threeYearBudgetExhaustedWithoutTarget: number;
  winnersPer1000Entrants: number;
  entrantsPerWinner: number | null;
  totalSpendCents: number;
  spendPerWinnerCents: number | null;
  medianBetsBeforeWin: number | null;
  medianMonthsBeforeWin: number | null;
  medianSpendBeforeWinCents: number | null;
  medianGrossPayoutCents: number | null;
  simulationErrorPercentagePoints12Months: number;
  simulationErrorPercentagePoints36Months: number;
};

export type MakeItBigSurvival = {
  gameId: string;
  strategyId: string;
  month: number;
  bets: number;
  exactSurvival: number;
  exactCumulativeIncidence: number;
  simulatedCumulativeIncidence: number;
};

export type MakeItBigData = {
  metadata: Record<string, string | number>;
  design: {
    targetPayoutCents: number;
    monthlyBudgetCents: number;
    maximumMonths: number;
    horizonsMonths: number[];
    entrantsPerCell: number;
    strategies: MakeItBigStrategy[];
  };
  games: MakeItBigGame[];
  summary: {
    experimentalCells: number;
    entrantsPerCell: number;
    totalEntrantRuns: number;
    totalThreeYearTargetHits: number;
    maximumAbsoluteSimulationErrorPercentagePoints: number;
  };
  cells: MakeItBigCell[];
  survival: MakeItBigSurvival[];
};

export const makeItBigData = dashboard as unknown as MakeItBigData;

export function makeItBigCell(gameId: string, strategyId: string) {
  const cell = makeItBigData.cells.find((candidate) => candidate.gameId === gameId && candidate.strategyId === strategyId);
  if (!cell) throw new Error(`Missing Make It Big cell: ${gameId}/${strategyId}`);
  return cell;
}
