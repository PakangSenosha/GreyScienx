import { casinoData, integer, pct, zar } from "@/lib/virtualCasino";

export default function CohortsPage() {
  return (
    <>
      <section className="vc-page-hero"><p className="vc-kicker">Ten groups · 100 policies each</p><h1>How the policy groups compared</h1><p>These are modelled policy families, not descriptions or diagnoses of people. Unless stated otherwise, the comparison reflects both behaviour and the exposure it produced.</p></section>
      <section className="vc-section">
        <div className="vc-table-wrap"><table className="vc-table vc-cohort-table"><caption>Visible-world and across-world cohort outcomes, retaining all 100 policies per cohort</caption><thead><tr><th scope="col">Cohort</th><th scope="col">Median P&amp;L</th><th scope="col">5th–95th percentile</th><th scope="col">Finished ahead</th><th scope="col">Ruin</th><th scope="col">Turnover</th><th scope="col">Across-world median</th></tr></thead><tbody>{casinoData.cohorts.map((cohort) => <tr key={cohort.id}><th scope="row"><span className="vc-cohort-index">{String(casinoData.cohorts.indexOf(cohort) + 1).padStart(2, "0")}</span>{cohort.label}<small>{integer(cohort.players)} / 100 policies</small></th><td className={cohort.medianPnlCents >= 0 ? "vc-positive" : "vc-negative"}>{zar(cohort.medianPnlCents)}</td><td>{zar(cohort.p05PnlCents)} to {zar(cohort.p95PnlCents)}</td><td>{integer(Math.round(cohort.probabilityAhead * 100))} / 100 ({pct(cohort.probabilityAhead, 1)})</td><td>{integer(Math.round(cohort.ruinRate * 100))} / 100 ({pct(cohort.ruinRate, 1)})</td><td>{zar(cohort.turnoverCents, true)}</td><td>{zar(cohort.replication.medianOfWorldMedianPnlCents)}<small>{zar(cohort.replication.p05WorldMedianPnlCents)} to {zar(cohort.replication.p95WorldMedianPnlCents)} world range</small></td></tr>)}</tbody></table></div>
      </section>
      <section className="vc-section vc-note-grid"><article><span>01</span><h2>Losing less is not the same as winning.</h2><p>A group may lose less simply because it wagers less. Stops alter exposure and timing; they do not make a negative-expectation wager profitable.</p></article><article><span>02</span><h2>The rankings did not hold.</h2><p>Across-world results keep each policy fixed while changing chance. They provide the needed context for an apparently exceptional cohort.</p></article><article><span>03</span><h2>Every policy remains counted.</h2><p>Each rate uses all 100 policies. Capped or inactive policies stay in the denominator.</p></article></section>
    </>
  );
}
