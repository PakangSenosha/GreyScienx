import type { Metadata } from "next";
import Link from "next/link";

import { integer, pct, zar } from "@/lib/virtualCasino";
import { makeItBigCell, makeItBigData } from "@/lib/virtualCasinoMakeItBig";
import { Metric } from "../_components/Metrics";

export const metadata: Metadata = {
  title: "Make It Big Study | Virtual Casino Experiment",
  description: "A reproducible study of the chance of a synthetic R100,000 gross payout before fixed R12,000 and R36,000 spending limits.",
};

const studyPages = [
  ["Results", "All 16 cells, exact probabilities, simulation checks and cost-per-winner estimates.", "/experiments/virtual-casino/make-it-big/results", "01"],
  ["Strategies", "Four ways to divide the same R1,000 monthly budget—and why stake size changes the target.", "/experiments/virtual-casino/make-it-big/strategies", "02"],
  ["Games", "Published outcome distributions, tail mechanics and replication classes for every synthetic game.", "/experiments/virtual-casino/make-it-big/games", "03"],
  ["Survival", "First-passage curves, time to target and the probability of reaching each spending cap without a hit.", "/experiments/virtual-casino/make-it-big/survival", "04"],
  ["Methods", "Frozen protocol, exact formula, seed, code hash, limitations and commands needed to reproduce the study.", "/experiments/virtual-casino/make-it-big/methods", "05"],
  ["Downloads", "Cell results, survival curves, audit sample, rulesets, protocol, dashboard snapshot and checksums.", "/experiments/virtual-casino/make-it-big/downloads", "06"],
  ["Safety", "What this synthetic experiment can establish—and what it cannot say about real-world gambling.", "/experiments/virtual-casino/make-it-big/safety", "07"],
] as const;

export default function MakeItBigPage() {
  const { design, summary, metadata } = makeItBigData;
  const slotLarge = makeItBigCell("jackpot_slot", "stake_50");
  const slotSmall = makeItBigCell("jackpot_slot", "stake_5");
  const lotteryLarge = makeItBigCell("lottery_tail", "stake_50");
  const lotterySmall = makeItBigCell("lottery_tail", "stake_5");
  const crashLarge = makeItBigCell("crash_target", "stake_50");
  const crashSmall = makeItBigCell("crash_target", "stake_5");

  return (
    <>
      <section className="vc-page-hero vc-mib-hero">
        <p className="vc-kicker">Experiment 02 · Protocol v{String(metadata.protocolVersion)}</p>
        <h1>What are the odds that R1,000 a month produces a <em>R100,000</em> payout?</h1>
        <p>Sixteen controlled cells measure the first target hit before R12,000 and R36,000 is spent. Exact probabilities are reported alongside 1.6 million seeded entrant paths.</p>
      </section>

      <section className="vc-definition-strip" aria-label="Make It Big study definitions">
        <p><strong>Target</strong><span>One gross payout ≥ R100,000</span></p>
        <p><strong>Monthly cap</strong><span>R1,000 in every strategy</span></p>
        <p><strong>Horizons</strong><span>12 and 36 months</span></p>
        <p><strong>Games</strong><span>Four published Class C models</span></p>
      </section>

      <section className="vc-section">
        <div className="vc-section-head"><div><p className="vc-kicker">The scale of the study</p><h2>The event is rare.<br />The denominator remains visible.</h2></div><p>Every percentage uses {integer(design.entrantsPerCell)} independent synthetic entrants in each game-strategy cell. A hit ends the entrant&apos;s path; otherwise it continues to the spending cap.</p></div>
        <div className="vc-metric-grid vc-metric-grid-primary">
          <Metric label="Experimental cells" value={integer(summary.experimentalCells)} note="4 games × 4 strategies" />
          <Metric label="Entrant paths" value={integer(summary.totalEntrantRuns)} note={`${integer(summary.entrantsPerCell)} per cell`} />
          <Metric label="Gross target" value={zar(design.targetPayoutCents)} note="Not the same as net wealth" />
          <Metric label="Largest MC deviation" value={`${summary.maximumAbsoluteSimulationErrorPercentagePoints.toFixed(3)} pp`} strong note="Versus exact probability" />
        </div>
      </section>

      <section className="vc-dark-section">
        <div className="vc-section-head"><div><p className="vc-kicker">The main finding</p><h2>More attempts did not always improve the odds.</h2></div><p>The monthly budget stayed fixed. The stake, number of attempts and payout multiple needed to reach R100,000 changed.</p></div>
        <div className="vc-mib-findings">
          <article><span>JACKPOT SLOT</span><strong>{pct(slotLarge.exactProbability36Months, 2)} → {pct(slotSmall.exactProbability36Months, 2)}</strong><p>Moving from 20 × R50 to 200 × R5 reduces three-year incidence because the smaller stake needs a much rarer multiplier.</p></article>
          <article><span>LOTTERY TAIL</span><strong>{pct(lotteryLarge.exactProbability36Months, 2)} → {pct(lotterySmall.exactProbability36Months, 2)}</strong><p>The same move increases incidence because every ticket shares one sufficiently large tail outcome and the smaller stake creates more attempts.</p></article>
          <article><span>CONSTANT EDGE</span><strong>{pct(crashLarge.exactProbability36Months, 2)} ≈ {pct(crashSmall.exactProbability36Months, 2)}</strong><p>The crash-target model makes probability approximately proportional to stake, so fixed spend nearly equalises the four strategies.</p></article>
        </div>
      </section>

      <section className="vc-section">
        <div className="vc-section-head"><div><p className="vc-kicker">The complete study</p><h2>Follow the evidence from result to reproduction.</h2></div><p>The overview is only the entry point. Every result, model, method and downloadable artifact has its own permanent page.</p></div>
        <div className="vc-subpage-grid">
          {studyPages.map(([label, description, href, number]) => (
            <Link href={href} key={href}>
              <span>{number}</span>
              <h3>{label}</h3>
              <p>{description}</p>
              <strong>Open section →</strong>
            </Link>
          ))}
        </div>
      </section>

      <section className="vc-safety-callout">
        <p className="vc-kicker">What the result does not mean</p><h2>A large payout is not a recommendation.</h2><p>The study uses fictional money, synthetic entrants and controlled probability laws. It does not identify a game to play, estimate an undisclosed commercial product or imply that a target hit is likely, repeatable or profitable after spending.</p>
        <p className="vc-more"><Link href="/experiments/virtual-casino/make-it-big/safety">Read the complete safety statement →</Link></p>
      </section>
    </>
  );
}
