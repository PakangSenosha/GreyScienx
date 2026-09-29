import type { Metadata } from "next";
import Link from "next/link";
import { SiteFooter } from "@/components/SiteFooter";
import { SiteHeader } from "@/components/SiteHeader";

export const metadata: Metadata = {
  title: "About",
  description: "How GreyScienx reports, edits and publishes independent research.",
};

export default function AboutPage() {
  return (
    <>
      <SiteHeader />
      <main>
        <section className="hero hero-solo">
          <div className="brand-wave wave-one" aria-hidden="true" />
          <div className="brand-wave wave-two" aria-hidden="true" />
          <div className="hero-copy">
            <p className="eyebrow">About the publication</p>
            <h1>
              The argument should
              <br />
              <em>stand on its own.</em>
            </h1>
            <p className="dek">
              GreyScienx publishes independent research for general readers. The summaries are
              concise; the evidence, assumptions and complete manuscripts remain available.
            </p>
          </div>
        </section>

        <section className="section-grid">
          <div className="section-label">
            <span>01</span>
            <p>The record</p>
          </div>
          <div className="hub-copy">
            <h2>A permanent record, not a passing post.</h2>
            <p>
              GreyScienx is organised around published studies, not a stream of updates. Each
              paper has a permanent page, a place in a named series and a complete manuscript.
            </p>
            <p>
              The publication is not confined to one discipline. A study may be quantitative or
              qualitative, theoretical or empirical. Its claims, reasoning and limits must still
              be open to inspection.
            </p>
          </div>
        </section>

        <section className="section-grid about-method">
          <div className="section-label">
            <span>02</span>
            <p>The reading experience</p>
          </div>
          <div className="hub-copy">
            <h2>Read the conclusion. Check the work.</h2>
            <p>
              The archive gives readers a clear route through related papers without reducing
              the research to a collection of charts or promotional summaries.
            </p>
            <p>
              The manuscript remains the source of record. It contains the sources, assumptions,
              model details, qualifications and failure cases.
            </p>
          </div>
        </section>

        <section className="section-grid">
          <div className="section-label">
            <span>03</span>
            <p>The scope</p>
          </div>
          <div className="hub-copy">
            <h2>One publication. Many subjects.</h2>
            <p>
              GreyScienx currently publishes its founding collection. It is not a personal
              portfolio or a closed list of subjects. New fields, and later new contributors,
              can enter under the same editorial standards.
            </p>
          </div>
        </section>

        <section className="author-panel compact-author-panel publication-panel">
          <div>
            <p className="eyebrow light-text">The person behind the publication</p>
            <h2>Meet the founder.</h2>
          </div>
          <div>
            <p>Read about Pakang Senosha&apos;s background and the work that began GreyScienx.</p>
            <div className="hero-actions">
              <Link className="button button-paper" href="/about/pakang-senosha">
                About Pakang Senosha
              </Link>
              <Link className="button button-secondary" href="/research">
                Read the research
              </Link>
            </div>
          </div>
        </section>
      </main>
      <SiteFooter />
    </>
  );
}
