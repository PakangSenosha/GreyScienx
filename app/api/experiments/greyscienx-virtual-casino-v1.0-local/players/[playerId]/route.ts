import { casinoPlayers } from "@/lib/virtualCasino";

export const dynamic = "force-static";

export function generateStaticParams() {
  return [...casinoPlayers.keys()].map((playerId) => ({ playerId }));
}

export async function GET(_request: Request, context: RouteContext<"/api/experiments/greyscienx-virtual-casino-v1.0-local/players/[playerId]">) {
  const { playerId } = await context.params;
  const player = casinoPlayers.get(playerId.toUpperCase());
  if (!player) return Response.json({ error: "Unknown synthetic player" }, { status: 404, headers: { "X-Robots-Tag": "noindex, nofollow, noarchive" } });
  return Response.json(player, { headers: { "Cache-Control": "public, max-age=3600, immutable", "X-Experiment-Mode": "synthetic-read-only", "X-Robots-Tag": "noindex, nofollow, noarchive" } });
}
