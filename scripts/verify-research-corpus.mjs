import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { researchGraph } from "../lib/research/graph.ts";
import { packageFor } from "../lib/research/packages.ts";
import { researchObjects } from "../lib/research/registry.ts";
import { manuscriptFor } from "../lib/research/manuscripts.ts";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const sourceRoot = path.join(root, "research", "source");
const failures = [];
const sourceIds = new Set();
const objectIds = new Set();
let fileCount = 0;
let externalSourceCount = 0;
let reproducedModelCount = 0;

check(researchObjects.length === 29, `Expected 29 studies; found ${researchObjects.length}.`);

for (const study of researchObjects) {
  check(study.extraction_status === "full_text_claim_led", `${study.id} has no full-text, claim-led extraction.`);
  check(study.claims.length > 0, `${study.id} has no claims.`);
  check(study.assumptions.length > 0, `${study.id} has no assumptions.`);
  check(study.results.length > 0, `${study.id} has no results.`);
  check(study.models.length > 0, `${study.id} has no model.`);
  check(Boolean(study.answer), `${study.id} has no answer-sized retrieval block.`);
  const manuscript = manuscriptFor(study.id);
  check(Boolean(manuscript), `${study.id} has no compiled full-text manuscript.`);
  if (manuscript) {
    const source = path.join(root, ...manuscript.source_path.split("/"));
    check(fs.existsSync(source), `${study.id} manuscript source is missing: ${manuscript.source_path}`);
    if (fs.existsSync(source)) {
      const normalized = fs.readFileSync(source, "utf8").replaceAll("\r\n", "\n");
      check(sha256(normalized) === manuscript.source_sha256, `${study.id} manuscript checksum is stale.`);
      check(normalized === manuscript.content_markdown, `${study.id} compiled manuscript differs from its source.`);
    }
    check(manuscript.word_count > 250, `${study.id} manuscript is unexpectedly short.`);
    check(manuscript.headings.length > 2, `${study.id} manuscript has too few indexed headings.`);
    check(study.links.manuscript.endsWith(`/api/v1/research/${study.slug}/manuscript`), `${study.id} manuscript API link is unstable.`);
  }

  for (const source of study.sources) {
    uniqueId(source.id);
    sourceIds.add(source.id);
    if (source.href) {
      checkUrl(source.href, `${source.id} source URL`);
      if (source.type !== "manuscript") externalSourceCount += 1;
    }
  }
  const assumptions = new Set(study.assumptions.map((item) => item.id));
  const results = new Set(study.results.map((item) => item.id));
  for (const item of [...study.claims, ...study.assumptions, ...study.results, ...study.models]) uniqueId(item.id);
  for (const claim of study.claims) {
    for (const id of claim.depends_on) check(assumptions.has(id), `${claim.id} cites missing assumption ${id}.`);
    for (const id of claim.results) check(results.has(id), `${claim.id} cites missing result ${id}.`);
    for (const id of claim.supported_by) check(sourceIds.has(id), `${claim.id} cites missing source ${id}.`);
    checkUrl(claim.href, `${claim.id} URL`);
  }

  const pack = packageFor(study.id);
  check(Boolean(pack), `${study.id} has no compiled package.`);
  if (!pack) continue;
  for (const file of pack.files) {
    fileCount += 1;
    const source = path.join(root, "research", "source", ...file.path.split("/"));
    const published = path.join(root, "public", ...file.href.replace(/^\//, "").split("/"));
    check(fs.existsSync(source), `${study.id} source package file is missing: ${file.path}`);
    check(fs.existsSync(published), `${study.id} published package file is missing: ${file.href}`);
    if (!fs.existsSync(source) || !fs.existsSync(published)) continue;
    const sourceBody = fs.readFileSync(source);
    const publishedBody = fs.readFileSync(published);
    const sourceHash = sha256(sourceBody);
    check(sourceHash === file.sha256, `${study.id} compiled checksum is stale for ${file.path}.`);
    check(sourceHash === sha256(publishedBody), `${study.id} public copy differs from ${file.path}.`);
    if (file.media_type === "application/json") {
      try {
        JSON.parse(sourceBody.toString("utf8"));
      } catch {
        failures.push(`${study.id} contains invalid JSON: ${file.path}`);
      }
    }
  }
}

const graph = researchGraph();
check(graph.edge_count > 0, "Research graph has no edges.");
check(graph.nodes.some((node) => node.type === "source"), "Research graph has no source nodes.");
check(graph.nodes.some((node) => node.type === "topic"), "Research graph has no topic nodes.");

const reproductionFile = path.join(root, "research", "templates", "semantic-twin", "model-reproduction-report.json");
check(fs.existsSync(reproductionFile), "Model reproduction report is missing.");
if (fs.existsSync(reproductionFile)) {
  const reproduction = JSON.parse(fs.readFileSync(reproductionFile, "utf8"));
  check(reproduction.passed === true, "The latest model reproduction report contains failures.");
  for (const model of reproduction.models ?? []) {
    const packageDir = path.join(sourceRoot, model.package);
    const modelFile = model.model_path
      ? path.join(root, ...String(model.model_path).split("/"))
      : path.join(packageDir, "model.py");
    const baseline = model.baseline_path
      ? path.join(root, ...String(model.baseline_path).split("/"))
      : path.join(packageDir, ...String(model.output).split("/"));
    check(fs.existsSync(modelFile), `Reproduced model file is missing: ${model.package}.`);
    check(fs.existsSync(baseline), `Reproduced baseline is missing: ${model.package}/${model.output}.`);
    if (!fs.existsSync(modelFile) || !fs.existsSync(baseline)) continue;
    check(sha256(fs.readFileSync(modelFile)) === model.model_sha256, `${model.package} model changed after reproduction.`);
    check(sha256(fs.readFileSync(baseline)) === model.baseline_sha256, `${model.package} baseline changed after reproduction.`);
    if (model.passed) reproducedModelCount += 1;
  }
}

const report = {
  schema_version: "GreyScienxCorpusVerification 1.0",
  generated_at: new Date().toISOString(),
  scope: "Static corpus integrity and traceability, including checksums from the latest isolated model-reproduction run. Reproduction is not independent empirical validation or human editorial review.",
  passed: failures.length === 0,
  studies: researchObjects.length,
  claims: researchObjects.reduce((sum, study) => sum + study.claims.length, 0),
  assumptions: researchObjects.reduce((sum, study) => sum + study.assumptions.length, 0),
  results: researchObjects.reduce((sum, study) => sum + study.results.length, 0),
  models: researchObjects.reduce((sum, study) => sum + study.models.length, 0),
  registered_external_sources: externalSourceCount,
  package_files_verified: fileCount,
  executable_models_reproduced: reproducedModelCount,
  graph_nodes: graph.node_count,
  graph_edges: graph.edge_count,
  failures,
};

const reportPath = path.join(root, "research", "templates", "semantic-twin", "verification-report.json");
fs.writeFileSync(reportPath, `${JSON.stringify(report, null, 2)}\n`, "utf8");
console.log(JSON.stringify(report, null, 2));
if (failures.length) process.exitCode = 1;

function uniqueId(id) {
  check(!objectIds.has(id), `Duplicate object id ${id}.`);
  objectIds.add(id);
}

function check(condition, message) {
  if (!condition) failures.push(message);
}

function checkUrl(value, label) {
  try {
    const url = new URL(value);
    check(url.protocol === "https:" || url.protocol === "http:", `${label} is not HTTP(S): ${value}`);
  } catch {
    failures.push(`${label} is invalid: ${value}`);
  }
}

function sha256(value) {
  return crypto.createHash("sha256").update(value).digest("hex");
}

