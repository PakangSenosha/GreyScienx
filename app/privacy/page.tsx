import type { Metadata } from "next";
import Link from "next/link";
import { SiteFooter } from "@/components/SiteFooter";
import { SiteHeader } from "@/components/SiteHeader";
import { site } from "@/lib/site";

export const metadata: Metadata = {
  title: "Privacy policy",
  description: "How GreyScienx handles information on its website and through its ChatGPT plugin.",
};

export default function PrivacyPage() {
  return (
    <>
      <SiteHeader />
      <main>
        <section className="hero hero-solo">
          <div className="brand-wave wave-one" aria-hidden="true" />
          <div className="brand-wave wave-two" aria-hidden="true" />
          <div className="hero-copy">
            <p className="eyebrow">Publication policy · effective 29 September 2026</p>
            <h1>
              Privacy,
              <br />
              <em>plainly stated.</em>
            </h1>
            <p className="dek">
              GreyScienx provides public research without requiring a reader account. This policy
              explains the limited information processed by the website and its public research tools.
            </p>
          </div>
        </section>

        <section className="section-grid">
          <div className="section-label"><span>01</span><p>The policy</p></div>
          <div className="policy-copy">
            <h2>What GreyScienx receives</h2>
            <p>
              The website may receive routine request information such as an IP address, browser or
              user-agent details, requested URL, timestamp and technical diagnostics. The GreyScienx
              ChatGPT plugin receives the tool request and arguments that ChatGPT sends to the public
              MCP endpoint. Those arguments may include words drawn from a conversation when needed to
              answer a user&apos;s request.
            </p>

            <h2>How information is used</h2>
            <p>
              Information is processed to deliver pages, search the published research corpus, return
              requested research records, protect the service and diagnose reliability problems.
              GreyScienx does not require an MCP account, build advertising profiles, sell personal
              information or use plugin requests to train a GreyScienx model.
            </p>

            <h2>Storage and retention</h2>
            <p>
              The MCP tools are read-only. Their application code does not intentionally persist tool
              arguments or create user profiles. Hosting and security providers may retain routine
              access and diagnostic logs for operational and security purposes under their own
              retention practices. Public research submissions made through separate community forms
              are governed by the disclosures shown on those forms.
            </p>

            <h2>Service providers and ChatGPT</h2>
            <p>
              GreyScienx uses Cloudflare to host and protect the website and MCP endpoint. When the
              plugin is used in ChatGPT, OpenAI controls the ChatGPT-side collection and use of account,
              conversation and memory data. Readers should review OpenAI&apos;s own privacy controls and
              avoid placing sensitive personal information in a research query when it is unnecessary.
            </p>

            <h2>Public research and external links</h2>
            <p>
              Research pages, manuscripts, citations and reproducibility files are public by design.
              External sources and linked services apply their own privacy terms. GreyScienx does not
              control those third-party sites.
            </p>

            <h2>Questions and requests</h2>
            <p>
              Privacy questions or requests may be sent to{" "}
              <a href={`mailto:${site.founder.email}`}>{site.founder.email}</a>. Include enough detail
              to identify the relevant request, but do not send passwords, financial information or
              other unnecessary sensitive data. See the <Link href="/support">support page</Link> for
              service help.
            </p>

            <h2>Changes</h2>
            <p>
              Material changes will be published on this page with a revised effective date. Continued
              use after a change means the service is used under the revised policy.
            </p>
          </div>
        </section>
      </main>
      <SiteFooter />
    </>
  );
}
