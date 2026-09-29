import { invalidJson, validateSubmission } from "@/lib/research/community";
import { readJson, writeJson, writeOptions } from "@/lib/research/http";
import { holdForReview, listReviewQueue } from "@/lib/research/review-queue";

export function OPTIONS() {
  return writeOptions();
}

export async function GET() {
  return writeJson({
    schema_version: "GreyCommunity 1.0",
    review: "human_review_required",
    storage: "review_queue",
    note: "POST a valid research object to keep it for review. The object stays unpublished until a person publishes it.",
    queue: (await listReviewQueue()).filter((item) => item.object_type === "submission"),
  });
}

export async function POST(request: Request) {
  const parsed = await readJson(request);
  if (!parsed.ok) return writeJson(invalidJson("submission"), 400);
  const result = await holdForReview(validateSubmission(parsed.value), parsed.value);
  return writeJson(result, result.valid ? 200 : 422);
}
