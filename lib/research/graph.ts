import { publicUrl } from "../urls";
import { formGraphEdges } from "./extractions/from-graph";
import { researchObjects } from "./registry";
import { topicBySlug } from "./topics";

export type GraphEdge = {
  subject_id: string;
  predicate: string;
  object_id: string;
  note: string;
};

export type GraphNode = {
  id: string;
  type: "study" | "series" | "claim" | "assumption" | "result" | "model" | "source" | "topic";
  label: string;
  evidence_status: "modelled" | null;
  href: string | null;
};

const registered = formGraphEdges.filter(
  (edge) => edge.object_id !== "none" && edge.object_id !== "none recorded",
);

export function researchGraph(studyId?: string | null) {
  const edges = allEdges();
  const scoped = studyId ? edges.filter((edge) => touchesStudy(edge, studyId)) : edges;
  const ids = new Set<string>();
  for (const edge of scoped) {
    ids.add(edge.subject_id);
    ids.add(edge.object_id);
  }
  return {
    schema_version: "GreyResearchGraph 1.0",
    study_id: studyId ?? null,
    node_count: ids.size,
    edge_count: scoped.length,
    nodes: [...ids].map(nodeFor).filter((node) => node !== null),
    edges: scoped,
  };
}

export function graphSummary() {
  const edges = allEdges();
  const predicates: Record<string, number> = {};
  for (const edge of edges) predicates[edge.predicate] = (predicates[edge.predicate] ?? 0) + 1;
  return {
    schema_version: "GreyResearchGraph 1.0",
    study_count: researchObjects.length,
    edge_count: edges.length,
    predicates,
  };
}

function allEdges(): GraphEdge[] {
  const edges: GraphEdge[] = [...registered];
  for (const study of researchObjects) {
    const seriesId = `GSX:${study.id.split(":")[1]?.split("-")[0]}`;
    edges.push({
      subject_id: study.id,
      predicate: "part_of",
      object_id: seriesId,
      note: study.series_title,
    });
    for (const claim of study.claims) {
      edges.push({
        subject_id: study.id,
        predicate: "has_claim",
        object_id: claim.id,
        note: "Registered claim.",
      });
      const model = study.models[0];
      if (model) {
        edges.push({
          subject_id: claim.id,
          predicate: "generated_by",
          object_id: model.id,
          note: model.name,
        });
      }
      for (const sourceId of claim.supported_by) {
        edges.push({
          subject_id: claim.id,
          predicate: "supported_by",
          object_id: sourceId,
          note: "Source registered on the conditional claim.",
        });
      }
      for (const sourceId of claim.contradicted_by) {
        edges.push({
          subject_id: claim.id,
          predicate: "contradicted_by",
          object_id: sourceId,
          note: "Contradicting source registered on the claim.",
        });
      }
      for (const claimId of claim.qualifies) {
        edges.push({ subject_id: claim.id, predicate: "qualifies", object_id: claimId, note: "Registered qualification." });
      }
      for (const claimId of claim.contradicts) {
        edges.push({ subject_id: claim.id, predicate: "contradicts", object_id: claimId, note: "Registered contradiction." });
      }
    }
    for (const topic of study.topics) {
      edges.push({
        subject_id: study.id,
        predicate: "has_topic",
        object_id: `GSX:TOPIC:${topic}`,
        note: "Registered topic.",
      });
    }
    for (const other of study.related_studies) {
      edges.push({
        subject_id: study.id,
        predicate: "related_to",
        object_id: other.id,
        note: study.series_title,
      });
    }
  }
  const assumptions = researchObjects.flatMap((study) => study.assumptions.map((assumption) => ({ study, assumption })));
  for (let left = 0; left < assumptions.length; left += 1) {
    for (let right = left + 1; right < assumptions.length; right += 1) {
      const a = assumptions[left];
      const b = assumptions[right];
      if (a.study.id === b.study.id) continue;
      if (a.assumption.name.trim().toLowerCase() !== b.assumption.name.trim().toLowerCase()) continue;
      edges.push({
        subject_id: a.assumption.id,
        predicate: "shares_assumption_name_with",
        object_id: b.assumption.id,
        note: a.assumption.name,
      });
    }
  }
  return edges;
}

function touchesStudy(edge: GraphEdge, studyId: string) {
  return (
    edge.subject_id === studyId ||
    edge.object_id === studyId ||
    edge.subject_id.startsWith(`${studyId}:`) ||
    edge.object_id.startsWith(`${studyId}:`)
  );
}

function nodeFor(id: string): GraphNode | null {
  if (id.startsWith("GSX:TOPIC:")) {
    const slug = id.slice("GSX:TOPIC:".length);
    const topic = topicBySlug.get(slug);
    return topic
      ? { id, type: "topic", label: topic.title, evidence_status: null, href: publicUrl(`/topics/${slug}`) }
      : null;
  }
  const study = researchObjects.find((item) => item.id === id || id.startsWith(`${item.id}:`));
  if (!study && id.startsWith("GSX:")) {
    const series = researchObjects.find((item) => item.id.startsWith(`${id}-`));
    if (!series) return null;
    return {
      id,
      type: "series",
      label: series.series_title,
      evidence_status: null,
      href: publicUrl(`/series/${series.series_slug}`),
    };
  }
  if (!study) return null;
  if (id === study.id) {
    return {
      id,
      type: "study",
      label: study.title,
      evidence_status: "modelled",
      href: study.links.html,
    };
  }
  const claim = study.claims.find((item) => item.id === id);
  if (claim) {
    return { id, type: "claim", label: claim.claim, evidence_status: "modelled", href: claim.href };
  }
  const assumption = study.assumptions.find((item) => item.id === id);
  if (assumption) {
    return { id, type: "assumption", label: assumption.statement, evidence_status: "modelled", href: study.links.json };
  }
  const result = study.results.find((item) => item.id === id);
  if (result) {
    return { id, type: "result", label: result.statement, evidence_status: "modelled", href: study.links.json };
  }
  const model = study.models.find((item) => item.id === id);
  if (model) {
    return { id, type: "model", label: model.name, evidence_status: "modelled", href: study.links.json };
  }
  const source = study.sources.find((item) => item.id === id);
  if (source) {
    return { id, type: "source", label: source.title, evidence_status: null, href: source.href };
  }
  return null;
}
