import Link from "next/link";
import type { Metadata } from "next";
import { JsonLd } from "@/components/JsonLd";
import { SiteFooter } from "@/components/SiteFooter";
import { SiteHeader } from "@/components/SiteHeader";
import { papers, researchSeries } from "@/lib/catalog";
import { site } from "@/lib/site";

const canonical = `https://${site.domain}`;

export const metadata: Metadata = {
  alternates: {
    canonical,
    types: {
      "application/rss+xml": `${canonical}/feed.xml`,
      "text/plain": `${canonical}/llms.txt`,
    },
  },
};

const editorialPrinciples = [
  {
    number: "01",
    title: "Start with the question",
    body: "Let the problem determine the method, rather than forcing it into a disciplinary category.",
  },
  {
    number: "02",
    title: "Show the reasoning",
    body: "State the evidence, assumptions, uncertainty and conditions under which the conclusion could fail.",
  },
  {
    number: "03",
    title: "Keep the full record",
    body: "Publish the complete manuscript so readers can inspect the argument for themselves.",
  },
];

export default function HomePage() {
  return (
    <>
      <JsonLd
        data={{
          "@context": "https://schema.org",
          "@type": "WebSite",
          name: site.name,
          url: canonical,
          description: site.description,
          publisher: {
            "@type": "Organization",
            name: site.name,
            url: canonical,
          },
          potentialAction: {
            "@type": "SearchAction",
            target: `${canonical}/api/v1/search?q={search_term_string}`,
            "query-input": "required name=search_term_string",
          },
        }}
      />
      <SiteHeader />
      <main>
        <section className="hero hero-solo home-hero" id="top">
          <div className="brand-wave wave-one" aria-hidden="true" />
          <div className="brand-wave wave-two" aria-hidden="true" />
          <div className="brand-wave wave-three" aria-hidden="true" />
          <div className="hero-copy">
            <p className="eyebrow">Independent research</p>
            <h1>
              Ideas examined
              <br />
              <em>in full.</em>
            </h1>
            <p className="dek">
              GreyScienx publishes original analysis for general readers. Each study states
              its assumptions, weighs uncertainty and links to the complete paper.
            </p>
            <div className="hero-actions">
              <Link className="button button-primary" href="/research">
                Read the research
              </Link>
              <Link className="button button-secondary" href="/about">
                About the publication
              </Link>
            </div>
            <p className="file-meta">Original analysis · Visible methods · Complete manuscripts</p>
          </div>
        </section>

        <section className="number-band" aria-label="GreyScienx at a glance">
          <div>
            <strong>{papers.length}</strong>
            <span>published studies</span>
          </div>
          <div>
            <strong>{researchSeries.length}</strong>
            <span>series</span>
          </div>
          <div>
            <strong>PDF</strong>
            <span>full manuscripts</span>
          </div>
          <div>
            <strong>All</strong>
            <span>subjects</span>
          </div>
        </section>

        <section className="section-grid" id="research">
          <div className="section-label">
            <span>01</span>
            <p>The archive</p>
          </div>
          <div className="hub-copy">
            <p className="kicker">Follow the inquiry</p>
            <h2>Research, arranged by series.</h2>
            <p>
              Each series follows a question across several papers. Readers can begin with the
              overview, trace the argument and open every manuscript in full.
            </p>
            <div className="series-card-grid">
              {researchSeries.map((series) => (
                <Link className="series-card" href={`/research#${series.slug}`} key={series.slug}>
                  <span>{series.number}</span>
                  <h3>{series.title}</h3>
                  <p>{series.description}</p>
                  <small>{series.papers.length} {series.papers.length === 1 ? "paper" : "papers"}</small>
                </Link>
              ))}
            </div>
            <p className="archive-link">
              <Link className="button button-ghost" href="/research">
                View all research
              </Link>
            </p>
          </div>
        </section>

        <section className="method section-grid programme-section">
          <div className="section-label light">
            <span>02</span>
            <p>How we work</p>
          </div>
          <div className="method-copy">
            <p className="eyebrow light-text">The reporting method</p>
            <h2>The question leads. The evidence decides.</h2>
            <p className="programme-intro">
              The subject may change. The standard does not: define the question, explain how
              the answer was reached and give readers enough evidence to disagree.
            </p>
            <div className="theme-grid">
              {editorialPrinciples.map((item) => (
                <article key={item.number}>
                  <span>{item.number}</span>
                  <h3>{item.title}</h3>
                  <p>{item.body}</p>
                </article>
              ))}
            </div>
          </div>
        </section>

        <section className="section-grid principles-section">
          <div className="section-label">
            <span>03</span>
            <p>Editorial standards</p>
          </div>
          <div className="hub-copy">
            <p className="kicker">Clarity without shortcuts</p>
            <h2>Plain language. Visible methods.</h2>
            <div className="principle-list">
              <article>
                <strong>Written for readers</strong>
                <p>Explain the argument in plain language and connect consequential claims to evidence.</p>
              </article>
              <article>
                <strong>Models have limits</strong>
                <p>Use scenarios to test scale and trade-offs without presenting estimates as forecasts.</p>
              </article>
              <article>
                <strong>Evidence before display</strong>
                <p>Use design to clarify the work, never to substitute for it.</p>
              </article>
              <article>
                <strong>Doubt belongs in the story</strong>
                <p>Keep limitations, counterarguments and the conditions for being wrong in view.</p>
              </article>
            </div>
          </div>
        </section>

        <section className="author-panel publication-panel">
          <div>
            <p className="eyebrow light-text">GreyScienx</p>
            <h2>A publication built to grow.</h2>
          </div>
          <div>
            <p>
              GreyScienx begins with a founding collection by Pakang Senosha. Its editorial
              structure is designed to accommodate new subjects and, in time, new contributors.
            </p>
            <div className="hero-actions">
              <Link className="button button-paper" href="/about">
                How GreyScienx works
              </Link>
              <Link className="button button-secondary" href="/about/pakang-senosha">
                Meet the founder
              </Link>
            </div>
          </div>
        </section>
      </main>
      <SiteFooter />
    </>
  );
}
