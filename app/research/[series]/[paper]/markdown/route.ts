import { getPaper, researchSeries } from "@/lib/catalog";
import { markdownHeaders, studyMarkdown } from "@/lib/research/markdown";
import { getStudy } from "@/lib/research/registry";

export const dynamic = "force-static";

export function generateStaticParams() {
  return researchSeries.flatMap((series) =>
    series.papers.map((paper) => ({
      series: series.slug,
      paper: paper.slug,
    })),
  );
}

export async function GET(
  _request: Request,
  context: { params: Promise<{ series: string; paper: string }> },
) {
  const { series, paper } = await context.params;
  const entry = getPaper(series, paper);
  const study = getStudy(paper);
  if (!entry || !study || study.series_slug !== series) {
    return new Response("Not found", { status: 404, headers: { "Content-Type": "text/plain; charset=utf-8" } });
  }
  return new Response(studyMarkdown(study), {
    headers: {
      ...markdownHeaders,
      Link: `<${study.links.html}>; rel="canonical"`,
    },
  });
}
