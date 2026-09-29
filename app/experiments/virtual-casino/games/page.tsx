import { casinoData, integer, pct, zar } from "@/lib/virtualCasino";

export default function GamesPage() {
  const moderate = casinoData.games.find((game) => game.id === "three_reel_slot")!;
  const high = casinoData.games.find((game) => game.id === "high_volatility_slot")!;
  return (
    <>
      <section className="vc-page-hero"><p className="vc-kicker">Ten games · Rules and returns published</p><h1>Inside the game models</h1><p>Each model publishes its rule, wager-specific expected return, realised return and role in the experiment.</p></section>
      <section className="vc-section vc-slot-comparison"><div><p className="vc-kicker">A controlled comparison</p><h2>The same expected return.<br/>A different ride.</h2><p>Both slot models return exactly 96 percent in expectation. The moderate model spreads payouts across more outcomes; the high-volatility model concentrates them in a 137× tail.</p></div><div className="vc-slot-card"><span>MODERATE</span><strong>96.00%</strong><small>theoretical RTP</small><dl><div><dt>Visible RTP</dt><dd>{pct(moderate.actualRtp)}</dd></div><div><dt>Wagers</dt><dd>{integer(moderate.wagerCount)}</dd></div><div><dt>Maximum payout</dt><dd>31× gross</dd></div></dl></div><div className="vc-slot-card vc-slot-card-high"><span>VERY HIGH</span><strong>96.00%</strong><small>theoretical RTP</small><dl><div><dt>Visible RTP</dt><dd>{pct(high.actualRtp)}</dd></div><div><dt>Wagers</dt><dd>{integer(high.wagerCount)}</dd></div><div><dt>Maximum payout</dt><dd>137× gross</dd></div></dl></div></section>
      <section className="vc-section"><div className="vc-game-grid">{casinoData.games.map((game, index) => <article className="vc-game-card" key={game.id}><header><span>{String(index + 1).padStart(2, "0")}</span><div><h2>{game.label}</h2><code>{game.ruleVersion}</code></div></header><div className="vc-game-numbers"><p><span>Visible RTP</span><strong>{pct(game.actualRtp)}</strong></p><p><span>Weighted theoretical</span><strong>{pct(game.theoreticalRtp)}</strong></p><p><span>Turnover</span><strong>{zar(game.turnoverCents, true)}</strong></p><p><span>Wagers</span><strong>{integer(game.wagerCount)}</strong></p></div><p className="vc-rule-note">{game.choices[0].ruleNote}</p><div className="vc-choice-list">{game.choices.map((choice) => <p key={choice.choice}><span>{choice.choice.replaceAll("_", " ")}</span><strong>RTP {pct(choice.theoreticalRtp)} · edge {pct(choice.houseEdge)}</strong></p>)}</div></article>)}</div></section>
      <section className="vc-safety-callout"><h2>These results do not identify a strategy.</h2><p>The figures describe expected values inside a synthetic protocol. They are not gambling advice, operator comparisons or instructions for play.</p></section>
    </>
  );
}
