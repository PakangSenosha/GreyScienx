import { casinoData } from "@/lib/virtualCasino";

export const dynamic = "force-static";

export function GET() {
  return Response.json({
    experimentId: casinoData.metadata.experimentId,
    version: casinoData.metadata.protocolVersion,
    status: casinoData.metadata.status,
    syntheticOnly: true,
    publicWriteEndpoints: false,
    summaryUrl: `/api/experiments/${casinoData.metadata.experimentId}/summary`,
  }, { headers: { "Cache-Control": "public, max-age=3600, immutable" } });
}
