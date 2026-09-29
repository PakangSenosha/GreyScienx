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

type ReproducePageProps = { params: Promise<{ series: string; paper: string }> };

export async function generateMetadata({ params }: ReproducePageProps): Promise<Metadata> {
  const loaded = await load(params);
  if (!loaded) return {};
  return {
    title: `Reproducibility · ${loaded.study.title}`,
    description: `Code, data, seed, and manuscript record for ${loaded.study.title}.`,
  };
}

export default async function ReproducePage({ params }: ReproducePageProps) {
  const loaded = await load(params);
  if (!loaded) notFound();
  const { study, pack } = loaded;
  const repo = pack?.reproducibility.repository_url;

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
              Reproducibility
              <br />
              <em>record.</em>
            </h1>
            <p className="dek">{study.title}</p>
          </div>
        </section>

        <section className="number-band" aria-label="Reproducibility summary">
          <div>
            <strong>{yesNo(pack?.reproducibility.code_available)}</strong>
            <span>code recorded</span>
          </div>
          <div>
            <strong>{yesNo(pack?.reproducibility.data_available)}</strong>
            <span>data recorded</span>
          </div>
          <div>
            <strong>{yesNo(pack?.reproducibility.environment_available)}</strong>
            <span>environment recorded</span>
          </div>
          <div>
            <strong>{repo ? "Yes" : "No"}</strong>
            <span>public repository</span>
          </div>
        </section>

        <section className="page-shell">
          <p className="kicker">What is published</p>
          <p>The manuscript PDF is the public reading copy. Code and data files listed here are the files named in the study record that exist in the authoring package.</p>
          <p>{pack?.reproducibility.random_seed || "No random seed is recorded."}</p>
          <p>Software: {pack?.reproducibility.software.join(", ") || "not recorded"}.</p>
          <p>
            {repo
              ? "The form records a repository URL."
              : "A separate public code repository is not published."}
          </p>
          {pack && pack.files.length > 0 ? (
            <ul className="dossier-questions">
              {pack.files.map((file) => (
                <li key={file.href}>
                  <a href={file.href}>{file.path}</a>
                  {` · ${file.role} · ${file.bytes} bytes`}
                </li>
              ))}
            </ul>
          ) : (
            <p>No separate code or data file is published for this study.</p>
          )}
          <p className="archive-links">
            <a href={study.links.pdf}>Manuscript PDF</a>
            <Link href={`/research/${study.series_slug}/${study.slug}/data`}>Datasets</Link>
            <Link href={`/research/${study.series_slug}/${study.slug}`}>Study</Link>
          </p>
        </section>
      </main>
      <SiteFooter />
    </>
  );
}

async function load(params: ReproducePageProps["params"]) {
  const { series, paper } = await params;
  const entry = getPaper(series, paper);
  const study = getStudy(paper);
  if (!entry || !study || study.series_slug !== series) return null;
  return { study, pack: packageFor(study.id) };
}

function yesNo(value: boolean | undefined) {
  return value ? "Yes" : "No";
}
