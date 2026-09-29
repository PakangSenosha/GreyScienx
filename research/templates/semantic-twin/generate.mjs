import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import yaml from "js-yaml";
import { researchObjects } from "../../../lib/research/registry.ts";

if (!process.argv.includes("--force")) {
  console.error(
    "Published semantic-twin forms are the authoring source. Edit research/templates/semantic-twin/published, then run node research/templates/semantic-twin/compile.mjs. Pass --force to overwrite those forms from the live registry.",
  );
  process.exit(1);
}

const here = path.dirname(fileURLToPath(import.meta.url));
const outputDir = path.join(here, "published");

fs.mkdirSync(outputDir, { recursive: true });
for (const name of fs.readdirSync(outputDir)) {
  if (name.endsWith(".yaml") || name.endsWith(".yml")) {
    fs.rmSync(path.join(outputDir, name));
  }
}

function unique(values) {
  return [...new Set(values.filter((value) => value !== null && value !== undefined && value !== ""))];
}

function assumptionToForm(item) {
  return {
    id: item.local_id,
    canonical_id: item.id,
    name: item.name,
    statement: item.statement,
    value: item.value,
    unit: item.unit,
    value_type: item.value === null ? "qualitative" : "declared",
    status: "model_assumption",
    provenance: item.provenance,
    source_ids: [],
    evidence_strength: item.evidence_strength,
    sensitivity: item.sensitivity,
    alternatives: item.alternatives,
  };
}

function modelToForm(item) {
  return {
    id: item.local_id,
    canonical_id: item.id,
    name: item.name,
    purpose: item.statement,
    model_class: null,
    statement: item.statement,
    inputs: [],
    outputs: [],
    time_step: null,
    implementation_file: null,
    version: "1.0",
  };
}

function resultToForm(item) {
  return {
    id: item.local_id,
    canonical_id: item.id,
    statement: item.statement,
    value: item.value,
    unit: item.unit,
    price_year: null,
    year_or_period: null,
    scenario_id: item.scenario,
    model_id: null,
    evidence_status: item.evidence_status,
    uncertainty: null,
    sensitivity: null,
    source_data_ids: [],
    reproducible_from: [],
  };
}

function claimToForm(item) {
  return {
    id: item.local_id,
    canonical_id: item.id,
    claim: item.claim,
    claim_type: item.claim_type,
    status: item.status,
    evidence_status: item.evidence_status,
    confidence: item.confidence,
    depends_on_assumptions: item.depends_on,
    derived_from_results: item.results,
    supported_by_sources: [],
    contradicted_by_sources: [],
    qualifies_claims: [],
    contradicted_claims: [],
    main_limitation: item.main_limitation,
    sensitivity: item.sensitivity,
    retrieval_text: item.claim,
    citation_text: `GreyScienx, ${item.id}, version ${item.version}.`,
    href: item.href,
  };
}

function sourceToRegister(item) {
  return {
    id: item.id,
    type: item.type,
    title: item.title,
    author_or_publisher: "GreyScienx",
    date: null,
    url: item.href,
    access_date: null,
    locator: `${item.pages} pages; ${item.size}`,
    supports: [],
    contradicts: [],
    note: "Published manuscript used for the semantic-twin extraction. External references remain represented in the manuscript unless separately registered.",
  };
}

function relatedStudyToForm(item) {
  return {
    id: item.id,
    slug: item.slug,
    title: item.title,
    href: item.href,
    relationship: "same_series",
  };
}

function buildForm(study) {
  const extracted = study.extraction_status === "partial" || study.extraction_status === "full_text_claim_led";
  const claimLimitations = unique(study.claims.map((claim) => claim.main_limitation));
  const assumptions = study.assumptions.map(assumptionToForm);
  const results = study.results.map(resultToForm);
  const claims = study.claims.map(claimToForm);
  const models = study.models.map(modelToForm);

  return {
    schema_version: "GreyResearchForm 1.0",
    target_object_schema: study.schema_version,
    identity: {
      id: study.id,
      slug: study.slug,
      title: study.title,
      subtitle: null,
      series_id: `${study.id.split("-")[0]}`,
      series_slug: study.series_slug,
      series_title: study.series_title,
      series_number: study.series_number,
      paper_number: study.paper_number,
      version: study.version,
      status: study.status,
      language: "en-ZA",
      date_created: null,
      date_modified: study.date_modified,
      date_published: null,
      canonical_url: study.links.html,
      previous_version: null,
      supersedes: [],
      superseded_by: [],
    },
    responsibility: {
      organisation: "GreyScienx",
      authors: study.authors,
      contributors: [],
      reviewers: [],
      corresponding_contact: null,
      ai_assistance: {
        disclosure: study.ai_assistance.disclosure,
        literature_search: null,
        data_extraction: null,
        code_generation: null,
        statistical_analysis: null,
        figure_generation: null,
        drafting: null,
        editing: null,
        interpretation: null,
        final_review: null,
      },
    },
    classification: {
      research_type: study.research_type,
      evidence_status: study.evidence_status,
      peer_review_status: study.peer_review_status,
      external_review_status: study.external_review_status,
      reproducibility_status: extracted ? "partial" : "not_audited",
      licence: null,
      topics: study.topics,
      keywords: study.keywords,
      geographies: study.geographies,
      temporal_coverage: {
        observed_start: null,
        observed_end: null,
        model_start: null,
        model_end: null,
      },
      currencies: [],
      price_basis: null,
    },
    research_definition: {
      central_question: study.primary_question,
      short_answer: null,
      abstract: study.summary,
      motivation: null,
      decision_relevance: null,
      main_output: null,
      bundled_questions: [],
      related_questions: study.related_questions,
      exclusions: [],
      unit_of_analysis: null,
      population_or_system: null,
      comparator: null,
      baseline: null,
      counterfactual: study.research_type === "counterfactual" ? null : "not_applicable",
      causal_scope: "Treat the study as modelled exploratory research unless the manuscript explicitly establishes another evidentiary status.",
    },
    epistemic_contract: {
      observed_facts: [],
      derived_facts: [],
      modelled_outputs: study.results.map((item) => item.id),
      interpretations: [],
      normative_judgements: [],
      unresolved_questions: [],
      confidence_statement: extracted
        ? "Only the registered conditional claims have been extracted. Read each with its dependencies and limitation."
        : "No claim-level extraction is registered for this manuscript.",
    },
    model: {
      models,
      assumptions,
      parameters: [],
      variables: [],
      equations: [],
      constraints: [],
      mechanisms: [],
      calibration: { method: null, target_ids: [], notes: null },
      validation: { internal_checks: [], external_benchmarks: [], holdout_tests: [] },
    },
    scenarios: [],
    data: {
      datasets: [],
      source_register: study.sources.map(sourceToRegister),
      provenance_notes: [],
    },
    results: {
      result_register: results,
      headline_results: [],
      sensitivity_results: [],
      robustness_results: [],
      negative_or_null_results: [],
    },
    claims: { claim_register: claims },
    distribution_and_welfare: {
      affected_groups: [],
      incidence: [],
      immediate_beneficiaries: [],
      immediate_cost_bearers: [],
      future_beneficiaries: [],
      future_cost_bearers: [],
      geographic_distribution: [],
      intergenerational_effects: [],
      welfare_metrics: [],
      rights_and_ethics: [],
      political_economy: [],
    },
    limitations_and_risks: {
      main_limitation: claimLimitations.length === 1 ? claimLimitations[0] : null,
      limitations: claimLimitations,
      data_gaps: [],
      model_risks: [],
      implementation_risks: [],
      external_validity_limits: [],
      misuse_risks: [
        "Do not present a modelled scenario as an observed outcome or forecast.",
        "Do not report the catalogue description as a finding.",
      ],
      falsification_conditions: [],
      update_triggers: [],
    },
    artifacts: {
      manuscript: {
        source_markdown: null,
        pdf: study.links.pdf,
        html: study.links.html,
        clean_markdown: study.links.markdown,
      },
      tables: [],
      figures: [],
      code: [],
      model_files: [],
      data_files: [],
      environment_files: [],
      checksums_file: null,
    },
    reproducibility: {
      repository_url: null,
      code_available: null,
      data_available: null,
      environment_available: null,
      random_seed: null,
      software: [],
      hardware_notes: null,
      run_command: null,
      build_command: null,
      validation_command: null,
      known_nondeterminism: [],
      reproduction_notes: "Populate from the manuscript source package during the reproducibility audit.",
    },
    relationships: {
      related_studies: study.related_studies.map(relatedStudyToForm),
      predecessor_studies: [],
      successor_studies: [],
      shared_assumptions: [],
      shared_datasets: [],
      shared_models: [],
      shared_topics: study.topics,
      critiques: [],
      forks: [],
      graph_edges: claims.flatMap((claim) => [
        ...claim.depends_on_assumptions.map((id) => ({ subject_id: claim.id, predicate: "depends_on", object_id: id, note: null })),
        ...claim.derived_from_results.map((id) => ({ subject_id: claim.id, predicate: "derived_from", object_id: id, note: null })),
      ]),
    },
    publication: {
      human_citation: study.citation.text,
      machine_citation: study.citation.machine,
      doi: null,
      isbn: null,
      rights_statement: null,
      embargo_until: null,
      links: {
        canonical: study.links.html,
        html: study.links.html,
        markdown: study.links.markdown,
        json: study.links.json,
        pdf: study.links.pdf,
        api: study.links.json,
        reproduce: null,
      },
      schema_org: {},
      sitemap: { include: true, priority: null },
      feed: { include: true },
      llms_txt: { include: true },
      content_negotiation: { html: true, markdown: true, json: true, pdf: true },
    },
    retrieval: {
      retrieval_note: study.retrieval_note,
      preferred_summary: study.summary,
      responsible_answer_template: extracted
        ? "Return only registered conditional claims, with their assumptions, results and main limitations."
        : "Describe the publication and its primary question, state that no claim-level extraction is registered, and do not infer findings from the summary.",
      chunks: [],
      question_aliases: study.related_questions,
      negative_retrieval_terms: [],
      citation_payload: {
        study_level: study.citation.machine,
        claim_level_pattern: `GreyScienx, ${study.id}:{claim_id}, version ${study.version}`,
      },
    },
    quality_control: {
      required_checks: {
        stable_ids: true,
        no_naked_claims: true,
        assumptions_linked: extracted,
        results_linked: extracted,
        sources_linked: false,
        units_complete: extracted && results.every((item) => item.unit !== null && item.unit !== ""),
        price_years_complete: false,
        scenario_labels_complete: extracted && results.every((item) => item.scenario_id !== null && item.scenario_id !== ""),
        figure_data_available: false,
        alt_text_complete: false,
        text_extraction_verified: false,
        pdf_visual_qa_complete: false,
        links_checked: false,
        reproducibility_checked: false,
        ai_disclosure_complete: study.ai_assistance.disclosure.length > 0,
        human_final_review: false,
      },
      blocking_issues: extracted
        ? ["External sources, datasets, figures, tables and reproducibility artifacts still require a manuscript audit."]
        : ["Claims, assumptions, results, models and external sources still require extraction from the published manuscript."],
      warnings: ["A published PDF does not by itself make every claim machine-audited."],
      reviewer_notes: [],
    },
    change_log: [
      {
        version: study.version,
        date: study.date_modified,
        author: "GreyScienx",
        summary: "Generated the harness intake form from the published research registry.",
        changed_ids: [
          ...models.map((item) => item.id),
          ...assumptions.map((item) => item.id),
          ...results.map((item) => item.id),
          ...claims.map((item) => item.id),
        ],
      },
    ],
  };
}

const entries = [];
for (const study of researchObjects) {
  const form = buildForm(study);
  const file = `${study.slug}.yaml`;
  fs.writeFileSync(
    path.join(outputDir, file),
    yaml.dump(form, { noRefs: true, lineWidth: -1, sortKeys: false, quotingType: '"', forceQuotes: false }),
    "utf8",
  );
  entries.push({
    id: study.id,
    slug: study.slug,
    title: study.title,
    series_slug: study.series_slug,
    series_title: study.series_title,
    paper_number: study.paper_number,
    version: study.version,
    extraction_status: study.extraction_status,
    file,
  });
}

const manifest = {
  schema_version: "GreyResearchFormManifest 1.0",
  generated_from: "lib/research/registry.ts",
  generated_date: new Date().toISOString().slice(0, 10),
  published_study_count: entries.length,
  studies: entries,
};

fs.writeFileSync(
  path.join(outputDir, "manifest.yaml"),
  yaml.dump(manifest, { noRefs: true, lineWidth: -1, sortKeys: false, quotingType: '"', forceQuotes: false }),
  "utf8",
);

console.log(`Generated ${entries.length} published GreyResearchForm files in ${outputDir}`);
