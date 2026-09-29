import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { generateManifest } from "../engine/policies.mjs";
import { hashObject, stream } from "../engine/random.mjs";
import { advanceAfterRuin, aggregatePlayers, simulateVisibleWorld } from "../engine/simulate.mjs";

const config = JSON.parse(readFileSync(new URL("../protocol-v1.0.json", import.meta.url), "utf8"));

test("manifest has exactly 1,000 stable policies balanced 100 per cohort", () => {
  const first = generateManifest(config);
  const second = generateManifest(config);
  assert.equal(first.length, 1000);
  assert.equal(hashObject(first), hashObject(second));
  assert.equal(new Set(first.map((player) => player.playerId)).size, 1000);
  for (const cohort of config.cohorts) assert.equal(first.filter((player) => player.cohortId === cohort.id).length, 100);
  for (const player of first) assert.ok(Math.abs(Object.values(player.gameWeights).reduce((sum, weight) => sum + weight, 0) - 1) < 0.00001);
});

test("random streams are deterministic and independently addressed", () => {
  const a = stream("world", "P0001", "slot", "outcome");
  const b = stream("world", "P0001", "slot", "outcome");
  const c = stream("world", "P0001", "stake");
  const valuesA = Array.from({ length: 12 }, () => a.nextUint());
  const valuesB = Array.from({ length: 12 }, () => b.nextUint());
  const valuesC = Array.from({ length: 12 }, () => c.nextUint());
  assert.deepEqual(valuesA, valuesB);
  assert.notDeepEqual(valuesA, valuesC);
});

test("visible world is byte-stable and enforces ledger/accounting invariants", () => {
  const smallConfig = { ...config, cohortSize: 2, population: 20, calendarDays: 28, sessionModel: { ...config.sessionModel, weeks: 4 } };
  const manifest = generateManifest(smallConfig);
  const first = simulateVisibleWorld(smallConfig, manifest, "test-visible-world");
  const second = simulateVisibleWorld(smallConfig, manifest, "test-visible-world");
  assert.equal(first.finalEventHash, second.finalEventHash);
  assert.equal(first.finalStateHash, second.finalStateHash);
  const betIds = new Set();
  for (const event of first.ledger) {
    if (event.eventType !== "wager_settled") continue;
    assert.equal(event.bankrollAfterCents, event.bankrollBeforeCents - event.stakeCents + event.grossPayoutCents);
    assert.ok(event.stakeCents <= event.bankrollBeforeCents);
    assert.ok(event.bankrollAfterCents >= 0);
    assert.ok(!betIds.has(event.betId));
    betIds.add(event.betId);
  }
  for (const player of first.players) assert.ok(player.allocationsUsed <= config.allocationCap);
  const aggregate = aggregatePlayers(first.players);
  assert.equal(aggregate.ggrCents, -aggregate.playerWagerPnlCents);
});

test("ruin resets exactly R10,000 until the sixth allocation, then inactivates", () => {
  const policy = { cooldownSessionsAfterRuin: 2 };
  const base = { allocationsUsed: 5, bankrollMonth: 5, cumulativeAllocatedCents: 5_000_000, bankrollCents: 0, allocationWagers: 9, allocationTurnoverCents: 900_000, allocationStartedAt: "earlier", cooldownRemaining: 0, status: "active" };
  assert.equal(advanceAfterRuin(config, policy, base, "2026-02-01T00:00:00.000Z"), "allocation-started");
  assert.equal(base.allocationsUsed, 6);
  assert.equal(base.bankrollMonth, 6);
  assert.equal(base.cumulativeAllocatedCents, 6_000_000);
  assert.equal(base.bankrollCents, 1_000_000);
  assert.equal(base.cooldownRemaining, 2);
  base.bankrollCents = 0;
  assert.equal(advanceAfterRuin(config, policy, base, "2026-03-01T00:00:00.000Z"), "player-inactivated");
  assert.equal(base.allocationsUsed, 6);
  assert.equal(base.cumulativeAllocatedCents, 6_000_000);
  assert.equal(base.status, "inactive-all-six-allocations-used");
});
