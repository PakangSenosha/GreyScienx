import { json, options } from "@/lib/research/http";
import { researchGraph } from "@/lib/research/graph";

export function OPTIONS() {
  return options();
}

export function GET() {
  return json(researchGraph());
}
