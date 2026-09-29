import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import yaml from "js-yaml";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const formsDir = path.join(root, "research", "templates", "semantic-twin", "published");
const reportFile = path.join(root, "research", "templates", "semantic-twin", "automated-pdf-render-report.json");
const workRoot = fs.mkdtempSync(path.join(os.tmpdir(), "gsx-pdf-render-"));
const failures = [];
const documents = [];

try {
  for (const filename of fs.readdirSync(formsDir).sort()) {
    if (!filename.endsWith(".yaml") || filename === "manifest.yaml") continue;
    const form = yaml.load(fs.readFileSync(path.join(formsDir, filename), "utf8"));
    const studyId = form?.identity?.id;
    const pdfUrl = (form?.data?.source_register ?? []).find((item) => item?.type === "manuscript")?.url;
    if (typeof studyId !== "string" || typeof pdfUrl !== "string") {
      failures.push(`${filename} does not register a study and manuscript PDF.`);
      continue;
    }
    const pdfPath = new URL(pdfUrl).pathname.replace(/^\//, "");
    const pdfFile = path.join(root, "public", ...pdfPath.split("/"));
    if (!fs.existsSync(pdfFile)) {
      failures.push(`${studyId} PDF is missing: ${pdfPath}`);
      continue;
    }
    const outputDir = path.join(workRoot, studyId.replaceAll(":", "-"));
    fs.mkdirSync(outputDir, { recursive: true });
    const prefix = path.join(outputDir, "page");
    try {
      const info = execFileSync("pdfinfo", [pdfFile], { encoding: "utf8", stdio: ["ignore", "pipe", "ignore"] });
      const expectedPages = Number(info.match(/^Pages:\s+(\d+)/m)?.[1] ?? 0);
      execFileSync("pdftoppm", ["-gray", "-r", "24", pdfFile, prefix], {
        encoding: "utf8",
        stdio: ["ignore", "pipe", "ignore"],
        timeout: 180_000,
      });
      const pages = fs.readdirSync(outputDir).filter((item) => item.endsWith(".pgm")).sort();
      const pageStats = pages.map((item, index) => ({ page: index + 1, ...pgmStats(fs.readFileSync(path.join(outputDir, item))) }));
      const pageFailures = [];
      if (expectedPages < 1) pageFailures.push("pdfinfo returned no pages");
      if (pages.length !== expectedPages) pageFailures.push(`expected ${expectedPages} rendered pages, found ${pages.length}`);
      if (pageStats.some((page) => page.width < 100 || page.height < 100)) pageFailures.push("one or more rendered pages has invalid dimensions");
      const dimensions = new Set(pageStats.map((page) => `${page.width}x${page.height}`));
      const passed = pageFailures.length === 0;
      if (!passed) failures.push(`${studyId}: ${pageFailures.join("; ")}.`);
      documents.push({
        study_id: studyId,
        pdf_path: `public/${pdfPath}`,
        expected_pages: expectedPages,
        rendered_pages: pages.length,
        rendered_dimensions: [...dimensions],
        minimum_ink_ratio: pageStats.length ? Math.min(...pageStats.map((page) => page.ink_ratio)) : 0,
        maximum_ink_ratio: pageStats.length ? Math.max(...pageStats.map((page) => page.ink_ratio)) : 0,
        near_blank_pages: pageStats.filter((page) => page.ink_ratio < 0.0005).map((page) => page.page),
        passed,
        failures: pageFailures,
      });
    } catch (error) {
      const message = error instanceof Error ? error.message.split("\n")[0] : String(error);
      failures.push(`${studyId} page rendering failed: ${message}`);
      documents.push({ study_id: studyId, pdf_path: `public/${pdfPath}`, passed: false, failures: [message] });
    }
  }
} finally {
  fs.rmSync(workRoot, { recursive: true, force: true });
}

if (documents.length !== 29) failures.push(`Expected 29 PDFs; inspected ${documents.length}.`);
const report = {
  schema_version: "GreyScienxAutomatedPdfRenderAudit 1.0",
  generated_at: new Date().toISOString(),
  scope: "Automated page-level render-integrity check. Every PDF page must rasterise at a valid size. Ink-density observations help identify suspicious blank pages but do not replace human visual review.",
  passed: failures.length === 0,
  document_count: documents.length,
  page_count: documents.reduce((sum, document) => sum + (document.rendered_pages ?? 0), 0),
  passed_documents: documents.filter((document) => document.passed).length,
  failed_documents: documents.filter((document) => !document.passed).length,
  documents,
  failures,
};
fs.writeFileSync(reportFile, `${JSON.stringify(report, null, 2)}\n`, "utf8");
console.log(JSON.stringify({
  passed: report.passed,
  document_count: report.document_count,
  page_count: report.page_count,
  passed_documents: report.passed_documents,
  failed_documents: report.failed_documents,
  failures: report.failures,
}, null, 2));
if (failures.length) process.exitCode = 1;

function pgmStats(buffer) {
  let offset = 0;
  const tokens = [];
  while (tokens.length < 4) {
    while (offset < buffer.length && /\s/.test(String.fromCharCode(buffer[offset]))) offset += 1;
    if (buffer[offset] === 35) {
      while (offset < buffer.length && buffer[offset] !== 10) offset += 1;
      continue;
    }
    const start = offset;
    while (offset < buffer.length && !/\s/.test(String.fromCharCode(buffer[offset]))) offset += 1;
    tokens.push(buffer.subarray(start, offset).toString("ascii"));
  }
  const [magic, widthValue, heightValue, maxValue] = tokens;
  if (magic !== "P5" || Number(maxValue) > 255) throw new Error("Unsupported PGM render output.");
  if (buffer[offset] === 13 && buffer[offset + 1] === 10) offset += 2;
  else offset += 1;
  const width = Number(widthValue);
  const height = Number(heightValue);
  const expected = width * height;
  const pixels = buffer.subarray(offset, offset + expected);
  if (pixels.length !== expected) throw new Error("Truncated PGM render output.");
  let ink = 0;
  for (const value of pixels) if (value < 245) ink += 1;
  return { width, height, ink_ratio: Number((ink / Math.max(1, pixels.length)).toFixed(6)) };
}
