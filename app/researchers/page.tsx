import type { Metadata } from "next";
import { SiteFooter } from "@/components/SiteFooter";
import { SiteHeader } from "@/components/SiteHeader";
import { papersFor, researchers } from "@/lib/catalog";
import { researcherHost, researcherPath } from "@/lib/urls";

export const metadata: Metadata = {
  title: "Researchers",
};

export default function ResearchersPage() {
  return (
    <>
      <SiteHeader />
      <main>
        <section className="hero hero-solo">
          <div className="brand-wave wave-one" aria-hidden="true" />
          <div className="hero-copy">
            <p className="eyebrow">Researcher homes</p>
            <h1>
              One name.
              <br />
              <em>Many sites.</em>
            </h1>
            <p className="dek">
              Each researcher on GreyScienx has a home address. Papers published under that
              name become their own research sites.
            </p>
          </div>
        </section>

        <section className="page-shell">
          <div className="research-cards">
            {researchers.map((researcher) => {
              const count = papersFor(researcher.slug).length;
              return (
                <a
                  className="research-card"
                  href={researcherPath(researcher)}
                  key={researcher.slug}
                >
                  <div className="research-card-body">
                    <p className="research-card-field">{researcher.affiliation}</p>
                    <h3>{researcher.name}</h3>
                    <p>{researcher.role}</p>
                    <p>{researcher.bio}</p>
                    <p className="research-card-host">
                      {researcherHost(researcher)} · {count} research {count === 1 ? "site" : "sites"}
                    </p>
                  </div>
                </a>
              );
            })}
          </div>
        </section>
      </main>
      <SiteFooter />
    </>
  );
}
