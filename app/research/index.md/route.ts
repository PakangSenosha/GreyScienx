import { markdownHeaders, researchIndexMarkdown } from "@/lib/research/markdown";

export const dynamic = "force-static";

export function GET() {
  return new Response(researchIndexMarkdown(), { headers: markdownHeaders });
}
