import { site } from "../site";

import { listSeriesRecords, listTopicRecords, researchObjects, researchTypeLabel } from "./registry";
import type { ResearchObject } from "./schema";
import { mathematicalStandard } from "./standard";
import { manuscriptFor } from "./manuscripts";

const origin = `https://${site.domain}`;

export function studyMarkdown(study: ResearchObject) {
  const manuscript = manuscriptFor(study.id);
  const related = study.related_studies
    .map((item) => `- [${item.title}](${item.href}) (${item.id})`)
    .join("\n");
  const questions = study.related_questions.map((question) => `- ${question}`).join("\n");

  return `# ${study.title}

Identifier: ${study.id}
Series: ${study.series_title}
Version: ${study.version}
Status: ${study.status}
Schema: ${study.schema_version}

## Primary question

${study.primary_question}

## Summary

${study.summary}

${study.retrieval_note}

## Conditional answer

${study.answer ? `${study.answer.conditional_answer}

- Evidence status: ${study.answer.evidence_status}
- Depends on: ${study.answer.assumption_ids.join(", ")}
- Derived from: ${study.answer.result_ids.join(", ")}
- Sensitivity: ${study.answer.sensitivity}
- Main limitation: ${study.answer.main_limitation}` : "No answer-sized claim is registered."}

## Related questions

${questions}

## Epistemic status

- Study type: ${researchTypeLabel(study.research_type)}
- Evidence status: Modelled
- Peer review: None
- External critique: None recorded
- AI assistance: ${study.ai_assistance.disclosure}
- Record date: ${study.date_modified}. ${study.date_note}

## Topics

${study.topics.map((topic) => `- [${topic}](${origin}/topics/${topic})`).join("\n")}

## Geographies

${study.geographies.map((place) => `- ${place}`).join("\n")}

## Assumptions

${lines(study.assumptions.map((item) => `- [${item.local_id}](${item.href}) ${item.name}. ${item.statement}`))}

## Model

${lines(study.models.map((item) => `- [${item.local_id}](${item.href}) ${item.name}. ${item.statement}`))}

## Results

${lines(study.results.map((item) => `- [${item.local_id}](${item.href}) ${item.statement} (${item.value} ${item.unit}; ${item.scenario}).`))}

## Sources

${lines(study.sources.map((source) => source.href ? `- ${source.id} [${source.title}](${source.href}) — ${source.note ?? source.type}` : `- ${source.id} ${source.title}`))}

## Manuscript

- [${study.title} (PDF, ${study.sources[0]?.pages ?? "?"} pages)](${study.links.pdf})
- Datasets: ${study.links.html.replace(/\/$/, "")}/data
- Reproducibility: ${study.links.html.replace(/\/$/, "")}/reproduce

## Related studies

${related || "- None in this series."}

## Machine-readable record

- JSON: ${study.links.json}
- Full-text manuscript API: ${study.links.manuscript}
- Canonical page: ${study.links.html}
- Citation: ${study.citation.text}

## Claim-level record

${claimSection(study)}

## Full manuscript

Source checksum: ${study.manuscript.source_sha256}

The text below is the complete Markdown source used to produce the manuscript, preserved separately from the semantic claim layer above.

---

${manuscript?.content_markdown ?? "Full manuscript text is unavailable."}
`;
}

function lines(items: string[]) {
  return items.length > 0 ? items.join("\n") : "- None registered.";
}

function claimSection(study: ResearchObject) {
  if (study.claims.length === 0) {
    return "Assumptions, claims, results, and models will be published as separate objects after manuscript extraction. This file states the catalog summary and the question the study asks.";
  }
  const claims = study.claims
    .map(
      (claim) => `### ${claim.id}

${claim.claim}

- Status: ${claim.status}
- Evidence status: ${claim.evidence_status}
- Depends on: ${claim.depends_on.join(", ")}
- Result: ${claim.result}
- Sensitivity: ${claim.sensitivity}
- Main limitation: ${claim.main_limitation}
- Page: ${claim.href}`,
    )
    .join("\n\n");
  return `${claims}

${study.assumptions.length} assumptions, ${study.results.length} results, and ${study.models.length} model descriptions are included in the JSON record.`;
}

export function researchIndexMarkdown() {
  const entries = researchObjects
    .map(
      (study) =>
        `## ${study.title}

- Identifier: ${study.id}
- Question: ${study.primary_question}
- Summary: ${study.summary}
- Evidence status: Modelled
- JSON: ${study.links.json}
- Markdown: ${study.links.markdown}
- Page: ${study.links.html}`,
    )
    .join("\n\n");

  return `# GreyScienx research index

${researchObjects.length} published studies. Each entry is a modelled, exploratory research object. Claim-level conclusions are not included in this index.

${entries}
`;
}

export function seriesIndexMarkdown() {
  const entries = listSeriesRecords()
    .map((series) => {
      const studies = series.studies
        .map((study) => `- ${study.id} [${study.title}](${study.links.html}) — ${study.primary_question}`)
        .join("\n");
      return `## ${series.title}

${series.question}

${studies}`;
    })
    .join("\n\n");

  return `# GreyScienx series index

${entries}
`;
}

export function standardMarkdown() {
  const sections = mathematicalStandard.sections
    .map((section) => `## ${section.title}\n\n${section.paragraphs.join("\n\n")}`)
    .join("\n\n");
  return `# ${mathematicalStandard.title}

${mathematicalStandard.id}

${mathematicalStandard.summary}

${sections}
`;
}

export function llmsTxt() {
  const topicLines = listTopicRecords()
    .map((topic) => `- ${origin}/topics/${topic.slug}`)
    .join("\n");
  return `# GreyScienx

> GreyScienx publishes open exploratory computational research, mathematical models, simulations, counterfactual studies, socioeconomic analyses, and reproducible research objects.

The public archive is the human interface. The same studies are available as Markdown, JSON, and a read-only API. GreyScienx does not host a general chatbot.

## Research

- ${origin}/research/index.md
- ${origin}/series/index.md
- ${origin}/research

## Topics

${topicLines}

## Standards

- ${origin}/standards/mathematical-writing
- ${origin}/standards/mathematical-writing/markdown

## Machine interfaces

- ${origin}/api/openapi.json
- ${origin}/api/v1/research
- ${origin}/api/v1/research/{id}/manuscript
- ${origin}/api/v1/search?q=
- ${origin}/mcp
- ${origin}/api/v1/graph
- ${origin}/feed.xml
- ${origin}/research/graph

## Community

Profiles, critiques, forks, revisions, and submissions. Validators check an object. A person reviews it before publication.

- ${origin}/community
- ${origin}/researchers
- ${origin}/api/v1/community
- ${origin}/api/v1/profiles
- ${origin}/api/v1/critiques
- ${origin}/api/v1/forks
- ${origin}/api/v1/revisions
- ${origin}/api/v1/submissions
`;
}

export const markdownHeaders = {
  "Content-Type": "text/markdown; charset=utf-8",
  "Cache-Control": "public, max-age=3600",
  "X-Robots-Tag": "all",
};
