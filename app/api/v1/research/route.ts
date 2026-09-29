import { SCHEMA_VERSION } from "@/lib/research/constants";
import { json, options } from "@/lib/research/http";
import { researchObjects, studySummary } from "@/lib/research/registry";

export const dynamic = "force-static";

export function OPTIONS() {
  return options();
}

export function GET() {
  return json({
    schema_version: SCHEMA_VERSION,
    count: researchObjects.length,
    studies: researchObjects.map(studySummary),
  });
}
