import { createGunzip } from "node:zlib";
import { createReadStream, readFileSync } from "node:fs";
import { resolve, dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { createInterface } from "node:readline";
import { pipeline } from "node:stream/promises";
import { PassThrough } from "node:stream";
import { generateManifest } from "../engine/policies.mjs";
import { aggregatePlayers, simulateVisibleWorld } from "../engine/simulate.mjs";
import { hashObject, sha256 } from "../engine/random.mjs";

const experimentDir = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const artifactDir = join(experimentDir, "artifacts", "v1.0");
const config = JSON.parse(readFileSync(join(experimentDir, "protocol-v1.0.json"), "utf8"));
const expected = JSON.parse(readFileSync(join(artifactDir, "run-metadata.json"), "utf8"));
const checkpoints = JSON.parse(readFileSync(join(artifactDir, "checkpoints.json"), "utf8"));

async function readLedger(path) {
  const output = new PassThrough();
  const events = [];
  const reading = (async () => {
    const lines = createInterface({ input: output, crlfDelay: Infinity });
    for await (const line of lines) if (line) events.push(JSON.parse(line));
  })();
  await pipeline(createReadStream(path), createGunzip(), output);
  await reading;
  return events;
}

function validateLedger(events) {
  let previousHash = "0".repeat(64);
  const betIds = new Set();
  let handleCents = 0;
  let payoutCents = 0;
  for (let index = 0; index < events.length; index += 1) {
    const event = events[index];
    if (event.sequenceNumber !== index + 1) throw new Error(`Non-monotonic sequence at ${index + 1}`);
    if (event.previousEventHash !== previousHash) throw new Error(`Broken hash chain at ${event.sequenceNumber}`);
    const { eventHash, ...body } = event;
    const calculated = sha256(previousHash + hashObject(body));
    if (calculated !== eventHash) throw new Error(`Event hash mismatch at ${event.sequenceNumber}`);
    if (event.eventType === "wager_settled") {
      if (betIds.has(event.betId)) throw new Error(`Duplicate settlement ${event.betId}`);
      betIds.add(event.betId);
      if (!Number.isSafeInteger(event.stakeCents) || event.stakeCents <= 0) throw new Error(`Invalid stake ${event.betId}`);
      if (event.stakeCents > event.bankrollBeforeCents) throw new Error(`Over-bankroll stake ${event.betId}`);
      if (event.bankrollAfterCents !== event.bankrollBeforeCents - event.stakeCents + event.grossPayoutCents) throw new Error(`Bankroll invariant failed ${event.betId}`);
      if (event.bankrollAfterCents < 0) throw new Error(`Negative bankroll ${event.betId}`);
      handleCents += event.stakeCents;
      payoutCents += event.grossPayoutCents;
    }
    if (event.eventType === "allocation_started" && event.bankrollMonth > config.allocationCap) throw new Error(`Allocation cap exceeded for ${event.playerId}`);
    previousHash = eventHash;
  }
  return { finalEventHash: previousHash, wagers: betIds.size, handleCents, payoutCents, ggrCents: handleCents - payoutCents };
}

const ledger = await readLedger(join(artifactDir, "visible-ledger.ndjson.gz"));
const ledgerReport = validateLedger(ledger);
const manifest = generateManifest(config);
const rerun = simulateVisibleWorld(config, manifest, config.visibleWorldSeed);
const rerunAggregate = aggregatePlayers(rerun.players);
const checkpointHashesValid = checkpoints.every((checkpoint) => {
  const { checkpointHash, ...body } = checkpoint;
  return hashObject(body) === checkpointHash;
});
const finalCheckpoint = checkpoints.findLast((checkpoint) => checkpoint.checkpointType === "final");
const finalCheckpointMatchesReplay = finalCheckpoint?.lastLedgerEventHash === rerun.finalEventHash && finalCheckpoint?.finalPlayerStateHash === rerun.finalStateHash;
const report = {
  valid: ledgerReport.finalEventHash === expected.finalEventHash && rerun.finalEventHash === expected.finalEventHash && rerun.finalStateHash === expected.finalStateHash && rerunAggregate.ggrCents === ledgerReport.ggrCents && checkpointHashesValid && finalCheckpointMatchesReplay,
  ledgerReport,
  expectedFinalEventHash: expected.finalEventHash,
  replayedFinalEventHash: rerun.finalEventHash,
  expectedFinalStateHash: expected.finalStateHash,
  replayedFinalStateHash: rerun.finalStateHash,
  checkpointsVerified: checkpoints.length,
  checkpointHashesValid,
  finalCheckpointMatchesReplay,
  casinoGgrReconcilesToNegativePlayerWagerPnl: rerunAggregate.ggrCents === -rerunAggregate.playerWagerPnlCents,
};
console.log(JSON.stringify(report, null, 2));
if (!report.valid || !report.casinoGgrReconcilesToNegativePlayerWagerPnl) process.exitCode = 1;
