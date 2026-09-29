import { notFound } from "next/navigation";
import Link from "next/link";
import { casinoData, casinoPlayers, gameLabel, integer, pct, zar } from "@/lib/virtualCasino";
import { LineChart } from "../../../_components/Charts";
import { Metric } from "../../../_components/Metrics";

export function generateStaticParams() {
  return casinoData.players.map((player) => ({ playerId: player.playerId }));
}

export default async function PlayerPage({ params }: PageProps<"/experiments/virtual-casino/house-edge/players/[playerId]">) {
  const { playerId } = await params;
  const player = casinoPlayers.get(playerId.toUpperCase());
  if (!player) notFound();
  const gameMix = Object.entries(player.gameStats).sort((a, b) => b[1].turnoverCents - a[1].turnoverCents);
  const typical = player.netPnlCents >= player.replication.p05PnlCents && player.netPnlCents <= player.replication.p95PnlCents;
  return (
    <>
      <section className="vc-page-hero vc-player-hero"><div><p className="vc-kicker">Synthetic policy · visible-world rank #{player.rank} of 1,000</p><h1>{player.playerId}</h1><p>{player.policy.cohortLabel}. The visible result sits at the {pct(player.replication.visiblePercentileWithinPolicy, 1)} percentile of this policy&apos;s 1,000 replicated outcomes.</p></div><div className="vc-status-stamp"><span>VISIBLE RESULT</span><strong>{typical ? "Within the 5–95% range" : "Tail result"}</strong><small>Not evidence of a repeatable advantage</small></div></section>
      <section className="vc-section"><div className="vc-metric-grid vc-metric-grid-primary"><Metric label="Current bankroll" value={zar(player.currentBankrollCents)} /><Metric label="Total allocated" value={zar(player.cumulativeAllocatedCents)} note={`${player.allocationsUsed} / 6 allocations`} /><Metric label="Observed lifetime P&L" value={zar(player.netPnlCents)} strong /><Metric label="Expected P&L given wagers" value={zar(player.cumulativeExpectedPnlCents)} note={`Deviation ${zar(player.deviationFromExpectationCents)}`} /></div></section>
      <section className="vc-section vc-grid-2"><div><p className="vc-kicker">The six-month record</p><h2>Profit and loss over time</h2><LineChart values={player.monthlyHistory.map((row) => row.netPnlCents)} label={`${player.playerId} cumulative P&L by calendar month`} description={`Month-six visible P&L ${zar(player.netPnlCents)}. Bankroll allocations used: ${player.allocationsUsed}.`} /></div><div className="vc-replication-card"><p className="vc-kicker">The same policy under new random paths</p><h2>{zar(player.replication.medianPnlCents)}</h2><p>Median final P&amp;L across worlds</p><dl><div><dt>5th–95th percentile</dt><dd>{zar(player.replication.p05PnlCents)} to {zar(player.replication.p95PnlCents)}</dd></div><div><dt>Finished ahead</dt><dd>{integer(Math.round(player.replication.probabilityAhead * 1000))} / 1,000 ({pct(player.replication.probabilityAhead, 1)})</dd></div><div><dt>At least one ruin</dt><dd>{integer(Math.round(player.replication.probabilityRuin * 1000))} / 1,000 ({pct(player.replication.probabilityRuin, 1)})</dd></div><div><dt>Median rank</dt><dd>#{integer(player.replication.medianRank)} / 1,000</dd></div></dl></div></section>
      <section className="vc-section vc-grid-2"><div><p className="vc-kicker">The fixed behaviour</p><h2>Policy settings</h2><dl className="vc-definition-list"><div><dt>Base stake</dt><dd>{pct(player.policy.baseStakeFraction, 2)} of bankroll</dd></div><div><dt>Sessions / week</dt><dd>{player.policy.sessionsPerWeek}</dd></div><div><dt>Mean bets / session</dt><dd>{player.policy.betsPerSessionMean}</dd></div><div><dt>Loss multiplier</dt><dd>{player.policy.lossResponse.stakeMultiplierAfterLoss}×, capped at {player.policy.lossResponse.maximumConsecutiveEscalations} escalations</dd></div><div><dt>Stop loss / win</dt><dd>{pct(player.policy.stopLossFractionOfSessionStart, 1)} / {pct(player.policy.stopWinFractionOfSessionStart, 1)} of session-start bankroll</dd></div></dl></div><div><p className="vc-kicker">The recorded exposure</p><h2>Where the money was wagered</h2><div className="vc-stack-list">{gameMix.map(([id, row]) => <div key={id}><span>{gameLabel(id)}</span><strong>{zar(row.turnoverCents)}</strong><small>{integer(row.wagerCount)} wagers · RTP {pct(row.turnoverCents ? row.payoutCents / row.turnoverCents : 0)}</small></div>)}</div></div></section>
      <section className="vc-safety-callout"><h2>What this profile can — and cannot — show</h2><p>A smaller loss is not a profit, and a high rank does not prove skill. Behaviour changes both the wagers selected and the amount of exposure. “Expected” and “luck” are descriptive components, not a perfect causal separation.</p><Link href="/experiments/virtual-casino/house-edge/players">← Return to all 1,000 policies</Link></section>
    </>
  );
}
