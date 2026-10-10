import { studyMarkdown } from "@/lib/research/markdown";
import { getStudy } from "@/lib/research/registry";

const headers = {
  "Access-Control-Allow-Origin": "*",
  "Cache-Control": "public, max-age=3600",
  "X-Robots-Tag": "noindex, nofollow, noarchive",
  Vary: "Accept",
};

export function OPTIONS() {
  return new Response(null, {
    status: 204,
    headers: { ...headers, "Access-Control-Allow-Methods": "GET, HEAD, OPTIONS" },
  });
}

export async function GET(request: Request, context: { params: Promise<{ series: string; paper: string }> }) {
  const { series, paper } = await context.params;
  const study = getStudy(paper);
  if (!study || study.series_slug !== series) {
    return Response.json({ error: "not_found" }, { status: 404, headers });
  }
  const accept = request.headers.get("accept")?.toLowerCase() ?? "";
  if (accept.includes("application/pdf")) return Response.redirect(study.links.pdf, 307);
  if (accept.includes("text/markdown")) {
    return new Response(studyMarkdown(study), {
      headers: { ...headers, "Content-Type": "text/markdown; charset=utf-8", "Content-Location": study.links.markdown },
    });
  }
  return Response.json(study, {
    headers: { ...headers, "Content-Location": study.links.json },
  });
}
