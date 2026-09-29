# GreyScienx semantic-twin research form

This directory contains a bare-bones authoring form for research that will later enter the GreyScienx AI-first harness.

## Files

- `grey-research-form.template.yaml` is the reusable blank form.
- `published/manifest.yaml` indexes every paper currently published in `lib/catalog.ts`.
- `published/<paper-slug>.yaml` is the complete intake form for one published paper.
- `editorial-review-manifest.json` records the publisher review attestation applied to the current published corpus.
- `profiles/<slug>.yaml` is the semantic twin for a published author. `compile-profiles.mjs` writes `lib/research/extractions/from-profiles.ts`. The founder page, Markdown biography, and profile API read that file. Empty biography fields are not left blank: an unpublished fact is written as an absence.
- `generate.mjs` regenerates the published forms from the live research registry.

## Intended flow

1. Copy the blank form for a new study, or regenerate published forms from the live registry.
2. Assign a stable study ID, slug and version before assigning claim, assumption, result, model, dataset, table or figure IDs.
3. Populate observed facts and source records before numerical modelling.
4. Keep observed facts, derived facts, modelled outputs, interpretations and normative judgements separate.
5. Link each claim to its assumptions, results and sources.
6. Leave unknown values as `null`; never use a plausible-looking placeholder number.
7. Block publication while any required quality-control item remains false or any blocking issue remains unresolved.
8. Compile the completed form into the public GreyResearchObject, clean Markdown, HTML, JSON, PDF metadata, retrieval chunks and claim graph.

## Relationship to the current harness

The existing `lib/research/schema.ts` describes the public `GreyResearchObject 1.2`. This form is deliberately broader: it is an editorial and reproducibility intake object from which the public object is derived. Version 1.1 added answer blocks, entities, methods, datasets, figures, tables, reproducibility, editorial status, richer sources and stable sub-object links. Version 1.2 adds a checksum-addressed complete Markdown manuscript, its heading index, full-text API retrieval, and PDF/source parity auditing.

The direct mappings include:

- `identity`, `classification` and `research_definition` -> study metadata;
- `model.assumptions` -> `assumptions`;
- `model.models` -> `models`;
- `results.result_register` -> `results`;
- `claims.claim_register` -> `claims`;
- `data.source_register` and `artifacts` -> `sources` and downloadable research assets;
- `relationships` -> related studies and the future claim graph;
- `retrieval` -> Markdown, API, MCP and semantic-search responses;
- `publication` -> HTML, JSON, Markdown and PDF representations.

All 29 current publications have manuscript-level semantic-twin records. Each form contains registered assumptions, models, results and conditional claims. The public registry calls these records `full_text_claim_led`: the full manuscript text is available, while the separate semantic claim register intentionally includes the principal conditional claims rather than pretending every sentence is a claim. `pending` is reserved for a publication with no registered claim extraction or full-text twin.

Manuscript extraction is distinct from reproducibility and editorial review. A form records `reproduced` when an executable model has regenerated a structurally identical primary JSON result from a temporary package copy, `source_package_available` when machine-readable files exist without an executable reproduced model, and `manuscript_only` otherwise. All 29 current model records reproduce their registered JSON baselines. Older calculation scripts stored at the source root are mapped to their study packages through `model-reproduction-manifest.json`. External-source normalisation, live-link checking, automated PDF rendering and publisher final review remain separately recorded quality-control checks. The current publisher attestation marks all 29 papers reviewed and accepts source candidates as contextual references without treating them as independent empirical proof of modelled outputs.

The fill workflow normalises cited HTTP(S) links from each manuscript into the source register without automatically assigning those contextual sources to a claim. `scripts/verify-research-corpus.mjs` validates stable identifiers, claim dependencies, package hashes and public copies. `scripts/reproduce-models.mjs` executes available Python models in temporary directories and compares generated JSON with the registered baselines.

## Compile onto the site

`published/<paper-slug>.yaml` is the authoring source for claims, assumptions, results and models. From the repository root:

```powershell
node research/templates/semantic-twin/compile.mjs
```

That writes `lib/research/extractions/from-forms.ts`, `from-graph.ts`, `from-packages.ts`, and `from-manuscripts.ts`, which the public registry loads. A form with an empty claim register would stay a pending study; the current 29-paper corpus has no such forms.

Run the integrity and model checks from the repository root:

```powershell
npm run research:check
npm run research:reproduce
npm run research:audit-twins
npm run research:audit-visuals
npm run research:suggest-sources
npm run deploy:validate
npm run indexnow:submit
```

The generated reports are `verification-report.json`, `model-reproduction-report.json`, `manuscript-twin-report.json`, `automated-pdf-render-report.json`, `claim-source-candidate-report.json`, `live-deployment-validation-report.json`, and `indexnow-submission-report.json` in this directory. The manuscript audit uses Poppler to compare the complete Markdown source with extractable text in the published PDF. The render audit rasterises every PDF page and records page counts, dimensions and ink-density observations. The source-candidate report ranks contextual references using manuscript proximity and lexical overlap. The live validator checks public DNS, the `www` redirect, HTTPS, cache behaviour, all sitemap URLs, discovery surfaces, search, content negotiation and MCP JSON-RPC/SSE behaviour against the deployed domain. The IndexNow submitter validates the public key and submits the unique canonical sitemap URLs. Static integrity, PDF/source parity, page rendering and executable reproduction remain machine checks; the publisher review decision is recorded separately in the editorial manifest.

Regenerating the forms from the registry overwrites authoring work. That path requires `--force`:

```powershell
node --import ./scripts/register-ts.mjs research/templates/semantic-twin/generate.mjs --force
```
