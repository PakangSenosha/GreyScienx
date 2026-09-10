import { site } from "./site";
import type { ResearchPaper, Researcher } from "./types";

export function researcherPath(researcher: Pick<Researcher, "slug">) {
  return `/r/${researcher.slug}`;
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
