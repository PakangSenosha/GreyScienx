import type { MetadataRoute } from "next";
import { researchSeries } from "@/lib/catalog";
import { site } from "@/lib/site";
import { articleUrl } from "@/lib/urls";

export default function sitemap(): MetadataRoute.Sitemap {
  const origin = `https://${site.domain}`;
  const now = new Date();

  const pages: MetadataRoute.Sitemap = [
    { url: origin, lastModified: now, changeFrequency: "weekly", priority: 1 },
    { url: `${origin}/research`, lastModified: now, changeFrequency: "weekly", priority: 0.9 },
    { url: `${origin}/about`, lastModified: now, changeFrequency: "monthly", priority: 0.5 },
    { url: `${origin}/about/pakang-senosha`, lastModified: now, changeFrequency: "monthly", priority: 0.4 },
  ];

  for (const series of researchSeries) {
    for (const paper of series.papers) {
      pages.push({
        url: articleUrl(series, paper),
        lastModified: now,
        changeFrequency: "monthly",
        priority: 0.8,
      });
    }
  }

  return pages;
}
