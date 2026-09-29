import { markdownHeaders, standardMarkdown } from "@/lib/research/markdown";
import { site } from "@/lib/site";

export const dynamic = "force-static";

export function GET() {
  return new Response(standardMarkdown(), {
    headers: {
      ...markdownHeaders,
      Link: `<https://${site.domain}/standards/mathematical-writing>; rel="canonical"`,
    },
  });
}
