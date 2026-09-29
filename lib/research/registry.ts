import { papers, researchers, researchSeries } from "../catalog";
import { publicUrl } from "../urls";
import {
  AI_DISCLOSURE,
  EXTRACTION_NOTES,
  RECORD_DATE,
  RECORD_DATE_NOTE,
  RETRIEVAL_NOTE,
  RETRIEVAL_NOTE_PARTIAL,
  SCHEMA_VERSION,
} from "./constants";
import { extractionFor } from "./extractions";
import { formPackages } from "./extractions/from-packages";
import { researchTypeForSeries, studyId } from "./ids";
import { studyOverlays } from "./overlay";
import { researchObjectSchema, type ResearchObject } from "./schema";
import { searchDocuments, tokenize, type SearchDocument } from "./search";
import { manuscriptFor, manuscriptMetadataFor } from "./manuscripts";
import { topicBySlug, topicDefinitions } from "./topics";

const authors = researchers.map((researcher) => ({
  name: researcher.name,
  affiliation: researcher.affiliation,
  slug: researcher.slug,
}));

function buildObjects(): ResearchObject[] {
  const drafts = papers.map((paper) => {
    const series = researchSeries.find((entry) => entry.papers.some((item) => item.slug === paper.slug));
    if (!series) throw new Error(`Paper ${paper.slug} is missing its series`);
    const overlay = studyOverlays[paper.slug];
    if (!overlay) throw new Error(`Paper ${paper.slug} is missing a research-object overlay`);

    for (const topic of overlay.topics) {
      if (!topicBySlug.has(topic)) throw new Error(`Unknown topic ${topic} on ${paper.slug}`);
    }

    const id = studyId(series.slug, paper.number);
    const extraction = extractionFor(id);
    if (extraction) validateExtraction(id, extraction);
    const pack = formPackages[id as keyof typeof formPackages];
    const manuscript = manuscriptMetadataFor(id);
    if (!manuscript) throw new Error(`Paper ${paper.slug} is missing its full-text manuscript twin`);
    const htmlPath = `/research/${series.slug}/${paper.slug}`;
    const markdownPath = `${htmlPath}/markdown`;
    const jsonPath = `/api/v1/research/${paper.slug}`;
    const keywords = unique([
      ...overlay.topics.map((topic) => topicBySlug.get(topic)?.title ?? topic),
      ...overlay.geographies,
      ...tokenize(paper.title),
      ...tokenize(overlay.primaryQuestion),
    ]);

    return {
      schema_version: SCHEMA_VERSION,
      id,
      slug: paper.slug,
      series_slug: series.slug,
      series_title: series.title,
      series_number: series.number,
      paper_number: paper.number,
      title: paper.title,
      version: "1.0" as const,
      status: "published" as const,
      primary_question: overlay.primaryQuestion,
      summary: paper.description,
      answer: pack?.answer_block ?? null,
      topics: overlay.topics,
      entities: pack?.entities ?? overlay.geographies,
      methods: pack?.methods ?? [],
      parameters: pack?.parameters ?? [],
      equations: pack?.equations ?? [],
      scenarios: pack?.scenarios ?? [],
      unresolved_questions: pack?.unresolved_questions ?? [],
      geographies: overlay.geographies,
      keywords,
      related_questions: overlay.relatedQuestions,
      research_type: researchTypeForSeries(series.slug),
      evidence_status: "modelled" as const,
      peer_review_status: "none" as const,
      external_review_status: "none" as const,
      ai_assistance: {
        disclosure: AI_DISCLOSURE,
        itemised: false as const,
      },
      date_modified: RECORD_DATE,
      date_note: RECORD_DATE_NOTE,
      authors,
      extraction_status: extraction ? ("full_text_claim_led" as const) : ("pending" as const),
      manuscript,
      claims: extraction?.claims ?? [],
      assumptions: (extraction?.assumptions ?? []).map((item) => ({
        ...item,
        href: publicUrl(`${htmlPath}/assumptions/${item.local_id}`),
      })),
      results: (extraction?.results ?? []).map((item) => ({
        ...item,
        href: publicUrl(`${htmlPath}/results/${item.local_id}`),
      })),
      models: (extraction?.models ?? []).map((item) => ({
        ...item,
        href: publicUrl(`${htmlPath}/models/${item.local_id}`),
      })),
      sources: pack?.sources?.length
        ? pack.sources.map((source) => ({
            ...source,
            href: source.href,
            ...(source.id === `${id}:PDF`
              ? { pages: paper.pages, size: paper.size, media_type: "application/pdf" }
              : {}),
          }))
        : [
            {
              id: `${id}:PDF`,
              type: "manuscript",
              title: paper.title,
              href: publicUrl(paper.href),
              pages: paper.pages,
              size: paper.size,
              media_type: "application/pdf",
            },
          ],
      datasets: pack?.datasets ?? [],
      figures: pack?.figures ?? [],
      tables: pack?.tables ?? [],
      reproducibility: pack?.reproducibility ?? {
        code_available: false,
        data_available: false,
        environment_available: false,
        random_seed: "not recorded",
        software: [],
        repository_url: null,
      },
      editorial: pack?.editorial ?? {
        required_checks: {},
        blocking_issues: ["No semantic-twin editorial record is compiled."],
        warnings: [],
        change_log: [],
      },
      links: {
        html: publicUrl(htmlPath),
        markdown: publicUrl(markdownPath),
        manuscript: publicUrl(`/api/v1/research/${paper.slug}/manuscript`),
        json: publicUrl(jsonPath),
        pdf: publicUrl(paper.href),
      },
      citation: {
        machine: `GreyScienx, ${id}, version 1.0`,
        text: `GreyScienx. ${paper.title}. ${id}. Version 1.0.`,
      },
      retrieval_note: extraction ? RETRIEVAL_NOTE_PARTIAL : RETRIEVAL_NOTE,
    };
  });

  const parsed = drafts.map((draft) => {
    const related_studies = drafts
      .filter((other) => other.series_slug === draft.series_slug && other.id !== draft.id)
      .map((other) => ({
        id: other.id,
        slug: other.slug,
        title: other.title,
        href: other.links.html,
      }));
    return researchObjectSchema.parse({ ...draft, related_studies });
  });

  const ids = new Set<string>();
  for (const study of parsed) {
    if (ids.has(study.id)) throw new Error(`Duplicate study id ${study.id}`);
    ids.add(study.id);
  }

  for (const topic of topicDefinitions) {
    if (!parsed.some((study) => study.topics.includes(topic.slug))) {
      throw new Error(`Topic ${topic.slug} has no studies`);
    }
    for (const connected of topic.connected) {
      if (!topicBySlug.has(connected)) throw new Error(`Topic ${topic.slug} links to unknown topic ${connected}`);
    }
  }

  for (const slug of Object.keys(studyOverlays)) {
    if (!parsed.some((study) => study.slug === slug)) {
      throw new Error(`Overlay ${slug} does not match a published paper`);
    }
  }

  return parsed;
}

function topicAssumptions(studies: ResearchObject[]) {
  const rank = { high: 0, moderate: 1, low: 2 };
  const seen = new Set<string>();
  return studies
    .flatMap((study) => study.assumptions.map((assumption) => ({ assumption, study })))
    .sort(
      (a, b) =>
        rank[a.assumption.sensitivity] - rank[b.assumption.sensitivity] ||
        a.assumption.name.localeCompare(b.assumption.name),
    )
    .flatMap(({ assumption, study }) => {
      const key = assumption.name.trim().toLowerCase();
      if (seen.has(key)) return [];
      seen.add(key);
      return [
        {
          id: assumption.id,
          name: assumption.name,
          sensitivity: assumption.sensitivity,
          study_id: study.id,
          href: publicUrl(`/research/${study.series_slug}/${study.slug}`),
        },
      ];
    })
    .slice(0, 8);
}

function unique(values: string[]) {
  return [...new Set(values.map((value) => value.trim()).filter(Boolean))];
}

export const researchObjects = buildObjects();

const byKey = new Map<string, ResearchObject>();
for (const study of researchObjects) {
  byKey.set(study.id.toLowerCase(), study);
  byKey.set(study.slug.toLowerCase(), study);
}

export function getStudy(idOrSlug: string) {
  const key = decodeURIComponent(idOrSlug).trim().toLowerCase();
  return byKey.get(key) ?? null;
}

export function getSeriesRecord(slug: string) {
  const series = researchSeries.find((entry) => entry.slug === slug);
  if (!series) return null;
  const studies = researchObjects.filter((study) => study.series_slug === slug);
  return {
    slug: series.slug,
    number: series.number,
    title: series.title,
    question: series.description,
    study_count: studies.length,
    geographies: unique(studies.flatMap((study) => study.geographies)),
    topics: unique(studies.flatMap((study) => study.topics)),
    studies: studies.map(studySummary),
    links: {
      html: publicUrl(`/series/${series.slug}`),
      json: publicUrl(`/api/v1/series/${series.slug}`),
    },
  };
}

export function listSeriesRecords() {
  return researchSeries.map((series) => getSeriesRecord(series.slug)).filter((series) => series !== null);
}

export function getTopicRecord(slug: string) {
  const topic = topicBySlug.get(slug);
  if (!topic) return null;
  const studies = researchObjects.filter((study) => study.topics.includes(slug));
  return {
    slug: topic.slug,
    title: topic.title,
    definition: topic.definition,
    connected_topics: topic.connected.map((connected) => {
      const match = topicBySlug.get(connected);
      return { slug: connected, title: match?.title ?? connected, href: publicUrl(`/topics/${connected}`) };
    }),
    study_count: studies.length,
    studies: studies.map(studySummary),
    related_questions: unique(studies.flatMap((study) => study.related_questions)).slice(0, 8),
    claims: studies.flatMap((study) => {
      const claim = study.claims[0];
      if (!claim) return [];
      return [
        {
          id: claim.id,
          claim: claim.claim,
          study_id: study.id,
          study_title: study.title,
          href: publicUrl(`/research/${study.series_slug}/${study.slug}/claims/${claim.local_id}`),
        },
      ];
    }),
    assumptions: topicAssumptions(studies),
    datasets: studies.flatMap((study) => {
      const pack = formPackages[study.id as keyof typeof formPackages];
      if (!pack) return [];
      return pack.datasets.map((dataset) => ({
        id: dataset.id,
        title: dataset.title,
        study_id: study.id,
        href: publicUrl(`/research/${study.series_slug}/${study.slug}/data`),
      }));
    }),
    links: {
      html: publicUrl(`/topics/${topic.slug}`),
      json: publicUrl(`/api/v1/topics/${topic.slug}`),
    },
  };
}

export function listTopicRecords() {
  return topicDefinitions.map((topic) => getTopicRecord(topic.slug)).filter((topic) => topic !== null);
}

export function searchResearch(query: string) {
  return searchDocuments(researchObjects.map(toSearchDocument), query);
}

export function studySummary(study: ResearchObject) {
  return {
    id: study.id,
    slug: study.slug,
    title: study.title,
    primary_question: study.primary_question,
    summary: study.summary,
    research_type: study.research_type,
    evidence_status: study.evidence_status,
    series_slug: study.series_slug,
    series_title: study.series_title,
    version: study.version,
    date_modified: study.date_modified,
    links: study.links,
  };
}

export function studyCollection(
  study: ResearchObject,
  kind: "claims" | "assumptions" | "results" | "models",
) {
  const items = study[kind];
  return {
    study_id: study.id,
    extraction_status: study.extraction_status,
    note: items.length > 0 ? extractedNote(kind) : EXTRACTION_NOTES[kind],
    retrieval_note: study.retrieval_note,
    [kind]: items,
  };
}

export function getClaim(study: ResearchObject, claimId: string | null) {
  if (!claimId) return studyCollection(study, "claims");
  const key = claimId.trim().toLowerCase();
  const claim = study.claims.find(
    (item) => item.local_id.toLowerCase() === key || item.id.toLowerCase() === key,
  );
  if (!claim) {
    return {
      study_id: study.id,
      claim_id: claimId,
      extraction_status: study.claims.length > 0 ? "not_found" : study.extraction_status,
      claim: null,
      note:
        study.claims.length > 0
          ? "That claim id is not in the extracted set for this study."
          : EXTRACTION_NOTES.claims,
      retrieval_note: study.retrieval_note,
    };
  }
  return claim;
}

export function getSubobject(
  study: ResearchObject,
  kind: "assumptions" | "results" | "models",
  objectId: string,
) {
  const key = objectId.trim().toLowerCase();
  return (
    study[kind].find(
      (item) => item.local_id.toLowerCase() === key || item.id.toLowerCase() === key,
    ) ?? null
  );
}

export function studySources(study: ResearchObject) {
  return {
    study_id: study.id,
    extraction_status: study.extraction_status,
    note: EXTRACTION_NOTES.sources,
    retrieval_note: study.retrieval_note,
    sources: study.sources,
  };
}

export function studyRelated(study: ResearchObject) {
  return {
    study_id: study.id,
    series_slug: study.series_slug,
    related_studies: study.related_studies,
  };
}

export function studyParams() {
  return researchObjects.map((study) => ({ id: study.slug }));
}

export function researchTypeLabel(researchType: ResearchObject["research_type"]) {
  if (researchType === "counterfactual") return "Counterfactual";
  return "Exploratory simulation";
}

function extractedNote(kind: "claims" | "assumptions" | "results" | "models") {
  return `These ${kind} are extracted from the manuscript. A claim stays conditional on the assumptions it names.`;
}

function validateExtraction(
  studyIdValue: string,
  extraction: NonNullable<ReturnType<typeof extractionFor>>,
) {
  const assumptionIds = new Set(extraction.assumptions.map((item) => item.id));
  const resultIds = new Set(extraction.results.map((item) => item.id));
  const seen = new Set<string>();
  for (const claim of extraction.claims) {
    if (claim.source_study !== studyIdValue) throw new Error(`${claim.id} names another study`);
    if (seen.has(claim.id)) throw new Error(`Duplicate claim ${claim.id}`);
    seen.add(claim.id);
    if (!resultIds.has(claim.result)) throw new Error(`${claim.id} cites a missing result ${claim.result}`);
    for (const resultId of claim.results) {
      if (!resultIds.has(resultId)) throw new Error(`${claim.id} cites a missing result ${resultId}`);
    }
    for (const assumptionId of claim.depends_on) {
      if (!assumptionIds.has(assumptionId)) {
        throw new Error(`${claim.id} depends on a missing assumption ${assumptionId}`);
      }
    }
  }
}

function toSearchDocument(study: ResearchObject): SearchDocument {
  return {
    id: study.id,
    slug: study.slug,
    seriesSlug: study.series_slug,
    seriesTitle: study.series_title,
    title: study.title,
    primaryQuestion: study.primary_question,
    summary: study.summary,
    topics: study.topics.flatMap((topic) => [topic, topicBySlug.get(topic)?.title ?? ""]),
    keywords: study.keywords,
    relatedQuestions: study.related_questions,
    claims: study.claims.map((claim) => ({
      id: claim.id,
      text: claim.claim,
      href: claim.href,
      dependsOn: claim.depends_on,
    })),
    assumptions: study.assumptions.map((assumption) => ({
      id: assumption.id,
      name: assumption.name,
      statement: assumption.statement,
      sensitivity: assumption.sensitivity,
    })),
    results: study.results.map((result) => result.statement),
    limitations: study.claims.map((claim) => claim.main_limitation),
    models: study.models.map((model) => `${model.name} ${model.statement}`),
    manuscriptText: manuscriptFor(study.id)?.content_markdown ?? "",
    geographies: study.geographies,
    researchType: study.research_type,
    version: study.version,
    dateModified: study.date_modified,
    canonicalUrl: study.links.html,
  };
}
