import { casinoData, integer, pct, zar } from "@/lib/virtualCasino";
import { Histogram } from "../_components/Charts";
import { Metric } from "../_components/Metrics";

export default function WorldsPage() {
  const counts = casinoData.replication.profitablePlayerCounts;
  const sorted = [...counts].sort((a, b) => a - b);
  const medianAhead = sorted[Math.floor(sorted.length / 2)];
  return (
    <>
      <section className="vc-page-hero"><p className="vc-kicker">The policies stayed fixed · chance changed</p><h1>What happened in 1,000 other worlds</h1><p>An apparent star may simply have received an extreme draw. Replication shows the full range of each policy&apos;s results instead of treating one rank as proof of skill.</p></section>
      <section className="vc-section"><div className="vc-metric-grid vc-metric-grid-primary"><Metric label="Completed worlds" value={integer(casinoData.replication.completedWorlds)} note="Independent recorded seeds" /><Metric label="Visible house-result percentile" value={pct(casinoData.replication.visibleWorldPercentile, 1)} note="Among replication-world GGR" /><Metric label="Median policies ahead" value={`${medianAhead} / 1,000`} note={pct(medianAhead / 1000, 1)} /><Metric label="Policy manifest" value="Fixed" note="Only declared stochastic choices and outcomes change" /></div></section>
      <section className="vc-section vc-grid-2"><div><p className="vc-kicker">Across all worlds</p><h2>The final house result</h2><Histogram bins={casinoData.replication.ggrDistribution} label="House result across replication worlds" description="Each bar is a completed six-month world with the same 1,000 policy definitions." /></div><div className="vc-replication-explainer"><p className="vc-kicker">Why replication matters</p><h2>A single winner makes an easy story.</h2><p>Among 1,000 policies, someone will look exceptional. The experiment does not infer ability from that maximum. It compares the visible result with the same policy&apos;s range, chance of profit, risk of ruin and median rank under new seeds.</p><ol><li>Hold policy and game definitions constant.</li><li>Generate an independent world stream.</li><li>Repeat the six-month schedule.</li><li>Report distributions rather than a selected world.</li></ol></div></section>
      <section className="vc-dark-section"><div className="vc-section-head"><div><p className="vc-kicker">The groups across worlds</p><h2>How cohort medians moved</h2></div><p>These ranges show how each cohort&apos;s median P&amp;L changed across 1,000 complete worlds.</p></div><div className="vc-world-cohorts">{casinoData.cohorts.map((cohort) => <article key={cohort.id}><h3>{cohort.label}</h3><strong>{zar(cohort.replication.medianOfWorldMedianPnlCents)}</strong><p>5th–95th world range<br/>{zar(cohort.replication.p05WorldMedianPnlCents)} to {zar(cohort.replication.p95WorldMedianPnlCents)}</p><small>Median ruin rate {pct(cohort.replication.medianRuinRate, 1)}</small></article>)}</div></section>
    </>
  );
}
