import type { Metadata } from "next";
import Link from "next/link";
import { SiteFooter } from "@/components/SiteFooter";
import { SiteHeader } from "@/components/SiteHeader";
import { site } from "@/lib/site";

export const metadata: Metadata = {
  title: "Support",
  description: "Help with GreyScienx research pages, downloads and the ChatGPT plugin.",
};

export default function SupportPage() {
  return (
    <>
      <SiteHeader />
      <main>
        <section className="hero hero-solo">
          <div className="brand-wave wave-one" aria-hidden="true" />
          <div className="brand-wave wave-two" aria-hidden="true" />
          <div className="hero-copy">
            <p className="eyebrow">Publication support</p>
            <h1>
              Find the record.
              <br />
              <em>Report the problem.</em>
            </h1>
            <p className="dek">
              Get help with a research page, manuscript download, reproducibility file or the
              GreyScienx ChatGPT plugin.
            </p>
          </div>
        </section>

        <section className="section-grid">
          <div className="section-label"><span>01</span><p>Get help</p></div>
          <div className="policy-copy">
            <h2>Before writing</h2>
            <p>
              For a research question, start with the <Link href="/research">research index</Link> or
              search GreyScienx in ChatGPT. The plugin can search studies, retrieve assumptions and
              results, compare papers, trace claims and return reproducibility records. It is read-only
              and does not publish submissions or alter research.
            </p>

            <h2>Report a technical issue</h2>
            <p>
              Email <a href={`mailto:${site.founder.email}`}>{site.founder.email}</a> with the page URL,
              approximate time, the action attempted and the error shown. For a plugin problem, include
              the tool name when ChatGPT displays it. Do not include passwords, authentication tokens,
              private documents or unrelated conversation content.
            </p>

            <h2>Corrections and research responses</h2>
            <p>
              Factual corrections should identify the study, exact passage, supporting source and the
              proposed correction. Formal critiques, forks and revisions can begin through the{" "}
              <Link href="/community">community page</Link>; every proposed object remains unpublished
              until human review.
            </p>

            <h2>Response expectations</h2>
            <p>
              GreyScienx is an independent publication. Requests are reviewed in good faith, but a
              response time is not guaranteed. Security or privacy reports receive priority over general
              research correspondence.
            </p>

            <h2>Policies</h2>
            <p>
              Read the <Link href="/privacy">privacy policy</Link> and <Link href="/terms">terms of use</Link>
              before sending personal information or relying on a modelled result.
            </p>
          </div>
        </section>
      </main>
      <SiteFooter />
    </>
  );
}
