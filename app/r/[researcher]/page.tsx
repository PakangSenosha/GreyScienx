import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { SiteFooter } from "@/components/SiteFooter";
import { SiteHeader } from "@/components/SiteHeader";
import { getResearcher, papersFor, researchers } from "@/lib/catalog";
import { paperHostPath, paperPath, researcherHost } from "@/lib/urls";

type ResearcherPageProps = {
  params: Promise<{ researcher: string }>;
};

export function generateStaticParams() {
  return researchers.map((researcher) => ({ researcher: researcher.slug }));
}

export async function generateMetadata({
  params,
}: ResearcherPageProps): Promise<Metadata> {
  const { researcher: slug } = await params;
  const researcher = getResearcher(slug);
  if (!researcher) return { title: "Researcher" };
  return {
    title: researcher.name,
    description: researcher.bio,
  };
}

export default async function ResearcherPage({ params }: ResearcherPageProps) {
  const { researcher: slug } = await params;
  const researcher = getResearcher(slug);
  if (!researcher) notFound();
  const papers = papersFor(researcher.slug);

  return (
    <>
      <SiteHeader />
      <main>
        <section className="hero hero-solo">
          <div className="brand-wave wave-one" aria-hidden="true" />
          <div className="brand-wave wave-two" aria-hidden="true" />
          <div className="hero-copy">
            <p className="eyebrow">
              {researcher.affiliation} · {researcher.role}
            </p>
            <h1>
              {researcher.givenName}
              <br />
              <em>{researcher.name.replace(researcher.givenName, "").trim() || "Research"}.</em>
            </h1>
            <p className="dek">{researcher.bio}</p>
            <p className="file-meta">{researcherHost(researcher)}</p>
          </div>
        </section>

        <section className="number-band">
          <div>
            <strong>{papers.length}</strong>
            <span>research sites</span>
          </div>
          <div>
            <strong>{researcher.givenName}</strong>
            <span>{researcher.affiliation}</span>
          </div>
          <div>
            <strong>PDF</strong>
            <span>open manuscripts</span>
          </div>
          <div>
            <strong>GreyScienx</strong>
            <span>press</span>
          </div>
        </section>

        <section className="page-shell">
          <p className="eyebrow">Research sites</p>
          <div className="research-cards">
            {papers.map((paper) => (
              <Link
                className="research-card"
                href={paperPath(researcher, paper)}
                key={paper.slug}
              >
                <div className="research-card-body">
                  <p className="research-card-field">{paper.protocol}</p>
                  <h3>
                    {paper.title} {paper.titleAccent}
                  </h3>
                  <p>{paper.dek}</p>
                  <p className="research-card-host">
                    {paperHostPath(researcher, paper)}
                  </p>
                </div>
              </Link>
            ))}
          </div>
        </section>
      </main>
      <SiteFooter
        left={researcher.name}
        right={`${researcher.role} · ${researcher.affiliation}`}
      />
    </>
  );
}
