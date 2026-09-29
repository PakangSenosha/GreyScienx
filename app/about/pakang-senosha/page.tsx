import type { Metadata } from "next";
import Link from "next/link";
import { SiteFooter } from "@/components/SiteFooter";
import { SiteHeader } from "@/components/SiteHeader";
import { researchers } from "@/lib/catalog";

export const metadata: Metadata = {
  title: "Pakang Senosha",
  description: "Pakang Senosha, founder of GreyScienx and a researcher in epidemiology and biostatistics.",
};

export default function PakangSenoshaPage() {
  const author = researchers[0];

  return (
    <>
      <SiteHeader />
      <main>
        <section className="hero hero-solo">
          <div className="brand-wave wave-one" aria-hidden="true" />
          <div className="brand-wave wave-two" aria-hidden="true" />
          <div className="hero-copy">
            <p className="eyebrow">Founder and researcher</p>
            <h1>
              Pakang
              <br />
              <em>Senosha.</em>
            </h1>
            <p className="dek">
              Pakang Senosha studies epidemiology and biostatistics at the University of
              Pretoria. He founded GreyScienx and wrote its first collection of research.
            </p>
          </div>
        </section>

        <section className="section-grid">
          <div className="section-label">
            <span>01</span>
            <p>Background</p>
          </div>
          <div className="hub-copy">
            <h2>Trained in numbers. Drawn to larger questions.</h2>
            <p>
              Based in Johannesburg, Senosha is trained in epidemiology and biostatistics. His work
              emphasises measurement, uncertainty and the distance between an interesting
              pattern and a defensible conclusion.
            </p>
            <p>
              GreyScienx applies that approach beyond a single academic department. The subjects
              change; the obligation to explain the reasoning does not.
            </p>
            <p className="domain-chip">Johannesburg, South Africa</p>
          </div>
        </section>

        <section className="section-grid about-method">
          <div className="section-label">
            <span>02</span>
            <p>Founding GreyScienx</p>
          </div>
          <div className="hub-copy">
            <h2>A place for arguments too large for a post.</h2>
            <p>
              Senosha created GreyScienx to publish independent research without compressing it
              into a social post or leaving it in a private folder. The site introduces each
              study; the manuscript carries the full argument.
            </p>
            <p>
              He is the publication&apos;s current author, not its permanent boundary. Other
              contributors may be added under the same editorial standards.
            </p>
          </div>
        </section>

        <section className="author-panel compact-author-panel">
          <div>
            <p className="eyebrow light-text">Further reading</p>
            <h2>Read the research.</h2>
          </div>
          <div>
            <p>Browse the complete collection or contact Senosha directly.</p>
            <div className="hero-actions">
              <Link className="button button-paper" href="/research">
                View all research
              </Link>
              <a className="button button-secondary" href={`mailto:${author.email}`}>
                {author.email}
              </a>
            </div>
          </div>
        </section>
      </main>
      <SiteFooter />
    </>
  );
}
