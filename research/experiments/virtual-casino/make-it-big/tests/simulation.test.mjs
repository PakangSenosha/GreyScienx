import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";
import { exactCumulativeIncidence, simulateStudy, targetProbability, validateProtocol } from "../engine/simulate.mjs";

const studyDir = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const config = JSON.parse(readFileSync(resolve(studyDir, "protocol-v1.0.json"), "utf8"));

test("protocol is internally consistent and all strategy arms spend R1,000 monthly", () => {
  assert.equal(validateProtocol(config), true);
  for (const strategy of config.strategies) {
    assert.equal(strategy.stakeCents * strategy.betsPerMonth, config.monthlyBudgetCents);
  }
});

test("the exact cumulative incidence matches the Bernoulli first-passage formula", () => {
  assert.equal(exactCumulativeIncidence(0.5, 1), 0.5);
  assert.equal(exactCumulativeIncidence(0.5, 2), 0.75);
});

test("the controlled crash arm holds target probability approximately constant by monthly spend", () => {
  const game = config.games.find((candidate) => candidate.id === "crash_target");
  const probabilities = config.strategies.map((strategy) => {
    const perBet = targetProbability(config, game, strategy);
    return exactCumulativeIncidence(perBet, strategy.betsPerMonth * 36);
  });
  assert.ok(Math.max(...probabilities) - Math.min(...probabilities) < 0.0001);
});

test("the jackpot slot and lottery tail answer the stake-frequency question differently", () => {
  const slot = config.games.find((candidate) => candidate.id === "jackpot_slot");
  const lottery = config.games.find((candidate) => candidate.id === "lottery_tail");
  const largeStake = config.strategies[0];
  const smallStake = config.strategies.at(-1);
  assert.ok(targetProbability(config, slot, largeStake) > targetProbability(config, slot, smallStake));
  assert.equal(targetProbability(config, lottery, largeStake), targetProbability(config, lottery, smallStake));
});

test("the reference study is deterministic and respects all accounting caps", () => {
  const first = simulateStudy(config);
  const second = simulateStudy(config);
  assert.deepEqual(first, second);
  for (const cell of first.cells) {
    assert.equal(cell.oneYearWinners + cell.oneYearBudgetExhaustedWithoutTarget, config.entrantsPerCell);
    assert.equal(cell.threeYearWinners + cell.threeYearBudgetExhaustedWithoutTarget, config.entrantsPerCell);
    assert.ok(cell.simulatedProbability36Months >= cell.simulatedProbability12Months);
    assert.ok(cell.totalSpendCents <= config.entrantsPerCell * config.monthlyBudgetCents * config.maximumMonths);
  }
});
