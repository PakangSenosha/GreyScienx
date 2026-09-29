import { researchObjects } from "@/lib/research/registry";
import { site } from "@/lib/site";

export const dynamic = "force-static";

export function GET() {
  const origin = `https://${site.domain}`;
  const items = researchObjects
    .map(
      (study) => `    <item>
      <title>${escapeXml(study.title)}</title>
      <link>${study.links.html}</link>
      <guid isPermaLink="false">${escapeXml(study.id)}</guid>
      <description>${escapeXml(study.primary_question)}</description>
      <category>${escapeXml(study.series_title)}</category>
      <pubDate>${new Date(`${study.date_modified}T00:00:00Z`).toUTCString()}</pubDate>
    </item>`,
    )
    .join("\n");
  const body = `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>${escapeXml(site.name)} research</title>
    <link>${origin}/research</link>
    <description>Published GreyScienx studies. Each item is a modelled research record, not a forecast.</description>
    <lastBuildDate>${new Date(`${researchObjects[0]?.date_modified ?? "2026-09-27"}T00:00:00Z`).toUTCString()}</lastBuildDate>
${items}
  </channel>
</rss>
`;
  return new Response(body, {
    headers: {
      "Content-Type": "application/rss+xml; charset=utf-8",
      "Cache-Control": "public, max-age=3600",
    },
  });
}

function escapeXml(value: string) {
  return value
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}
