import { json, jsonError, options, readParam } from "@/lib/research/http";
import { getStudy } from "@/lib/research/registry";

export function OPTIONS() {
  return options();
}

export async function GET(_request: Request, context: { params: Promise<Record<string, string>> }) {
  const study = getStudy(await readParam(context, "id"));
  if (!study) return jsonError(404, "not_found");
  const version = await readParam(context, "version");
  if (version !== study.version) return jsonError(404, "version_not_found");
  return json({ ...study, version_record: { current: true, changes: study.editorial.change_log } });
}
