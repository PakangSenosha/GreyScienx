import type { Metadata } from "next";
import Link from "next/link";
import { SiteFooter } from "@/components/SiteFooter";
import { SiteHeader } from "@/components/SiteHeader";
import { researchers } from "@/lib/catalog";
import { site } from "@/lib/site";
import { researcherHost, researcherPath } from "@/lib/urls";

export const metadata: Metadata = {
  title: "About",
};

export default function AboutPage() {
  const founder = researchers[0];

  return (
    <>
      <SiteHeader />
      <main>
        <section className="hero hero-solo">
          <div className="brand-wave wave-one" aria-hidden="true" />
          <div className="brand-wave wave-two" aria-hidden="true" />
          <div className="hero-copy">
            <p className="eyebrow">About the press</p>
            <h1>
              Semi-professional
              <br />
              <em>research, public.</em>
            </h1>
            <p className="dek">{site.description}</p>
          </div>
        </section>

        <section className="section-grid">
          <div className="section-label">
            <span>01</span>
            <p>The idea</p>
          </div>
          <div className="hub-copy">
            <h2>A paper should be able to stand as a site.</h2>
            <p>
              GreyScienx is not a journal and not a social feed. It is a layout and an address
              system for work that already exists as an armchair paper: methods, results,
              limitations, and a file people can download.
            </p>
            <p>
              The domain is {site.domain}. A researcher lives at a subdomain. A paper lives
              on a path under that name. The same template receives every distillation so
              readers always know where the finding, the numbers, and the manuscript are.
            </p>
          </div>
        </section>

        <section className="section-grid">
          <div className="section-label">
            <span>02</span>
            <p>Who built it</p>
          </div>
          <div className="hub-copy">
            <h2>{site.founder.name}.</h2>
            <p>
              {founder.bio} The first two GreyScienx sites are his: a reproducibility audit of
              trading edges, and a census of first tertiary education among Wits staff.
            </p>
            <p className="domain-chip">{researcherHost(founder)}</p>
            <p>
              <Link className="button button-ghost" href={researcherPath(founder)}>
                Researcher home
              </Link>
            </p>
          </div>
        </section>
      </main>
      <SiteFooter />
    </>
  );
}
