import { casinoData } from "@/lib/virtualCasino";
import { Histogram } from "../_components/Charts";
import { PlayerTable } from "../_components/Metrics";

export default function PlayersPage() {
  const players = [...casinoData.players].sort((a, b) => a.rank - b.rank);
  return (
    <>
      <section className="vc-page-hero"><p className="vc-kicker">The complete population · 1,000 of 1,000 policies</p><h1>Every player, not only the winners</h1><p>The table includes all policies, including those that reached the allocation cap. No result was removed because it was inactive or unremarkable.</p></section>
      <section className="vc-section"><Histogram bins={casinoData.distribution.histogram} label="Allocation-adjusted final P&L" description="Bars encode losses and gains independently of colour; the table below is the complete text alternative." /></section>
      <section className="vc-section vc-section-tight"><PlayerTable players={players} caption="All 1,000 synthetic policies ordered by visible-world lifetime allocation-adjusted P&L" /></section>
    </>
  );
}
