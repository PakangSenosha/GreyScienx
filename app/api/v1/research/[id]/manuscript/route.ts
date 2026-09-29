import { json, jsonError, options, readParam } from "@/lib/research/http";
import { manuscriptResponse } from "@/lib/research/manuscripts";
import { getStudy, studyParams } from "@/lib/research/registry";

export const dynamic = "force-static";

export function generateStaticParams() {
  return studyParams();
}

export function OPTIONS() {
  return options();
}

export async function GET(
  request: Request,
  context: { params: Promise<{ id: string }> },
) {
  const study = getStudy(await readParam(context, "id"));
  if (!study) return jsonError(404, "not_found");
  const section = new URL(request.url).searchParams.get("section");
  const manuscript = manuscriptResponse(study.id, section);
  if (!manuscript) return jsonError(404, section ? "section_not_found" : "manuscript_not_found");

  if ((request.headers.get("accept") ?? "").includes("text/markdown")) {
    return new Response(manuscript.content_markdown, {
      headers: {
        "Content-Type": "text/markdown; charset=utf-8",
        "Cache-Control": "public, max-age=3600",
        Link: `<${study.links.html}>; rel="canonical"`,
      },
    });
  }
  return json(manuscript, 200, "public, max-age=3600");
}
