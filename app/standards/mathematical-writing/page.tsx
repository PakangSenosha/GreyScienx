import type { Metadata } from "next";
import Link from "next/link";
import { SiteFooter } from "@/components/SiteFooter";
import { SiteHeader } from "@/components/SiteHeader";
import { mathematicalStandard } from "@/lib/research/standard";
import { site } from "@/lib/site";

const canonical = `https://${site.domain}/standards/mathematical-writing`;

export const metadata: Metadata = {
  title: "Mathematical writing",
  description: mathematicalStandard.summary,
  alternates: {
    canonical,
    types: {
      "text/markdown": `${canonical}/markdown`,
    },
  },
};

export default function MathematicalWritingPage() {
  return (
    <>
      <SiteHeader />
      <main>
        <section className="hero hero-solo">
          <div className="brand-wave wave-one" aria-hidden="true" />
          <div className="brand-wave wave-two" aria-hidden="true" />
          <div className="hero-copy">
            <p className="eyebrow">Standard {mathematicalStandard.version}</p>
            <h1>
              Mathematical
              <br />
              <em>writing.</em>
            </h1>
            <p className="dek">{mathematicalStandard.summary}</p>
            <p className="file-meta">{mathematicalStandard.id}</p>
            <div className="hero-actions">
              <Link className="button button-primary" href="/standards/mathematical-writing/markdown">
                Markdown
              </Link>
              <Link className="button button-ghost" href="/research">
                All research
              </Link>
            </div>
          </div>
        </section>

        {mathematicalStandard.sections.map((section) => (
          <section className="section-grid" key={section.number}>
            <div className="section-label">
              <span>{section.number}</span>
              <p>{section.label}</p>
            </div>
            <div className="hub-copy">
              <h2>{section.title}</h2>
              {section.paragraphs.map((paragraph) => (
                <p key={paragraph}>{paragraph}</p>
              ))}
            </div>
          </section>
        ))}
      </main>
      <SiteFooter />
    </>
  );
}
