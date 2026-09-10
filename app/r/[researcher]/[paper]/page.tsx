import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { ResearchSite } from "@/components/ResearchSite";
import { getPaper, getResearcher, papers, researchers } from "@/lib/catalog";

type PaperPageProps = {
  params: Promise<{ researcher: string; paper: string }>;
};

export function generateStaticParams() {
  return papers.flatMap((paper) => {
    const researcher = researchers.find((item) => item.slug === paper.researcherSlug);
    if (!researcher) return [];
    return [{ researcher: researcher.slug, paper: paper.slug }];
  });
}

export async function generateMetadata({ params }: PaperPageProps): Promise<Metadata> {
  const { researcher: researcherSlug, paper: paperSlug } = await params;
  const paper = getPaper(researcherSlug, paperSlug);
  const researcher = getResearcher(researcherSlug);
  if (!paper || !researcher) return { title: "Research" };
  return {
    title: `${paper.title} ${paper.titleAccent}`.replace(/\s+/g, " ").trim(),
    description: paper.dek,
  };
}

export default async function PaperPage({ params }: PaperPageProps) {
  const { researcher: researcherSlug, paper: paperSlug } = await params;
  const paper = getPaper(researcherSlug, paperSlug);
  const researcher = getResearcher(researcherSlug);
  if (!paper || !researcher) notFound();

  return <ResearchSite paper={paper} researcher={researcher} />;
}
