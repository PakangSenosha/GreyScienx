import { json, options } from "@/lib/research/http";
import { listSeriesRecords } from "@/lib/research/registry";

export const dynamic = "force-static";

export function OPTIONS() {
  return options();
}

export function GET() {
  return json({ series: listSeriesRecords() });
}
