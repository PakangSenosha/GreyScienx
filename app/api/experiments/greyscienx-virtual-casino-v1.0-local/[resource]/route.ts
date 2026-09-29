import { casinoData } from "@/lib/virtualCasino";
import { casinoDownloadFiles } from "@/lib/virtualCasinoDownloads";

export const dynamic = "force-static";

export function generateStaticParams() {
  return ["summary", "timeseries", "players", "cohorts", "games", "worlds", "methods", "downloads"].map((resource) => ({ resource }));
}

export async function GET(_request: Request, context: RouteContext<"/api/experiments/greyscienx-virtual-casino-v1.0-local/[resource]">) {
  const { resource } = await context.params;
  const resources: Record<string, unknown> = {
    summary: { metadata: casinoData.metadata, summary: casinoData.summary, distribution: casinoData.distribution },
    timeseries: casinoData.timeseries,
    players: casinoData.players,
    cohorts: casinoData.cohorts,
    games: casinoData.games,
    worlds: casinoData.replication,
    methods: casinoData.methods,
    downloads: casinoDownloadFiles.map((file) => ({ file, url: `/experiments/virtual-casino/v1.0/${file}` })),
  };
  if (!(resource in resources)) return Response.json({ error: "Unknown read-only resource" }, { status: 404 });
  return Response.json(resources[resource], { headers: { "Cache-Control": "public, max-age=3600, immutable", "X-Experiment-Mode": "synthetic-read-only" } });
}
