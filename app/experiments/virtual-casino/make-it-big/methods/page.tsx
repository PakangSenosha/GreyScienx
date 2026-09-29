import type { Metadata } from "next";
import { integer, zar } from "@/lib/virtualCasino";
import { makeItBigData } from "@/lib/virtualCasinoMakeItBig";

export const metadata: Metadata = { title: "Methods | Make It Big Study" };

export default function MakeItBigMethodsPage() {
  const { design, metadata } = makeItBigData;
  return (
    <>
      <section className="vc-page-hero"><p className="vc-kicker">Frozen protocol · v{String(metadata.protocolVersion)}</p><h1>Exact probabilities, seeded paths.</h1><p>The primary estimand is analytical. Monte Carlo verifies the implementation and supplies conditional winner-economics summaries.</p></section>
      <section className="vc-section vc-grid-2"><div><p className="vc-kicker">Study design</p><h2>Fixed spend, fixed target</h2><dl className="vc-definition-list"><div><dt>Gross target</dt><dd>{zar(design.targetPayoutCents)}</dd></div><div><dt>Monthly budget</dt><dd>{zar(design.monthlyBudgetCents)}</dd></div><div><dt>Maximum horizon</dt><dd>{design.maximumMonths} months</dd></div><div><dt>Entrants per cell</dt><dd>{integer(design.entrantsPerCell)}</dd></div><div><dt>Cells</dt><dd>4 strategies × 4 games</dd></div></dl></div><div className="vc-replication-card"><p className="vc-kicker">Primary formula</p><h2>1 − (1 − p)ⁿ</h2><p>Cumulative incidence after n independent attempts with per-attempt target probability p.</p><dl><div><dt>Survival</dt><dd>(1 − p)ⁿ</dd></div><div><dt>Target event</dt><dd>First gross payout ≥ R100,000</dd></div><div><dt>Exit rule</dt><dd>Hit or spending horizon</dd></div></dl></div></section>
      <section className="vc-dark-section"><div className="vc-section-head"><div><p className="vc-kicker">Reproducibility</p><h2>One seed, independent streams.</h2></div><p>A geometric first-passage draw compresses redundant non-target wagers without changing the preregistered endpoint.</p></div><dl className="vc-hash-list"><div><dt>Experiment ID</dt><dd><code>{String(metadata.experimentId)}</code></dd></div><div><dt>Configuration hash</dt><dd><code>{String(metadata.configHash)}</code></dd></div><div><dt>Source hash</dt><dd><code>{String(metadata.sourceHash)}</code></dd></div><div><dt>PRNG</dt><dd>{String(metadata.prng)}</dd></div></dl><pre className="vc-command"><code>npm run casino:make-it-big:test{"\n"}npm run casino:make-it-big:generate</code></pre></section>
      <section className="vc-section"><div className="vc-section-head"><div><p className="vc-kicker">Known limits</p><h2>What this model does not establish</h2></div></div><ol className="vc-limitations"><li>Synthetic entrants are not people.</li><li>The four distributions are controlled models, not commercial product estimates.</li><li>Gross target payout is not net profit or wealth.</li><li>Independent wagers omit changing behaviour and voluntary exit.</li><li>RTP does not determine target-hit probability by itself.</li><li>Real-product estimates require verified product-specific paytables.</li></ol></section>
    </>
  );
}
