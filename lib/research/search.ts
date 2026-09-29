import type { ResearchType, SearchHit } from "./schema";

const STOP_WORDS = new Set([
  "a",
  "an",
  "the",
  "of",
  "and",
  "or",
  "to",
  "in",
  "on",
  "for",
  "with",
  "from",
  "by",
  "at",
  "is",
  "are",
  "was",
  "were",
  "be",
  "as",
  "that",
  "this",
  "these",
  "those",
  "how",
  "what",
  "when",
  "does",
  "do",
  "can",
  "if",
  "into",
  "over",
  "under",
  "than",
  "then",
  "its",
  "it",
  "their",
  "about",
  "between",
  "across",
  "after",
  "before",
  "during",
  "would",
  "could",
  "should",
  "where",
  "will",
  "people",
  "person",
  "live",
  "lives",
  "if",
  "but",
  "who",
  "whom",
  "just",
  "also",
  "more",
  "most",
  "such",
  "only",
  "not",
  "they",
  "them",
  "our",
  "we",
  "you",
  "your",
]);

export type SearchDocument = {
  id: string;
  slug: string;
  seriesSlug: string;
  seriesTitle: string;
  title: string;
  primaryQuestion: string;
  summary: string;
  topics: string[];
  keywords: string[];
  relatedQuestions: string[];
  claims: Array<{ id: string; text: string; href: string; dependsOn: string[] }>;
  assumptions: Array<{ id: string; name: string; statement: string; sensitivity: "low" | "moderate" | "high" }>;
  results: string[];
  limitations: string[];
  models: string[];
  manuscriptText: string;
  geographies: string[];
  researchType: ResearchType;
  version: "1.0";
  dateModified: string;
  canonicalUrl: string;
};

type Field = {
  weight: number;
  text: string;
};

export function tokenize(value: string) {
  return normalize(value)
    .split(" ")
    .filter((token) => token.length > 1 && !STOP_WORDS.has(token));
}

const CONCEPTS = [
  ["housing", "house", "houses", "home", "homes", "dwelling", "dwellings", "accommodation"],
  ["decline", "declines", "declining", "shrink", "shrinks", "shrinking", "fall", "falls", "falling"],
  ["population", "populations", "demographic", "demographics"],
  ["ageing", "aging", "ages", "lifespan", "longevity"],
  ["cohabitation", "cohabit"],
  ["pension", "pensions"],
  ["grant", "grants", "srd"],
  ["unemployment", "joblessness", "jobless"],
  ["inheritance", "inherit", "inherited", "bequest", "bequests"],
];

const conceptOf = new Map<string, string>();
for (const group of CONCEPTS) {
  for (const word of group) conceptOf.set(word, group[0]);
}

export function searchDocuments(documents: SearchDocument[], query: string): SearchHit[] {
  const normalizedQuery = expandQuery(normalize(query));
  const tokens = distinctConcepts(tokenize(normalizedQuery));
  if (!normalizedQuery || tokens.length === 0) return [];

  const ranked = documents
    .map((document) => ({ document, score: scoreDocument(document, tokens, normalizedQuery) }))
    .filter((entry) => entry.score > 0)
    .sort((a, b) => b.score - a.score || a.document.title.localeCompare(b.document.title))
    .slice(0, 20);

  return ranked.map(({ document }) => {
    const claim = bestClaim(document, tokens);
    return {
      id: document.id,
      slug: document.slug,
      title: document.title,
      primary_question: document.primaryQuestion,
      summary: document.summary,
      research_type: document.researchType,
      evidence_status: "modelled" as const,
      series_slug: document.seriesSlug,
      series_title: document.seriesTitle,
      canonical_url: document.canonicalUrl,
      version: document.version,
      date_modified: document.dateModified,
      most_relevant_claim: claim,
      key_assumptions: matchingAssumptions(document, tokens, claim?.id ?? null),
    };
  });
}

function scoreDocument(document: SearchDocument, tokens: string[], normalizedQuery: string) {
  const fields: Field[] = [
    { weight: 8, text: document.id },
    { weight: 6, text: document.title },
    { weight: 6, text: document.slug },
    { weight: 5, text: document.primaryQuestion },
    { weight: 5, text: document.claims.map((claim) => claim.text).join(" ") },
    { weight: 5, text: document.limitations.join(" ") },
    { weight: 4, text: document.assumptions.map((item) => `${item.name} ${item.statement}`).join(" ") },
    { weight: 4, text: document.results.join(" ") },
    { weight: 3, text: document.models.join(" ") },
    { weight: 4, text: document.relatedQuestions.join(" ") },
    { weight: 4, text: document.topics.join(" ") },
    { weight: 3, text: document.keywords.join(" ") },
    { weight: 3, text: document.summary },
    { weight: 2, text: document.geographies.join(" ") },
    { weight: 2, text: document.seriesTitle },
    { weight: 1, text: document.manuscriptText },
  ];

  const prepared = fields.map((field) => ({
    weight: field.weight,
    tokens: normalize(field.text).split(" ").filter(Boolean),
  }));

  let score = 0;
  let matched = 0;
  for (const token of tokens) {
    let best = 0;
    for (const field of prepared) {
      for (const word of field.tokens) best = Math.max(best, matchWeight(word, token, field.weight));
    }
    if (best > 0) {
      matched += 1;
      score += best;
    }
  }

  if (matched === tokens.length) score += 12;
  const phraseFields = [
    document.title,
    document.primaryQuestion,
    ...document.relatedQuestions,
    document.topics.join(" "),
    ...document.assumptions.map((item) => `${item.name} ${item.statement}`),
    ...document.results,
    ...document.limitations,
    ...document.models,
  ];
  if (phraseFields.some((field) => normalize(field).includes(normalizedQuery))) score += 8;
  return score + conceptVectorScore(document, normalizedQuery);
}

function conceptVectorScore(document: SearchDocument, query: string) {
  const documentText = [
    document.title,
    document.primaryQuestion,
    document.summary,
    ...document.relatedQuestions,
    ...document.topics,
    ...document.keywords,
    ...document.claims.map((item) => item.text),
    ...document.assumptions.map((item) => `${item.name} ${item.statement}`),
    ...document.results,
    ...document.limitations,
    ...document.models,
  ].join(" ");
  const left = sparseConceptVector(query);
  const right = sparseConceptVector(documentText);
  let dot = 0;
  let leftNorm = 0;
  let rightNorm = 0;
  for (const value of left.values()) leftNorm += value * value;
  for (const value of right.values()) rightNorm += value * value;
  for (const [term, value] of left) dot += value * (right.get(term) ?? 0);
  if (leftNorm === 0 || rightNorm === 0) return 0;
  return 10 * (dot / Math.sqrt(leftNorm * rightNorm));
}

function sparseConceptVector(value: string) {
  const vector = new Map<string, number>();
  for (const token of tokenize(expandQuery(normalize(value)))) {
    const concept = conceptOf.get(token) ?? token;
    vector.set(concept, (vector.get(concept) ?? 0) + 1);
  }
  return vector;
}

function matchingAssumptions(document: SearchDocument, tokens: string[], claimId: string | null) {
  const scored = document.assumptions
    .map((assumption) => {
      const words = normalize(`${assumption.name} ${assumption.statement}`).split(" ").filter(Boolean);
      let score = 0;
      for (const token of tokens) {
        if (words.some((word) => sameWord(word, token))) score += 1;
      }
      return { assumption, score };
    })
    .filter((item) => item.score > 0)
    .sort((a, b) => b.score - a.score || a.assumption.name.localeCompare(b.assumption.name));

  const matched = scored.slice(0, 3).map((item) => item.assumption);
  const claim = document.claims.find((item) => item.id === claimId);
  const depended = claim
    ? claim.dependsOn
        .map((id) => document.assumptions.find((item) => item.id === id))
        .filter((item) => item !== undefined)
    : [];
  const chosen = matched.length > 0 ? matched : depended.slice(0, 3);
  return chosen.map((assumption) => ({
    id: assumption.id,
    name: assumption.name,
    sensitivity: assumption.sensitivity,
  }));
}

function bestClaim(document: SearchDocument, tokens: string[]) {
  let best: SearchDocument["claims"][number] | null = null;
  let bestScore = 0;
  for (const claim of document.claims) {
    const words = normalize(claim.text).split(" ").filter(Boolean);
    let score = 0;
    for (const token of tokens) {
      if (words.some((word) => sameWord(word, token))) score += 1;
    }
    if (score > bestScore) {
      best = claim;
      bestScore = score;
    }
  }
  if (!best || bestScore === 0) return null;
  return {
    id: best.id,
    claim: best.text,
    claim_type: "conditional" as const,
    evidence_status: "modelled" as const,
    href: best.href,
  };
}

function expandQuery(normalized: string) {
  const additions: string[] = [];
  const add = (phrase: string, concepts: string) => {
    if (normalized.includes(phrase)) additions.push(concepts);
  };
  add("where will people live", "housing");
  add("where people live", "housing");
  add("property values", "housing");
  add("real estate", "housing");
  add("dwelling occupancy", "housing");
  add("live longer", "ageing");
  add("longer lives", "ageing");
  add("longer life", "ageing");
  add("nation ages", "ageing");
  add("society ages", "ageing");
  add("demographic contraction", "population decline");
  add("fewer people", "population decline");
  add("births fall", "population decline");
  add("headcount drops", "population decline");
  return additions.length > 0 ? `${normalized} ${additions.join(" ")}` : normalized;
}

function distinctConcepts(tokens: string[]) {
  const seen = new Set<string>();
  const unique: string[] = [];
  for (const token of tokens) {
    const key = conceptOf.get(token) ?? token;
    if (seen.has(key)) continue;
    seen.add(key);
    unique.push(token);
  }
  return unique;
}

function matchWeight(word: string, token: string, weight: number) {
  if (word === token || pluralOf(word, token)) return weight;
  if (sameConcept(word, token)) return Math.max(1, weight - 1);
  return 0;
}

function pluralOf(word: string, token: string) {
  return (word.endsWith("s") && word.slice(0, -1) === token && token.length >= 4) ||
    (token.endsWith("s") && token.slice(0, -1) === word && word.length >= 4);
}

function sameWord(word: string, token: string) {
  return matchWeight(word, token, 1) > 0;
}

function sameConcept(word: string, token: string) {
  const left = conceptOf.get(word);
  return left !== undefined && left === conceptOf.get(token) && word !== token;
}

function normalize(value: string) {
  return value
    .toLowerCase()
    .replace(/['’]/g, "")
    .replace(/[^a-z0-9]+/g, " ")
    .trim();
}
