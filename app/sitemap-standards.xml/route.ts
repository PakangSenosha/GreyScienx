import { sitemapResponse } from "@/lib/research/sitemap-xml";

export const dynamic = "force-static";

export function GET() {
  return sitemapResponse([
    "/standards/mathematical-writing",
    "/standards/mathematical-writing/markdown",
  ]);
}
