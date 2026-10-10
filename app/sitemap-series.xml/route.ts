import { researchSeries } from "@/lib/catalog";
import { sitemapResponse } from "@/lib/research/sitemap-xml";

export const dynamic = "force-static";

export function GET() {
  return sitemapResponse(["/series", ...researchSeries.map((series) => `/series/${series.slug}`)]);
}
