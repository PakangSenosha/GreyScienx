import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { PaperRow } from "@/components/PaperRow";
import { JsonLd } from "@/components/JsonLd";
import { SiteFooter } from "@/components/SiteFooter";
import { SiteHeader } from "@/components/SiteHeader";
import { researchSeries } from "@/lib/catalog";
import { seriesContext } from "@/lib/research/packages";
import { seriesJsonLd } from "@/lib/research/jsonld";
import { getSeriesRecord, getTopicRecord } from "@/lib/research/registry";

type SeriesPageProps = {
  params: Promise<{ slug: string }>;
};

export function generateStaticParams() {
  return researchSeries.map((series) => ({ slug: series.slug }));
}

export async function generateMetadata({ params }: SeriesPageProps): Promise<Metadata> {
  const series = getSeriesRecord((await params).slug);
  if (!series) return {};
  return {
    title: series.title,
    description: series.question,
    alternates: { canonical: series.links.html },
  };
}

export default async function SeriesPage({ params }: SeriesPageProps) {
  const series = getSeriesRecord((await params).slug);
  if (!series) notFound();
  const topics = series.topics
    .map((slug) => getTopicRecord(slug))
    .filter((topic) => topic !== null);
  const context = seriesContext(series.slug);

  return (
    <>
      <JsonLd data={seriesJsonLd(series)} />
      <SiteHeader />
      <main>
        <section className="hero hero-solo">
          <div className="brand-wave wave-one" aria-hidden="true" />
          <div className="brand-wave wave-two" aria-hidden="true" />
          <div className="hero-copy">
            <p className="eyebrow">
              <Link href="/series">Series {series.number}</Link>
            </p>
            <h1>{series.title}</h1>
            <p className="dek">{series.question}</p>
            <p className="file-meta">
              {series.study_count} studies · {series.geographies.join(", ")}
            </p>
            <div className="hero-actions">
              <Link className="button button-primary" href="/research">
                All research
              </Link>
            </div>
          </div>
        </section>

        <section className="series-stack article-related">
          <section className="series-block">
            <header className="series-heading">
              <div>
                <span>{series.number}</span>
                <p>Studies</p>
              </div>
              <div>
                <h2>Constituent studies</h2>
                <p>Each study keeps its own identifier, question, and manuscript.</p>
              </div>
            </header>
            <div className="paper-list">
              {series.studies.map((study) => (
                <PaperRow
                  key={study.id}
                  number={study.id}
                  title={study.title}
                  description={study.primary_question}
                  href={`/research/${study.series_slug}/${study.slug}`}
                  meta="Modelled"
                />
              ))}
            </div>
          </section>
        </section>

        <section className="page-shell">
          <p className="kicker">Shared record</p>
          <h2>Assumptions, models, and open questions</h2>
          {context.repeated_assumptions.length > 0 ? (
            <p>
              Assumption names used by more than one study:{" "}
              {context.repeated_assumptions.map((item) => item.name).join("; ")}.
            </p>
          ) : (
            <p>No assumption name is registered on more than one study in this series.</p>
          )}
          {context.shared_assumptions.map((note) => (
            <p key={note}>{note}</p>
          ))}
          {context.shared_models.map((note) => (
            <p key={note}>{note}</p>
          ))}
          {context.shared_datasets.map((note) => (
            <p key={note}>{note}</p>
          ))}
          <p>
            Published contradictions: {context.contradictions.length}. Published qualifying links:{" "}
            {context.qualifications.length}.
          </p>
        </section>

        {context.unresolved_questions.length > 0 ? (
          <section className="page-shell">
            <p className="kicker">Unresolved questions</p>
            <ul className="dossier-questions">
              {context.unresolved_questions.map((question) => (
                <li key={question}>{question}</li>
              ))}
            </ul>
          </section>
        ) : null}

        {topics.length > 0 ? (
          <section className="page-shell">
            <p className="kicker">Topics in this series</p>
            <ul className="topic-links">
              {topics.map((topic) => (
                <li key={topic.slug}>
                  <Link href={`/topics/${topic.slug}`}>{topic.title}</Link>
                </li>
              ))}
            </ul>
          </section>
        ) : null}
      </main>
      <SiteFooter />
    </>
  );
}
