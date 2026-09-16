import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { ShareResearch } from "@/components/ShareResearch";
import { SiteFooter } from "@/components/SiteFooter";
import { SiteHeader } from "@/components/SiteHeader";
import { getPaper, researchSeries } from "@/lib/catalog";
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
  return {
    title: entry.paper.title,
    description: entry.paper.description,
    alternates: { canonical: url },
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
  const related = series.papers.filter((item) => item.slug !== paper.slug);

  return (
    <>
      <SiteHeader />
      <main>
        <section className="hero hero-solo article-hero">
          <div className="brand-wave wave-one" aria-hidden="true" />
          <div className="brand-wave wave-two" aria-hidden="true" />
          <div className="hero-copy">
            <p className="eyebrow">
              <Link href={`/research#${series.slug}`}>
                {series.number} · {series.title}
              </Link>
            </p>
            <h1>{paper.title}</h1>
            <p className="dek">{paper.description}</p>
            <div className="hero-actions">
              <a className="button button-primary" href={paper.href} rel="noreferrer" target="_blank">
                Open manuscript
              </a>
              <Link className="button button-ghost" href="/research">
                Full archive
              </Link>
            </div>
            <p className="file-meta">
              PDF · {paper.pages} pages · {paper.size} · {series.number}.{paper.number}
            </p>
          </div>
        </section>

        <section className="article-share-panel" aria-label="Shareable link">
          <div>
            <p className="kicker">Share this paper</p>
            <h2>A stable public URL.</h2>
            <p>
              This page is the shareable record for the article. The PDF remains the complete
              manuscript.
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
                  <p>Same series</p>
                </div>
                <div>
                  <h2>{series.title}</h2>
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
