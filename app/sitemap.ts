import type { MetadataRoute } from "next";
import { researchSeries } from "@/lib/catalog";
import { listTopicRecords, researchObjects } from "@/lib/research/registry";
import { site } from "@/lib/site";
import { articleUrl } from "@/lib/urls";

export default function sitemap(): MetadataRoute.Sitemap {
  const origin = `https://${site.domain}`;
  const now = new Date();

  const pages: MetadataRoute.Sitemap = [
    { url: origin, lastModified: now, changeFrequency: "weekly", priority: 1 },
    { url: `${origin}/research`, lastModified: now, changeFrequency: "weekly", priority: 0.9 },
    { url: `${origin}/about`, lastModified: now, changeFrequency: "monthly", priority: 0.5 },
    { url: `${origin}/privacy`, lastModified: now, changeFrequency: "yearly", priority: 0.3 },
    { url: `${origin}/terms`, lastModified: now, changeFrequency: "yearly", priority: 0.3 },
    { url: `${origin}/support`, lastModified: now, changeFrequency: "monthly", priority: 0.3 },
    { url: `${origin}/series`, lastModified: now, changeFrequency: "weekly", priority: 0.7 },
    { url: `${origin}/topics`, lastModified: now, changeFrequency: "weekly", priority: 0.7 },
    { url: `${origin}/standards/mathematical-writing`, lastModified: now, changeFrequency: "monthly", priority: 0.4 },
    { url: `${origin}/research/graph`, lastModified: now, changeFrequency: "weekly", priority: 0.5 },
    { url: `${origin}/community`, lastModified: now, changeFrequency: "monthly", priority: 0.5 },
    { url: `${origin}/researchers`, lastModified: now, changeFrequency: "monthly", priority: 0.5 },
    { url: `${origin}/feed.xml`, lastModified: now, changeFrequency: "weekly", priority: 0.4 },
    { url: `${origin}/research/index.md`, lastModified: now, changeFrequency: "weekly", priority: 0.5 },
    { url: `${origin}/series/index.md`, lastModified: now, changeFrequency: "weekly", priority: 0.4 },
    { url: `${origin}/about/pakang-senosha`, lastModified: now, changeFrequency: "monthly", priority: 0.4 },
    { url: `${origin}/experiments/virtual-casino`, lastModified: now, changeFrequency: "monthly", priority: 0.9 },
    { url: `${origin}/experiments/virtual-casino/house-edge`, lastModified: now, changeFrequency: "monthly", priority: 0.8 },
    { url: `${origin}/experiments/virtual-casino/house-edge/players`, lastModified: now, changeFrequency: "monthly", priority: 0.7 },
    { url: `${origin}/experiments/virtual-casino/house-edge/cohorts`, lastModified: now, changeFrequency: "monthly", priority: 0.7 },
    { url: `${origin}/experiments/virtual-casino/house-edge/games`, lastModified: now, changeFrequency: "monthly", priority: 0.7 },
    { url: `${origin}/experiments/virtual-casino/house-edge/worlds`, lastModified: now, changeFrequency: "monthly", priority: 0.7 },
    { url: `${origin}/experiments/virtual-casino/make-it-big`, lastModified: now, changeFrequency: "monthly", priority: 0.8 },
    { url: `${origin}/experiments/virtual-casino/make-it-big/results`, lastModified: now, changeFrequency: "monthly", priority: 0.7 },
    { url: `${origin}/experiments/virtual-casino/make-it-big/strategies`, lastModified: now, changeFrequency: "monthly", priority: 0.7 },
    { url: `${origin}/experiments/virtual-casino/make-it-big/games`, lastModified: now, changeFrequency: "monthly", priority: 0.7 },
    { url: `${origin}/experiments/virtual-casino/make-it-big/survival`, lastModified: now, changeFrequency: "monthly", priority: 0.7 },
    { url: `${origin}/experiments/virtual-casino/make-it-big/methods`, lastModified: now, changeFrequency: "monthly", priority: 0.6 },
    { url: `${origin}/experiments/virtual-casino/make-it-big/downloads`, lastModified: now, changeFrequency: "monthly", priority: 0.6 },
    { url: `${origin}/experiments/virtual-casino/make-it-big/safety`, lastModified: now, changeFrequency: "monthly", priority: 0.6 },
    { url: `${origin}/experiments/virtual-casino/house-edge/methods`, lastModified: now, changeFrequency: "monthly", priority: 0.6 },
    { url: `${origin}/experiments/virtual-casino/house-edge/safety`, lastModified: now, changeFrequency: "monthly", priority: 0.6 },
  ];

  for (const series of researchSeries) {
    pages.push({
      url: `${origin}/series/${series.slug}`,
      lastModified: now,
      changeFrequency: "monthly",
      priority: 0.7,
    });
    for (const paper of series.papers) {
      pages.push({
        url: articleUrl(series, paper),
        lastModified: now,
        changeFrequency: "monthly",
        priority: 0.8,
      });
    }
  }

  for (const study of researchObjects) {
    pages.push({
      url: study.links.markdown,
      lastModified: now,
      changeFrequency: "monthly",
      priority: 0.4,
    });
    pages.push({
      url: `${origin}/research/${study.series_slug}/${study.slug}/data`,
      lastModified: now,
      changeFrequency: "monthly",
      priority: 0.3,
    });
    pages.push({
      url: `${origin}/research/${study.series_slug}/${study.slug}/reproduce`,
      lastModified: now,
      changeFrequency: "monthly",
      priority: 0.3,
    });
    pages.push({
      url: `${origin}/research/${study.series_slug}/${study.slug}/versions`,
      lastModified: now,
      changeFrequency: "monthly",
      priority: 0.3,
    });
    for (const claim of study.claims) {
      pages.push({
        url: claim.href,
        lastModified: now,
        changeFrequency: "monthly",
        priority: 0.5,
      });
    }
    for (const item of [...study.assumptions, ...study.results, ...study.models]) {
      pages.push({
        url: item.href,
        lastModified: now,
        changeFrequency: "monthly",
        priority: 0.4,
      });
    }
  }

  for (const topic of listTopicRecords()) {
    pages.push({
      url: topic.links.html,
      lastModified: now,
      changeFrequency: "monthly",
      priority: 0.6,
    });
  }

  return pages;
}
