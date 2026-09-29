export const SERIES_CODES = {
  "household-economics": "HH",
  "population-futures": "POP",
  "r350-counterfactual": "SRD",
  "strategic-industrialisation": "IND",
  "african-convergence": "AFR",
  "wealth-and-place": "WPL",
} as const;

export type SeriesSlug = keyof typeof SERIES_CODES;
export type SeriesCode = (typeof SERIES_CODES)[SeriesSlug];

export const SERIES_RESEARCH_TYPE = {
  "household-economics": "exploratory_simulation",
  "population-futures": "exploratory_simulation",
  "r350-counterfactual": "counterfactual",
  "strategic-industrialisation": "exploratory_simulation",
  "african-convergence": "exploratory_simulation",
  "wealth-and-place": "exploratory_simulation",
} as const;

export type ResearchType = (typeof SERIES_RESEARCH_TYPE)[SeriesSlug];

export function seriesCode(seriesSlug: string): SeriesCode {
  const code = SERIES_CODES[seriesSlug as SeriesSlug];
  if (!code) throw new Error(`No GreyScienx series code for ${seriesSlug}`);
  return code;
}

export function studyId(seriesSlug: string, paperNumber: string) {
  return `GSX:${seriesCode(seriesSlug)}-${paperNumber.padStart(3, "0")}`;
}

export function researchTypeForSeries(seriesSlug: string): ResearchType {
  const researchType = SERIES_RESEARCH_TYPE[seriesSlug as SeriesSlug];
  if (!researchType) throw new Error(`No research type for ${seriesSlug}`);
  return researchType;
}
