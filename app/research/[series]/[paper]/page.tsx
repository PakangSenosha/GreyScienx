import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { JsonLd } from "@/components/JsonLd";
import { ShareResearch } from "@/components/ShareResearch";
import { StudyDossier } from "@/components/StudyDossier";
import { SiteFooter } from "@/components/SiteFooter";
import { SiteHeader } from "@/components/SiteHeader";
import { getPaper, researchSeries } from "@/lib/catalog";
import { studyJsonLd } from "@/lib/research/jsonld";
import { studyCommunity } from "@/lib/research/community";
import { getStudy, researchTypeLabel } from "@/lib/research/registry";
import { articlePath, articleUrl } from "@/lib/urls";

export const dynamicParams = false;

export function generateStaticParams() {
  return researchSeries.flatMap((series) =>
    series.papers.map((paper) => ({
      series: series.slug,
      paper: paper.slug,
    })),
  );
}

export async function generateMetadata({
  params,
}: PageProps<"/research/[series]/[paper]">): Promise<Metadata> {
  const { series: seriesSlug, paper: paperSlug } = await params;
  const entry = getPaper(seriesSlug, paperSlug);
  if (!entry) return {};

  const url = articleUrl(entry.series, entry.paper);
  const study = getStudy(paperSlug);
  return {
    title: entry.paper.title,
    description: entry.paper.description,
    keywords: study?.keywords,
    alternates: {
      canonical: url,
      types: study
        ? {
            "text/markdown": study.links.markdown,
            "application/json": study.links.json,
          }
        : undefined,
    },
    openGraph: {
      type: "article",
      title: entry.paper.title,
      description: entry.paper.description,
      url,
    },
    twitter: {
      card: "summary",
      title: entry.paper.title,
      description: entry.paper.description,
    },
  };
}

export default async function PaperPage({
  params,
}: PageProps<"/research/[series]/[paper]">) {
  const { series: seriesSlug, paper: paperSlug } = await params;
  const entry = getPaper(seriesSlug, paperSlug);
  if (!entry) notFound();

  const { series, paper } = entry;
  const path = articlePath(series, paper);
  const study = getStudy(paper.slug);
  if (!study || study.series_slug !== series.slug) notFound();
  const related = series.papers.filter((item) => item.slug !== paper.slug);
  const critiques = studyCommunity(study.id, "critiques");
  const forks = studyCommunity(study.id, "forks");
  const revisions = studyCommunity(study.id, "revisions");

  return (
    <>
      <JsonLd data={studyJsonLd(study)} />
      <SiteHeader />
      <main>
        <section className="hero hero-solo article-hero">
          <div className="brand-wave wave-one" aria-hidden="true" />
          <div className="brand-wave wave-two" aria-hidden="true" />
          <div className="hero-copy">
            <p className="eyebrow">
              <Link href={`/series/${series.slug}`}>
                {series.number} · {series.title}
              </Link>
            </p>
            <h1>{paper.title}</h1>
            <p className="dek">{paper.description}</p>
            <div className="hero-actions">
              <a className="button button-primary" href={paper.href} rel="noreferrer" target="_blank">
                Read the manuscript
              </a>
              <Link className="button button-ghost" href="/research">
                All research
              </Link>
            </div>
            <p className="file-meta">
              PDF · {paper.pages} pages · {paper.size} · {series.number}.{paper.number} · {study.id}
            </p>
          </div>
        </section>

        <section className="article-share-panel" aria-label="Study record">
          <div>
            <p className="kicker">Study record · {study.id}</p>
            <h2 className="study-question">{study.primary_question}</h2>
            <p>
              Evidence status: Modelled. {researchTypeLabel(study.research_type)}. Version{" "}
              {study.version}. Peer review: none. The paragraph under the title is the published
              summary.
            </p>
          </div>
          <div className="machine-links">
            <Link href="/standards/mathematical-writing">Mathematical standard</Link>
            <Link href="/community">Community</Link>
          </div>
        </section>

        <StudyDossier study={study} />

        <section className="article-share-panel" aria-label="Community record">
          <div>
            <p className="kicker">Community record · version {study.version}</p>
            <h2>
              Published community record: {critiques.count} critiques, {forks.count} forks, and {revisions.count} revisions.
            </h2>
            <p>
              {study.authors.map((author) => author.name).join(", ")}{" "}
              {study.authors.length === 1 ? "is" : "are"} the author
              {study.authors.length === 1 ? "" : "s"} on this version. External review: none. A
              later critique or revision appears here after a person publishes it.
            </p>
          </div>
          <div className="machine-links">
            {study.authors.map((author) => (
              <Link key={author.slug} href={`/about/${author.slug}`}>
                {author.name}
              </Link>
            ))}
          </div>
        </section>

        <section className="article-share-panel" aria-label="Shareable link">
          <div>
            <p className="kicker">Share this article</p>
            <h2>A permanent link to the work.</h2>
            <p>
              Use this page when citing or sharing the study. The PDF contains the complete
              analysis.
            </p>
          </div>
          <ShareResearch href={path} title={paper.title} showUrl />
        </section>

        {related.length > 0 ? (
          <section className="series-stack article-related">
            <section className="series-block">
              <header className="series-heading">
                <div>
                  <span>{series.number}</span>
                  <p>More in this series</p>
                </div>
                <div>
                  <h2>
                    <Link href={`/series/${series.slug}`}>{series.title}</Link>
                  </h2>
                  <p>{series.description}</p>
                </div>
              </header>
              <div className="paper-list">
                {related.map((item) => (
                  <article className="paper-row" key={item.slug}>
                    <Link className="paper-row-link" href={articlePath(series, item)}>
                      <span className="paper-number">{series.number}.{item.number}</span>
                      <span className="paper-copy">
                        <strong>{item.title}</strong>
                        <span>{item.description}</span>
                      </span>
                      <span className="paper-meta">{item.pages} pages · {item.size}</span>
                    </Link>
                    <ShareResearch href={articlePath(series, item)} title={item.title} />
                  </article>
                ))}
              </div>
            </section>
          </section>
        ) : null}
      </main>
      <SiteFooter />
    </>
  );
}
