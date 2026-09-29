import type { Metadata } from "next";
import { pct, zar } from "@/lib/virtualCasino";
import { makeItBigData } from "@/lib/virtualCasinoMakeItBig";
import { ProbabilityChart } from "../_components/ProbabilityChart";

export const metadata: Metadata = { title: "Survival Analysis | Make It Big Study" };

export default function MakeItBigSurvivalPage() {
  const { games, cells } = makeItBigData;
  return (
    <>
      <section className="vc-page-hero"><p className="vc-kicker">First-passage and competing horizons</p><h1>Time until target—or spending cap.</h1><p>Survival is the probability that no R100,000-or-larger gross payout has occurred by a given month. Cumulative incidence is one minus survival.</p></section>
      <section className="vc-section"><dl className="vc-definition-cards"><div><dt>T</dt><dd>Number of months until the first target payout.</dd></div><div><dt>S(t)</dt><dd>Probability that the target has not been reached by month t.</dd></div><div><dt>1 − S(t)</dt><dd>Cumulative incidence of at least one target hit.</dd></div><div><dt>Competing horizon</dt><dd>R12,000 at month 12 or R36,000 at month 36 without a target.</dd></div></dl></section>
      <section className="vc-section vc-mib-chart-grid">{games.map((game) => <div key={game.id}><p className="vc-kicker">{pct(game.theoreticalRtp, 0)} theoretical RTP</p><h2>{game.label}</h2><ProbabilityChart gameId={game.id} /></div>)}</section>
      <section className="vc-dark-section"><div className="vc-section-head"><div><p className="vc-kicker">Winner timing and cost</p><h2>Conditional summaries</h2></div><p>Median timing is calculated among observed winners only. Population spend per winner retains all unsuccessful entrant paths in the denominator.</p></div><div className="vc-table-wrap"><table className="vc-table"><caption>Seeded winner timing and population cost by cell</caption><thead><tr><th scope="col">Game</th><th scope="col">Strategy</th><th scope="col">Median months</th><th scope="col">Median spend before hit</th><th scope="col">36-month no-hit</th><th scope="col">Population spend / winner</th></tr></thead><tbody>{cells.map((cell) => <tr key={`${cell.gameId}-${cell.strategyId}`}><th scope="row">{cell.gameLabel}</th><td>{cell.strategyLabel}</td><td>{cell.medianMonthsBeforeWin?.toFixed(1) ?? "—"}</td><td>{cell.medianSpendBeforeWinCents === null ? "—" : zar(cell.medianSpendBeforeWinCents)}</td><td>{pct(1 - cell.exactProbability36Months, 2)}</td><td>{cell.spendPerWinnerCents === null ? "—" : zar(cell.spendPerWinnerCents)}</td></tr>)}</tbody></table></div></section>
    </>
  );
}
