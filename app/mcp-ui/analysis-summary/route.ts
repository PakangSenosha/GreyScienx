import { analysisSummaryResource, buildAnalysisSummaryPayload } from "@/lib/research/conversational-ui";
import { getStudy } from "@/lib/research/registry";

export function GET(request: Request) {
  const url = new URL(request.url);
  const studyId = url.searchParams.get("study_id") ?? "GSX:POP-001";
  const claimId = url.searchParams.get("claim_id") ?? undefined;
  const study = getStudy(studyId);

  if (!study) {
    return new Response("No GreyScienx study matches the requested preview.", {
      status: 404,
      headers: {
        "Content-Type": "text/plain; charset=utf-8",
        "Cache-Control": "no-store",
        "X-Robots-Tag": "noindex, nofollow, noarchive",
      },
    });
  }

  try {
    const payload = buildAnalysisSummaryPayload(study, claimId);
    const resource = analysisSummaryResource(payload);
    return new Response(resource.text, {
      headers: {
        "Content-Type": "text/html; charset=utf-8",
        "Cache-Control": "no-store",
        "Content-Security-Policy":
          "default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; connect-src 'none'; img-src data:; base-uri 'none'; form-action 'none'",
        "X-Content-Type-Options": "nosniff",
        "X-Robots-Tag": "noindex, nofollow, noarchive",
      },
    });
  } catch (error) {
    const message = error instanceof Error ? error.message : "The preview could not be created.";
    return new Response(message, {
      status: 400,
      headers: {
        "Content-Type": "text/plain; charset=utf-8",
        "Cache-Control": "no-store",
        "X-Robots-Tag": "noindex, nofollow, noarchive",
      },
    });
  }
}
