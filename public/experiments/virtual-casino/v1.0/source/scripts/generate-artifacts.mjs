import { createHash } from "node:crypto";
import { createGzip } from "node:zlib";
import { execFileSync } from "node:child_process";
import { createReadStream, createWriteStream, existsSync, mkdirSync, readFileSync, writeFileSync, copyFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { pipeline } from "node:stream/promises";
import { availableParallelism } from "node:os";
import { Worker } from "node:worker_threads";
import { fileURLToPath } from "node:url";
import { generateManifest } from "../engine/policies.mjs";
import { aggregatePlayers, simulateVisibleWorld } from "../engine/simulate.mjs";
import { addReplicationWorld, buildReplicationAccumulator, checkpointRows, cohortSummaries, finaliseReplication, gameSummaries, ledgerTimeSeries, playerMonthlyHistory, pnlHistogram } from "../engine/analysis.mjs";
import { gameValidationRows } from "../engine/games.mjs";
import { hashObject, sha256 } from "../engine/random.mjs";

const experimentDir = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const repoDir = resolve(experimentDir, "../../..");
const artifactDir = join(experimentDir, "artifacts", "v1.0");
const publicDir = join(repoDir, "public", "experiments", "virtual-casino", "v1.0");
mkdirSync(artifactDir, { recursive: true });
mkdirSync(publicDir, { recursive: true });

const configPath = join(experimentDir, "protocol-v1.0.json");
const config = JSON.parse(readFileSync(configPath, "utf8"));
const configHash = hashObject(config);
const manifest = generateManifest(config);
const manifestHash = hashObject(manifest);
const visibleSeedCommitment = sha256(config.visibleWorldSeed);
const sourceFiles = [
  "engine/random.mjs", "engine/games.mjs", "engine/policies.mjs", "engine/simulate.mjs", "engine/analysis.mjs",
  "scripts/generate-artifacts.mjs", "scripts/replication-worker.mjs", "scripts/replay.mjs",
  "tests/games.test.mjs", "tests/protocol.test.mjs", "schemas/ledger-event.schema.json", "schemas/postgres.sql",
];
const sourceHash = hashObject(Object.fromEntries(sourceFiles.map((file) => [file, readFileSync(join(experimentDir, file), "utf8")])));
const codeRevision = (() => {
  try {
    const revision = execFileSync("git", ["rev-parse", "HEAD"], { cwd: repoDir, encoding: "utf8" }).trim();
    const dirty = execFileSync("git", ["status", "--porcelain", "--", "research/experiments/virtual-casino", "app/experiments/virtual-casino", "lib/virtualCasino.ts"], { cwd: repoDir, encoding: "utf8" }).trim();
    return `${revision}${dirty ? "+dirty" : ""}`;
  }
  catch { return "uncommitted-local-worktree"; }
})();

function writeJson(path, data) {
  writeFileSync(path, `${JSON.stringify(data, null, 2)}\n`);
}

function csvValue(value) {
  if (value === null || value === undefined) return "";
  const text = typeof value === "object" ? JSON.stringify(value) : String(value);
  return /[",\n]/.test(text) ? `"${text.replaceAll('"', '""')}"` : text;
}

function writeCsv(path, rows) {
  if (!rows.length) return writeFileSync(path, "");
  const columns = Object.keys(rows[0]);
  writeFileSync(path, `${columns.join(",")}\n${rows.map((row) => columns.map((column) => csvValue(row[column])).join(",")).join("\n")}\n`);
}

async function writeGzipLedger(path, ledger) {
  const source = join(artifactDir, ".visible-ledger.ndjson.tmp");
  writeFileSync(source, `${ledger.map((event) => JSON.stringify(event)).join("\n")}\n`);
  await pipeline(createReadStream(source), createGzip({ level: 9 }), createWriteStream(path));
  const { unlinkSync } = await import("node:fs");
  unlinkSync(source);
}

function fileHash(path) {
  return createHash("sha256").update(readFileSync(path)).digest("hex");
}

console.log("[1/5] Generating the frozen 1,000-player policy manifest");
writeJson(join(artifactDir, "player-manifest.json"), { experimentId: config.experimentId, protocolVersion: config.protocolVersion, manifestHash, players: manifest });
copyFileSync(configPath, join(artifactDir, "protocol-v1.0.json"));

console.log("[2/5] Running visible world and immutable ledger");
const visible = simulateVisibleWorld(config, manifest, config.visibleWorldSeed);
const summary = aggregatePlayers(visible.players);
const timeseries = ledgerTimeSeries(config, visible.ledger);
const histories = playerMonthlyHistory(config, visible.ledger);
const cohorts = cohortSummaries(config, visible.players);
const games = gameSummaries(config, visible.players);
const checkpoints = checkpointRows(config, visible.ledger, visible.players, configHash, manifestHash);
await writeGzipLedger(join(artifactDir, "visible-ledger.ndjson.gz"), visible.ledger);
writeJson(join(artifactDir, "checkpoints.json"), checkpoints);
writeJson(join(artifactDir, "game-mathematics.json"), gameValidationRows());

console.log("[3/5] Running 1,000 independently seeded replication worlds");
const accumulator = buildReplicationAccumulator(config, manifest);
await new Promise((resolvePool, rejectPool) => {
  const workerCount = Math.min(16, Math.max(1, availableParallelism()), config.replicationWorlds);
  let nextWorld = 1;
  let completed = 0;
  let closed = 0;
  const workers = Array.from({ length: workerCount }, () => new Worker(new URL("./replication-worker.mjs", import.meta.url), { workerData: { config, manifest } }));
  const assign = (worker) => {
    if (nextWorld <= config.replicationWorlds) worker.postMessage(nextWorld++);
    else worker.postMessage(null);
  };
  for (const worker of workers) {
    worker.on("message", ({ worldIndex, players: worldPlayers }) => {
      addReplicationWorld(accumulator, config, worldIndex, worldPlayers);
      completed += 1;
      if (completed % 100 === 0) console.log(`  completed ${completed}/${config.replicationWorlds}`);
      assign(worker);
    });
    worker.on("error", rejectPool);
    worker.on("exit", (code) => {
      if (code !== 0) return rejectPool(new Error(`Replication worker exited ${code}`));
      closed += 1;
      if (closed === workers.length) resolvePool();
    });
    assign(worker);
  }
});
const replication = finaliseReplication(accumulator, config, visible.players, summary);
const replicationByPlayer = new Map(replication.players.map((row) => [row.playerId, row]));
const policyByPlayer = new Map(manifest.map((row) => [row.playerId, row]));
const ranked = [...visible.players].sort((a, b) => b.netPnlCents - a.netPnlCents);
const rankByPlayer = new Map(ranked.map((player, index) => [player.playerId, index + 1]));
const players = visible.players.map((player) => ({
  ...player,
  rank: rankByPlayer.get(player.playerId),
  policy: policyByPlayer.get(player.playerId),
  monthlyHistory: histories[player.playerId] ?? [],
  replication: replicationByPlayer.get(player.playerId),
}));
const replicationCohorts = new Map(replication.cohorts.map((row) => [row.cohortId, row]));
const cohortRows = cohorts.map((row) => ({ ...row, replication: replicationCohorts.get(row.id) }));

console.log("[4/5] Writing audit, analysis, and dashboard artifacts");
const runMetadata = {
  experimentId: config.experimentId,
  protocolVersion: config.protocolVersion,
  status: config.status,
  generatedAt: new Date(Date.parse(config.calendarStart) + config.calendarDays * 86_400_000 - 1).toISOString(),
  codeRevision,
  sourceHash,
  configHash,
  manifestHash,
  visibleSeedCommitment,
  visibleSeed: config.visibleWorldSeed,
  visibleSeedStatus: config.visibleWorldSeedStatus,
  finalEventHash: visible.finalEventHash,
  finalStateHash: visible.finalStateHash,
  replicationWorlds: config.replicationWorlds,
  syntheticOnly: true,
};
writeJson(join(artifactDir, "run-metadata.json"), runMetadata);
writeJson(join(artifactDir, "source-manifest.json"), { sourceHash, files: sourceFiles });
copyFileSync(join(repoDir, "package-lock.json"), join(artifactDir, "environment-package-lock.json"));
writeJson(join(artifactDir, "visible-summary.json"), { metadata: runMetadata, summary });
writeCsv(join(artifactDir, "players.csv"), players.map(({ policy, replication: playerReplication, gameStats, ...player }) => {
  const { monthlyHistory, ...summaryPlayer } = player;
  return { ...summaryPlayer, gameStats, historyMonths: monthlyHistory.length, policyId: policy.policyVersion, replicationMedianPnlCents: playerReplication.medianPnlCents, replicationProbabilityAhead: playerReplication.probabilityAhead };
}));
writeCsv(join(artifactDir, "cohorts.csv"), cohortRows.map((row) => ({ ...row, replication: row.replication })));
writeCsv(join(artifactDir, "games.csv"), games.map((row) => ({ ...row, choices: row.choices })));
writeCsv(join(artifactDir, "daily-timeseries.csv"), timeseries);
writeCsv(join(artifactDir, "replication-worlds.csv"), replication.worlds);
writeCsv(join(artifactDir, "replication-players.csv"), replication.players);
writeCsv(join(artifactDir, "replication-cohorts.csv"), replication.cohorts);

const highlightedIds = new Set([...ranked.slice(0, 5), ...ranked.slice(-5)].map((player) => player.playerId));
const dashboard = {
  metadata: runMetadata,
  summary,
  distribution: {
    histogram: pnlHistogram(players),
    orderedPlayerIds: ranked.map((player) => player.playerId),
    p05PnlCents: ranked[Math.floor(ranked.length * 0.95)].netPnlCents,
    medianPnlCents: ranked[Math.floor(ranked.length * 0.5)].netPnlCents,
    p95PnlCents: ranked[Math.floor(ranked.length * 0.05)].netPnlCents,
  },
  timeseries,
  players,
  cohorts: cohortRows,
  games,
  replication: {
    completedWorlds: replication.completedWorlds,
    visibleWorldPercentile: replication.visibleWorldPercentile,
    ggrDistribution: pnlHistogram(replication.worlds.map((world) => ({ netPnlCents: world.ggrCents })), 24),
    profitablePlayerCounts: replication.worlds.map((world) => world.playersAhead),
    highlightedPolicies: replication.players.filter((row) => highlightedIds.has(row.playerId)),
    cohorts: replication.cohorts,
  },
  methods: {
    hypotheses: ["Exposure", "Frequency convergence", "Stake-size ruin", "Loss-chasing", "Limit-setting", "Equal-RTP volatility", "Winner persistence", "Replication", "Roulette rules"],
    limitations: [
      "Synthetic agents are simplified behavioural models, not people.",
      "Results depend on the frozen policies, game abstractions, stake limits, and six-month horizon.",
      "Bankroll month is an allocation episode, not a calendar month.",
      "The resolved-hand blackjack model is auditable but is not a card-by-card shoe implementation.",
      "Rare jackpot estimates remain unstable even across 1,000 worlds.",
    ],
  },
};
writeJson(join(artifactDir, "dashboard.json"), dashboard);

console.log("[5/5] Publishing the read-only reproducibility download bundle");
const publicFiles = [
  "protocol-v1.0.json", "player-manifest.json", "run-metadata.json", "source-manifest.json", "environment-package-lock.json", "visible-summary.json", "game-mathematics.json", "checkpoints.json",
  "players.csv", "cohorts.csv", "games.csv", "daily-timeseries.csv", "replication-worlds.csv", "replication-players.csv", "replication-cohorts.csv", "visible-ledger.ndjson.gz",
];
for (const file of publicFiles) copyFileSync(join(artifactDir, file), join(publicDir, file));
for (const file of sourceFiles) {
  const destination = join(publicDir, "source", file);
  mkdirSync(dirname(destination), { recursive: true });
  copyFileSync(join(experimentDir, file), destination);
}
const documentationFiles = ["README.md", "ARCHITECTURE.md", "PREREGISTRATION.md", "METHODS.md", "SAFETY.md", "DATA_DICTIONARY.md", "PRODUCTION-SCALE.md", "CHANGELOG.md"];
for (const file of documentationFiles) {
  const source = join(experimentDir, "docs", file);
  if (existsSync(source)) copyFileSync(source, join(publicDir, file));
}
const checksumFiles = [...publicFiles, ...sourceFiles.map((file) => `source/${file}`), ...documentationFiles.filter((file) => existsSync(join(publicDir, file)))];
const checksums = checksumFiles.map((file) => `${fileHash(join(publicDir, file))}  ${file}`).join("\n") + "\n";
writeFileSync(join(publicDir, "checksums.sha256"), checksums);
writeFileSync(join(artifactDir, "checksums.sha256"), checksums);
console.log(JSON.stringify({ wagers: summary.wagers, ledgerEvents: visible.ledger.length, replicationWorlds: replication.completedWorlds, finalEventHash: visible.finalEventHash, finalStateHash: visible.finalStateHash }, null, 2));
