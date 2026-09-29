import { publicUrl } from "../../urls";
import type { Assumption, Claim, ModelRecord, ResultRecord } from "../schema";
import { formExtractions } from "./from-forms";

export type StudyExtraction = {
  assumptions: Assumption[];
  results: ResultRecord[];
  models: ModelRecord[];
  claims: Claim[];
};

export function extractionFor(studyId: string): StudyExtraction | null {
  const extraction = formExtractions[studyId as keyof typeof formExtractions];
  if (!extraction) return null;
  return {
    assumptions: extraction.assumptions.map((assumption) => ({
      ...assumption,
      href: publicUrl(`/api/v1/research/${studyId}/assumptions/${assumption.local_id}`),
    })),
    results: extraction.results.map((result) => ({
      ...result,
      href: publicUrl(`/api/v1/research/${studyId}/results/${result.local_id}`),
    })),
    models: extraction.models.map((model) => ({
      ...model,
      href: publicUrl(`/api/v1/research/${studyId}/models/${model.local_id}`),
    })),
    claims: extraction.claims.map((claim) => ({
      ...claim,
      href: publicUrl(claim.href),
    })),
  } as StudyExtraction;
}
