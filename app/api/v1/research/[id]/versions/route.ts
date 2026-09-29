import { json, jsonError, options, readParam } from "@/lib/research/http";
import { getStudy } from "@/lib/research/registry";

export function OPTIONS() {
  return options();
}

export async function GET(_request: Request, context: { params: Promise<Record<string, string>> }) {
  const study = getStudy(await readParam(context, "id"));
  if (!study) return jsonError(404, "not_found");
  return json({
    study_id: study.id,
    current_version: study.version,
    versions: [{
      version: study.version,
      status: study.status,
      current: true,
      date_modified: study.date_modified,
      changes: study.editorial.change_log,
      href: `${study.links.json}/versions/${study.version}`,
    }],
  });
}
