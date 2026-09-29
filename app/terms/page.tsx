import type { Metadata } from "next";
import Link from "next/link";
import { SiteFooter } from "@/components/SiteFooter";
import { SiteHeader } from "@/components/SiteHeader";
import { site } from "@/lib/site";

export const metadata: Metadata = {
  title: "Terms of use",
  description: "Terms for using GreyScienx research, website resources and public research tools.",
};

export default function TermsPage() {
  return (
    <>
      <SiteHeader />
      <main>
        <section className="hero hero-solo">
          <div className="brand-wave wave-one" aria-hidden="true" />
          <div className="brand-wave wave-two" aria-hidden="true" />
          <div className="hero-copy">
            <p className="eyebrow">Publication terms · effective 29 September 2026</p>
            <h1>
              Use the work.
              <br />
              <em>Keep its limits visible.</em>
            </h1>
            <p className="dek">
              These terms apply to the GreyScienx website, manuscripts, downloads and public research
              tools, including the GreyScienx ChatGPT plugin.
            </p>
          </div>
        </section>

        <section className="section-grid">
          <div className="section-label"><span>01</span><p>The terms</p></div>
          <div className="policy-copy">
            <h2>Research, not professional advice</h2>
            <p>
              GreyScienx publishes exploratory research, models, simulations and counterfactuals for
              general information. It does not provide financial, investment, legal, medical, tax or
              other professional advice. A modelled result is not a forecast, guarantee or instruction
              to act. Decisions should use appropriate professional advice and current primary data.
            </p>

            <h2>Accuracy and interpretation</h2>
            <p>
              The publication aims to expose assumptions, evidence status, limitations and source
              records. Research may still contain errors, use uncertain inputs or become outdated.
              Users must not present scenarios as predictions, catalog summaries as findings, or
              conditional results without their assumptions and limitations.
            </p>

            <h2>Permitted use</h2>
            <p>
              Readers may link to GreyScienx, quote reasonable portions with clear attribution and use
              the public research tools to retrieve and analyse published records. Source material and
              third-party datasets retain their respective rights. Unless a specific work states a
              broader licence, complete republication or commercial redistribution requires written
              permission.
            </p>

            <h2>Acceptable use</h2>
            <p>Users must not:</p>
            <ul>
              <li>misrepresent GreyScienx research or remove material qualifications;</li>
              <li>interfere with, overload, probe or attempt to bypass the service&apos;s security;</li>
              <li>use the tools to violate law, intellectual-property rights or another person&apos;s privacy;</li>
              <li>claim endorsement by GreyScienx, its contributors or cited institutions without permission.</li>
            </ul>

            <h2>Availability and changes</h2>
            <p>
              GreyScienx may correct, revise, replace or withdraw content and may change or suspend the
              service. Stable study identifiers and version records are intended to make revisions
              visible, but continuous availability is not guaranteed.
            </p>

            <h2>No warranty and limitation</h2>
            <p>
              The service is provided as available, without warranties of accuracy, completeness,
              fitness for a particular purpose or uninterrupted access. To the extent permitted by law,
              GreyScienx and its contributors are not liable for indirect or consequential loss arising
              from use of, or reliance on, the service.
            </p>

            <h2>Privacy, support and contact</h2>
            <p>
              Use is also subject to the <Link href="/privacy">privacy policy</Link>. Questions may be
              sent through the <Link href="/support">support page</Link> or to{" "}
              <a href={`mailto:${site.founder.email}`}>{site.founder.email}</a>.
            </p>

            <h2>Governing law</h2>
            <p>
              These terms are governed by the laws of the Republic of South Africa. Any dispute that
              cannot be resolved informally will be subject to the competent courts of South Africa.
            </p>
          </div>
        </section>
      </main>
      <SiteFooter />
    </>
  );
}
