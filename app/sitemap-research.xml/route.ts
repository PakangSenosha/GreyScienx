import { sitemapResponse } from "@/lib/research/sitemap-xml";
import { researchObjects } from "@/lib/research/registry";

export const dynamic = "force-static";

export function GET() {
  const paths = ["/research"];
  for (const study of researchObjects) {
    const base = `/research/${study.series_slug}/${study.slug}`;
    paths.push(base);
  }
  return sitemapResponse(paths);
}
