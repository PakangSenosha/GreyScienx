import { z } from "zod";

export const researchTypeSchema = z.enum(["exploratory_simulation", "counterfactual"]);

export type ResearchType = z.infer<typeof researchTypeSchema>;

export const authorSchema = z.object({
  name: z.string(),
  affiliation: z.string(),
  slug: z.string(),
});

export const sourceSchema = z.object({
  id: z.string(),
  type: z.string(),
  title: z.string(),
  href: z.string().nullable(),
  author_or_publisher: z.string().optional(),
  date: z.string().optional(),
  locator: z.string().optional(),
  note: z.string().optional(),
  supports: z.array(z.string()).optional(),
  contradicts: z.array(z.string()).optional(),
  pages: z.number().optional(),
  size: z.string().optional(),
  media_type: z.string().optional(),
});

export const relatedStudySchema = z.object({
  id: z.string(),
  slug: z.string(),
  title: z.string(),
  href: z.string(),
});

export const linkSchema = z.object({
  html: z.string(),
  markdown: z.string(),
  manuscript: z.string(),
  json: z.string(),
  pdf: z.string(),
});

export const manuscriptSchema = z.object({
  study_id: z.string(),
  source_path: z.string(),
  source_sha256: z.string().regex(/^[a-f0-9]{64}$/),
  source_bytes: z.number().int().positive(),
  character_count: z.number().int().positive(),
  word_count: z.number().int().positive(),
  headings: z.array(
    z.object({
      level: z.number().int().min(1).max(6),
      title: z.string(),
      slug: z.string(),
      line: z.number().int().positive(),
    }),
  ),
});

export const citationSchema = z.object({
  machine: z.string(),
  text: z.string(),
});

export const assumptionSchema = z.object({
  id: z.string(),
  local_id: z.string(),
  name: z.string(),
  statement: z.string(),
  value: z.string().nullable(),
  unit: z.string().nullable(),
  type: z.literal("model assumption"),
  provenance: z.string(),
  evidence_strength: z.string(),
  sensitivity: z.enum(["low", "moderate", "high"]),
  alternatives: z.array(z.string()),
  href: z.string(),
});

export const resultSchema = z.object({
  id: z.string(),
  local_id: z.string(),
  statement: z.string(),
  value: z.string(),
  unit: z.string(),
  scenario: z.string(),
  evidence_status: z.literal("modelled"),
  href: z.string(),
});

export const modelSchema = z.object({
  id: z.string(),
  local_id: z.string(),
  name: z.string(),
  statement: z.string(),
  href: z.string(),
});

export const claimSchema = z.object({
  id: z.string(),
  local_id: z.string(),
  claim: z.string(),
  claim_type: z.literal("conditional"),
  status: z.literal("conditional"),
  evidence_status: z.literal("modelled"),
  confidence: z.null(),
  depends_on: z.array(z.string()),
  result: z.string(),
  results: z.array(z.string()),
  sensitivity: z.enum(["low", "moderate", "high"]),
  main_limitation: z.string(),
  source_study: z.string(),
  version: z.literal("1.0"),
  href: z.string(),
  supported_by: z.array(z.string()),
  contradicted_by: z.array(z.string()),
  qualifies: z.array(z.string()),
  contradicts: z.array(z.string()),
});

export type Assumption = z.infer<typeof assumptionSchema>;
export type ResultRecord = z.infer<typeof resultSchema>;
export type ModelRecord = z.infer<typeof modelSchema>;
export type Claim = z.infer<typeof claimSchema>;

export const researchObjectSchema = z.object({
  schema_version: z.literal("GreyResearchObject 1.2"),
  id: z.string(),
  slug: z.string(),
  series_slug: z.string(),
  series_title: z.string(),
  series_number: z.string(),
  paper_number: z.string(),
  title: z.string(),
  version: z.literal("1.0"),
  status: z.literal("published"),
  primary_question: z.string(),
  summary: z.string(),
  topics: z.array(z.string()),
  geographies: z.array(z.string()),
  keywords: z.array(z.string()),
  related_questions: z.array(z.string()),
  answer: z
    .object({
      conditional_answer: z.string(),
      evidence_status: z.string(),
      assumption_ids: z.array(z.string()),
      result_ids: z.array(z.string()),
      main_limitation: z.string(),
      sensitivity: z.string(),
    })
    .nullable(),
  entities: z.array(z.string()),
  methods: z.array(z.record(z.string(), z.unknown())),
  parameters: z.array(z.record(z.string(), z.unknown())),
  equations: z.array(z.string()),
  scenarios: z.array(z.record(z.string(), z.unknown())),
  unresolved_questions: z.array(z.string()),
  research_type: researchTypeSchema,
  evidence_status: z.literal("modelled"),
  peer_review_status: z.literal("none"),
  external_review_status: z.literal("none"),
  ai_assistance: z.object({
    disclosure: z.string(),
    itemised: z.literal(false),
  }),
  date_modified: z.string(),
  date_note: z.string(),
  authors: z.array(authorSchema),
  extraction_status: z.enum(["pending", "partial", "full_text_claim_led"]),
  manuscript: manuscriptSchema,
  claims: z.array(claimSchema),
  assumptions: z.array(assumptionSchema),
  results: z.array(resultSchema),
  models: z.array(modelSchema),
  sources: z.array(sourceSchema),
  datasets: z.array(z.record(z.string(), z.unknown())),
  figures: z.array(z.record(z.string(), z.unknown())),
  tables: z.array(z.record(z.string(), z.unknown())),
  reproducibility: z.object({
    code_available: z.boolean(),
    data_available: z.boolean(),
    environment_available: z.boolean(),
    random_seed: z.string(),
    software: z.array(z.string()),
    repository_url: z.string().nullable(),
  }),
  editorial: z.object({
    required_checks: z.record(z.string(), z.unknown()),
    blocking_issues: z.array(z.string()),
    warnings: z.array(z.string()),
    change_log: z.array(z.record(z.string(), z.unknown())),
  }),
  related_studies: z.array(relatedStudySchema),
  links: linkSchema,
  citation: citationSchema,
  retrieval_note: z.string(),
});

export type ResearchObject = z.infer<typeof researchObjectSchema>;

export const searchHitSchema = z.object({
  id: z.string(),
  slug: z.string(),
  title: z.string(),
  primary_question: z.string(),
  summary: z.string(),
  research_type: researchTypeSchema,
  evidence_status: z.literal("modelled"),
  series_slug: z.string(),
  series_title: z.string(),
  canonical_url: z.string(),
  version: z.literal("1.0"),
  date_modified: z.string(),
  most_relevant_claim: z
    .object({
      id: z.string(),
      claim: z.string(),
      claim_type: z.literal("conditional"),
      evidence_status: z.literal("modelled"),
      href: z.string(),
    })
    .nullable(),
  key_assumptions: z.array(
    z.object({
      id: z.string(),
      name: z.string(),
      sensitivity: z.enum(["low", "moderate", "high"]),
    }),
  ),
});

export type SearchHit = z.infer<typeof searchHitSchema>;
