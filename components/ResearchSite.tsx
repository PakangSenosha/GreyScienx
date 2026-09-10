import { Brand } from "./Brand";
import { PaperCover } from "./PaperCover";
import { SiteFooter } from "./SiteFooter";
import { paperHostPath, researcherPath } from "@/lib/urls";
import type { ResearchPaper, Researcher } from "@/lib/types";

type ResearchSiteProps = {
  paper: ResearchPaper;
  researcher: Researcher;
  preview?: boolean;
};

export function ResearchSite({
  paper,
  researcher,
  preview = false,
}: ResearchSiteProps) {
  const home = researcherPath(researcher);
  const pdfName = paper.pdf.filename;

  return (
    <>
      <a className="skip-link" href="#main">
        Skip to content
      </a>

      <header className="site-header">
        <Brand href="/" division={researcher.givenName} />
        <nav aria-label="Primary navigation">
          <a href="#results">Results</a>
          <a href="#findings">Findings</a>
          <a href="#method">Method</a>
          <a
            className="nav-download"
            href={paper.pdf.href}
            download={pdfName}
          >
            Download PDF
          </a>
        </nav>
      </header>

      <main id="main">
        {preview ? (
          <p className="preview-banner">
            Distillation preview · not yet published to {paperHostPath(researcher, paper)}
          </p>
        ) : null}

        <section className="hero" id="top">
          <div className="brand-wave wave-one" aria-hidden="true" />
          <div className="brand-wave wave-two" aria-hidden="true" />
          <div className="brand-wave wave-three" aria-hidden="true" />
          <div className="hero-copy">
            <p className="eyebrow">
              {researcher.name} · {paper.protocol}
            </p>
            <h1>
              {paper.title}
              <br />
              <em>{paper.titleAccent}</em>
            </h1>
            <p className="dek">{paper.dek}</p>
            <div className="hero-actions">
              <a className="button button-primary" href={paper.pdf.href} download={pdfName}>
                <span>Download the research</span>
                <span aria-hidden="true">↓</span>
              </a>
              <a
                className="button button-secondary"
                href={paper.pdf.href}
                target="_blank"
                rel="noopener"
              >
                Read in browser
              </a>
            </div>
            <p className="file-meta">
              PDF · {paper.pdf.pages} pages · {paper.pdf.size} · Original manuscript
            </p>
          </div>

          <div className="paper-stage" aria-label="Preview of the research paper">
            <div className="paper-shadow" aria-hidden="true" />
            <a
              href={paper.pdf.href}
              target="_blank"
              rel="noopener"
              className="paper-preview"
            >
              <PaperCover paper={paper} researcher={researcher} />
            </a>
            <span className="page-chip">{paper.pdf.pages} pages</span>
          </div>
        </section>

        <section className="number-band" aria-label="Research scope">
          {paper.stats.map((stat) => (
            <div key={stat.label}>
              <strong>{stat.value}</strong>
              <span>{stat.label}</span>
            </div>
          ))}
        </section>

        <section className="verdict section-grid" id="findings">
          <div className="section-label">
            <span>01</span>
            <p>The finding</p>
          </div>
          <div className="verdict-copy">
            <p className="kicker">{paper.finding.kicker}</p>
            <h2>{paper.finding.headline}</h2>
            <p>{paper.finding.body}</p>
          </div>
        </section>

        <section className="randomness section-grid" id="results">
          <div className="section-label">
            <span>02</span>
            <p>Results</p>
          </div>
          <div className="randomness-content">
            <p className="eyebrow">{paper.results.eyebrow}</p>
            <h2>{paper.results.headline}</h2>
            <p className="randomness-intro">{paper.results.intro}</p>
            <div className="randomness-grid">
              {paper.results.metrics.map((metric) => (
                <article key={metric.label}>
                  <strong>{metric.value}</strong>
                  <span>{metric.label}</span>
                  <p>{metric.note}</p>
                </article>
              ))}
            </div>
            {paper.results.figure ? (
              <figure className="randomness-figure">
                <img
                  src={paper.results.figure.src}
                  alt={paper.results.figure.alt}
                  loading="lazy"
                />
                <figcaption>{paper.results.figure.caption}</figcaption>
              </figure>
            ) : null}
            {paper.results.qualification ? (
              <div className="qualification">
                <strong>{paper.results.qualification.title}</strong>
                <p>{paper.results.qualification.body}</p>
              </div>
            ) : null}
          </div>
        </section>

        <section className="evidence section-grid">
          <div className="section-label">
            <span>03</span>
            <p>Evidence</p>
          </div>
          <div className="evidence-content">
            <div className="evidence-grid">
              {paper.evidence.cards.map((card) => (
                <article key={card.title}>
                  <p className="card-number">{card.value}</p>
                  <h3>{card.title}</h3>
                  <p>{card.body}</p>
                </article>
              ))}
            </div>
            {paper.evidence.figure ? (
              <figure className="chart-card">
                <img
                  src={paper.evidence.figure.src}
                  alt={paper.evidence.figure.alt}
                  loading="lazy"
                />
                <figcaption>{paper.evidence.figure.caption}</figcaption>
              </figure>
            ) : null}
          </div>
        </section>

        <section className="method section-grid" id="method">
          <div className="section-label light">
            <span>04</span>
            <p>Method</p>
          </div>
          <div className="method-copy">
            <p className="eyebrow light-text">{paper.method.eyebrow}</p>
            <h2>{paper.method.headline}</h2>
            <ol className="gate-list">
              {paper.method.steps.map((step, index) => (
                <li key={step.title}>
                  <span>{String(index + 1).padStart(2, "0")}</span>
                  <div>
                    <strong>{step.title}</strong>
                    <p>{step.body}</p>
                  </div>
                </li>
              ))}
            </ol>
          </div>
        </section>

        <section className="inside section-grid">
          <div className="section-label">
            <span>05</span>
            <p>Inside</p>
          </div>
          <div className="inside-copy">
            <div>
              <p className="eyebrow">{paper.inside.eyebrow}</p>
              <h2>{paper.inside.headline}</h2>
            </div>
            <div className="contents-grid">
              <ul>
                {paper.inside.items.slice(0, 4).map((item) => (
                  <li key={item}>{item}</li>
                ))}
              </ul>
              <ul>
                {paper.inside.items.slice(4).map((item) => (
                  <li key={item}>{item}</li>
                ))}
              </ul>
            </div>
            {paper.inside.integrity ? (
              <div className="integrity">
                <span>File integrity</span>
                <code>{paper.inside.integrity}</code>
              </div>
            ) : (
              <div className="integrity">
                <span>Researcher home</span>
                <a href={home}>{researcher.name}</a>
              </div>
            )}
          </div>
        </section>

        <section className="download-panel">
          <div>
            <p className="eyebrow light-text">Original manuscript</p>
            <h2>
              Read the armchair paper,
              <br />
              not only the site.
            </h2>
          </div>
          <div>
            <p>{paper.downloadNote}</p>
            <a className="button button-paper" href={paper.pdf.href} download={pdfName}>
              Download PDF <span aria-hidden="true">↓</span>
            </a>
          </div>
        </section>
      </main>

      <SiteFooter
        left={`${paper.title} ${paper.titleAccent}`.replace(/\s+/g, " ").trim()}
        right={paper.footerNote}
      />
    </>
  );
}
