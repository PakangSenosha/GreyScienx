import { sitemapResponse } from "@/lib/research/sitemap-xml";
import { researchObjects } from "@/lib/research/registry";

export const dynamic = "force-static";

export function GET() {
  return sitemapResponse(researchObjects.map((study) => `/research/${study.series_slug}/${study.slug}/data`));
}
