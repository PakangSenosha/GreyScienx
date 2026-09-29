import Link from "next/link";
import type { CasinoPlayer } from "@/lib/virtualCasino";
import { integer, pct, zar } from "@/lib/virtualCasino";

export function Metric({ label, value, note, strong = false }: { label: string; value: string; note?: string; strong?: boolean }) {
  return <article className={`vc-metric${strong ? " vc-metric-strong" : ""}`}><p>{label}</p><strong>{value}</strong>{note && <small>{note}</small>}</article>;
}

export function PlayerTable({ players, caption }: { players: CasinoPlayer[]; caption: string }) {
  return (
    <div className="vc-table-wrap">
      <table className="vc-table">
        <caption>{caption}</caption>
        <thead><tr><th scope="col">Rank / policy</th><th scope="col">Cohort</th><th scope="col">Observed P&amp;L</th><th scope="col">Expected P&amp;L</th><th scope="col">Across-world median</th><th scope="col">Ahead across worlds</th><th scope="col">Wagers</th></tr></thead>
        <tbody>
          {players.map((player) => (
            <tr key={player.playerId}>
              <th scope="row"><span className="vc-rank">#{player.rank}</span><Link href={`/experiments/virtual-casino/house-edge/players/${player.playerId}`}>{player.playerId}</Link></th>
              <td>{player.policy.cohortLabel}</td>
              <td className={player.netPnlCents >= 0 ? "vc-positive" : "vc-negative"}>{zar(player.netPnlCents)}</td>
              <td>{zar(player.cumulativeExpectedPnlCents)}</td>
              <td>{zar(player.replication.medianPnlCents)}</td>
              <td>{integer(Math.round(player.replication.probabilityAhead * 1000))} / 1,000 ({pct(player.replication.probabilityAhead, 1)})</td>
              <td>{integer(player.wagerCount)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
