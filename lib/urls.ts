import { site } from "./site";
import type { ArchivePaper, ResearchPaper, ResearchSeries, Researcher } from "./types";

export function researcherPath(researcher: Pick<Researcher, "slug">) {
  return `/r/${researcher.slug}`;
}

export function articlePath(
  series: Pick<ResearchSeries, "slug">,
  paper: Pick<ArchivePaper, "slug">,
) {
  return `/research/${series.slug}/${paper.slug}`;
}

export function articleUrl(
  series: Pick<ResearchSeries, "slug">,
  paper: Pick<ArchivePaper, "slug">,
) {
  return `https://${site.domain}${articlePath(series, paper)}`;
}

export function publicUrl(path: string) {
  return new URL(path, `https://${site.domain}`).toString();
}

export function paperPath(
  researcher: Pick<Researcher, "slug">,
  paper: Pick<ResearchPaper, "slug">,
) {
  return `/r/${researcher.slug}/${paper.slug}`;
}

export function researcherHost(researcher: Pick<Researcher, "subdomain">) {
  return `${researcher.subdomain}.${site.domain}`;
}

export function paperHostPath(
  researcher: Pick<Researcher, "subdomain">,
  paper: Pick<ResearchPaper, "slug">,
) {
  return `${researcherHost(researcher)}/${paper.slug}`;
}
