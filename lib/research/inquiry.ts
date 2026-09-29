import { publicUrl } from "../urls";
import { researchGraph } from "./graph";
import { packageFor } from "./packages";
import type { ResearchObject } from "./schema";

export function compareStudies(left: ResearchObject, right: ResearchObject) {
  const leftNames = new Map(left.assumptions.map((item) => [item.name.trim().toLowerCase(), item.name]));
  const sharedAssumptions = right.assumptions.flatMap((item) => {
    const name = leftNames.get(item.name.trim().toLowerCase());
    return name ? [name] : [];
  });
  const edges = researchGraph().edges.filter((edge) => crosses(edge.subject_id, edge.object_id, left.id, right.id));
  return {
    note: "This comparison lists overlap already published in the two studies. It does not create a new result.",
    studies: [studyCard(left), studyCard(right)],
    shared_topics: left.topics.filter((topic) => right.topics.includes(topic)),
    shared_geographies: left.geographies.filter((place) => right.geographies.includes(place)),
    shared_assumption_names: [...new Set(sharedAssumptions)],
    contradictions: edges.filter((edge) => edge.predicate === "contradicts"),
    qualifications: edges.filter((edge) => edge.predicate === "qualifies"),
    links: edges.filter((edge) => edge.predicate === "related_to"),
  };
}

export function traceClaim(study: ResearchObject, claimId: string) {
  const key = claimId.trim().toLowerCase();
  const record = study.claims.find(
    (item) => item.local_id.toLowerCase() === key || item.id.toLowerCase() === key,
  );
  if (!record) {
    return {
      study_id: study.id,
      claim: null,
      assumptions: [],
      results: [],
      model: null,
      note:
        study.claims.length > 0
          ? "That claim id is not in the extracted set for this study."
          : "No claim has been extracted for this study.",
    };
  }
  const generatedBy = researchGraph(study.id).edges.find(
    (edge) => edge.subject_id === record.id && edge.predicate === "generated_by",
  );
  const model = study.models.find((item) => item.id === generatedBy?.object_id) ?? study.models[0] ?? null;
  return {
    study_id: study.id,
    claim: record,
    assumptions: study.assumptions.filter((item) => record.depends_on.includes(item.id)),
    results: study.results.filter((item) => record.results.includes(item.id)),
    model,
    evidence_status: record.evidence_status,
    main_limitation: record.main_limitation,
  };
}

export function findCounterarguments(study: ResearchObject, claimId: string | null) {
  const claims = claimId
    ? study.claims.filter(
        (item) => item.local_id.toLowerCase() === claimId.toLowerCase() || item.id.toLowerCase() === claimId.toLowerCase(),
      )
    : study.claims;
  const edges = researchGraph(study.id).edges;
  return {
    study_id: study.id,
    claim_id: claimId,
    external_critiques: [],
    note: "No external critique is published. Limitations below are the study's own recorded limits.",
    contradictions: edges.filter((edge) => edge.predicate === "contradicts"),
    qualifications: edges.filter((edge) => edge.predicate === "qualifies"),
    limitations: claims.map((item) => ({
      claim_id: item.id,
      evidence_status: item.evidence_status,
      main_limitation: item.main_limitation,
    })),
  };
}

export function modelSpec(study: ResearchObject) {
  return {
    study_id: study.id,
    extraction_status: study.extraction_status,
    models: study.models,
    note:
      study.models.length > 0
        ? "These model statements are extracted from the manuscript."
        : "No model object is registered for this study.",
  };
}

export function reproducibilityPackage(study: ResearchObject) {
  const pack = packageFor(study.id);
  return {
    study_id: study.id,
    reproduce: publicUrl(`/research/${study.series_slug}/${study.slug}/reproduce`),
    data: publicUrl(`/research/${study.series_slug}/${study.slug}/data`),
    datasets: pack?.datasets ?? [],
    reproducibility: pack?.reproducibility ?? null,
    files: pack?.files ?? [],
    unresolved_questions: pack?.unresolved_questions ?? [],
  };
}

function studyCard(study: ResearchObject) {
  return {
    id: study.id,
    title: study.title,
    primary_question: study.primary_question,
    research_type: study.research_type,
    evidence_status: study.evidence_status,
    version: study.version,
    href: study.links.html,
  };
}

function crosses(subject: string, object: string, left: string, right: string) {
  const subjectStudy = studyOf(subject);
  const objectStudy = studyOf(object);
  return (subjectStudy === left && objectStudy === right) || (subjectStudy === right && objectStudy === left);
}

function studyOf(id: string) {
  const match = id.match(/^(GSX:[A-Z]+-\d+)/);
  return match?.[1] ?? id;
}
