import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { SiteFooter } from "@/components/SiteFooter";
import { SiteHeader } from "@/components/SiteHeader";
import { getPaper, researchSeries } from "@/lib/catalog";
import { packageFor } from "@/lib/research/packages";
import { getStudy } from "@/lib/research/registry";

export const dynamicParams = false;

export function generateStaticParams() {
  return researchSeries.flatMap((series) => series.papers.map((paper) => ({ series: series.slug, paper: paper.slug })));
}

type DataPageProps = { params: Promise<{ series: string; paper: string }> };

export async function generateMetadata({ params }: DataPageProps): Promise<Metadata> {
  const loaded = await load(params);
  if (!loaded) return {};
  return {
    title: `Datasets · ${loaded.study.title}`,
    description: `Dataset record for ${loaded.study.title}.`,
  };
}

export default async function DataPage({ params }: DataPageProps) {
  const loaded = await load(params);
  if (!loaded) notFound();
  const { study, datasets } = loaded;

  return (
    <>
      <SiteHeader />
      <main>
        <section className="hero hero-solo">
          <div className="brand-wave wave-one" aria-hidden="true" />
          <div className="brand-wave wave-two" aria-hidden="true" />
          <div className="hero-copy">
            <p className="eyebrow">
              <Link href={`/research/${study.series_slug}/${study.slug}`}>{study.id}</Link>
            </p>
            <h1>
              Dataset
              <br />
              <em>record.</em>
            </h1>
            <p className="dek">{study.title}</p>
            <div className="hero-actions">
              <a className="button button-primary" href={`/api/v1/research/${study.slug}/datasets`}>
                Datasets JSON
              </a>
            </div>
          </div>
        </section>

        <div className="series-stack">
          {datasets.length === 0 ? (
            <section className="page-shell">
              <p>No dataset object is published for this study. The manuscript remains the source.</p>
            </section>
          ) : (
            datasets.map((dataset) => (
              <section className="series-block" key={dataset.id}>
                <header className="series-heading">
                  <div>
                    <span>{dataset.id}</span>
                    <p>Dataset</p>
                  </div>
                  <div>
                    <h2>{dataset.title || study.title}</h2>
                    <p>{dataset.description}</p>
                    {dataset.geographic_coverage ? <p>{dataset.geographic_coverage}</p> : null}
                    {dataset.licence ? <p>{dataset.licence}</p> : null}
                  </div>
                </header>
              </section>
            ))
          )}
        </div>
      </main>
      <SiteFooter />
    </>
  );
}

async function load(params: DataPageProps["params"]) {
  const { series, paper } = await params;
  const entry = getPaper(series, paper);
  const study = getStudy(paper);
  if (!entry || !study || study.series_slug !== series) return null;
  return { study, datasets: packageFor(study.id)?.datasets ?? [] };
}
