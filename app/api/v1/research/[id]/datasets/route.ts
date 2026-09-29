import { packageFor } from "@/lib/research/packages";
import { json, jsonError, options, readParam } from "@/lib/research/http";
import { getStudy, studyParams } from "@/lib/research/registry";

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
  const pack = packageFor(study.id);
  return json({
    study_id: study.id,
    datasets: pack?.datasets ?? [],
    reproducibility: pack?.reproducibility ?? null,
    files: pack?.files ?? [],
  });
}
