import { json, jsonError, options, readParam } from "@/lib/research/http";
import { getStudy, studyCollection, studyParams } from "@/lib/research/registry";

export const dynamic = "force-static";

export function generateStaticParams() {
  return studyParams();
}

export function OPTIONS() {
  return options();
}

export async function GET(_request: Request, context: { params: Promise<Record<string, string>> }) {
  const study = getStudy(await readParam(context, "id"));
  if (!study) return jsonError(404, "not_found");
  return json(studyCollection(study, "assumptions"));
}
