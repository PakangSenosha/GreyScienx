import { RETRIEVAL_NOTE } from "@/lib/research/constants";
import { json, jsonError, options } from "@/lib/research/http";
import { matchesDiscovery } from "@/lib/research/packages";
import { searchResearch } from "@/lib/research/registry";

export function OPTIONS() {
  return options();
}

export function GET(request: Request) {
  const params = new URL(request.url).searchParams;
  const query = params.get("q") ?? "";
  const recordedMethod = params.get("method") ?? "";
  const code = params.get("code") ?? "";
  if (query.length > 500) return jsonError(400, "query_too_long");
  return json(
    {
      query,
      method: "hybrid_concept_vector_v1",
      filters: { method: recordedMethod, code },
      retrieval_note: RETRIEVAL_NOTE,
      results: searchResearch(query).filter((hit) => matchesDiscovery(hit.id, recordedMethod, code)),
    },
    200,
    "public, max-age=300",
  );
}
