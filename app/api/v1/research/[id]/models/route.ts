import { json, jsonError, options, readParam } from "@/lib/research/http";
import { getStudy, studyCollection } from "@/lib/research/registry";

export function OPTIONS() {
  return options();
}

export async function GET(_request: Request, context: { params: Promise<Record<string, string>> }) {
  const study = getStudy(await readParam(context, "id"));
  if (!study) return jsonError(404, "not_found");
  return json(studyCollection(study, "models"));
}
