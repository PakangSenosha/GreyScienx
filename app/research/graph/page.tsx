import type { Metadata } from "next";
import Link from "next/link";
import { SiteFooter } from "@/components/SiteFooter";
import { SiteHeader } from "@/components/SiteHeader";
import { graphSummary } from "@/lib/research/graph";
import { researchObjects } from "@/lib/research/registry";
import { agentOnlyRobots } from "@/lib/research/visibility";

export const metadata: Metadata = {
  title: "Research graph",
  description: "How GreyScienx studies, claims, assumptions, results, and models connect.",
  robots: agentOnlyRobots,
};

export default function ResearchGraphPage() {
  const summary = graphSummary();
  const predicates = Object.entries(summary.predicates).sort((a, b) => b[1] - a[1]);

  return (
    <>
      <SiteHeader />
      <main>
        <section className="hero hero-solo">
          <div className="brand-wave wave-one" aria-hidden="true" />
          <div className="brand-wave wave-two" aria-hidden="true" />
          <div className="hero-copy">
            <p className="eyebrow">
              <Link href="/research">Research</Link>
            </p>
            <h1>
              Research
              <br />
              <em>graph.</em>
            </h1>
            <p className="dek">
              Claims depend on assumptions, cite modelled results, and belong to a study. Studies
              belong to a series.
            </p>
            <div className="hero-actions">
              <a className="button button-primary" href="/api/v1/graph">
                Graph JSON
              </a>
              <a className="button button-secondary" href="/feed.xml">
                Study feed
              </a>
            </div>
          </div>
        </section>

        <section className="number-band" aria-label="Graph summary">
          <div>
            <strong>{summary.study_count}</strong>
            <span>studies</span>
          </div>
          <div>
            <strong>{summary.edge_count}</strong>
            <span>edges</span>
          </div>
          <div>
            <strong>{predicates.length}</strong>
            <span>predicates</span>
          </div>
          <div>
            <strong>Read-only</strong>
            <span>no hosted model</span>
          </div>
        </section>

        <section className="page-shell">
          <p className="kicker">Predicates</p>
          <ul className="topic-links">
            {predicates.map(([predicate, count]) => (
              <li key={predicate}>
                <span>
                  {predicate} · {count}
                </span>
              </li>
            ))}
          </ul>
        </section>

        <div className="series-stack">
          {researchObjects.map((study) => (
            <section className="series-block" key={study.id}>
              <header className="series-heading">
                <div>
                  <span>{study.claims.length}</span>
                  <p>{study.claims.length === 1 ? "claim" : "claims"}</p>
                </div>
                <div>
                  <h2>
                    <Link href={`/research/${study.series_slug}/${study.slug}`}>{study.title}</Link>
                  </h2>
                  <p>
                    {study.id}. {study.primary_question}
                  </p>
                </div>
                <p className="series-count">
                  <a href={`/api/v1/research/${study.slug}/graph`}>Study graph</a>
                </p>
              </header>
            </section>
          ))}
        </div>
      </main>
      <SiteFooter />
    </>
  );
}
