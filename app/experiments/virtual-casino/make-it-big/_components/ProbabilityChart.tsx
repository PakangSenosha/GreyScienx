import { pct } from "@/lib/virtualCasino";
import { makeItBigData } from "@/lib/virtualCasinoMakeItBig";

const lineColours = ["#f26157", "#72d2b3", "#91b7d9", "#f2d45c"];

export function ProbabilityChart({ gameId }: { gameId: string }) {
  const width = 760;
  const height = 250;
  const series = makeItBigData.design.strategies.map((strategy) => ({
    strategy,
    values: makeItBigData.survival.filter((row) => row.gameId === gameId && row.strategyId === strategy.id),
  }));
  const max = Math.max(...series.flatMap((item) => item.values.map((row) => row.exactCumulativeIncidence)), 0.01);
  const game = makeItBigData.games.find((candidate) => candidate.id === gameId)!;
  return (
    <figure className="vc-chart vc-incidence-chart">
      <svg viewBox={`0 0 ${width} ${height}`} role="img" aria-labelledby={`${gameId}-chart-title ${gameId}-chart-desc`}>
        <title id={`${gameId}-chart-title`}>{`${game.label} target-hit probability by month`}</title>
        <desc id={`${gameId}-chart-desc`}>Exact cumulative incidence for all four fixed monthly budget strategies over 36 months.</desc>
        {[0, 0.5, 1].map((fraction) => <line className="vc-chart-grid" x1="0" x2={width} y1={height * fraction} y2={height * fraction} key={fraction} />)}
        {series.map((item, index) => {
          const points = item.values.map((row) => `${(row.month / 36) * width},${height - (row.exactCumulativeIncidence / max) * height}`).join(" ");
          return <polyline key={item.strategy.id} points={points} fill="none" stroke={lineColours[index]} strokeWidth="4" vectorEffect="non-scaling-stroke" />;
        })}
      </svg>
      <div className="vc-chart-legend">{series.map((item, index) => <span key={item.strategy.id}><i style={{ background: lineColours[index] }} />{item.strategy.label}</span>)}</div>
      <figcaption><strong>{game.label}.</strong> Vertical scale reaches {pct(max, 1)}; horizontal scale is 0–36 months.</figcaption>
    </figure>
  );
}
