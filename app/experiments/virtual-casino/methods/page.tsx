import Link from "next/link";
import { casinoData, integer } from "@/lib/virtualCasino";

const definitions = [
  ["Handle", "Sum of every accepted stake."],
  ["Player payouts", "Sum of gross amounts returned after settlement."],
  ["GGR", "Handle minus gross payouts; allocation injections are excluded."],
  ["Actual RTP", "Gross payouts divided by handle in the realised ledger."],
  ["Theoretical RTP", "Stake-weighted expected gross payout from each exact wager choice."],
  ["Net P&L", "Current bankroll minus all R10,000 allocations received."],
  ["Ruin", "After settlement, bankroll is below the R1 minimum legal stake."],
  ["Bankroll month", "A numbered allocation episode, separate from calendar month."],
];

export default function MethodsPage() {
  const m = casinoData.metadata;
  return (
    <>
      <section className="vc-page-hero"><p className="vc-kicker">Protocol · Code · Ledger · Replay</p><h1>How the experiment was built and checked</h1><p>The definitions were fixed before the results were interpreted. Any change to a rule, pay table, cohort, bug or displayed definition requires a new version.</p></section>
      <section className="vc-section vc-audit-grid"><article><p className="vc-kicker">Release identity</p><h2>v{String(m.protocolVersion)}</h2><dl className="vc-hash-list"><div><dt>Experiment</dt><dd>{String(m.experimentId)}</dd></div><div><dt>Configuration SHA-256</dt><dd><code>{String(m.configHash)}</code></dd></div><div><dt>Manifest SHA-256</dt><dd><code>{String(m.manifestHash)}</code></dd></div><div><dt>Final ledger hash</dt><dd><code>{String(m.finalEventHash)}</code></dd></div><div><dt>Final state hash</dt><dd><code>{String(m.finalStateHash)}</code></dd></div></dl></article><article><p className="vc-kicker">Seed integrity</p><h2>Committed, then revealed</h2><dl className="vc-hash-list"><div><dt>Commitment</dt><dd><code>{String(m.visibleSeedCommitment)}</code></dd></div><div><dt>Revealed seed</dt><dd><code>{String(m.visibleSeed)}</code></dd></div><div><dt>Status</dt><dd>{String(m.visibleSeedStatus).replaceAll("-", " ")}</dd></div><div><dt>Code revision</dt><dd><code>{String(m.codeRevision)}</code></dd></div></dl></article></section>
      <section className="vc-section"><div className="vc-section-head"><div><p className="vc-kicker">Terms used in the study</p><h2>The definitions stayed fixed</h2></div><p>Every percentage identifies its denominator. Expected values are calculated wager by wager and stored in integer cents.</p></div><dl className="vc-definition-cards">{definitions.map(([term, definition]) => <div key={term}><dt>{term}</dt><dd>{definition}</dd></div>)}</dl></section>
      <section className="vc-dark-section"><div className="vc-section-head"><div><p className="vc-kicker">Questions set in advance</p><h2>Nine hypothesis families</h2></div><p>Exploratory comparisons are identified as such and require confirmation on held-out data.</p></div><ol className="vc-hypotheses">{casinoData.methods.hypotheses.map((hypothesis, index) => <li key={hypothesis}><span>H{index + 1}</span>{hypothesis}</li>)}</ol></section>
      <section className="vc-section vc-grid-2"><div><p className="vc-kicker">Deterministic streams</p><h2>Concurrency cannot alter a draw.</h2><p>Each schedule, game choice, stake variation, bet choice, and game outcome stream is addressed by stable world, player, game, and purpose identifiers. The xoshiro128** generator advances locally; SHA-256 protects commitments, manifests, checkpoints, and ledger integrity.</p><p>Changing a dashboard refresh or worker count therefore cannot shift the sequence used by another player.</p></div><div><p className="vc-kicker">Replay procedure</p><h2>{integer(casinoData.summary.wagers)} settlements rechecked.</h2><pre className="vc-command"><code>npm run casino:test{"\n"}npm run casino:generate{"\n"}npm run casino:replay</code></pre><p>The replay validates sequence and predecessor hashes, duplicate bet IDs, integer stakes, bankroll arithmetic, non-negative balances, allocation caps, final ledger/state hashes, and casino-to-player reconciliation.</p></div></section>
      <section className="vc-section"><div className="vc-section-head"><div><p className="vc-kicker">Limits of the evidence</p><h2>What this model cannot establish</h2></div></div><ol className="vc-limitations">{casinoData.methods.limitations.map((limitation) => <li key={limitation}>{limitation}</li>)}</ol><p className="vc-more"><Link href="/experiments/virtual-casino/house-edge/downloads">Download the protocol, manifest, schema, aggregates, ledger and checksums →</Link></p></section>
    </>
  );
}
