import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { JsonLd } from "@/components/JsonLd";
import { SiteFooter } from "@/components/SiteFooter";
import { SiteHeader } from "@/components/SiteHeader";
import { getPaper, researchSeries } from "@/lib/catalog";
import { getStudy } from "@/lib/research/registry";
import { site } from "@/lib/site";

type ClaimPageProps = {
  params: Promise<{ series: string; paper: string; claimId: string }>;
};

export function generateStaticParams() {
  return researchSeries.flatMap((series) =>
    series.papers.flatMap((paper) => {
      const study = getStudy(paper.slug);
      if (!study || study.series_slug !== series.slug) return [];
      return study.claims.map((claim) => ({
        series: series.slug,
        paper: paper.slug,
        claimId: claim.local_id,
      }));
    }),
  );
}

export async function generateMetadata({ params }: ClaimPageProps): Promise<Metadata> {
  const claim = await loadClaim(params);
  if (!claim) return {};
  return {
    title: `${claim.claim.local_id} · ${claim.study.title}`,
    description: claim.claim.claim,
    alternates: { canonical: claim.claim.href },
  };
}

export default async function ClaimPage({ params }: ClaimPageProps) {
  const loaded = await loadClaim(params);
  if (!loaded) notFound();
  const { study, claim } = loaded;
  const assumptions = study.assumptions.filter((item) => claim.depends_on.includes(item.id));
  const results = study.results.filter((item) => claim.results.includes(item.id));
  const sources = study.sources.filter((item) => claim.supported_by.includes(item.id));

  return (
    <>
      <JsonLd
        data={{
          "@context": "https://schema.org",
          "@type": "Claim",
          text: claim.claim,
          identifier: claim.id,
          url: claim.href,
          isPartOf: study.links.html,
          author: { "@type": "Organization", name: site.name },
        }}
      />
      <SiteHeader />
      <main>
        <section className="hero hero-solo article-hero">
          <div className="brand-wave wave-one" aria-hidden="true" />
          <div className="brand-wave wave-two" aria-hidden="true" />
          <div className="hero-copy">
            <p className="eyebrow">
              <Link href={`/research/${study.series_slug}/${study.slug}`}>{study.title}</Link>
            </p>
            <h1>{claim.local_id}</h1>
            <p className="dek">{claim.claim}</p>
            <p className="file-meta">
              {claim.id} · Modelled · Conditional · {claim.sensitivity} sensitivity · Version{" "}
              {claim.version}
            </p>
          </div>
        </section>

        <section className="article-share-panel" aria-label="Claim status">
          <div>
            <p className="kicker">Main limitation</p>
            <h2 className="study-question">{claim.main_limitation}</h2>
          </div>
          <div className="machine-links">
            <Link href={`/research/${study.series_slug}/${study.slug}`}>Study page</Link>
            <a href={`/api/v1/research/${study.slug}/claims/${claim.local_id}`}>Claim JSON</a>
            <a href={`/api/v1/research/${study.slug}`}>Study JSON</a>
          </div>
        </section>

        <section className="page-shell">
          <p className="kicker">Depends on</p>
          <div className="paper-list">
            {assumptions.map((assumption) => (
              <article className="paper-row" key={assumption.id}>
                <Link className="paper-row-link" href={`/research/${study.series_slug}/${study.slug}/assumptions/${assumption.local_id}`}>
                  <span className="paper-number">{assumption.local_id}</span>
                  <span className="paper-copy">
                    <strong>{assumption.name}</strong>
                    <span>{assumption.statement}</span>
                  </span>
                  <span className="paper-meta">{assumption.sensitivity} sensitivity</span>
                </Link>
              </article>
            ))}
          </div>
        </section>

        <section className="page-shell">
          <p className="kicker">Modelled results cited</p>
          <div className="paper-list">
            {results.map((result) => (
              <article className="paper-row" key={result.id}>
                <Link className="paper-row-link" href={`/research/${study.series_slug}/${study.slug}/results/${result.local_id}`}>
                  <span className="paper-number">{result.local_id}</span>
                  <span className="paper-copy">
                    <strong>{result.scenario}</strong>
                    <span>{result.statement}</span>
                  </span>
                  <span className="paper-meta">{result.evidence_status}</span>
                </Link>
              </article>
            ))}
          </div>
        </section>

        <section className="page-shell">
          <p className="kicker">Registered supporting sources</p>
          {sources.length ? (
            <ul className="dossier-questions">
              {sources.map((source) => (
                <li key={source.id}>
                  {source.href ? <a href={source.href}>{source.title}</a> : source.title}
                  {` · ${source.id}`}
                </li>
              ))}
            </ul>
          ) : (
            <p>No claim-level source assignment is registered.</p>
          )}
        </section>
      </main>
      <SiteFooter />
    </>
  );
}

async function loadClaim(params: ClaimPageProps["params"]) {
  const { series, paper, claimId } = await params;
  const entry = getPaper(series, paper);
  const study = getStudy(paper);
  if (!entry || !study || study.series_slug !== series) return null;
  const claim = study.claims.find((item) => item.local_id.toLowerCase() === claimId.toLowerCase());
  if (!claim) return null;
  return { study, claim };
}
