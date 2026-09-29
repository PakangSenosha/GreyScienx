import type { MetadataRoute } from "next";
import { site } from "@/lib/site";

export default function robots(): MetadataRoute.Robots {
  return {
    rules: { userAgent: "*", allow: "/" },
    sitemap: [
      `https://${site.domain}/sitemap.xml`,
      `https://${site.domain}/sitemap-research.xml`,
      `https://${site.domain}/sitemap-series.xml`,
      `https://${site.domain}/sitemap-datasets.xml`,
      `https://${site.domain}/sitemap-standards.xml`,
    ],
  };
}
