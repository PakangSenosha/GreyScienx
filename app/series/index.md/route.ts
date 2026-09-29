import { markdownHeaders, seriesIndexMarkdown } from "@/lib/research/markdown";

export const dynamic = "force-static";

export function GET() {
  return new Response(seriesIndexMarkdown(), { headers: markdownHeaders });
}
