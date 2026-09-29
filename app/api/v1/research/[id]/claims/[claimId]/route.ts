import { json, jsonError, options, readParam } from "@/lib/research/http";
import { getClaim, getStudy } from "@/lib/research/registry";

export function OPTIONS() {
  return options();
}

export async function GET(_request: Request, context: { params: Promise<Record<string, string>> }) {
  const study = getStudy(await readParam(context, "id"));
  if (!study) return jsonError(404, "not_found");
  const claim = getClaim(study, await readParam(context, "claimId"));
  if ("claim" in claim && claim.claim === null) return json(claim, 404);
  return json(claim);
}
