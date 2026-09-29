import { researchSeries } from "@/lib/catalog";
import { sitemapResponse } from "@/lib/research/sitemap-xml";

export const dynamic = "force-static";

export function GET() {
  return sitemapResponse(["/series", "/series/index.md", ...researchSeries.map((series) => `/series/${series.slug}`)]);
}
