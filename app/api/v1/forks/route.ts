import { communityIndex, invalidJson, validateFork } from "@/lib/research/community";
import { readJson, writeJson, writeOptions } from "@/lib/research/http";
import { holdForReview } from "@/lib/research/review-queue";

export function OPTIONS() {
  return writeOptions();
}

export async function GET() {
  const index = await communityIndex();
  return writeJson({
    schema_version: index.schema_version,
    count: index.counts.forks,
    note: index.counts.forks ? `Published forks: ${index.counts.forks}.` : "Published forks: none.",
    forks: index.forks,
  });
}

export async function POST(request: Request) {
  const parsed = await readJson(request);
  if (!parsed.ok) return writeJson(invalidJson("fork"), 400);
  const result = await holdForReview(validateFork(parsed.value), parsed.value);
  return writeJson(result, result.valid ? 200 : 422);
}
