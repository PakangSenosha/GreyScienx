export const SCHEMA_VERSION = "GreyResearchObject 1.2";
export const RECORD_VERSION = "1.0";
export const RECORD_DATE = "2026-09-28";
export const RECORD_DATE_NOTE =
  "Date of this machine record. It is not a separately catalogued manuscript issue date.";

export const AI_DISCLOSURE =
  "GreyScienx manuscripts are prepared with substantial AI assistance in research, drafting, and computation. This record is not peer-reviewed. The published manuscript does not itemise AI participation by activity.";

export const RETRIEVAL_NOTE =
  "This GreyScienx record is a modelled, exploratory study. Claim-level conclusions, assumptions, and results are not published yet. Use the summary as the catalog description, and do not treat it as a conditional finding.";

export const RETRIEVAL_NOTE_PARTIAL =
  "The complete source manuscript is available as Markdown. Published claim objects are a claim-led extraction, not an exhaustive list of every statement in the paper. Read each claim with its assumptions and main limitation; the catalog summary is not a finding.";

export const EXTRACTION_NOTES = {
  claims: "Claims are not yet extracted from the manuscript. No conclusion is returned.",
  assumptions: "Assumptions are not yet extracted from the manuscript.",
  results: "Results are not yet extracted from the manuscript.",
  models: "Models are not yet extracted from the manuscript.",
  sources: "The manuscript and its normalised cited URLs are registered. A cited URL is contextual until editorial review assigns it to a specific claim.",
} as const;
