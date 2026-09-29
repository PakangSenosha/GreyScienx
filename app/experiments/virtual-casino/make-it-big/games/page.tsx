import type { Metadata } from "next";
import { integer, pct } from "@/lib/virtualCasino";
import { makeItBigData } from "@/lib/virtualCasinoMakeItBig";

export const metadata: Metadata = { title: "Games and Rules | Make It Big Study" };

export default function MakeItBigGamesPage() {
  const { games } = makeItBigData;
  return (
    <>
      <section className="vc-page-hero"><p className="vc-kicker">Ruleset registry</p><h1>Four controlled tail models.</h1><p>Every model is explicitly Class C and synthetic. They isolate probability mechanics and are not presented as copies of named commercial products.</p></section>
      <section className="vc-section"><div className="vc-mib-rules">{games.map((game) => <article key={game.id}><header><h2>{game.label}</h2><span>{pct(game.theoreticalRtp, 0)} RTP</span></header><code>{game.rulesVersion}</code><dl><div><dt>Replication class</dt><dd>{game.replicationClass}</dd></div><div><dt>Maximum multiple</dt><dd>{integer(game.maximumMultiplier)}×</dd></div><div><dt>Model</dt><dd>{game.sourceReference}</dd></div><div><dt>Rule type</dt><dd>{game.ruleType === "targetMultiplier" ? "Declared target formula" : "Discrete multiplier table"}</dd></div></dl><p>{game.assumptions}</p>{game.outcomes && <div className="vc-outcome-table"><strong>Published outcome table</strong>{game.outcomes.filter((outcome) => outcome.multiplier > 0).map((outcome) => <span key={outcome.multiplier}>{integer(outcome.multiplier)}× <em>{pct(outcome.probability, 4)}</em></span>)}</div>}</article>)}</div></section>
      <section className="vc-safety-callout"><h2>RTP and target probability are different quantities.</h2><p>RTP averages all gross returns. Target incidence uses only the outcomes large enough to cross R100,000 at the selected stake.</p></section>
    </>
  );
}
