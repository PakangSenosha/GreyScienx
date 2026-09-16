import type { Metadata } from "next";
import Link from "next/link";
import { SiteFooter } from "@/components/SiteFooter";
import { SiteHeader } from "@/components/SiteHeader";

export const metadata: Metadata = {
  title: "About",
  description: "About GreyScienx, an independent research publication across fields of study.",
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
            <p className="eyebrow">About GreyScienx</p>
            <h1>
              Research should
              <br />
              <em>stand on its own.</em>
            </h1>
            <p className="dek">
              GreyScienx is an independent publication for clear research across fields of
              study. It organises related work into readable series while preserving every
              complete manuscript.
            </p>
          </div>
        </section>

        <section className="section-grid">
          <div className="section-label">
            <span>01</span>
            <p>The publication</p>
          </div>
          <div className="hub-copy">
            <h2>A paper is more than a feed item.</h2>
            <p>
              GreyScienx is organised around research objects rather than a stream of posts.
              Each paper receives a stable place in a named series, with the original manuscript
              available to readers who want the full record.
            </p>
            <p>
              The publication is field-neutral. A project may be quantitative or qualitative,
              theoretical or empirical, narrow or speculative. What matters is that its claims,
              reasoning, uncertainty and limitations can be inspected.
            </p>
          </div>
        </section>

        <section className="section-grid about-method">
          <div className="section-label">
            <span>02</span>
            <p>The standard</p>
          </div>
          <div className="hub-copy">
            <h2>Simple at the front. Complete underneath.</h2>
            <p>
              The public archive is deliberately text-led. It helps readers see how papers relate
              without turning the work into a dashboard or a gallery of graphs.
            </p>
            <p>
              The manuscript remains authoritative. Sources, assumptions, model details,
              qualifications and failure cases belong there and remain downloadable.
            </p>
          </div>
        </section>

        <section className="section-grid">
          <div className="section-label">
            <span>03</span>
            <p>The structure</p>
          </div>
          <div className="hub-copy">
            <h2>Neutral enough to grow.</h2>
            <p>
              GreyScienx currently publishes its founding body of work. The publication is not
              presented as a personal portfolio or limited to a fixed list of subjects. New
              fields—and, later, additional collaborators—can enter without changing its core
              editorial identity.
            </p>
          </div>
        </section>

        <section className="author-panel compact-author-panel publication-panel">
          <div>
            <p className="eyebrow light-text">Separate from the publication</p>
            <h2>The founder.</h2>
          </div>
          <div>
            <p>The founder&apos;s background and current research archive live on their own pages.</p>
            <div className="hero-actions">
              <Link className="button button-paper" href="/about/pakang-senosha">
                About Pakang Senosha
              </Link>
              <Link className="button button-secondary" href="/research">
                Browse the archive
              </Link>
            </div>
          </div>
        </section>
      </main>
      <SiteFooter />
    </>
  );
}
