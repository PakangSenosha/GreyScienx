import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { PaperRow } from "@/components/PaperRow";
import { JsonLd } from "@/components/JsonLd";
import { SiteFooter } from "@/components/SiteFooter";
import { SiteHeader } from "@/components/SiteHeader";
import { getTopicRecord, listTopicRecords } from "@/lib/research/registry";
import { topicJsonLd } from "@/lib/research/jsonld";

type TopicPageProps = {
  params: Promise<{ slug: string }>;
};

export function generateStaticParams() {
  return listTopicRecords().map((topic) => ({ slug: topic.slug }));
}

export async function generateMetadata({ params }: TopicPageProps): Promise<Metadata> {
  const topic = getTopicRecord((await params).slug);
  if (!topic) return {};
  return {
    title: topic.title,
    description: topic.definition,
    alternates: { canonical: topic.links.html },
  };
}

export default async function TopicPage({ params }: TopicPageProps) {
  const topic = getTopicRecord((await params).slug);
  if (!topic) notFound();

  return (
    <>
      <JsonLd data={topicJsonLd(topic)} />
      <SiteHeader />
      <main>
        <section className="hero hero-solo">
          <div className="brand-wave wave-one" aria-hidden="true" />
          <div className="brand-wave wave-two" aria-hidden="true" />
          <div className="hero-copy">
            <p className="eyebrow">
              <Link href="/topics">Topic</Link>
            </p>
            <h1>{topic.title}</h1>
            <p className="dek">{topic.definition}</p>
            <div className="hero-actions">
              <Link className="button button-primary" href="/research">
                All research
              </Link>
            </div>
          </div>
        </section>

        <TopicRecord topic={topic} />

        <section className="series-stack article-related">
          <section className="series-block">
            <header className="series-heading">
              <div>
                <span>{topic.study_count}</span>
                <p>{topic.study_count === 1 ? "study" : "studies"}</p>
              </div>
              <div>
                <h2>Studies</h2>
                <p>The question each study asks, with its stable identifier.</p>
              </div>
            </header>
            <div className="paper-list">
              {topic.studies.map((study) => (
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
          <p className="kicker">Connected topics</p>
          <ul className="topic-links">
            {topic.connected_topics.map((connected) => (
              <li key={connected.slug}>
                <Link href={`/topics/${connected.slug}`}>{connected.title}</Link>
              </li>
            ))}
          </ul>
        </section>
      </main>
      <SiteFooter />
    </>
  );
}

function TopicRecord({ topic }: { topic: NonNullable<ReturnType<typeof getTopicRecord>> }) {
  return (
    <section className="page-shell topic-record">
      <div>
        <p className="kicker">Related questions</p>
        {topic.related_questions.length > 0 ? (
          <ul className="dossier-questions">
            {topic.related_questions.map((question) => (
              <li key={question}>{question}</li>
            ))}
          </ul>
        ) : (
          <p>No related question is registered for this topic.</p>
        )}
      </div>

      <div>
        <p className="kicker">Relevant claims</p>
        {topic.claims.length > 0 ? (
          <ul className="dossier-questions">
            {topic.claims.map((claim) => (
              <li key={claim.id}>
                <strong>{claim.study_id}</strong>
                {": "}
                {claim.claim}
              </li>
            ))}
          </ul>
        ) : (
          <p>No claim has been extracted for this topic.</p>
        )}
      </div>

      <div>
        <p className="kicker">Major assumptions</p>
        {topic.assumptions.length > 0 ? (
          <ul className="dossier-questions">
            {topic.assumptions.map((assumption) => (
              <li key={assumption.id}>
                <strong>{assumption.name}</strong>
                {` · ${assumption.sensitivity} sensitivity · ${assumption.study_id}`}
              </li>
            ))}
          </ul>
        ) : (
          <p>No assumption is registered for this topic.</p>
        )}
      </div>

      <div>
        <p className="kicker">Datasets</p>
        {topic.datasets.length > 0 ? (
          <ul className="dossier-questions">
            {topic.datasets.map((dataset) => (
              <li key={`${dataset.study_id}-${dataset.id}`}>
                <strong>{dataset.title}</strong>
                {` · ${dataset.study_id}`}
              </li>
            ))}
          </ul>
        ) : (
          <p>No dataset is registered for this topic.</p>
        )}
      </div>
    </section>
  );
}
