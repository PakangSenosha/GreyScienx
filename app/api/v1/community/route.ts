import { communityIndex } from "@/lib/research/community";
import { json, options } from "@/lib/research/http";

export const dynamic = "force-dynamic";

export function OPTIONS() {
  return options();
}

export async function GET() {
  return json(await communityIndex());
}
