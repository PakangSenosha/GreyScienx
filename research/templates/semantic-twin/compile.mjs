import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import yaml from "js-yaml";

const here = path.dirname(fileURLToPath(import.meta.url));
const publishedDir = path.join(here, "published");
const outputFile = path.resolve(here, "../../../lib/research/extractions/from-forms.ts");
const graphFile = path.resolve(here, "../../../lib/research/extractions/from-graph.ts");
const manuscriptFile = path.resolve(here, "../../../lib/research/extractions/from-manuscripts.ts");

const extractions = {};
const graphEdges = [];
const packages = {};
const manuscripts = {};
const packageFile = path.resolve(here, "../../../lib/research/extractions/from-packages.ts");
const repoRoot = path.resolve(here, "../../..");
const publicRoot = path.join(repoRoot, "public");
const sourceRoot = path.join(repoRoot, "research", "source");
const allowedExt = new Set([".py", ".json", ".md", ".csv", ".txt", ".mjs", ".r", ".yaml", ".yml"]);
const maxBytes = 1_500_000;

clearPublishedPackages(path.join(publicRoot, "research"));

for (const name of fs.readdirSync(publishedDir).sort()) {
  if (!name.endsWith(".yaml") || name === "manifest.yaml") continue;
  const form = yaml.load(fs.readFileSync(path.join(publishedDir, name), "utf8"));
  const studyId = form?.identity?.id;
  if (typeof studyId === "string") {
    const manuscript = toManuscript(form);
    manuscripts[studyId] = manuscript;
    packages[studyId] = toPackage(form, manuscript);
  }
  const claims = form?.claims?.claim_register ?? [];
  if (!Array.isArray(claims) || claims.length === 0 || typeof studyId !== "string") continue;
  const assumptions = (form.model?.assumptions ?? []).map(toAssumption);
  const results = (form.results?.result_register ?? []).map(toResult);
  const models = (form.model?.models ?? []).map(toModel);
  extractions[studyId] = {
    assumptions,
    results,
    models,
    claims: claims.map((claim) => toClaim(claim, studyId)),
  };
  for (const edge of form.relationships?.graph_edges ?? []) {
    if (!edge?.subject_id || !edge?.predicate || !edge?.object_id) continue;
    const objectId = qualify(studyId, edge.object_id);
    if (objectId === "none" || objectId === "none recorded" || objectId.endsWith(":none")) continue;
    graphEdges.push({
      subject_id: qualify(studyId, edge.subject_id),
      predicate: edge.predicate,
      object_id: objectId,
      note: edge.note ?? "",
    });
  }
}

const banner = `// Generated from research/templates/semantic-twin/published by compile.mjs.
// Edit the YAML forms, then run: node research/templates/semantic-twin/compile.mjs
`;

fs.writeFileSync(
  outputFile,
  `${banner}export const formExtractions = ${JSON.stringify(extractions, null, 2)};\n`,
  "utf8",
);

fs.writeFileSync(
  graphFile,
  `${banner}export const formGraphEdges = ${JSON.stringify(graphEdges, null, 2)};\n`,
  "utf8",
);

fs.writeFileSync(
  packageFile,
  `${banner}export const formPackages = ${JSON.stringify(packages, null, 2)};\n`,
  "utf8",
);

fs.writeFileSync(
  manuscriptFile,
  `${banner}export const formManuscripts = ${JSON.stringify(manuscripts, null, 2)};\n`,
  "utf8",
);

console.log(`Compiled ${Object.keys(extractions).length} studies with claims into ${outputFile}`);
console.log(`Compiled ${graphEdges.length} graph edges into ${graphFile}`);
const fileCount = Object.values(packages).reduce((sum, pack) => sum + pack.files.length, 0);
console.log(`Compiled ${Object.keys(packages).length} study packages into ${packageFile}`);
console.log(`Compiled ${Object.keys(manuscripts).length} full-text manuscripts into ${manuscriptFile}`);
console.log(`Published ${fileCount} reproducibility files under public/research`);

await import("./compile-profiles.mjs");

function toPackage(form, manuscript) {
  const datasets = Array.isArray(form.data?.datasets) ? form.data.datasets : [];
  const sources = Array.isArray(form.data?.source_register) ? form.data.source_register : [];
  const reproducibility = form.reproducibility ?? {};
  const claims = Array.isArray(form.claims?.claim_register) ? form.claims.claim_register : [];
  const lead = claims[0] ?? null;
  return {
    manuscript: manuscriptMetadata(manuscript),
    answer_block: lead
      ? {
          conditional_answer: publishedText(lead.claim),
          evidence_status: publishedText(lead.evidence_status) || "modelled",
          assumption_ids: textList(lead.depends_on_assumptions),
          result_ids: textList(lead.derived_from_results),
          main_limitation: publishedText(lead.main_limitation),
          sensitivity: publishedText(lead.sensitivity),
        }
      : null,
    unresolved_questions: textList(form.epistemic_contract?.unresolved_questions),
    entities: [...new Set([
      ...textList(form.classification?.geographies),
      ...textList(form.classification?.topics),
    ])],
    methods: (form.model?.models ?? []).map((model) => ({
      id: String(model.canonical_id ?? model.id ?? ""),
      name: publishedText(model.name),
      model_class: publishedText(model.model_class),
      purpose: publishedText(model.purpose ?? model.statement),
      implementation_file: publishedText(model.implementation_file),
    })),
    parameters: form.model?.parameters ?? [],
    equations: textList(form.model?.equations),
    scenarios: form.scenarios ?? [],
    datasets: datasets.map((dataset) => ({
      id: String(dataset.id ?? ""),
      title: publishedText(dataset.title),
      description: publishedText(dataset.description),
      href: isUrl(dataset.url) ? dataset.url : null,
      geographic_coverage: publishedText(dataset.geographic_coverage),
      licence: publishedText(dataset.licence),
    })),
    sources: sources.map((source) => ({
      id: String(source.id ?? ""),
      type: publishedText(source.type),
      title: publishedText(source.title),
      author_or_publisher: publishedText(source.author_or_publisher),
      date: publishedText(source.date),
      href: isUrl(source.url) ? source.url : null,
      locator: publishedText(source.locator),
      supports: textList(source.supports),
      contradicts: textList(source.contradicts),
      note: publishedText(source.note),
    })),
    figures: (form.artifacts?.figures ?? []).map((figure) => ({
      id: String(figure.id ?? ""),
      title: publishedText(figure.title),
      caption: publishedText(figure.caption),
      alt_text: publishedText(figure.alt_text),
      image_file: publishedText(figure.image_file),
      data_file: publishedText(figure.data_file),
      result_ids: textList(figure.result_ids),
      source_ids: textList(figure.source_ids),
    })),
    tables: (form.artifacts?.tables ?? []).map((table) => ({
      id: String(table.id ?? ""),
      title: publishedText(table.title),
      description: publishedText(table.description),
      file: publishedText(table.file),
      result_ids: textList(table.result_ids),
      source_ids: textList(table.source_ids),
    })),
    reproducibility: {
      code_available: reproducibility.code_available === true,
      data_available: reproducibility.data_available === true,
      environment_available: reproducibility.environment_available === true,
      random_seed: publishedText(reproducibility.random_seed),
      software: textList(reproducibility.software),
      repository_url: isUrl(reproducibility.repository_url) ? reproducibility.repository_url : null,
    },
    shared_assumptions: textList(form.relationships?.shared_assumptions),
    shared_datasets: textList(form.relationships?.shared_datasets),
    shared_models: textList(form.relationships?.shared_models),
    editorial: {
      required_checks: form.quality_control?.required_checks ?? {},
      blocking_issues: textList(form.quality_control?.blocking_issues),
      warnings: textList(form.quality_control?.warnings),
      change_log: form.change_log ?? [],
    },
    files: publishFiles(form),
  };
}

function toManuscript(form) {
  const studyId = form?.identity?.id;
  const datasets = Array.isArray(form?.data?.datasets) ? form.data.datasets : [];
  const source = datasets.find(
    (dataset) => typeof dataset?.file === "string" && dataset.file.toLowerCase().endsWith(".md"),
  );
  if (typeof studyId !== "string" || typeof source?.file !== "string") {
    throw new Error(`Study ${studyId ?? "unknown"} has no Markdown manuscript source.`);
  }
  const sourcePath = source.file.replaceAll("\\", "/");
  const absolutePath = path.resolve(repoRoot, sourcePath);
  if (!absolutePath.startsWith(repoRoot + path.sep) || !fs.existsSync(absolutePath)) {
    throw new Error(`Study ${studyId} manuscript source does not exist: ${sourcePath}`);
  }
  const content = fs.readFileSync(absolutePath, "utf8").replaceAll("\r\n", "\n");
  if (!content.trim()) throw new Error(`Study ${studyId} manuscript source is empty.`);
  const bytes = Buffer.byteLength(content, "utf8");
  const words = content.match(/[\p{L}\p{N}][\p{L}\p{N}'’.-]*/gu) ?? [];
  return {
    study_id: studyId,
    source_path: sourcePath,
    source_sha256: crypto.createHash("sha256").update(content).digest("hex"),
    source_bytes: bytes,
    character_count: content.length,
    word_count: words.length,
    headings: manuscriptHeadings(content),
    content_markdown: content,
  };
}

function manuscriptMetadata(manuscript) {
  return {
    study_id: manuscript.study_id,
    source_path: manuscript.source_path,
    source_sha256: manuscript.source_sha256,
    source_bytes: manuscript.source_bytes,
    character_count: manuscript.character_count,
    word_count: manuscript.word_count,
    headings: manuscript.headings,
  };
}

function manuscriptHeadings(content) {
  const seen = new Map();
  return content.split("\n").flatMap((line, index) => {
    const match = line.match(/^(#{1,6})\s+(.+?)\s*#*\s*$/);
    if (!match) return [];
    const title = match[2].trim();
    const base = title
      .toLowerCase()
      .normalize("NFKD")
      .replace(/[\u0300-\u036f]/g, "")
      .replace(/[^a-z0-9]+/g, "-")
      .replace(/^-|-$/g, "") || `section-${index + 1}`;
    const occurrence = (seen.get(base) ?? 0) + 1;
    seen.set(base, occurrence);
    return [{
      level: match[1].length,
      title,
      slug: occurrence === 1 ? base : `${base}-${occurrence}`,
      line: index + 1,
    }];
  });
}

function publishFiles(form) {
  const series = form.identity?.series_slug;
  const slug = form.identity?.slug;
  if (typeof series !== "string" || typeof slug !== "string") return [];
  const published = [];
  const seen = new Set();
  for (const item of listedFiles(form)) {
    const rel = item.file.replaceAll("\\", "/");
    if (!rel.startsWith("research/source/") || seen.has(rel)) continue;
    seen.add(rel);
    const abs = path.resolve(repoRoot, rel);
    const ext = path.extname(abs).toLowerCase();
    if (!abs.startsWith(sourceRoot + path.sep) || !allowedExt.has(ext)) continue;
    if (!fs.existsSync(abs) || !fs.statSync(abs).isFile()) continue;
    const bytes = fs.statSync(abs).size;
    if (bytes === 0 || bytes > maxBytes) continue;
    const inside = path.relative(sourceRoot, abs).replaceAll("\\", "/");
    const href = `/research/${series}/${slug}/package/${inside}`;
    const dest = path.join(publicRoot, href);
    fs.mkdirSync(path.dirname(dest), { recursive: true });
    const body = fs.readFileSync(abs);
    fs.writeFileSync(dest, body);
    published.push({
      path: inside,
      href,
      bytes,
      sha256: crypto.createHash("sha256").update(body).digest("hex"),
      media_type: mediaType(ext),
      role: item.role,
    });
  }
  return published;
}

function listedFiles(form) {
  const items = [];
  const add = (file, role) => {
    if (typeof file === "string" && file.trim()) items.push({ file: file.trim(), role });
  };
  for (const model of form.model?.models ?? []) add(model.implementation_file, "model");
  for (const file of form.artifacts?.model_files ?? []) add(file, "model");
  for (const file of form.artifacts?.data_files ?? []) add(file, "data");
  for (const code of form.artifacts?.code ?? []) add(code?.file, "code");
  for (const table of form.artifacts?.tables ?? []) add(table?.file, "data");
  return items;
}

function mediaType(ext) {
  if (ext === ".py") return "text/x-python";
  if (ext === ".json") return "application/json";
  if (ext === ".md") return "text/markdown";
  if (ext === ".csv") return "text/csv";
  if (ext === ".mjs") return "text/javascript";
  if (ext === ".yaml" || ext === ".yml") return "text/yaml";
  return "text/plain";
}

function clearPublishedPackages(dir) {
  if (!fs.existsSync(dir)) return;
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (!entry.isDirectory()) continue;
    const full = path.join(dir, entry.name);
    if (entry.name === "package") fs.rmSync(full, { recursive: true, force: true });
    else clearPublishedPackages(full);
  }
}

function textList(value) {
  if (!Array.isArray(value)) return [];
  return value.map(publishedText).filter(Boolean);
}

function publishedText(value) {
  if (typeof value !== "string") return "";
  const text = value.trim();
  if (!text || text === "none" || text.startsWith("none ")) return "";
  if (/^see the /i.test(text)) return "";
  return text;
}

function isUrl(value) {
  return typeof value === "string" && /^https?:\/\//.test(value);
}

function qualify(studyId, id) {
  if (id === "none" || id === "none recorded") return id;
  return id.includes(":") ? id : `${studyId}:${id}`;
}

function localId(item, fallback) {
  return item.id ?? fallback;
}

function toAssumption(item) {
  return {
    id: item.canonical_id,
    local_id: localId(item),
    name: item.name,
    statement: item.statement,
    value: item.value === undefined ? null : item.value,
    unit: item.unit === undefined ? null : item.unit,
    type: "model assumption",
    provenance: item.provenance,
    evidence_strength: item.evidence_strength,
    sensitivity: item.sensitivity,
    alternatives: item.alternatives ?? [],
  };
}

function toResult(item) {
  return {
    id: item.canonical_id,
    local_id: localId(item),
    statement: item.statement,
    value: String(item.value),
    unit: item.unit,
    scenario: item.scenario_id,
    evidence_status: "modelled",
  };
}

function toModel(item) {
  return {
    id: item.canonical_id,
    local_id: localId(item),
    name: item.name,
    statement: item.statement,
  };
}

function toClaim(item, studyId) {
  const results = item.derived_from_results ?? [];
  return {
    id: item.canonical_id,
    local_id: localId(item),
    claim: item.claim,
    claim_type: "conditional",
    status: "conditional",
    evidence_status: "modelled",
    confidence: null,
    depends_on: item.depends_on_assumptions ?? [],
    result: results[0],
    results,
    sensitivity: item.sensitivity,
    main_limitation: item.main_limitation,
    source_study: studyId,
    version: "1.0",
    href: item.href,
    supported_by: textList(item.supported_by_sources),
    contradicted_by: textList(item.contradicted_by_sources),
    qualifies: textList(item.qualifies_claims),
    contradicts: textList(item.contradicted_claims),
  };
}
