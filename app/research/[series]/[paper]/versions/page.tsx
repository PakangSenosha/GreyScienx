import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { SiteFooter } from "@/components/SiteFooter";
import { SiteHeader } from "@/components/SiteHeader";
import { researchSeries } from "@/lib/catalog";
import { getStudy } from "@/lib/research/registry";

export function generateStaticParams() {
  return researchSeries.flatMap((series) => series.papers.map((paper) => ({ series: series.slug, paper: paper.slug })));
}

export async function generateMetadata({ params }: PageProps<"/research/[series]/[paper]/versions">): Promise<Metadata> {
  const { paper } = await params;
  const study = getStudy(paper);
  return study ? { title: `Version history · ${study.title}` } : {};
}

export default async function VersionsPage({ params }: PageProps<"/research/[series]/[paper]/versions">) {
  const { series, paper } = await params;
  const study = getStudy(paper);
  if (!study || study.series_slug !== series) notFound();
  return (
    <>
      <SiteHeader />
      <main>
        <section className="hero hero-solo article-hero">
          <div className="brand-wave wave-one" aria-hidden="true" />
          <div className="brand-wave wave-two" aria-hidden="true" />
          <div className="hero-copy">
            <p className="eyebrow"><Link href={`/research/${series}/${paper}`}>{study.title}</Link></p>
            <h1>Version history</h1>
            <p className="dek">Immutable public versions and the changes recorded for each release.</p>
          </div>
        </section>
        <section className="page-shell">
          <p className="kicker">Current version · {study.version}</p>
          {study.editorial.change_log.map((change, index) => (
            <article key={`${String(change.version ?? study.version)}-${index}`}>
              <h2>{String(change.version ?? study.version)}</h2>
              <p>{String(change.summary ?? "No change summary is recorded.")}</p>
              <p className="file-meta">{String(change.date ?? study.date_modified)} · {String(change.author ?? "GreyScienx")}</p>
            </article>
          ))}
          <p>Earlier immutable versions: none. This study currently has one published machine-record version.</p>
          <p><a href={`/api/v1/research/${study.slug}/versions`}>Version history JSON</a></p>
        </section>
      </main>
      <SiteFooter />
    </>
  );
}
