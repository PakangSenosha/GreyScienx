const MILLION = 1_000_000;

function categorical(stream, rows, denominator = MILLION) {
  const draw = stream.integer(denominator);
  let cursor = 0;
  for (const row of rows) {
    cursor += row.units;
    if (draw < cursor) return { row, draw, denominator };
  }
  throw new Error(`Incomplete probability table: ${cursor}/${denominator}`);
}

function expectationFromRows(stakeCents, rows, denominator = MILLION) {
  const numerator = rows.reduce((sum, row) => sum + row.units * Math.floor(stakeCents * row.grossMultiplierBps / 10_000), 0);
  return Math.round(numerator / denominator);
}

const rouletteChoices = {
  red: { winningPockets: 18, grossMultiplier: 2 },
  dozen: { winningPockets: 12, grossMultiplier: 3 },
  column: { winningPockets: 12, grossMultiplier: 3 },
  straight: { winningPockets: 1, grossMultiplier: 36 },
  split: { winningPockets: 2, grossMultiplier: 18 },
  corner: { winningPockets: 4, grossMultiplier: 9 },
};

function roulette(stream, stakeCents, choice, pockets, american = false) {
  const rule = rouletteChoices[choice];
  if (!rule) throw new Error(`Unknown roulette choice: ${choice}`);
  const pocketIndex = stream.integer(pockets);
  const pocket = american && pocketIndex === 37 ? "00" : String(pocketIndex);
  const won = pocketIndex > 0 && pocketIndex <= rule.winningPockets;
  const grossPayoutCents = won ? stakeCents * rule.grossMultiplier : 0;
  const expectedGrossCents = Math.round(stakeCents * rule.winningPockets * rule.grossMultiplier / pockets);
  return { outcome: { pocket, won }, grossPayoutCents, expectedGrossCents, probabilityReference: `${rule.winningPockets}/${pockets}` };
}

const blackjackTables = {
  basic: [
    { id: "loss", units: 481_000, grossMultiplierBps: 0 },
    { id: "push", units: 85_000, grossMultiplierBps: 10_000 },
    { id: "win", units: 389_000, grossMultiplierBps: 20_000 },
    { id: "blackjack", units: 45_000, grossMultiplierBps: 25_000 },
  ],
  novice: [
    { id: "loss", units: 492_000, grossMultiplierBps: 0 },
    { id: "push", units: 85_000, grossMultiplierBps: 10_000 },
    { id: "win", units: 378_000, grossMultiplierBps: 20_000 },
    { id: "blackjack", units: 45_000, grossMultiplierBps: 25_000 },
  ],
  random: [
    { id: "loss", units: 510_000, grossMultiplierBps: 0 },
    { id: "push", units: 85_000, grossMultiplierBps: 10_000 },
    { id: "win", units: 360_000, grossMultiplierBps: 20_000 },
    { id: "blackjack", units: 45_000, grossMultiplierBps: 25_000 },
  ],
};

const baccaratTables = {
  banker: [
    { id: "banker", units: 458_597, grossMultiplierBps: 19_500 },
    { id: "player", units: 446_247, grossMultiplierBps: 0 },
    { id: "tie", units: 95_156, grossMultiplierBps: 10_000 },
  ],
  player: [
    { id: "banker", units: 458_597, grossMultiplierBps: 0 },
    { id: "player", units: 446_247, grossMultiplierBps: 20_000 },
    { id: "tie", units: 95_156, grossMultiplierBps: 10_000 },
  ],
  tie: [
    { id: "banker", units: 458_597, grossMultiplierBps: 0 },
    { id: "player", units: 446_247, grossMultiplierBps: 0 },
    { id: "tie", units: 95_156, grossMultiplierBps: 90_000 },
  ],
};

const moderateSlot = [
  { id: "no_win", units: 500_000, grossMultiplierBps: 0 },
  { id: "half_return", units: 200_000, grossMultiplierBps: 5_000 },
  { id: "stake_return", units: 150_000, grossMultiplierBps: 10_000 },
  { id: "two_x", units: 100_000, grossMultiplierBps: 20_000 },
  { id: "five_x", units: 40_000, grossMultiplierBps: 50_000 },
  { id: "thirty_one_x", units: 10_000, grossMultiplierBps: 310_000 },
];

const highSlot = [
  { id: "no_win", units: 860_000, grossMultiplierBps: 0 },
  { id: "stake_return", units: 100_000, grossMultiplierBps: 10_000 },
  { id: "five_x", units: 35_000, grossMultiplierBps: 50_000 },
  { id: "one_hundred_thirty_seven_x", units: 5_000, grossMultiplierBps: 1_370_000 },
];

const crapsTables = {
  pass_line: [
    { id: "win", units: 492_929, grossMultiplierBps: 20_000 },
    { id: "loss", units: 507_071, grossMultiplierBps: 0 },
  ],
  field: [
    { id: "win_even", units: 388_889, grossMultiplierBps: 20_000 },
    { id: "win_double", units: 55_555, grossMultiplierBps: 30_000 },
    { id: "loss", units: 555_556, grossMultiplierBps: 0 },
  ],
  any_seven: [
    { id: "seven", units: 166_667, grossMultiplierBps: 50_000 },
    { id: "other", units: 833_333, grossMultiplierBps: 0 },
  ],
};

const lotteryTable = [
  { id: "no_prize", units: 888_960, grossMultiplierBps: 0 },
  { id: "two_x", units: 100_000, grossMultiplierBps: 20_000 },
  { id: "ten_x", units: 10_000, grossMultiplierBps: 100_000 },
  { id: "hundred_x", units: 1_000, grossMultiplierBps: 1_000_000 },
  { id: "jackpot", units: 40, grossMultiplierBps: 100_000_000 },
];

function settleRows(stream, stakeCents, rows) {
  const { row, draw, denominator } = categorical(stream, rows);
  return {
    outcome: { outcomeId: row.id, draw, denominator },
    grossPayoutCents: Math.floor(stakeCents * row.grossMultiplierBps / 10_000),
    expectedGrossCents: expectationFromRows(stakeCents, rows),
    probabilityReference: `table/${denominator}`,
  };
}

function sports(stream, stakeCents, choice) {
  const legCount = choice === "parlay" ? 2 : 1;
  const probabilities = [];
  let trueProbability = 1;
  for (let index = 0; index < legCount; index += 1) {
    const p = 0.28 + stream.uniform() * 0.44;
    probabilities.push(Number(p.toFixed(6)));
    trueProbability *= p;
  }
  const margin = 0.06;
  const offeredDecimalOdds = Math.max(1.01, Number(((1 - margin) / trueProbability).toFixed(4)));
  const won = stream.uniform() < trueProbability;
  const grossPayoutCents = won ? Math.floor(stakeCents * offeredDecimalOdds) : 0;
  const expectedGrossCents = Math.round(stakeCents * offeredDecimalOdds * trueProbability);
  return {
    outcome: { won, trueProbabilities: probabilities, trueProbability: Number(trueProbability.toFixed(8)), offeredDecimalOdds, impliedProbability: Number((1 / offeredDecimalOdds).toFixed(8)), margin },
    grossPayoutCents,
    expectedGrossCents,
    probabilityReference: `synthetic-event/${trueProbability.toFixed(8)}`,
  };
}

function crash(stream, stakeCents, choice) {
  const target = Number(choice);
  const houseFactor = 0.97;
  const survivalProbability = houseFactor / target;
  const uniform = stream.uniform();
  const reachedTarget = uniform < survivalProbability;
  const grossPayoutCents = reachedTarget ? Math.floor(stakeCents * target) : 0;
  const realisedCrashMultiplier = Number(Math.max(1, houseFactor / Math.max(uniform, 0.0000001)).toFixed(2));
  return {
    outcome: { declaredTarget: target, reachedTarget, realisedCrashMultiplier },
    grossPayoutCents,
    expectedGrossCents: Math.round(stakeCents * houseFactor),
    probabilityReference: `0.97/${target}`,
  };
}

export const GAME_MATH = {
  european_roulette: { label: "European Roulette", volatility: "medium", rtpRange: [36 / 37, 36 / 37], choices: Object.keys(rouletteChoices), note: "37 equiprobable pockets; standard gross payouts." },
  american_roulette: { label: "American Roulette", volatility: "medium", rtpRange: [36 / 38, 36 / 38], choices: Object.keys(rouletteChoices), note: "38 equiprobable pockets including 00; standard gross payouts." },
  blackjack: { label: "Blackjack", volatility: "medium", rtpRange: [0.9175, 0.9755], choices: Object.keys(blackjackTables), note: "Auditable resolved-hand probability tables for frozen six-deck S17/DAS/3:2 policy classes; full shoe decisions are a documented production extension." },
  baccarat: { label: "Baccarat", volatility: "low-medium", rtpRange: [0.856404, 0.989418], choices: Object.keys(baccaratTables), note: "Standard eight-deck outcome probabilities; banker pays 0.95 profit and ties push main bets." },
  three_reel_slot: { label: "Three-Reel Slot", volatility: "medium", rtpRange: [0.96, 0.96], choices: ["spin"], note: "Published one-million-stop virtual reel table; 50% hit rate and 31x maximum gross payout." },
  high_volatility_slot: { label: "High-Volatility Video Slot", volatility: "very high", rtpRange: [0.96, 0.96], choices: ["spin"], note: "Published one-million-stop table; 14% hit rate and 137x maximum gross payout." },
  craps: { label: "Craps / Dice", volatility: "medium-high", rtpRange: [0.833335, 0.985858], choices: Object.keys(crapsTables), note: "Restricted resolved-bet catalogue: pass line, field, and any seven." },
  virtual_sports: { label: "Virtual Sports Betting", volatility: "high", rtpRange: [0.939, 0.941], choices: ["single", "parlay"], note: "Synthetic independent event probabilities with a declared 6% margin; no real match data." },
  crash: { label: "Crash", volatility: "very high", rtpRange: [0.97, 0.97], choices: ["1.25", "2", "5", "10"], note: "Targets are declared before the draw; P(reach target)=0.97/target." },
  lottery: { label: "Lottery / Jackpot", volatility: "extreme", rtpRange: [0.8, 0.8], choices: ["ticket"], note: "Published one-million-ticket table; jackpot probability 40 in 1,000,000 and 10,000x gross payout." },
};

export function theoreticalRtp(gameId, choice, stakeCents = 10_000) {
  if (gameId === "european_roulette") return 36 / 37;
  if (gameId === "american_roulette") return 36 / 38;
  if (gameId === "blackjack") return expectationFromRows(10_000, blackjackTables[choice]) / 10_000;
  if (gameId === "baccarat") return expectationFromRows(10_000, baccaratTables[choice]) / 10_000;
  if (gameId === "three_reel_slot") return 0.96;
  if (gameId === "high_volatility_slot") return 0.96;
  if (gameId === "craps") return expectationFromRows(10_000, crapsTables[choice]) / 10_000;
  if (gameId === "virtual_sports") return 0.94;
  if (gameId === "crash") return 0.97;
  if (gameId === "lottery") return 0.8;
  const mock = { integer: () => 0, uniform: () => 0 };
  return settleGame(gameId, choice, stakeCents, mock).expectedGrossCents / stakeCents;
}

export function settleGame(gameId, choice, stakeCents, outcomeStream) {
  if (!Number.isSafeInteger(stakeCents) || stakeCents <= 0) throw new Error("Stake must be a positive integer number of cents");
  switch (gameId) {
    case "european_roulette": return roulette(outcomeStream, stakeCents, choice, 37, false);
    case "american_roulette": return roulette(outcomeStream, stakeCents, choice, 38, true);
    case "blackjack": return settleRows(outcomeStream, stakeCents, blackjackTables[choice]);
    case "baccarat": return settleRows(outcomeStream, stakeCents, baccaratTables[choice]);
    case "three_reel_slot": return settleRows(outcomeStream, stakeCents, moderateSlot);
    case "high_volatility_slot": return settleRows(outcomeStream, stakeCents, highSlot);
    case "craps": return settleRows(outcomeStream, stakeCents, crapsTables[choice]);
    case "virtual_sports": return sports(outcomeStream, stakeCents, choice);
    case "crash": return crash(outcomeStream, stakeCents, choice);
    case "lottery": return settleRows(outcomeStream, stakeCents, lotteryTable);
    default: throw new Error(`Unknown game: ${gameId}`);
  }
}

export function gameValidationRows(stakeCents = 10_000) {
  return Object.entries(GAME_MATH).flatMap(([gameId, game]) => game.choices.map((choice) => ({
    gameId,
    game: game.label,
    choice,
    theoreticalRtp: theoreticalRtp(gameId, choice, stakeCents),
    houseEdge: 1 - theoreticalRtp(gameId, choice, stakeCents),
    volatility: game.volatility,
    ruleNote: game.note,
  })));
}
