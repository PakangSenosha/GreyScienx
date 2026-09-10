import { z } from "zod";
import type { ResearchPaper, Researcher } from "./types";
import { slugify, subdomainFromName } from "./slug";

export const distillSchema = z.object({
  protocol: z.string(),
  field: z.string(),
  title: z.string(),
  titleAccent: z.string(),
  dek: z.string(),
  date: z.string(),
  pages: z.number(),
  stats: z
    .array(z.object({ value: z.string(), label: z.string() }))
    .length(4),
  finding: z.object({
    kicker: z.string(),
    headline: z.string(),
    body: z.string(),
  }),
  results: z.object({
    eyebrow: z.string(),
    headline: z.string(),
    intro: z.string(),
    metrics: z
      .array(
        z.object({
          value: z.string(),
          label: z.string(),
          note: z.string(),
        }),
      )
      .length(8),
    qualification: z.object({
      title: z.string(),
      body: z.string(),
    }),
  }),
  evidence: z.object({
    cards: z
      .array(
        z.object({
          value: z.string(),
          title: z.string(),
          body: z.string(),
        }),
      )
      .length(4),
  }),
  method: z.object({
    eyebrow: z.string(),
    headline: z.string(),
    steps: z
      .array(z.object({ title: z.string(), body: z.string() }))
      .length(8),
  }),
  inside: z.object({
    eyebrow: z.string(),
    headline: z.string(),
    items: z.array(z.string()).length(8),
  }),
  downloadNote: z.string(),
  footerNote: z.string(),
});

export type DistillOutput = z.infer<typeof distillSchema>;

export type DistillInput = {
  researcherName: string;
  affiliation: string;
  role: string;
  email?: string;
  title?: string;
  field?: string;
  manuscript: string;
};

function take(values: string[], count: number, fallback: string) {
  const next = [...values];
  while (next.length < count) next.push(fallback);
  return next.slice(0, count);
}

function extractNumbers(text: string) {
  const matches = text.match(/[-−]?\d+(?:[.,]\d+)?%?|\bp\s*=\s*0\.\d+/gi) ?? [];
  return [...new Set(matches.map((item) => item.replace(",", "")))].slice(0, 12);
}

function paragraphs(text: string) {
  return text
    .split(/\n{2,}/)
    .map((part) => part.replace(/\s+/g, " ").trim())
    .filter((part) => part.length > 40);
}

function sentences(text: string) {
  return text
    .split(/(?<=[.?!])\s+/)
    .map((part) => part.trim())
    .filter((part) => part.length > 20);
}

export function heuristicDistill(input: DistillInput): DistillOutput {
  const blocks = paragraphs(input.manuscript);
  const lines = input.manuscript
    .split(/\n/)
    .map((line) => line.trim())
    .filter(Boolean);
  const titleLine =
    input.title ||
    lines.find((line) => line.length > 12 && line.length < 140) ||
    "Untitled research";
  const parts = titleLine.replace(/[.]+$/, "").split(/[:—–-]/);
  const title = parts[0]?.trim() || "Research";
  const titleAccent = `${(parts.slice(1).join(" ").trim() || "Findings").replace(/[.]+$/, "")}.`;
  const dek = blocks[0] || input.manuscript.slice(0, 280);
  const findingBody = blocks[1] || blocks[0] || dek;
  const numbers = extractNumbers(input.manuscript);
  const metricValues = take(numbers, 8, "—");
  const sent = sentences(input.manuscript);
  const year = new Date().getFullYear();

  return {
    protocol: "Evidence protocol",
    field: input.field || "Semi-professional research",
    title,
    titleAccent,
    dek,
    date: String(year),
    pages: Math.max(1, Math.round(input.manuscript.length / 2800)),
    stats: [
      { value: String(blocks.length || 1), label: "extracted sections" },
      { value: String(numbers.length), label: "reported quantities" },
      { value: String(Math.max(1, Math.round(input.manuscript.length / 500))), label: "approx. paragraphs" },
      { value: "PDF", label: "original manuscript" },
    ],
    finding: {
      kicker: "GreyScienx distilled the submitted manuscript:",
      headline: sent[0] || titleLine,
      body: findingBody,
    },
    results: {
      eyebrow: "The measured record",
      headline: sent[1] || "The paper reports a finite set of findings.",
      intro: blocks[2] || blocks[0] || dek,
      metrics: metricValues.map((value, index) => ({
        value,
        label: sent[index + 2]?.slice(0, 48) || `Reported quantity ${index + 1}`,
        note: sent[index + 2] || "Extracted from the submitted manuscript.",
      })),
      qualification: {
        title: "How this site was written",
        body: "This layout is a GreyScienx distillation of the submitted armchair paper. The original manuscript remains available for download and is the source of record.",
      },
    },
    evidence: {
      cards: take(sent.slice(3), 4, "See the original manuscript for the supporting result.").map(
        (body, index) => ({
          value: metricValues[index] || String(index + 1).padStart(2, "0"),
          title: body.slice(0, 42),
          body,
        }),
      ),
    },
    method: {
      eyebrow: "How the work was framed",
      headline: "The methods were read out of the submitted paper.",
      steps: take(
        lines.filter((line) => line.length > 18 && line.length < 160),
        8,
        "See the original manuscript for the corresponding method step.",
      ).map((line, index) => ({
        title: `Step ${index + 1}`,
        body: line,
      })),
    },
    inside: {
      eyebrow: "The complete record",
      headline: "Summaries on this site. The paper underneath.",
      items: take(
        lines.filter((line) => line.length > 12 && line.length < 80),
        8,
        "Original manuscript",
      ),
    },
    downloadNote:
      "The original armchair paper remains the source of record. This site is a GreyScienx distillation of its findings, methods, and quantities.",
    footerNote: `${input.researcherName} · ${input.affiliation} · Distilled ${year}`,
  };
}

export function toPreviewRecord(
  input: DistillInput,
  distilled: DistillOutput,
): { researcher: Researcher; paper: ResearchPaper } {
  const slug = slugify(input.researcherName);
  const paperSlug = slugify(`${distilled.title} ${distilled.titleAccent}`);
  const researcher: Researcher = {
    slug,
    subdomain: subdomainFromName(input.researcherName),
    name: input.researcherName,
    givenName: input.researcherName.split(/\s+/)[0] || "Researcher",
    affiliation: input.affiliation,
    role: input.role || "Independent researcher",
    bio: `${input.researcherName} submitted this manuscript to GreyScienx for distillation into a research site.`,
    location: input.affiliation,
    email: input.email || "",
    links: [],
  };

  const paper: ResearchPaper = {
    slug: paperSlug,
    researcherSlug: slug,
    protocol: distilled.protocol,
    field: distilled.field,
    title: distilled.title,
    titleAccent: distilled.titleAccent,
    dek: distilled.dek,
    date: distilled.date,
    pdf: {
      href: "#manuscript",
      pages: distilled.pages,
      size: "Original upload",
      filename: `${paperSlug}.pdf`,
    },
    stats: distilled.stats,
    finding: distilled.finding,
    results: {
      ...distilled.results,
    },
    evidence: distilled.evidence,
    method: distilled.method,
    inside: distilled.inside,
    downloadNote: distilled.downloadNote,
    footerNote: distilled.footerNote,
  };

  return { researcher, paper };
}

export const DISTILL_PROMPT = `You distill an armchair research paper into a GreyScienx research-site template.
Write like a serious methods-and-results press: short, specific, numerical, no marketing.
Split the title: "title" is the opening phrase, "titleAccent" is the emphatic remainder ending with a period.
stats must be 4 items. results.metrics must be 8 items. evidence.cards must be 4 items. method.steps must be 8 items. inside.items must be 8 items.
Prefer quantities that actually appear in the manuscript. Do not invent precise statistics that are not in the text.
finding.headline should be the single most important result in plain language.
The original paper will still be downloadable; this is the public site, not a replacement.`;
