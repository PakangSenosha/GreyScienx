import test from "node:test";
import assert from "node:assert/strict";
import { GAME_MATH, gameValidationRows, settleGame, theoreticalRtp } from "../engine/games.mjs";
import { stream } from "../engine/random.mjs";

test("all ten games publish finite, negative-expectation mathematics", () => {
  assert.equal(Object.keys(GAME_MATH).length, 10);
  for (const row of gameValidationRows()) {
    assert.ok(row.theoreticalRtp > 0 && row.theoreticalRtp < 1, `${row.gameId}/${row.choice}`);
    assert.equal(row.houseEdge, 1 - row.theoreticalRtp);
  }
});

test("roulette rules differ only by the extra American pocket", () => {
  assert.equal(theoreticalRtp("european_roulette", "red"), 36 / 37);
  assert.equal(theoreticalRtp("american_roulette", "red"), 36 / 38);
  for (const choice of GAME_MATH.european_roulette.choices) assert.equal(theoreticalRtp("european_roulette", choice), 36 / 37);
});

test("slot pair has equal exact RTP and unequal empirical variance", () => {
  assert.equal(theoreticalRtp("three_reel_slot", "spin"), 0.96);
  assert.equal(theoreticalRtp("high_volatility_slot", "spin"), 0.96);
  const sample = (gameId) => {
    const rng = stream("slot-test", gameId);
    const values = Array.from({ length: 200_000 }, () => settleGame(gameId, "spin", 10_000, rng).grossPayoutCents / 10_000);
    const mean = values.reduce((sum, value) => sum + value, 0) / values.length;
    const variance = values.reduce((sum, value) => sum + (value - mean) ** 2, 0) / values.length;
    return { mean, variance };
  };
  const moderate = sample("three_reel_slot");
  const high = sample("high_volatility_slot");
  assert.ok(Math.abs(moderate.mean - 0.96) < 0.03);
  assert.ok(Math.abs(high.mean - 0.96) < 0.08);
  assert.ok(high.variance > moderate.variance * 5);
});

test("settlements use integer cents and never produce a negative gross payout", () => {
  for (const [gameId, game] of Object.entries(GAME_MATH)) {
    for (const choice of game.choices) {
      const result = settleGame(gameId, choice, 10_000, stream("integer-test", gameId, choice));
      assert.ok(Number.isSafeInteger(result.grossPayoutCents));
      assert.ok(Number.isSafeInteger(result.expectedGrossCents));
      assert.ok(result.grossPayoutCents >= 0);
    }
  }
});

test("representative large samples converge toward each implemented return", () => {
  const cases = [
    ["european_roulette", "red", 0.012],
    ["american_roulette", "red", 0.014],
    ["blackjack", "basic", 0.012],
    ["baccarat", "banker", 0.012],
    ["three_reel_slot", "spin", 0.025],
    ["high_volatility_slot", "spin", 0.07],
    ["craps", "pass_line", 0.012],
    ["virtual_sports", "single", 0.02],
    ["crash", "2", 0.02],
    ["lottery", "ticket", 0.2],
  ];
  for (const [gameId, choice, tolerance] of cases) {
    const rng = stream("all-game-convergence-v1", gameId);
    let payout = 0;
    const draws = gameId === "lottery" ? 1_000_000 : 200_000;
    for (let index = 0; index < draws; index += 1) payout += settleGame(gameId, choice, 10_000, rng).grossPayoutCents;
    const observed = payout / (draws * 10_000);
    assert.ok(Math.abs(observed - theoreticalRtp(gameId, choice)) < tolerance, `${gameId}: observed ${observed}`);
  }
});
