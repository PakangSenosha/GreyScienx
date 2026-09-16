import Link from "next/link";
import { SiteFooter } from "@/components/SiteFooter";
import { SiteHeader } from "@/components/SiteHeader";
import { papers, researchSeries } from "@/lib/catalog";

const editorialPrinciples = [
  {
    number: "01",
    title: "Begin with the question",
    body: "Start from a problem worth understanding without forcing it into a disciplinary category first.",
  },
  {
    number: "02",
    title: "Expose the reasoning",
    body: "Make the evidence, assumptions, models, uncertainty and failure conditions visible.",
  },
  {
    number: "03",
    title: "Publish the full record",
    body: "Keep the complete manuscript available as the source of record.",
  },
];

export default function HomePage() {
  return (
    <>
      <SiteHeader />
      <main>
        <section className="hero hero-solo home-hero" id="top">
          <div className="brand-wave wave-one" aria-hidden="true" />
          <div className="brand-wave wave-two" aria-hidden="true" />
          <div className="brand-wave wave-three" aria-hidden="true" />
          <div className="hero-copy">
            <p className="eyebrow">Independent research publication</p>
            <h1>
              Questions worth
              <br />
              <em>modelling.</em>
            </h1>
            <p className="dek">
              GreyScienx publishes readable, model-led research across fields of study. The
              archive preserves complete papers and organises related questions into series.
            </p>
            <div className="hero-actions">
              <Link className="button button-primary" href="/research">
                Browse all research
              </Link>
              <Link className="button button-secondary" href="/about">
                About GreyScienx
              </Link>
            </div>
            <p className="file-meta">Open manuscripts · Transparent assumptions · No field boundary</p>
          </div>
        </section>

        <section className="number-band" aria-label="GreyScienx at a glance">
          <div>
            <strong>{papers.length}</strong>
            <span>published papers</span>
          </div>
          <div>
            <strong>{researchSeries.length}</strong>
            <span>research series</span>
          </div>
          <div>
            <strong>PDF</strong>
            <span>source of record</span>
          </div>
          <div>
            <strong>All</strong>
            <span>fields of study</span>
          </div>
        </section>

        <section className="section-grid" id="research">
          <div className="section-label">
            <span>01</span>
            <p>Research programmes</p>
          </div>
          <div className="hub-copy">
            <p className="kicker">The complete archive</p>
            <h2>Research organised by series.</h2>
            <p>
              Related papers sit together so a reader can follow an argument from its first
              question to its wider system. The archive stays text-led and opens directly into
              the complete manuscripts.
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
                Open the full archive
              </Link>
            </p>
          </div>
        </section>

        <section className="method section-grid programme-section">
          <div className="section-label light">
            <span>02</span>
            <p>Publication model</p>
          </div>
          <div className="method-copy">
            <p className="eyebrow light-text">How the work is built</p>
            <h2>Research without a departmental boundary.</h2>
            <p className="programme-intro">
              The subject can change completely. The discipline of the publication does not:
              frame the question clearly, show how the conclusion was reached and preserve
              enough detail for a critical reader to disagree.
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
            <p>Editorial standard</p>
          </div>
          <div className="hub-copy">
            <p className="kicker">Readable does not mean vague</p>
            <h2>The argument first. The machinery still exposed.</h2>
            <div className="principle-list">
              <article>
                <strong>Accessible, but sourced</strong>
                <p>Write for a serious general reader and connect important claims to evidence.</p>
              </article>
              <article>
                <strong>Models, not oracles</strong>
                <p>Use scenarios to test scale and trade-offs. Resist false precision.</p>
              </article>
              <article>
                <strong>Evidence before decoration</strong>
                <p>Keep the public archive simple and let the manuscript carry the full analysis.</p>
              </article>
              <article>
                <strong>Failure stays visible</strong>
                <p>Limitations, counterarguments and conditions for being wrong remain in the work.</p>
              </article>
            </div>
          </div>
        </section>

        <section className="author-panel publication-panel">
          <div>
            <p className="eyebrow light-text">GreyScienx</p>
            <h2>A home for the work.</h2>
          </div>
          <div>
            <p>
              GreyScienx currently carries its founding body of research. Its structure is
              broader than one person or discipline, so future collaborators can be added
              without changing the publication&apos;s identity.
            </p>
            <div className="hero-actions">
              <Link className="button button-paper" href="/about">
                About the publication
              </Link>
              <Link className="button button-secondary" href="/about/pakang-senosha">
                About the founder
              </Link>
            </div>
          </div>
        </section>
      </main>
      <SiteFooter />
    </>
  );
}
