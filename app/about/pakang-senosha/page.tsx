import type { Metadata } from "next";
import Link from "next/link";
import { SiteFooter } from "@/components/SiteFooter";
import { SiteHeader } from "@/components/SiteHeader";
import { researchers } from "@/lib/catalog";

export const metadata: Metadata = {
  title: "Pakang Senosha",
  description: "About Pakang Senosha, founder of GreyScienx.",
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
            <p className="eyebrow">Founder · Researcher</p>
            <h1>
              Pakang
              <br />
              <em>Senosha.</em>
            </h1>
            <p className="dek">
              MSc Epidemiology and Biostatistics at the University of Pretoria. Founder of
              GreyScienx and author of its founding research collection.
            </p>
          </div>
        </section>

        <section className="section-grid">
          <div className="section-label">
            <span>01</span>
            <p>Background</p>
          </div>
          <div className="hub-copy">
            <h2>Quantitative training. Broad questions.</h2>
            <p>
              Pakang Senosha is based in Pretoria, South Africa. His formal training is in
              epidemiology and biostatistics, with an emphasis on careful measurement,
              uncertainty and the difference between an interesting pattern and a defensible
              conclusion.
            </p>
            <p>
              GreyScienx extends that habit of inquiry beyond any single academic department.
              The subjects can change; the commitment to transparent reasoning remains.
            </p>
            <p className="domain-chip">{author.location}</p>
          </div>
        </section>

        <section className="section-grid about-method">
          <div className="section-label">
            <span>02</span>
            <p>Why GreyScienx</p>
          </div>
          <div className="hub-copy">
            <h2>A publication built around the work.</h2>
            <p>
              GreyScienx began as a way to publish substantial independent research without
              compressing it into a post or hiding it in a folder. The website gives each paper
              an accessible front door; the manuscript preserves its depth.
            </p>
            <p>
              Pakang is the current author, not the permanent boundary of the publication.
              Additional collaborators can be introduced later under the same field-neutral
              editorial system.
            </p>
          </div>
        </section>

        <section className="author-panel compact-author-panel">
          <div>
            <p className="eyebrow light-text">Continue</p>
            <h2>Read the work.</h2>
          </div>
          <div>
            <p>Browse the complete collection or contact Pakang directly.</p>
            <div className="hero-actions">
              <Link className="button button-paper" href="/research">
                Research archive
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
