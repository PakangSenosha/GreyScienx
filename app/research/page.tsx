import type { Metadata } from "next";
import { SiteFooter } from "@/components/SiteFooter";
import { SiteHeader } from "@/components/SiteHeader";
import { papers, researchSeries } from "@/lib/catalog";

export const metadata: Metadata = {
  title: "Research archive",
  description: "The complete GreyScienx research archive, organised by series.",
};

export default function ResearchPage() {
  return (
    <>
      <SiteHeader />
      <main>
        <section className="hero hero-solo archive-hero">
          <div className="brand-wave wave-one" aria-hidden="true" />
          <div className="brand-wave wave-two" aria-hidden="true" />
          <div className="hero-copy">
            <p className="eyebrow">Research archive</p>
            <h1>
              The work,
              <br />
              <em>by series.</em>
            </h1>
            <p className="dek">
              Browse complete manuscripts organised into connected research series. Choose a
              paper to open the full publication.
            </p>
          </div>
        </section>

        <section className="number-band" aria-label="Research archive summary">
          <div>
            <strong>{papers.length}</strong>
            <span>papers</span>
          </div>
          <div>
            <strong>{researchSeries.length}</strong>
            <span>research series</span>
          </div>
          <div>
            <strong>PDF</strong>
            <span>complete record</span>
          </div>
          <div>
            <strong>Open</strong>
            <span>read & download</span>
          </div>
        </section>

        <nav className="series-index" aria-label="Research series">
          {researchSeries.map((series) => (
            <a href={`#${series.slug}`} key={series.slug}>
              <span>{series.number}</span>
              {series.title}
            </a>
          ))}
        </nav>

        <div className="series-stack">
          {researchSeries.map((series) => (
            <section className="series-block" id={series.slug} key={series.slug}>
              <header className="series-heading">
                <div>
                  <span>{series.number}</span>
                  <p>Research series</p>
                </div>
                <div>
                  <h2>{series.title}</h2>
                  <p>{series.description}</p>
                </div>
                <p className="series-count">{series.papers.length} {series.papers.length === 1 ? "paper" : "papers"}</p>
              </header>

              <div className="paper-list">
                {series.papers.map((paper) => (
                  <a
                    className="paper-row"
                    href={paper.href}
                    key={paper.slug}
                    rel="noreferrer"
                    target="_blank"
                  >
                    <span className="paper-number">{series.number}.{paper.number}</span>
                    <span className="paper-copy">
                      <strong>{paper.title}</strong>
                      <span>{paper.description}</span>
                    </span>
                    <span className="paper-meta">PDF · {paper.pages} pages · {paper.size} ↗</span>
                  </a>
                ))}
              </div>
            </section>
          ))}
        </div>
      </main>
      <SiteFooter />
    </>
  );
}
