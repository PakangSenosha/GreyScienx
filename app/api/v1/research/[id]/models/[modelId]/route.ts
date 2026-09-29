import { json, jsonError, options, readParam } from "@/lib/research/http";
import { getStudy, getSubobject } from "@/lib/research/registry";

export function OPTIONS() {
  return options();
}

export async function GET(_request: Request, context: { params: Promise<Record<string, string>> }) {
  const study = getStudy(await readParam(context, "id"));
  if (!study) return jsonError(404, "not_found");
  const model = getSubobject(study, "models", await readParam(context, "modelId"));
  return model ? json(model) : jsonError(404, "not_found");
}
