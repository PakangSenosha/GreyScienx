import { json, jsonError, options, readParam } from "@/lib/research/http";
import { getStudy, getSubobject } from "@/lib/research/registry";

export function OPTIONS() {
  return options();
}

export async function GET(_request: Request, context: { params: Promise<Record<string, string>> }) {
  const study = getStudy(await readParam(context, "id"));
  if (!study) return jsonError(404, "not_found");
  const result = getSubobject(study, "results", await readParam(context, "resultId"));
  return result ? json(result) : jsonError(404, "not_found");
}
