import { listProfiles } from "@/lib/research/community";
import { json, options } from "@/lib/research/http";

export const dynamic = "force-static";

export function OPTIONS() {
  return options();
}

export function GET() {
  const profiles = listProfiles();
  return json({
    schema_version: "GreyCommunity 1.0",
    count: profiles.length,
    profiles,
  });
}
