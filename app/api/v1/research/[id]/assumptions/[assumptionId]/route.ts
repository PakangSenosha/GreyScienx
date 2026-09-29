import { json, jsonError, options, readParam } from "@/lib/research/http";
import { getStudy, getSubobject } from "@/lib/research/registry";

export function OPTIONS() {
  return options();
}

export async function GET(_request: Request, context: { params: Promise<Record<string, string>> }) {
  const study = getStudy(await readParam(context, "id"));
  if (!study) return jsonError(404, "not_found");
  const assumption = getSubobject(study, "assumptions", await readParam(context, "assumptionId"));
  return assumption ? json(assumption) : jsonError(404, "not_found");
}
