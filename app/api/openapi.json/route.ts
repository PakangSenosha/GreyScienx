import { json, options } from "@/lib/research/http";
import { openApiDocument } from "@/lib/research/openapi";

export const dynamic = "force-static";

export function OPTIONS() {
  return options();
}

export function GET() {
  return json(openApiDocument());
}
