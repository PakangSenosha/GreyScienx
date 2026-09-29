import { packageFor } from "@/lib/research/packages";
import { sitemapResponse } from "@/lib/research/sitemap-xml";
import { researchObjects } from "@/lib/research/registry";

export const dynamic = "force-static";

export function GET() {
  const paths = ["/research", "/research/index.md", "/research/graph"];
  for (const study of researchObjects) {
    const base = `/research/${study.series_slug}/${study.slug}`;
    paths.push(base, `${base}/markdown`, `${base}/data`, `${base}/reproduce`, `${base}/versions`);
    for (const claim of study.claims) paths.push(`${base}/claims/${claim.local_id}`);
    for (const assumption of study.assumptions) paths.push(`${base}/assumptions/${assumption.local_id}`);
    for (const result of study.results) paths.push(`${base}/results/${result.local_id}`);
    for (const model of study.models) paths.push(`${base}/models/${model.local_id}`);
    for (const file of packageFor(study.id)?.files ?? []) paths.push(file.href);
  }
  return sitemapResponse(paths);
}
