import { json, jsonError, options, readParam } from "@/lib/research/http";
import { listTopicRecords, getTopicRecord } from "@/lib/research/registry";

export const dynamic = "force-static";

export function generateStaticParams() {
  return listTopicRecords().map((topic) => ({ slug: topic.slug }));
}

export function OPTIONS() {
  return options();
}

export async function GET(_request: Request, context: { params: Promise<Record<string, string>> }) {
  const topic = getTopicRecord(await readParam(context, "slug"));
  if (!topic) return jsonError(404, "not_found");
  return json(topic);
}
