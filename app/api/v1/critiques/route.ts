import { communityIndex, invalidJson, validateCritique } from "@/lib/research/community";
import { readJson, writeJson, writeOptions } from "@/lib/research/http";
import { holdForReview } from "@/lib/research/review-queue";

export function OPTIONS() {
  return writeOptions();
}

export async function GET() {
  const index = await communityIndex();
  return writeJson({
    schema_version: index.schema_version,
    count: index.counts.critiques,
    note: index.counts.critiques ? `Published critiques: ${index.counts.critiques}.` : "Published critiques: none.",
    critique_types: index.critique_types,
    critiques: index.critiques,
  });
}

export async function POST(request: Request) {
  const parsed = await readJson(request);
  if (!parsed.ok) return writeJson(invalidJson("critique"), 400);
  const result = await holdForReview(validateCritique(parsed.value), parsed.value);
  return writeJson(result, result.valid ? 200 : 422);
}
