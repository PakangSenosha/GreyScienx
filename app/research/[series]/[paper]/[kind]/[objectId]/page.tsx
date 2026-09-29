import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { JsonLd } from "@/components/JsonLd";
import { SiteFooter } from "@/components/SiteFooter";
import { SiteHeader } from "@/components/SiteHeader";
import { researchSeries } from "@/lib/catalog";
import { getStudy, getSubobject } from "@/lib/research/registry";
import { site } from "@/lib/site";

const allowed = ["assumptions", "results", "models"] as const;
type Kind = (typeof allowed)[number];

type SubobjectPageProps = {
  params: Promise<{ series: string; paper: string; kind: string; objectId: string }>;
};

type Subobject = {
  id: string;
  local_id: string;
  href: string;
  statement: string;
  name?: string;
  value?: string;
  unit?: string | null;
  sensitivity?: string;
  provenance?: string;
  scenario?: string;
};

export function generateStaticParams() {
  return researchSeries.flatMap((series) =>
    series.papers.flatMap((paper) => {
      const study = getStudy(paper.slug);
      if (!study) return [];
      return allowed.flatMap((kind) =>
        study[kind].map((item) => ({
          series: series.slug,
          paper: paper.slug,
          kind,
          objectId: item.local_id,
        })),
      );
    }),
  );
}

export async function generateMetadata({ params }: SubobjectPageProps): Promise<Metadata> {
  const loaded = await loadRecord(params);
  if (!loaded) return {};
  return {
    title: `${loaded.item.local_id} · ${loaded.study.title}`,
    description: statementFor(loaded.kind, loaded.item),
    alternates: { canonical: loaded.item.href },
  };
}

export default async function SubobjectPage({ params }: SubobjectPageProps) {
  const loaded = await loadRecord(params);
  if (!loaded) notFound();
  const { study, kind, item } = loaded;
  const statement = statementFor(kind, item);
  const claims = study.claims.filter((claim) => {
    if (kind === "assumptions") return claim.depends_on.includes(item.id);
    if (kind === "results") return claim.results.includes(item.id);
    return study.models[0]?.id === item.id;
  });

  return (
    <>
      <JsonLd
        data={{
          "@context": "https://schema.org",
          "@type": "CreativeWork",
          additionalType: labelFor(kind),
          identifier: item.id,
          name: titleFor(kind, item),
          description: statement,
          url: item.href,
          isPartOf: study.links.html,
          publisher: { "@type": "Organization", name: site.name },
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
            <h1>{item.local_id}</h1>
            <p className="dek">{titleFor(kind, item)}</p>
            <p className="file-meta">{item.id} · {labelFor(kind)} · Version {study.version}</p>
          </div>
        </section>

        <section className="article-share-panel" aria-label={`${labelFor(kind)} record`}>
          <div>
            <p className="kicker">Machine-readable statement</p>
            <h2 className="study-question">{statement}</h2>
            {kind === "assumptions" ? (
              <p>Sensitivity: {item.sensitivity}. Provenance: {item.provenance}.</p>
            ) : null}
            {kind === "results" ? <p>Scenario: {item.scenario}. Evidence: modelled.</p> : null}
          </div>
          <div className="machine-links">
            <Link href={`/research/${study.series_slug}/${study.slug}`}>Study page</Link>
            <a href={`/api/v1/research/${study.slug}/${kind}/${item.local_id}`}>JSON record</a>
          </div>
        </section>

        <section className="page-shell">
          <p className="kicker">Connected conditional claims</p>
          {claims.length ? (
            <div className="paper-list">
              {claims.map((claim) => (
                <article className="paper-row" key={claim.id}>
                  <Link
                    className="paper-row-link"
                    href={`/research/${study.series_slug}/${study.slug}/claims/${claim.local_id}`}
                  >
                    <span className="paper-number">{claim.local_id}</span>
                    <span className="paper-copy"><strong>{claim.id}</strong><span>{claim.claim}</span></span>
                    <span className="paper-meta">{claim.sensitivity} sensitivity</span>
                  </Link>
                </article>
              ))}
            </div>
          ) : (
            <p>No claim-level edge is registered for this object.</p>
          )}
        </section>
      </main>
      <SiteFooter />
    </>
  );
}

async function loadRecord(params: SubobjectPageProps["params"]) {
  const { series, paper, kind, objectId } = await params;
  if (!allowed.includes(kind as Kind)) return null;
  const study = getStudy(paper);
  if (!study || study.series_slug !== series) return null;
  const typedKind = kind as Kind;
  const item = getSubobject(study, typedKind, objectId) as Subobject | null;
  return item ? { study, kind: typedKind, item } : null;
}

function labelFor(kind: Kind) {
  if (kind === "assumptions") return "Model assumption";
  if (kind === "results") return "Modelled result";
  return "Model specification";
}

function titleFor(kind: Kind, item: Subobject) {
  if (kind === "assumptions" || kind === "models") return item.name ?? item.local_id;
  return `${item.value ?? ""} ${item.unit ?? ""}`.trim() || item.local_id;
}

function statementFor(_kind: Kind, item: Subobject) {
  return item.statement;
}
