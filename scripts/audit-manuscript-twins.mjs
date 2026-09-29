import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import yaml from "js-yaml";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const formsDir = path.join(root, "research", "templates", "semantic-twin", "published");
const reportFile = path.join(root, "research", "templates", "semantic-twin", "manuscript-twin-report.json");
const failures = [];
const manuscripts = [];
const STOP_WORDS = new Set([
  "and", "are", "but", "for", "from", "has", "have", "into", "not", "that", "the", "their", "then",
  "there", "these", "this", "those", "was", "were", "what", "when", "where", "which", "while", "with",
  "would", "www", "https", "http", "com", "org", "pdf",
]);

for (const filename of fs.readdirSync(formsDir).sort()) {
  if (!filename.endsWith(".yaml") || filename === "manifest.yaml") continue;
  const form = yaml.load(fs.readFileSync(path.join(formsDir, filename), "utf8"));
  const studyId = form?.identity?.id;
  const title = form?.identity?.title;
  const dataset = (form?.data?.datasets ?? []).find(
    (item) => typeof item?.file === "string" && item.file.toLowerCase().endsWith(".md"),
  );
  const pdfSource = (form?.data?.source_register ?? []).find((item) => item?.type === "manuscript");
  const sourcePath = dataset?.file;
  const pdfUrl = pdfSource?.url;
  if (typeof studyId !== "string" || typeof title !== "string") {
    failures.push(`${filename} has no study identity.`);
    continue;
  }
  if (typeof sourcePath !== "string" || typeof pdfUrl !== "string") {
    failures.push(`${studyId} does not register both Markdown and PDF manuscript sources.`);
    continue;
  }

  const sourceFile = path.join(root, ...sourcePath.replaceAll("\\", "/").split("/"));
  const pdfPath = new URL(pdfUrl).pathname.replace(/^\//, "");
  const pdfFile = path.join(root, "public", ...pdfPath.split("/"));
  if (!fs.existsSync(sourceFile)) {
    failures.push(`${studyId} Markdown source is missing: ${sourcePath}`);
    continue;
  }
  if (!fs.existsSync(pdfFile)) {
    failures.push(`${studyId} PDF is missing: ${pdfPath}`);
    continue;
  }

  try {
    const markdown = fs.readFileSync(sourceFile, "utf8").replaceAll("\r\n", "\n");
    const pdfText = execFileSync("pdftotext", ["-layout", pdfFile, "-"], {
      encoding: "utf8",
      maxBuffer: 32 * 1024 * 1024,
      stdio: ["ignore", "pipe", "ignore"],
    });
    const info = execFileSync("pdfinfo", [pdfFile], {
      encoding: "utf8",
      maxBuffer: 1024 * 1024,
      stdio: ["ignore", "pipe", "ignore"],
    });
    const pages = Number(info.match(/^Pages:\s+(\d+)/m)?.[1] ?? 0);
    const sourceTokens = significantTokens(markdown);
    const pdfTokens = new Set(significantTokens(pdfText));
    const shared = [...new Set(sourceTokens)].filter((token) => pdfTokens.has(token));
    const coverage = shared.length / Math.max(1, new Set(sourceTokens).size);
    const titleTokens = significantTokens(title);
    const titleCoverage = titleTokens.filter((token) => pdfTokens.has(token)).length / Math.max(1, titleTokens.length);
    const passed = pages > 0 && pdfText.trim().length > 500 && coverage >= 0.72 && titleCoverage >= 0.75;
    if (!passed) failures.push(`${studyId} did not meet the PDF/source parity threshold.`);
    manuscripts.push({
      study_id: studyId,
      slug: form.identity.slug,
      source_path: sourcePath.replaceAll("\\", "/"),
      pdf_path: `public/${pdfPath}`,
      source_sha256: sha256(fs.readFileSync(sourceFile)),
      pdf_sha256: sha256(fs.readFileSync(pdfFile)),
      source_words: sourceTokens.length,
      pdf_words: significantTokens(pdfText).length,
      indexed_headings: markdown.split("\n").filter((line) => /^#{1,6}\s+/.test(line)).length,
      pages,
      unique_source_token_coverage_in_pdf: Number(coverage.toFixed(4)),
      title_token_coverage_in_pdf: Number(titleCoverage.toFixed(4)),
      passed,
    });
  } catch (error) {
    failures.push(`${studyId} PDF inspection failed: ${error instanceof Error ? error.message : String(error)}`);
  }
}

if (manuscripts.length !== 29) failures.push(`Expected 29 manuscript twins; inspected ${manuscripts.length}.`);
const report = {
  schema_version: "GreyScienxManuscriptTwinAudit 1.0",
  generated_at: new Date().toISOString(),
  scope:
    "Automated parity check between each complete Markdown manuscript source and its published PDF. Token coverage verifies content presence; it does not replace human visual or editorial review.",
  thresholds: {
    unique_source_token_coverage_in_pdf: 0.72,
    title_token_coverage_in_pdf: 0.75,
  },
  passed: failures.length === 0,
  manuscript_count: manuscripts.length,
  passed_manuscripts: manuscripts.filter((item) => item.passed).length,
  failed_manuscripts: manuscripts.filter((item) => !item.passed).length,
  manuscripts,
  failures,
};

fs.writeFileSync(reportFile, `${JSON.stringify(report, null, 2)}\n`, "utf8");
console.log(JSON.stringify({
  passed: report.passed,
  manuscript_count: report.manuscript_count,
  passed_manuscripts: report.passed_manuscripts,
  failed_manuscripts: report.failed_manuscripts,
  failures: report.failures,
}, null, 2));
if (failures.length) process.exitCode = 1;

function significantTokens(value) {
  return (value
    .normalize("NFKD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase()
    .replace(/['’]/g, "")
    .replace(/[-–—]/g, " ")
    .match(/[a-z0-9][a-z0-9]{2,}/g) ?? [])
    .filter((token) => !STOP_WORDS.has(token));
}

function sha256(value) {
  return crypto.createHash("sha256").update(value).digest("hex");
}

