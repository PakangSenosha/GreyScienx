import { createHash } from "node:crypto";
import { copyFileSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { hashObject } from "../../engine/random.mjs";
import { simulateStudy } from "../engine/simulate.mjs";

const studyDir = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const casinoDir = resolve(studyDir, "..");
const repoDir = resolve(casinoDir, "../../..");
const artifactDir = join(studyDir, "artifacts", "v1.0");
const publicDir = join(repoDir, "public", "experiments", "virtual-casino", "make-it-big", "v1.0");
const publicSourceDir = join(publicDir, "source");
mkdirSync(artifactDir, { recursive: true });
mkdirSync(publicSourceDir, { recursive: true });

const configPath = join(studyDir, "protocol-v1.0.json");
const config = JSON.parse(readFileSync(configPath, "utf8"));
const sourceFiles = ["engine/simulate.mjs", "scripts/generate-artifacts.mjs", "tests/simulation.test.mjs"];
const sourceHash = hashObject(Object.fromEntries(sourceFiles.map((file) => [file, readFileSync(join(studyDir, file), "utf8")])));
const configHash = hashObject(config);
const result = simulateStudy(config);

function writeJson(path, value) {
  writeFileSync(path, `${JSON.stringify(value, null, 2)}\n`);
}

function csvValue(value) {
  if (value === null || value === undefined) return "";
  const text = String(value);
  return /[",\n]/.test(text) ? `"${text.replaceAll('"', '""')}"` : text;
}

function writeCsv(path, rows) {
  const columns = Object.keys(rows[0]);
  writeFileSync(path, `${columns.join(",")}\n${rows.map((row) => columns.map((column) => csvValue(row[column])).join(",")).join("\n")}\n`);
}

function fileHash(path) {
  return createHash("sha256").update(readFileSync(path)).digest("hex");
}

const dashboard = {
  metadata: {
    experimentId: config.experimentId,
    protocolVersion: config.protocolVersion,
    status: config.status,
    generatedAt: config.generatedAt,
    configHash,
    sourceHash,
    simulationSeed: config.simulationSeed,
    prng: "xoshiro128** with cyrb128 stream initialisation",
  },
  design: {
    targetPayoutCents: config.targetPayoutCents,
    monthlyBudgetCents: config.monthlyBudgetCents,
    maximumMonths: config.maximumMonths,
    horizonsMonths: config.horizonsMonths,
    entrantsPerCell: config.entrantsPerCell,
    strategies: config.strategies,
  },
  games: config.games.map(({ outcomes, ...game }) => ({ ...game, outcomes: outcomes ?? null })),
  ...result,
};

writeJson(join(artifactDir, "dashboard.json"), dashboard);
writeJson(join(artifactDir, "run-metadata.json"), dashboard.metadata);
writeJson(join(artifactDir, "rulesets.json"), dashboard.games);
writeCsv(join(artifactDir, "cell-results.csv"), result.cells);
writeCsv(join(artifactDir, "survival.csv"), result.survival);
writeCsv(join(artifactDir, "audit-entrants.csv"), result.auditEntrants);
copyFileSync(configPath, join(artifactDir, "protocol-v1.0.json"));

const releaseFiles = [
  "dashboard.json",
  "run-metadata.json",
  "rulesets.json",
  "cell-results.csv",
  "survival.csv",
  "audit-entrants.csv",
  "protocol-v1.0.json",
];
for (const file of releaseFiles) copyFileSync(join(artifactDir, file), join(publicDir, file));
for (const file of ["README.md", "METHODS.md"]) copyFileSync(join(studyDir, "docs", file), join(publicDir, file));
for (const file of sourceFiles) {
  const destination = join(publicSourceDir, file.replaceAll("/", "-"));
  copyFileSync(join(studyDir, file), destination);
}

const publicFiles = [
  ...releaseFiles,
  "README.md",
  "METHODS.md",
  ...sourceFiles.map((file) => `source/${file.replaceAll("/", "-")}`),
];
writeFileSync(join(publicDir, "checksums.sha256"), `${publicFiles.map((file) => `${fileHash(join(publicDir, file))}  ${file}`).join("\n")}\n`);

console.log(JSON.stringify({ ...result.summary, configHash, sourceHash }, null, 2));
