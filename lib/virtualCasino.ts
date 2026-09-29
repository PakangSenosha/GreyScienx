import dashboard from "@/research/experiments/virtual-casino/artifacts/v1.0/dashboard.json";

export type CasinoPlayer = {
  playerId: string;
  cohortId: string;
  currentBankrollCents: number;
  cumulativeAllocatedCents: number;
  cumulativeTurnoverCents: number;
  cumulativePayoutCents: number;
  cumulativeExpectedPnlCents: number;
  netPnlCents: number;
  deviationFromExpectationCents: number;
  wagerCount: number;
  sessionsCompleted: number;
  allocationsUsed: number;
  ruinCount: number;
  firstRuinAt: string | null;
  peakBankrollCents: number;
  maximumDrawdownCents: number;
  averageStakeCents: number;
  medianStakeCents: number;
  realisedRtp: number;
  status: string;
  rank: number;
  gameStats: Record<string, { wagerCount: number; turnoverCents: number; payoutCents: number; expectedPnlCents: number }>;
  monthlyHistory: { month: number; netPnlCents: number }[];
  policy: {
    cohortLabel: string;
    baseStakeFraction: number;
    sessionsPerWeek: number;
    betsPerSessionMean: number;
    gameWeights: Record<string, number>;
    stopLossFractionOfSessionStart: number;
    stopWinFractionOfSessionStart: number;
    maximumStakeCents: number;
    lossResponse: { stakeMultiplierAfterLoss: number; maximumConsecutiveEscalations: number };
  };
  replication: {
    medianPnlCents: number;
    p05PnlCents: number;
    p95PnlCents: number;
    p01PnlCents: number;
    p99PnlCents: number;
    probabilityAhead: number;
    probabilityRuin: number;
    medianTurnoverCents: number;
    medianWagerCount: number;
    medianRank: number;
    visiblePercentileWithinPolicy: number;
  };
};

export type CasinoCohort = {
  id: string;
  label: string;
  players: number;
  meanPnlCents: number;
  medianPnlCents: number;
  p05PnlCents: number;
  p25PnlCents: number;
  p75PnlCents: number;
  p95PnlCents: number;
  probabilityAhead: number;
  ruinRate: number;
  turnoverCents: number;
  allocatedCents: number;
  expectedPnlCents: number;
  actualRtp: number;
  theoreticalRtp: number;
  replication: { medianOfWorldMedianPnlCents: number; p05WorldMedianPnlCents: number; p95WorldMedianPnlCents: number; medianRuinRate: number; medianAheadRate: number };
};

export type CasinoGame = {
  id: string;
  label: string;
  ruleVersion: string;
  wagerCount: number;
  turnoverCents: number;
  payoutCents: number;
  expectedPnlCents: number;
  uniquePlayers: number;
  ggrCents: number;
  actualRtp: number;
  theoreticalRtp: number;
  choices: { choice: string; theoreticalRtp: number; houseEdge: number; volatility: string; ruleNote: string }[];
};

export type CasinoData = {
  metadata: Record<string, string | number | boolean>;
  summary: Record<string, number>;
  timeseries: { day: number; simulatedDate: string; handleCents: number; payoutCents: number; ggrCents: number; actualRtp: number; theoreticalRtp: number; playersAhead: number; denominator: number }[];
  distribution: { histogram: { lowerCents: number; upperCents: number; count: number }[]; orderedPlayerIds: string[]; p05PnlCents: number; medianPnlCents: number; p95PnlCents: number };
  players: CasinoPlayer[];
  cohorts: CasinoCohort[];
  games: CasinoGame[];
  replication: {
    completedWorlds: number;
    visibleWorldPercentile: number;
    ggrDistribution: { lowerCents: number; upperCents: number; count: number }[];
    profitablePlayerCounts: number[];
    highlightedPolicies: CasinoPlayer["replication"][];
    cohorts: CasinoCohort["replication"][];
  };
  methods: { hypotheses: string[]; limitations: string[] };
};

export const casinoData = dashboard as unknown as CasinoData;
export const casinoPlayers = new Map(casinoData.players.map((player) => [player.playerId, player]));
export const casinoGames = new Map(casinoData.games.map((game) => [game.id, game]));

export function zar(cents: number, compact = false) {
  return new Intl.NumberFormat("en-ZA", {
    style: "currency",
    currency: "ZAR",
    maximumFractionDigits: 0,
    notation: compact ? "compact" : "standard",
  }).format(cents / 100);
}

export function pct(value: number, digits = 2) {
  return new Intl.NumberFormat("en-ZA", { style: "percent", maximumFractionDigits: digits, minimumFractionDigits: digits }).format(value);
}

export function integer(value: number) {
  return new Intl.NumberFormat("en-ZA").format(value);
}

export function gameLabel(id: string) {
  return casinoGames.get(id)?.label ?? id.replaceAll("_", " ");
}
