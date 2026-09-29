import type { Metadata } from "next";
import { integer, pct, zar } from "@/lib/virtualCasino";
import { makeItBigData } from "@/lib/virtualCasinoMakeItBig";

export const metadata: Metadata = { title: "Strategies | Make It Big Study" };

export default function MakeItBigStrategiesPage() {
  const { design, games, cells } = makeItBigData;
  return (
    <>
      <section className="vc-page-hero"><p className="vc-kicker">Fixed-budget comparison</p><h1>Same R1,000.<br/>Different paths.</h1><p>Stake size changes the number of attempts and the payout multiple required to reach the same R100,000 gross target.</p></section>
      <section className="vc-section"><div className="vc-mib-strategies">{design.strategies.map((strategy, index) => <article key={strategy.id}><span>{String(index + 1).padStart(2, "0")}</span><h2>{strategy.label}</h2><dl><div><dt>Stake</dt><dd>{zar(strategy.stakeCents)}</dd></div><div><dt>Bets / month</dt><dd>{integer(strategy.betsPerMonth)}</dd></div><div><dt>Maximum 36-month bets</dt><dd>{integer(strategy.betsPerMonth * 36)}</dd></div><div><dt>Required payout multiple</dt><dd>{integer(design.targetPayoutCents / strategy.stakeCents)}×</dd></div></dl></article>)}</div></section>
      <section className="vc-dark-section"><div className="vc-section-head"><div><p className="vc-kicker">Three-year exact incidence</p><h2>The direction changes by game.</h2></div><p>No stake-frequency rule is universally better. The prize distribution determines whether more lower-stake attempts expose more or less target-eligible probability.</p></div><div className="vc-table-wrap"><table className="vc-table"><caption>Exact probability of the target by 36 months under each strategy</caption><thead><tr><th scope="col">Strategy</th>{games.map((game) => <th scope="col" key={game.id}>{game.label}</th>)}</tr></thead><tbody>{design.strategies.map((strategy) => <tr key={strategy.id}><th scope="row">{strategy.label}</th>{games.map((game) => { const cell = cells.find((candidate) => candidate.gameId === game.id && candidate.strategyId === strategy.id)!; return <td key={game.id}>{pct(cell.exactProbability36Months, 2)}</td>; })}</tr>)}</tbody></table></div></section>
      <section className="vc-safety-callout"><h2>This is a comparison of probability structures.</h2><p>Strategy labels describe experimental arms. They are not recommendations, optimisation advice, or evidence that a betting system changes a negative expected return.</p></section>
    </>
  );
}
