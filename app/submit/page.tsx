import type { Metadata } from "next";
import { SiteFooter } from "@/components/SiteFooter";
import { SiteHeader } from "@/components/SiteHeader";
import { SubmitForm } from "@/components/SubmitForm";

export const metadata: Metadata = {
  title: "Submit research",
};

export default function SubmitPage() {
  return (
    <>
      <SiteHeader action={{ href: "/", label: "GreyScienx" }} />
      <main>
        <section className="hero hero-solo">
          <div className="brand-wave wave-one" aria-hidden="true" />
          <div className="brand-wave wave-two" aria-hidden="true" />
          <div className="hero-copy">
            <p className="eyebrow">Submit · Distill · Publish layout</p>
            <h1>
              Send the paper.
              <br />
              <em>Receive a site.</em>
            </h1>
            <p className="dek">
              Paste the armchair manuscript. GreyScienx distills the finding, quantities,
              evidence, and methods into the shared research-site template. The original
              paper remains the source of record.
            </p>
          </div>
        </section>
        <section className="page-shell">
          <SubmitForm />
        </section>
      </main>
      <SiteFooter />
    </>
  );
}
