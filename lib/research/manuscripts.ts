import { formManuscripts } from "./extractions/from-manuscripts";

export type ManuscriptHeading = {
  level: number;
  title: string;
  slug: string;
  line: number;
};

export type ManuscriptRecord = {
  study_id: string;
  source_path: string;
  source_sha256: string;
  source_bytes: number;
  character_count: number;
  word_count: number;
  headings: ManuscriptHeading[];
  content_markdown: string;
};

export function manuscriptFor(studyId: string): ManuscriptRecord | null {
  return (formManuscripts[studyId as keyof typeof formManuscripts] as ManuscriptRecord | undefined) ?? null;
}

export function manuscriptMetadataFor(studyId: string) {
  const manuscript = manuscriptFor(studyId);
  if (!manuscript) return null;
  return {
    study_id: manuscript.study_id,
    source_path: manuscript.source_path,
    source_sha256: manuscript.source_sha256,
    source_bytes: manuscript.source_bytes,
    character_count: manuscript.character_count,
    word_count: manuscript.word_count,
    headings: manuscript.headings,
  };
}

export function manuscriptResponse(studyId: string, sectionSelector?: string | null) {
  const manuscript = manuscriptFor(studyId);
  if (!manuscript) return null;
  const selector = sectionSelector?.trim();
  if (!selector) {
    return {
      ...manuscriptMetadataFor(studyId),
      section: null,
      content_markdown: manuscript.content_markdown,
    };
  }

  const key = normalize(selector);
  const heading = manuscript.headings.find(
    (item) => item.slug === key || normalize(item.title) === key,
  );
  if (!heading) return null;
  const lines = manuscript.content_markdown.split("\n");
  const start = heading.line - 1;
  const following = manuscript.headings.find(
    (item) => item.line > heading.line && item.level <= heading.level,
  );
  const end = following ? following.line - 1 : lines.length;
  return {
    ...manuscriptMetadataFor(studyId),
    section: heading,
    content_markdown: lines.slice(start, end).join("\n").trimEnd() + "\n",
  };
}

function normalize(value: string) {
  return value
    .toLowerCase()
    .normalize("NFKD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-|-$/g, "");
}
