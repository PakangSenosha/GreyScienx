import { parentPort, workerData } from "node:worker_threads";
import { simulateWorldSummary } from "../engine/simulate.mjs";

const { config, manifest } = workerData;

parentPort.on("message", (worldIndex) => {
  if (worldIndex === null) return process.exit(0);
  const seed = `${config.replicationSeedPrefix}|${String(worldIndex).padStart(4, "0")}`;
  const players = simulateWorldSummary(config, manifest, seed).map((player) => ({
    playerId: player.playerId,
    cohortId: player.cohortId,
    netPnlCents: player.netPnlCents,
    cumulativeTurnoverCents: player.cumulativeTurnoverCents,
    cumulativePayoutCents: player.cumulativePayoutCents,
    cumulativeExpectedPnlCents: player.cumulativeExpectedPnlCents,
    cumulativeAllocatedCents: player.cumulativeAllocatedCents,
    wagerCount: player.wagerCount,
    ruinCount: player.ruinCount,
    allocationsUsed: player.allocationsUsed,
    status: player.status,
  }));
  parentPort.postMessage({ worldIndex, players });
});
