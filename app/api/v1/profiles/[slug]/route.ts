import { getProfile, listProfiles } from "@/lib/research/community";
import { json, jsonError, options, readParam } from "@/lib/research/http";

export const dynamic = "force-static";

export function generateStaticParams() {
  return listProfiles().map((profile) => ({ slug: profile.slug }));
}

export function OPTIONS() {
  return options();
}

export async function GET(_request: Request, context: { params: Promise<Record<string, string>> }) {
  const profile = getProfile(await readParam(context, "slug"));
  if (!profile) return jsonError(404, "not_found");
  return json(profile);
}
