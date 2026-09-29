import type { Metadata } from "next";

export const metadata: Metadata = { title: "Downloads | Make It Big Study" };

const root = "/experiments/virtual-casino/make-it-big/v1.0";
const groups = [
  { title: "Results", files: [["Cell results", "cell-results.csv", "CSV"], ["Monthly survival curves", "survival.csv", "CSV"], ["Audit entrant sample", "audit-entrants.csv", "CSV"], ["Dashboard snapshot", "dashboard.json", "JSON"]] },
  { title: "Protocol and rules", files: [["Frozen protocol", "protocol-v1.0.json", "JSON"], ["Ruleset registry", "rulesets.json", "JSON"], ["Run metadata", "run-metadata.json", "JSON"], ["Methods", "METHODS.md", "MD"]] },
  { title: "Reproduction source", files: [["Simulation engine", "source/engine-simulate.mjs", "MJS"], ["Artifact generator", "source/scripts-generate-artifacts.mjs", "MJS"], ["Validation tests", "source/tests-simulation.test.mjs", "MJS"], ["Release guide", "README.md", "MD"]] },
] as const;

export default function MakeItBigDownloadsPage() {
  return (
    <>
      <section className="vc-page-hero"><p className="vc-kicker">Make It Big · Reproducibility bundle</p><h1>Download the study.</h1><p>Frozen inputs, aggregate results, survival curves, audit records, executable source, validation tests, and hashes are published as static read-only files.</p></section>
      <section className="vc-section vc-download-groups">{groups.map((group) => <article key={group.title}><h2>{group.title}</h2><div>{group.files.map(([label, file, type]) => <a href={`${root}/${file}`} download key={file}><span><strong>{label}</strong><small>{file}</small></span><em>{type} ↓</em></a>)}</div></article>)}</section>
      <section className="vc-safety-callout"><h2>Verify before analysing.</h2><p>Use <a href={`${root}/checksums.sha256`} download>checksums.sha256</a> to verify every public file. The configuration and source hashes are also printed on the methods page.</p></section>
    </>
  );
}
