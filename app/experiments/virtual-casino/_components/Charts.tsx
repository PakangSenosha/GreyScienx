import { zar } from "@/lib/virtualCasino";

export function LineChart({
  values,
  label,
  description,
  tone = "coral",
}: {
  values: number[];
  label: string;
  description: string;
  tone?: "coral" | "ink" | "green";
}) {
  const width = 760;
  const height = 240;
  const min = Math.min(0, ...values);
  const max = Math.max(1, ...values);
  const span = max - min || 1;
  const points = values.map((value, index) => `${(index / Math.max(1, values.length - 1)) * width},${height - ((value - min) / span) * height}`).join(" ");
  const zeroY = height - ((0 - min) / span) * height;
  return (
    <figure className="vc-chart">
      <svg viewBox={`0 0 ${width} ${height}`} role="img" aria-labelledby={`${label.replaceAll(" ", "-")}-title ${label.replaceAll(" ", "-")}-desc`}>
        <title id={`${label.replaceAll(" ", "-")}-title`}>{label}</title>
        <desc id={`${label.replaceAll(" ", "-")}-desc`}>{description}</desc>
        <line className="vc-chart-grid" x1="0" x2={width} y1={zeroY} y2={zeroY} />
        <polyline className={`vc-line vc-line-${tone}`} points={points} />
      </svg>
      <figcaption>{description}</figcaption>
    </figure>
  );
}

export function Histogram({
  bins,
  label,
  description,
}: {
  bins: { lowerCents: number; upperCents: number; count: number }[];
  label: string;
  description: string;
}) {
  const max = Math.max(...bins.map((bin) => bin.count), 1);
  return (
    <figure className="vc-chart vc-histogram">
      <div className="vc-bars" role="img" aria-label={`${label}. ${description}`}>
        {bins.map((bin) => (
          <span
            className={bin.upperCents < 0 ? "vc-bar vc-bar-loss" : bin.lowerCents > 0 ? "vc-bar vc-bar-gain" : "vc-bar vc-bar-zero"}
            key={`${bin.lowerCents}-${bin.upperCents}`}
            style={{ height: `${Math.max(2, (bin.count / max) * 100)}%` }}
            title={`${zar(bin.lowerCents)} to ${zar(bin.upperCents)}: ${bin.count} observations`}
          />
        ))}
      </div>
      <div className="vc-axis"><span>{zar(bins[0].lowerCents, true)}</span><span>Final P&amp;L</span><span>{zar(bins.at(-1)!.upperCents, true)}</span></div>
      <figcaption><strong>{label}.</strong> {description}</figcaption>
    </figure>
  );
}
