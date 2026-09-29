import { site } from "../site";
import type { ResearchObject } from "./schema";

export function studyJsonLd(study: ResearchObject) {
  const article = {
    "@type": "ScholarlyArticle",
    "@id": study.links.html,
    headline: study.title,
    name: study.title,
    abstract: study.summary,
    description: study.answer?.conditional_answer ?? study.summary,
    identifier: study.id,
    keywords: study.keywords.join(", "),
    url: study.links.html,
    dateModified: study.date_modified,
    version: study.version,
    isPartOf: {
      "@type": "CreativeWorkSeries",
      name: study.series_title,
      url: `https://${site.domain}/series/${study.series_slug}`,
    },
    author: study.authors.map((author) => ({
      "@type": "Person",
      name: author.name,
      affiliation: {
        "@type": "Organization",
        name: author.affiliation,
      },
    })),
    publisher: {
      "@type": "Organization",
      name: site.name,
      url: `https://${site.domain}`,
    },
    citation: study.sources.filter((source) => source.href).map((source) => source.href),
    spatialCoverage: study.geographies.map((place) => ({
      "@type": "Place",
      name: place,
    })),
    about: study.entities.map((entity) => ({ "@type": "Thing", name: entity })),
    associatedMedia: [
      {
        "@type": "MediaObject",
        contentUrl: study.links.pdf,
        encodingFormat: "application/pdf",
      },
      {
        "@type": "MediaObject",
        contentUrl: study.links.markdown,
        encodingFormat: "text/markdown",
        contentSize: `${study.manuscript.source_bytes} bytes`,
        sha256: study.manuscript.source_sha256,
      },
    ],
  };
  const datasets = study.datasets.map((dataset) => ({
    "@type": "Dataset",
    "@id": `${study.links.html}/data#${String(dataset.id ?? "dataset")}`,
    name: String(dataset.title ?? `${study.title} dataset`),
    description: String(dataset.description ?? ""),
    url: `${study.links.html}/data`,
    license: String(dataset.licence ?? ""),
    spatialCoverage: String(dataset.geographic_coverage ?? ""),
    isPartOf: { "@id": study.links.html },
  }));
  const software = study.reproducibility.code_available
    ? [{
        "@type": "SoftwareSourceCode",
        "@id": `${study.links.html}/reproduce#code`,
        name: `${study.title} reproducibility package`,
        codeRepository: study.reproducibility.repository_url ?? `${study.links.html}/reproduce`,
        programmingLanguage: study.reproducibility.software,
        isPartOf: { "@id": study.links.html },
      }]
    : [];
  return {
    "@context": "https://schema.org",
    "@graph": [article, ...datasets, ...software],
  };
}

export function seriesJsonLd(series: {
  slug: string;
  title: string;
  question: string;
  studies: Array<{ title: string; links: { html: string } }>;
}) {
  return {
    "@context": "https://schema.org",
    "@type": "CreativeWorkSeries",
    name: series.title,
    description: series.question,
    url: `https://${site.domain}/series/${series.slug}`,
    hasPart: series.studies.map((study) => ({ "@type": "ScholarlyArticle", name: study.title, url: study.links.html })),
  };
}

export function topicJsonLd(topic: {
  slug: string;
  title: string;
  definition: string;
  studies: Array<{ title: string; links: { html: string } }>;
}) {
  return {
    "@context": "https://schema.org",
    "@type": "DefinedTerm",
    name: topic.title,
    description: topic.definition,
    url: `https://${site.domain}/topics/${topic.slug}`,
    subjectOf: topic.studies.map((study) => ({ "@type": "ScholarlyArticle", name: study.title, url: study.links.html })),
  };
}
