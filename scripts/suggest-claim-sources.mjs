import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import yaml from "js-yaml";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const formsDir = path.join(root, "research", "templates", "semantic-twin", "published");
const reportFile = path.join(formsDir, "..", "claim-source-candidate-report.json");
const reviewFile = path.join(formsDir, "..", "editorial-review-manifest.json");
const review = fs.existsSync(reviewFile) ? JSON.parse(fs.readFileSync(reviewFile, "utf8")) : null;
const candidatesAccepted = review?.decisions?.claim_source_candidates === "accepted_as_contextual_references";
const studies = [];
const STOP_WORDS = new Set([
  "about", "after", "also", "because", "before", "being", "between", "could", "from", "have", "into", "more", "most", "other", "over", "paper", "scenario", "study", "than", "that", "their", "there", "these", "this", "those", "under", "were", "when", "where", "which", "while", "with", "would",
]);

for (const filename of fs.readdirSync(formsDir).sort()) {
  if (!filename.endsWith(".yaml") || filename === "manifest.yaml") continue;
  const form = yaml.load(fs.readFileSync(path.join(formsDir, filename), "utf8"));
  const studyId = form.identity.id;
  const manuscriptPath = (form.data.datasets ?? []).find((item) => String(item.file).endsWith(".md"))?.file;
  if (!manuscriptPath) continue;
  const manuscript = fs.readFileSync(path.join(root, ...manuscriptPath.replaceAll("\\", "/").split("/")), "utf8");
  const lines = manuscript.replaceAll("\r\n", "\n").split("\n");
  const headings = headingIndex(lines);
  const paragraphs = lines
    .map((text, index) => ({ line: index + 1, text: cleanMarkdown(text), tokens: tokens(text) }))
    .filter((item) => item.tokens.length >= 3);
  const sources = (form.data.source_register ?? [])
    .filter((source) => source.type !== "manuscript" && /^https?:\/\//.test(String(source.url)))
    .map((source) => {
      const occurrences = lines.flatMap((line, index) => line.includes(source.url) ? [index + 1] : []);
      const locations = occurrences.map((line) => ({
        line,
        heading: headingAt(headings, line),
        context: cleanMarkdown(lines[line - 1]),
      }));
      return { source, locations };
    });
  const claims = (form.claims.claim_register ?? []).map((claim) => {
    const claimTokens = tokens(claim.claim);
    const anchor = paragraphs
      .map((paragraph) => ({ ...paragraph, overlap: overlapScore(claimTokens, paragraph.tokens) }))
      .sort((a, b) => b.overlap - a.overlap || a.line - b.line)[0];
    const candidates = sources.map(({ source, locations }) => {
      const bestLocation = (locations.length ? locations : [{ line: null, heading: null, context: source.title }])
        .map((location) => {
          const contextTokens = tokens(`${source.title} ${location.heading ?? ""} ${location.context ?? ""}`);
          const lexical = overlapScore(claimTokens, contextTokens);
          const distance = anchor && location.line ? Math.abs(anchor.line - location.line) : null;
          const proximity = distance === null ? 0 : 1 / (1 + distance / 40);
          return { ...location, lexical, distance, score: 0.7 * lexical + 0.3 * proximity };
        })
        .sort((a, b) => b.score - a.score || (a.distance ?? 1e9) - (b.distance ?? 1e9))[0];
      return {
        source_id: source.id,
        title: source.title,
        url: source.url,
        manuscript_line: bestLocation.line,
        heading: bestLocation.heading,
        context: bestLocation.context,
        lexical_score: round(bestLocation.lexical),
        line_distance_from_claim_anchor: bestLocation.distance,
        candidate_score: round(bestLocation.score),
      };
    }).sort((a, b) => b.candidate_score - a.candidate_score).slice(0, 5);
    return {
      claim_id: claim.canonical_id,
      claim: claim.claim,
      manuscript_anchor: anchor ? { line: anchor.line, heading: headingAt(headings, anchor.line), lexical_score: round(anchor.overlap) } : null,
      candidate_sources: candidates,
      editorial_status: candidatesAccepted ? "accepted_as_contextual_references" : "unreviewed_candidate_matches",
      editorial_note: candidatesAccepted ? review.evidence_note : "Candidate matches require editorial review.",
    };
  });
  studies.push({ study_id: studyId, manuscript_path: manuscriptPath.replaceAll("\\", "/"), claim_count: claims.length, external_source_count: sources.length, claims });
}

const report = {
  schema_version: "GreyScienxClaimSourceCandidates 1.0",
  generated_at: new Date().toISOString(),
  scope: candidatesAccepted
    ? "Publisher-reviewed contextual-reference decisions. Candidate sources remain ranked by manuscript proximity and lexical overlap and are not represented as independent empirical proof of modelled outputs."
    : "Editorial aid only. Candidate sources are ranked by manuscript proximity and lexical overlap. They are not claim-support assignments and must be approved or rejected by a human editor.",
  editorial_review: review,
  study_count: studies.length,
  claim_count: studies.reduce((sum, study) => sum + study.claim_count, 0),
  source_record_count: studies.reduce((sum, study) => sum + study.external_source_count, 0),
  claims_with_candidates: studies.reduce((sum, study) => sum + study.claims.filter((claim) => claim.candidate_sources.length).length, 0),
  studies,
};
fs.writeFileSync(reportFile, `${JSON.stringify(report, null, 2)}\n`, "utf8");
console.log(JSON.stringify({
  study_count: report.study_count,
  claim_count: report.claim_count,
  source_record_count: report.source_record_count,
  claims_with_candidates: report.claims_with_candidates,
  output: path.relative(root, reportFile).replaceAll("\\", "/"),
}, null, 2));

function headingIndex(lines) {
  return lines.flatMap((line, index) => {
    const match = line.match(/^(#{1,6})\s+(.+)$/);
    return match ? [{ line: index + 1, level: match[1].length, title: cleanMarkdown(match[2]) }] : [];
  });
}

function headingAt(headings, line) {
  return [...headings].reverse().find((heading) => heading.line <= line)?.title ?? null;
}

function cleanMarkdown(value) {
  return String(value)
    .replace(/!\[([^\]]*)\]\([^)]+\)/g, "$1")
    .replace(/\[([^\]]+)\]\([^)]+\)/g, "$1")
    .replace(/<https?:\/\/[^>]+>/g, "")
    .replace(/[*_`>#|]/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function tokens(value) {
  return [...new Set((String(value).toLowerCase().match(/[a-z0-9][a-z0-9-]{2,}/g) ?? [])
    .filter((token) => !STOP_WORDS.has(token)))];
}

function overlapScore(left, right) {
  const rightSet = new Set(right);
  return left.length ? left.filter((token) => rightSet.has(token)).length / left.length : 0;
}

function round(value) {
  return Number(value.toFixed(4));
}
