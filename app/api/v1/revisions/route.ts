import { communityIndex, invalidJson, validateRevision } from "@/lib/research/community";
import { readJson, writeJson, writeOptions } from "@/lib/research/http";
import { holdForReview } from "@/lib/research/review-queue";

export function OPTIONS() {
  return writeOptions();
}

export async function GET() {
  const index = await communityIndex();
  return writeJson({
    schema_version: index.schema_version,
    count: index.counts.revisions,
    note: index.counts.revisions ? `Published revisions: ${index.counts.revisions}.` : "Published revisions: none. Each study remains at version 1.0.",
    revisions: index.revisions,
  });
}

export async function POST(request: Request) {
  const parsed = await readJson(request);
  if (!parsed.ok) return writeJson(invalidJson("revision"), 400);
  const result = await holdForReview(validateRevision(parsed.value), parsed.value);
  return writeJson(result, result.valid ? 200 : 422);
}
