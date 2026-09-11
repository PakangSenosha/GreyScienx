import Link from "next/link";
import { SiteFooter } from "@/components/SiteFooter";
import { SiteHeader } from "@/components/SiteHeader";
import { papers, researchers } from "@/lib/catalog";
import { site } from "@/lib/site";
import { paperHostPath, paperPath, researcherHost, researcherPath } from "@/lib/urls";

export default function HomePage() {
  const founder = researchers[0];

  return (
    <>
      <SiteHeader />
      <main>
        <section className="hero hero-solo" id="top">
          <div className="brand-wave wave-one" aria-hidden="true" />
          <div className="brand-wave wave-two" aria-hidden="true" />
          <div className="brand-wave wave-three" aria-hidden="true" />
          <div className="hero-copy">
            <p className="eyebrow">GreyScienx · Semi-professional research</p>
            <h1>
              Each paper
              <br />
              <em>becomes a site.</em>
            </h1>
            <p className="dek">
              GreyScienx is a research press built by {site.founder.name}, {site.founder.role}.
              Researchers get a home. Submitted work is distilled into a public research site.
              The original armchair paper stays downloadable.
            </p>
            <div className="hero-actions">
              <Link className="button button-primary" href="/submit">
                Submit research
              </Link>
              <Link className="button button-secondary" href={researcherPath(founder)}>
                {founder.name}
              </Link>
            </div>
            <p className="file-meta">
              {researcherHost(founder)} / research-title
            </p>
          </div>
        </section>

        <section className="number-band" aria-label="GreyScienx scope">
          <div>
            <strong>{researchers.length}</strong>
            <span>researcher homes</span>
          </div>
          <div>
            <strong>{papers.length}</strong>
            <span>research sites</span>
          </div>
          <div>
            <strong>AI</strong>
            <span>distills the paper</span>
          </div>
          <div>
            <strong>PDF</strong>
            <span>original manuscript</span>
          </div>
        </section>

        <section className="section-grid">
          <div className="section-label">
            <span>01</span>
            <p>How it works</p>
          </div>
          <div className="hub-copy">
            <p className="kicker">A paper is not a feed item.</p>
            <h2>Submit the armchair paper. GreyScienx writes the site.</h2>
            <p>
              The layout is shared. The findings are not. Once a manuscript is in, the press
              extracts the result, the quantities, the evidence, and the method, then places
              them on a dedicated research site under the researcher&apos;s name.
            </p>
            <div className="work-grid">
              <article>
                <span>01</span>
                <h3>Researcher home</h3>
                <p>
                  Each researcher receives a GreyScienx address, for example {researcherHost(founder)}.
                </p>
              </article>
              <article>
                <span>02</span>
                <h3>Research site</h3>
                <p>
                  Each paper gets its own site at {researcherHost(founder)}/research-title, using the GreyScienx template.
                </p>
              </article>
              <article>
                <span>03</span>
                <h3>Original paper</h3>
                <p>
                  The distillation is public. The manuscript remains available for download and in-browser reading.
                </p>
              </article>
            </div>
          </div>
        </section>

        <section className="section-grid">
          <div className="section-label">
            <span>02</span>
            <p>Live research</p>
          </div>
          <div className="hub-copy">
            <p className="kicker">First sites on the press</p>
            <h2>Two papers. Two sites. One researcher.</h2>
            <div className="research-cards">
              {papers.map((paper) => {
                const researcher = researchers.find(
                  (item) => item.slug === paper.researcherSlug,
                );
                if (!researcher) return null;
                return (
                  <Link
                    className="research-card"
                    href={paperPath(researcher, paper)}
                    key={paper.slug}
                  >
                    <div className="research-card-body">
                      <p className="research-card-field">{paper.field}</p>
                      <h3>
                        {paper.title} {paper.titleAccent}
                      </h3>
                      <p>{paper.dek}</p>
                      <p className="research-card-host">
                        {paperHostPath(researcher, paper)}
                      </p>
                    </div>
                  </Link>
                );
              })}
            </div>
          </div>
        </section>

        <section className="method section-grid">
          <div className="section-label light">
            <span>03</span>
            <p>Founder</p>
          </div>
          <div className="method-copy">
            <p className="eyebrow light-text">{site.founder.shortRole}</p>
            <h2>{site.founder.name}.</h2>
            <p className="randomness-intro" style={{ color: "#c8c8c8" }}>
              {founder.bio}
            </p>
            <p className="domain-chip" style={{ background: "#161616", color: "#fff" }}>
              {researcherHost(founder)}
            </p>
            <div className="hero-actions">
              <Link className="button button-primary" href={researcherPath(founder)}>
                Open researcher home
              </Link>
              <Link className="button button-secondary" href="/about">
                About GreyScienx
              </Link>
            </div>
          </div>
        </section>

        <section className="download-panel">
          <div>
            <p className="eyebrow light-text">Submit</p>
            <h2>
              Distill a paper
              <br />
              into the template.
            </h2>
          </div>
          <div>
            <p>
              Paste a manuscript. GreyScienx writes the finding, the numbers, the evidence,
              and the method into the research-site layout used by the live papers.
            </p>
            <Link className="button button-paper" href="/submit">
              Submit research
            </Link>
          </div>
        </section>
      </main>
      <SiteFooter />
    </>
  );
}
