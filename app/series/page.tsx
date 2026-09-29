import type { Metadata } from "next";
import Link from "next/link";
import { SiteFooter } from "@/components/SiteFooter";
import { SiteHeader } from "@/components/SiteHeader";
import { listSeriesRecords } from "@/lib/research/registry";

export const metadata: Metadata = {
  title: "Research series",
  description: "GreyScienx series, the question each series asks, and the studies inside it.",
};

export default function SeriesIndexPage() {
  const seriesList = listSeriesRecords();

  return (
    <>
      <SiteHeader />
      <main>
        <section className="hero hero-solo">
          <div className="brand-wave wave-one" aria-hidden="true" />
          <div className="brand-wave wave-two" aria-hidden="true" />
          <div className="hero-copy">
            <p className="eyebrow">Collections</p>
            <h1>
              Series,
              <br />
              <em>one question each.</em>
            </h1>
            <p className="dek">
              A series gathers studies that share a question. Open a series for its studies, or
              read the archive as a list.
            </p>
            <div className="hero-actions">
              <Link className="button button-primary" href="/research">
                All research
              </Link>
            </div>
          </div>
        </section>

        <div className="series-stack">
          {seriesList.map((series) => (
            <section className="series-block" key={series.slug}>
              <header className="series-heading">
                <div>
                  <span>{series.number}</span>
                  <p>{series.study_count} studies</p>
                </div>
                <div>
                  <h2>
                    <Link href={`/series/${series.slug}`}>{series.title}</Link>
                  </h2>
                  <p>{series.question}</p>
                </div>
              </header>
            </section>
          ))}
        </div>
      </main>
      <SiteFooter />
    </>
  );
}
