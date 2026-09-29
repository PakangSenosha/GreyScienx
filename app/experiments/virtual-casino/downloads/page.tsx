import { casinoData } from "@/lib/virtualCasino";
import { casinoDownloadGroups } from "@/lib/virtualCasinoDownloads";

const root = "/experiments/virtual-casino/v1.0";

export default function DownloadsPage() {
  return (
    <>
      <section className="vc-page-hero"><p className="vc-kicker">Research files · v{String(casinoData.metadata.protocolVersion)}</p><h1>Download the record</h1><p>The fixed inputs, aggregate results, compressed ledger, audit metadata and documentation are published as read-only files.</p></section>
      <section className="vc-section vc-download-groups">{casinoDownloadGroups.map((group) => <article key={group.title}><h2>{group.title}</h2><div>{group.files.map(({ label, file, type }) => <a href={`${root}/${file}`} download key={file}><span><strong>{label}</strong><small>{file}</small></span><em>{type} ↓</em></a>)}</div></article>)}</section>
      <section className="vc-safety-callout"><h2>Verify the files before using them.</h2><p>Use <code>checksums.sha256</code> to check each public file. The replay procedure reconstructs the visible world from the revealed seed and compares the final event and state hashes.</p></section>
    </>
  );
}
