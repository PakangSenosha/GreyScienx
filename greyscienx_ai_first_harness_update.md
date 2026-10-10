# GreyScienx AI-First / Harness-Ready Website Update

## Purpose

GreyScienx should not host its own AI assistant.

Existing systems such as ChatGPT, Claude, Gemini, and future AI agents already provide the intelligence layer, user interface, model maintenance, multimodal interaction, and conversational experience.

GreyScienx should instead become a **machine-readable research platform** that these systems can discover, retrieve from, cite, and interact with.

The architectural principle is:

```text
GreyScienx ≠ AI chatbot

GreyScienx = research corpus + research objects + standards + provenance + search + APIs + MCP + community
```

The website remains the human-readable interface.

The same underlying research should also be available to:

- search engines
- AI search systems
- ChatGPT
- Claude
- Gemini
- local AI agents
- MCP clients
- future autonomous research agents
- external applications
- academic tools

---

# 1. Core Product Principle

GreyScienx should be designed as:

```text
Research Object
    |
    +--> Human webpage
    +--> Markdown
    +--> JSON
    +--> REST API
    +--> MCP
    +--> Search index
    +--> RSS / feeds
    +--> PDF
    +--> Dataset
    +--> Code / reproducibility artifacts
```

The research object is the source of truth.

The webpage is only one rendering.

---

# 2. Do Not Build an AI Chatbot on GreyScienx

GreyScienx should not attempt to recreate ChatGPT or another general conversational interface.

Reasons:

- major AI platforms are already highly capable
- they are continuously maintained and improved
- users already understand their interfaces
- model costs should not become a GreyScienx operating burden
- GreyScienx should remain model-agnostic
- the research corpus should be usable by any future AI system
- intelligence should stay on the user's side wherever practical

Analogy:

```text
Website : Chrome
GreyScienx : ChatGPT / Claude / Gemini
```

A website does not need to build its own browser.

GreyScienx does not need to build its own general AI.

---

# 3. Main Objective

The target experience is not:

```text
@GreyScienx find me a study about population decline.
```

The ideal experience is:

```text
User:
What happens to housing if population declines but people live longer?

AI:
GreyScienx has a relevant model examining this question...
```

The user should not need to know GreyScienx exists beforehand.

This is the main AI-discovery goal.

---

# 4. Three Discovery Modes

## 4.1 Brand Discovery

The user explicitly asks for GreyScienx.

Example:

```text
Search GreyScienx for studies about housing and population decline.
```

This is the easiest mode.

## 4.2 Installed Harness / Plugin Discovery

The user has connected or installed GreyScienx in an AI environment.

The AI can call GreyScienx tools when relevant.

Example:

```text
User:
Has anyone modelled whether living with your parents for three years after employment changes lifetime wealth?
```

The AI may identify:

```text
The First Three Years Advantage
```

without the user naming GreyScienx.

## 4.3 Open-Web Semantic Discovery

The user has not installed GreyScienx.

The AI searches the web and discovers a relevant GreyScienx page because the page is:

- well indexed
- semantically explicit
- structured
- readable
- relevant
- richly interconnected
- clearly titled
- answerable
- citation-friendly

This is the AI-era equivalent of traditional SEO.

---

# 5. Intent SEO

GreyScienx should optimise for questions, concepts, and research intent.

Do not focus only on brand keywords.

Examples of target discovery queries:

```text
population decline property prices
living with parents lifetime wealth
cohabitation household economics
South Africa R350 grant industrialisation
inheritance racial wealth South Africa
retirement age longevity population decline
probability of winning R100000 gambling
housing demand falling population longer life expectancy
informal traders South Africa economic infrastructure
South Africa relevance in African economic growth
civil war economic counterfactual South Africa
```

A GreyScienx study should be discoverable from the underlying question even if the user has never heard of the study title.

---

# 6. GreyResearchObject v1

Every research item should be stored as a structured object.

Suggested base schema:

```text
ResearchObject
├── id
├── slug
├── title
├── subtitle
├── primary_question
├── short_answer
├── abstract
├── authors[]
├── contributors[]
├── date_created
├── date_modified
├── version
├── status
├── research_type
├── evidence_status
├── ai_assistance
├── peer_review_status
├── external_review_status
│
├── related_questions[]
├── topics[]
├── entities[]
├── geographies[]
├── keywords[]
│
├── hypotheses[]
├── assumptions[]
├── claims[]
├── equations[]
├── parameters[]
├── methods[]
├── datasets[]
├── models[]
├── experiments[]
├── results[]
├── sensitivity_analyses[]
├── counterarguments[]
├── limitations[]
├── conclusions[]
│
├── sources[]
├── citations[]
├── figures[]
├── tables[]
├── code_artifacts[]
├── downloadable_files[]
├── reproducibility[]
│
├── critiques[]
├── revisions[]
├── related_studies[]
├── contradictions[]
├── superseded_claims[]
│
└── provenance
```

---

# 7. Stable Research Identifiers

Every study and important sub-object should have a stable identifier.

Example:

```text
GSX:POP-004
GSX:POP-004:A07
GSX:POP-004:C19
GSX:POP-004:R12
GSX:POP-004:M03
```

Possible meaning:

```text
GSX:POP-004       Study
A07               Assumption 7
C19               Claim 19
R12               Result 12
M03               Model 3
```

These IDs should remain stable across revisions.

They should be usable in:

- webpages
- Markdown
- APIs
- MCP
- citations
- critiques
- revisions
- external tools

---

# 8. Claim-Level URLs

Do not force AI systems to cite an entire paper for a single claim.

Support URLs such as:

```text
/research/pop-004
/research/pop-004/claims/C19
/research/pop-004/assumptions/A07
/research/pop-004/results/R12
/research/pop-004/models/M03
```

Each sub-object page should contain:

- the object text
- its study
- supporting evidence
- dependencies
- sources
- current version
- critique status
- relevant limitations

---

# 9. Question Graph

Every study should expose the questions it answers.

Example:

```text
Study:
The Demographic Housing Paradox

Primary question:
Can housing scarcity rise while population falls?

Related questions:
- What happens to house prices when population declines?
- Does increasing longevity reduce housing turnover?
- Can household formation increase while population falls?
- Does falling household size offset demographic decline?
- What happens to inheritance when people live longer?
- Are longer mortgages justified by longer lifespans?
- Can housing remain scarce in a shrinking country?
```

These should be stored as structured data, not only prose.

---

# 10. Topic and Entity Graph

Each study should be connected to explicit concepts.

Example:

```text
Topics:
- housing
- demography
- mortgages
- inheritance
- longevity
- population decline
- household formation
- property investment

Geographies:
- South Africa
- Gauteng
- Johannesburg

Methods:
- cohort simulation
- scenario modelling
- stock-flow modelling
```

This makes semantic retrieval easier.

---

# 11. Assumptions as First-Class Objects

Assumptions must not be buried inside prose.

Example:

```json
{
  "id": "GSX:POP-004:A07",
  "name": "Average household size declines",
  "value": 2.3,
  "unit": "persons per household",
  "type": "model assumption",
  "provenance": "demographic scenario",
  "evidence_strength": "moderate",
  "sensitivity": "high",
  "alternatives": [2.0, 2.6, 3.0]
}
```

Every result should be able to identify which assumptions materially affect it.

---

# 12. Conditional Conclusions

GreyScienx should not expose conclusions without dependencies.

Example:

```json
{
  "claim": "Housing scarcity can persist despite population decline.",
  "status": "conditional",
  "depends_on": [
    "GSX:POP-004:A04",
    "GSX:POP-004:A07",
    "GSX:POP-004:A11"
  ],
  "result": "GSX:POP-004:R19",
  "sensitivity": "high",
  "evidence_status": "modelled"
}
```

AI systems should be able to retrieve:

```text
Conclusion
+
Conditions
+
Evidence status
+
Sensitivity
```

together.

---

# 13. Human Page Structure

Every human-facing research page should have a predictable structure.

Recommended order:

```text
Title
Primary question
Short answer
Evidence status
Study type
Last updated
Authors / contributors

Abstract

What was asked?
Why does it matter?

Assumptions
Methods
Data
Model
Results
Sensitivity
Counterarguments
Limitations
Conclusion

Reproducibility
Sources
Related research
External critiques
Revision history
```

---

# 14. Answer-Sized Research Blocks

Every study should expose a concise machine-readable summary.

Example:

```text
Question:
Can housing scarcity increase while population falls?

Conditional answer:
Yes. In scenarios where average household size declines and
longer lifespans keep existing dwellings occupied for longer,
household demand can remain high even while total population falls.

Key dependencies:
- mortality
- household size
- construction
- migration

Evidence status:
Modelled / exploratory

Main limitation:
The result depends strongly on assumptions about household formation.
```

This block should be reusable by:

- search snippets
- AI tools
- MCP
- structured data
- social cards
- feeds

---

# 15. Clean Markdown Representation

Every research page should have a clean Markdown version.

Example:

```text
/research/demographic-housing-paradox.md
```

The Markdown version should contain:

- no menus
- no decorative UI
- no animation
- no unrelated navigation
- no marketing copy

It should contain the research itself in a clean, structured form.

---

# 16. JSON Representation

Every study should have a JSON representation.

Example:

```text
/api/v1/research/demographic-housing-paradox
```

Possible response:

```json
{
  "id": "GSX:POP-004",
  "title": "The Demographic Housing Paradox",
  "primary_question": "Can housing scarcity increase while population falls?",
  "status": "published",
  "research_type": "simulation",
  "evidence_status": "exploratory",
  "version": "1.2",
  "claims": [],
  "assumptions": [],
  "results": [],
  "sources": []
}
```

---

# 17. Content Negotiation

Where practical, allow the same resource to be requested in different forms.

Possible representations:

```text
text/html
text/markdown
application/json
application/pdf
```

Example conceptual behaviour:

```text
/research/pop-004
```

can resolve to different formats depending on request headers or explicit extension.

---

# 18. llms.txt

Add:

```text
https://greyscienx.com/llms.txt
```

Suggested initial content:

```md
# GreyScienx

> GreyScienx publishes open exploratory computational research,
> mathematical models, simulations, counterfactual studies,
> socioeconomic analyses, and reproducible research objects.

## Research
- https://greyscienx.com/research/index.md
- https://greyscienx.com/series/index.md

## Standards
- https://greyscienx.com/standards/index.md
- https://greyscienx.com/standards/mathematical-writing.md

## Machine Interfaces
- https://greyscienx.com/api/openapi.json
- https://greyscienx.com/mcp

## About
- https://greyscienx.com/about.md
- https://greyscienx.com/methodology.md
```

`llms.txt` should supplement, not replace, ordinary SEO, sitemaps, structured data, and APIs.

---

# 19. OpenAPI

Publish a machine-readable API specification.

Suggested location:

```text
/api/openapi.json
```

Initial read-only endpoints:

```text
GET /api/v1/research
GET /api/v1/research/{id}
GET /api/v1/research/{id}/claims
GET /api/v1/research/{id}/assumptions
GET /api/v1/research/{id}/results
GET /api/v1/research/{id}/sources
GET /api/v1/research/{id}/datasets
GET /api/v1/research/{id}/related
GET /api/v1/search
GET /api/v1/topics
GET /api/v1/series
```

Later authenticated endpoints may include:

```text
POST /api/v1/submissions
POST /api/v1/critiques
POST /api/v1/forks
POST /api/v1/revisions
```

---

# 20. GreyScienx MCP

Create an MCP server.

Possible endpoint:

```text
https://greyscienx.com/mcp
```

or:

```text
https://mcp.greyscienx.com
```

Start read-only.

Initial tools:

```text
search_research
get_study
get_claim
get_assumptions
get_results
get_sources
get_dataset
get_related_research
get_series
get_topic
```

Later:

```text
compare_studies
trace_claim
find_counterarguments
get_model_spec
get_reproducibility_package
```

Authenticated community actions may later include:

```text
submit_research
submit_critique
fork_study
propose_revision
respond_to_critique
```

---

# 21. MCP Tool Descriptions Matter

Use semantically rich tool descriptions.

Bad:

```text
search()
```

Better:

```text
search_research

Search GreyScienx exploratory research, mathematical models,
simulations, counterfactual studies, socioeconomic analyses,
demographic models, and public-policy scenarios.

Use when the user asks whether a question has been modelled,
wants evidence or assumptions relevant to a research question,
or wants structured exploratory work on a topic covered by GreyScienx.
```

The description should help AI systems understand when GreyScienx is relevant.

---

# 22. Semantic Search

Do not index only whole articles.

Index:

- titles
- questions
- claims
- assumptions
- methods
- results
- conclusions
- limitations
- source abstracts
- related questions

Semantic search should return research objects, not only text chunks.

Example query:

```text
What happens to houses when people live longer but population declines?
```

Potential match:

```text
The Demographic Housing Paradox
```

even if the wording differs.

---

# 23. Claim Graph

Build a research graph over time.

Conceptual relationships:

```text
Claim
├── supported_by -> Evidence
├── derived_from -> Result
├── depends_on -> Assumption
├── generated_by -> Model
├── contradicts -> Claim
├── qualifies -> Claim
├── supersedes -> Claim
├── replicated_by -> Study
└── challenged_by -> Critique
```

This should become a major long-term GreyScienx asset.

---

# 24. Research Graph Example

```text
Lower fertility
    |
    v
Smaller younger cohorts
    |
    v
Potentially fewer future workers
    |
    +----------------------+
    |                      |
    v                      v
Pension pressure      Housing demand pressure

Longer lifespan
    |
    +----------------------+
    |                      |
    v                      v
Longer labour participation     Longer dwelling occupation
```

GreyScienx should eventually understand that separate studies interact through shared claims and assumptions.

---

# 25. Epistemic Metadata

Every study should expose its epistemic status.

Example:

```text
Study type: Simulation
Evidence status: Exploratory
External critique: 2
Peer review: None
AI assistance: Substantial
Data: Public secondary data
Reproducible: Yes
Code available: Yes
Version: 1.3
Last revised: 2026-09-24
```

This metadata should be available in:

- webpage
- Markdown
- JSON
- API
- MCP

---

# 26. AI Assistance Disclosure

GreyScienx should be explicit about AI participation.

Suggested fields:

```text
ai_assistance:
  literature_search: true
  code_generation: true
  statistical_analysis: true
  drafting: true
  editing: true
  interpretation: human_ai_joint
  final_review: human
```

Do not hide AI involvement.

Do not imply AI-generated work is peer-reviewed.

---

# 27. Structured Data / JSON-LD

Every research page should expose structured metadata.

Use appropriate Schema.org types such as:

```text
ScholarlyArticle
Dataset
Person
Organization
CreativeWork
SoftwareSourceCode
```

Possible article metadata:

```text
headline
abstract
author
datePublished
dateModified
keywords
citation
isPartOf
version
license
about
spatialCoverage
temporalCoverage
associatedMedia
```

Dataset pages should separately expose dataset metadata.

---

# 28. Sitemap

Maintain dedicated sitemaps.

Possible structure:

```text
/sitemap.xml
/sitemap-research.xml
/sitemap-series.xml
/sitemap-datasets.xml
/sitemap-standards.xml
```

Every published object should have:

- canonical URL
- updated timestamp
- stable slug or ID

---

# 29. Internal Linking

GreyScienx should build topical density through strong internal links.

Example:

```text
Population decline
    ↓
Housing
    ↓
Inheritance
    ↓
Wealth
    ↓
Retirement
    ↓
Fiscal policy
```

Every paper should link to:

- related studies
- predecessor studies
- competing studies
- critiques
- shared assumptions
- related models
- relevant datasets

---

# 30. Series Pages

Series should become structured research collections.

Example:

```text
/series/population-futures
```

Expose:

- series question
- constituent studies
- shared assumptions
- shared datasets
- shared models
- unresolved questions
- contradictory findings
- current research status

---

# 31. Topic Pages

Create machine-readable topic hubs.

Examples:

```text
/topics/population-decline
/topics/cohabitation
/topics/housing
/topics/south-africa
/topics/inheritance
/topics/gambling
/topics/informal-economy
/topics/industrialisation
```

Each topic page should contain:

- concise definition
- related questions
- related studies
- relevant claims
- major assumptions
- relevant datasets
- connected topics

---

# 32. Research Discovery Page

Add a discovery interface built around questions.

Possible filters:

```text
Topic
Country
Method
Research type
Evidence status
Year
Series
Reproducibility
AI involvement
External critique
```

Search should accept natural language.

Example:

```text
How much can staying home after employment change lifetime wealth?
```

---

# 33. Search Result Objects

Search results should not return only article titles.

Return:

```text
Study
Primary question
Short answer
Study type
Evidence status
Most relevant claim
Key assumptions
Last updated
```

This helps both humans and agents judge relevance before loading the full study.

---

# 34. No Forced GreyScienx Invocation

Do not design GreyScienx so that users must type:

```text
@GreyScienx
```

Explicit invocation can remain supported.

But the long-term target is:

```text
User intent
    ↓
AI recognises relevant research need
    ↓
GreyScienx discovered or called
    ↓
Relevant research retrieved
```

The platform should be discoverable by meaning.

---

# 35. Model-Agnostic Architecture

GreyScienx must not depend on one AI company.

Target:

```text
ChatGPT --------\
Claude ----------\
Gemini -----------\
Local models ------> GreyScienx MCP / API
Future agents -----/
```

GreyScienx owns:

- research corpus
- research standards
- structured objects
- provenance
- search
- community
- hosting
- identity
- research graph

The AI provider owns:

- conversational intelligence
- reasoning
- user interface
- local context
- model improvement

---

# 36. Bring Your Own AI

A future contributor should be able to create work using:

- ChatGPT
- Claude
- Gemini
- local open models
- R
- Python
- Stata
- Julia
- spreadsheets
- manual writing

GreyScienx should accept the resulting research object regardless of tool choice.

The standard is the output format and disclosure, not the model provider.

---

# 37. Submission Architecture

Future machine submission flow:

```text
User / AI agent
    |
    v
GreyScienx MCP
    |
    v
validate_research_object()
    |
    v
provenance_check()
    |
    v
human review / moderation
    |
    v
publish()
```

Submission should not require GreyScienx-hosted inference.

---

# 38. Reproducibility Artifacts

Every computational study should support links to:

- data
- code
- model specification
- parameter file
- environment description
- random seed
- generated tables
- generated figures
- version information

Example:

```text
/research/pop-004/reproduce
```

---

# 39. Mathematical Writing Standard

GreyScienx should maintain a separate mathematical and reproducibility standard.

Possible location:

```text
/standards/mathematical-writing
```

This standard should govern:

- variable definitions
- equation numbering
- units
- parameter provenance
- distributions
- uncertainty
- simulation reporting
- sensitivity analysis
- counterfactual language
- causal language
- numerical precision
- random seeds
- data provenance
- model version
- software version
- claim traceability

The prose tone may be derived from a curated external corpus.

The mathematical reporting rules should remain explicit and versioned.

---

# 40. Prose Corpus

GreyScienx should not ask an AI to invent the house tone.

Instead:

1. curate a reference corpus of high-quality expository writing
2. use selected Wikipedia articles as the main surface-tone corpus
3. define measurable stylistic constraints
4. separate tone from reporting rules

Concept:

```text
GreyScienx prose
=
approved expository corpus
+
mathematical reporting standard
+
research-object structure
```

---

# 41. Versioning

Research and standards should be versioned.

Example:

```text
GreyResearchObject 1.0
GreyScienx Mathematical Standard 1.0
GreyScienx API v1
GreyScienx MCP v1
```

Studies:

```text
Study v1.0
Study v1.1
Study v2.0
```

Version history should remain public.

---

# 42. Critiques

A critique should itself become a structured object.

Example:

```text
Critique
├── id
├── target_study
├── target_claim
├── author
├── critique_type
├── argument
├── evidence
├── proposed_change
├── status
└── response
```

Critique types:

```text
assumption
method
data
interpretation
mathematics
source
reproducibility
scope
```

---

# 43. Forks

Eventually allow:

```text
Fork study
```

A fork should record:

```text
parent study
changed assumptions
changed data
changed methods
new results
new conclusion
```

This makes disagreement executable.

---

# 44. AI Retrieval Contract

When an AI retrieves a GreyScienx claim, return enough information to phrase it responsibly.

Suggested response:

```json
{
  "claim": "...",
  "claim_type": "conditional",
  "evidence_status": "modelled",
  "confidence": "moderate",
  "depends_on": [],
  "main_limitation": "...",
  "source_study": "...",
  "version": "1.2"
}
```

Never return a naked conclusion without its epistemic metadata.

---

# 45. Research Citation Format

Develop a stable GreyScienx citation form.

Example:

```text
GreyScienx, GSX:POP-004:C19, version 1.2
```

Human-readable citation:

```text
GreyScienx. The Demographic Housing Paradox. Claim C19. Version 1.2.
```

This is separate from external referencing styles such as APA or Harvard.

---

# 46. AI-Era SEO Checklist

Every study should have:

- clear descriptive title
- explicit primary question
- short answer
- structured abstract
- stable URL
- canonical URL
- metadata
- JSON-LD
- Markdown alternative
- JSON API representation
- topic links
- series links
- related questions
- related research
- assumption objects
- claim objects
- source links
- sitemap entry
- RSS/feed inclusion
- version metadata
- last-modified timestamp
- evidence status
- reproducibility status

---

# 47. Existing GreyScienx Content Migration

For each current paper:

## Step 1

Create stable study ID.

## Step 2

Extract:

- primary question
- related questions
- abstract
- assumptions
- claims
- methods
- results
- limitations
- conclusion
- sources

## Step 3

Assign stable IDs to:

- assumptions
- claims
- results
- models

## Step 4

Generate:

- webpage
- Markdown
- JSON
- structured metadata

## Step 5

Connect related papers.

## Step 6

Add to semantic index.

---

# 48. Initial MCP v1 Scope

Do not overbuild.

Start with:

```text
search_research
get_study
get_claim
get_assumptions
get_results
get_sources
get_related_research
```

Read-only.

No central AI.

No hosted research agent.

No automatic paper generation.

No expensive inference layer.

---

# 49. Initial API v1 Scope

Start with:

```text
GET /research
GET /research/{id}
GET /research/{id}/claims
GET /research/{id}/assumptions
GET /research/{id}/results
GET /research/{id}/sources
GET /search
GET /series
GET /topics
```

---

# 50. Initial Implementation Order

## Phase 1 — Research Object

Build:

```text
GreyResearchObject v1
```

Convert current papers.

## Phase 2 — Multi-format publishing

Generate:

```text
HTML
Markdown
JSON
```

from one source.

## Phase 3 — Search and metadata

Add:

```text
semantic search
JSON-LD
sitemaps
topic pages
question graph
```

## Phase 4 — Machine discovery

Add:

```text
llms.txt
OpenAPI
```

## Phase 5 — Harness

Build:

```text
GreyScienx MCP
```

read-only.

## Phase 6 — Research graph

Connect:

```text
claims
assumptions
evidence
models
results
studies
```

## Phase 7 — Community

Add:

```text
profiles
critiques
forks
revisions
submissions
```

---

# 51. Long-Term Architecture

```text
                      ┌─────────────────┐
                      │   Researchers   │
                      │      Humans      │
                      └────────┬────────┘
                               │
                               v
                    ┌─────────────────────┐
                    │ GreyResearchObject  │
                    │        Core         │
                    └─────────┬───────────┘
                              │
          ┌───────────────────┼───────────────────┐
          │                   │                   │
          v                   v                   v
       Website            API / JSON          Markdown
          │                   │                   │
          │                   │                   │
          └─────────────┬─────┴─────────────┬────┘
                        │                   │
                        v                   v
                  Semantic Index        Claim Graph
                        │                   │
                        └─────────┬─────────┘
                                  │
                                  v
                           GreyScienx MCP
                                  │
            ┌─────────────────────┼──────────────────────┐
            │                     │                      │
            v                     v                      v
         ChatGPT               Claude                 Gemini
            │                     │                      │
            └─────────────────────┼──────────────────────┘
                                  │
                                  v
                              User intent
```

---

# 52. North-Star Principle

GreyScienx should not become:

> a website with an AI chatbot.

It should become:

> **a research network that any AI system can understand and use.**

The long-term objective is:

```text
Human can read it
+
Search engine can index it
+
AI can discover it
+
Agent can retrieve it
+
Software can interpret it
+
Another model can reproduce it
+
A community can critique and extend it
```

---

# 53. Definition of Harness-Ready

GreyScienx is harness-ready when:

- users do not need to visit the website to benefit from its research
- users do not need to know the GreyScienx brand beforehand
- AI systems can discover relevant GreyScienx studies from natural-language intent
- AI systems can retrieve precise claims rather than scraping whole webpages
- conclusions are returned with assumptions and evidence status
- studies have stable identifiers
- APIs are documented
- MCP access exists
- the system is model-agnostic
- the same research object powers every interface

---

# 54. Final Product Thesis

The website is not the product boundary.

The research corpus is.

The interface is not the moat.

The organisation, standards, corpus, provenance, research graph, and community are.

GreyScienx should therefore be built so that future users can interact with its research from whatever AI environment they already use.

The ideal request is not:

```text
Open GreyScienx.
```

It is:

```text
What happens to property values when population falls but people live longer?
```

and GreyScienx becomes relevant because it has already asked, modelled, documented, and exposed that question in a form the AI can understand.

---

# 55. Implementation Status — 28 September 2026

The AI-first harness described above is implemented in the repository for the current 29-paper corpus.

## Implemented interfaces

- GreyResearchObject records for every catalogued paper
- checksum-addressed complete Markdown manuscript twins for every PDF
- semantic-twin YAML authoring forms
- stable study, claim, assumption, result and model identifiers
- human pages for studies and each registered sub-object
- clean Markdown and JSON representations
- full-manuscript API retrieval and heading-level MCP retrieval
- HTTP content negotiation for canonical study URLs
- answer-sized conditional research blocks
- question, topic, series and research-graph records
- hybrid concept-vector research search
- claim tracing with assumptions, results, models, sources and limitations
- normalised manuscript-cited web-source registers
- claim-to-source editorial candidate worksheet with manuscript-line context
- article, claim, dataset, software, series and topic JSON-LD
- dedicated research, series, dataset and standards sitemaps
- RSS, `llms.txt` and OpenAPI discovery
- read-only MCP retrieval and comparison tools
- submission, critique, fork and revision validation
- unpublished review queues and a human-reviewed publication command
- immutable version-history routes for published machine records
- downloadable source-package files with SHA-256 checksums
- automated corpus-integrity, model-reproduction, test, lint and production-build checks
- a versioned prose-reference manifest separate from the mathematical standard
- continuous-integration configuration for the full harness

## Verified current corpus

```text
29 studies
63 conditional claims
87 assumptions
68 results
29 model records
359 registered external-source records
87 checksum-verified downloadable package files
732 research-graph edges
29 of 29 published model records reproduced their registered primary JSON baseline
29 of 29 complete Markdown sources passed automated PDF/source content-parity checks
674 of 674 pages across all 29 PDFs passed automated page-render integrity checks
63 of 63 claim records have ranked source-review candidates with manuscript-line context
302 unique external URLs checked: 250 reachable, 40 access-restricted, 12 transient or network-unverified, 0 confirmed dead links
```

Every study now has extraction status `full_text_claim_led`. This means the entire source manuscript is machine-readable and checksum-addressed, while the separate semantic claim register remains a deliberate selection of principal conditional claims rather than an automated sentence-by-sentence assertion that every line is a claim.

The link check is intentionally conservative. `access-restricted` means the publisher rejected or gated the automated request; `unverified` means a timeout, network error or transient server response prevented a result. Neither category is counted as a dead citation, and neither is treated as evidence that a source supports a claim.

## Completed editorial gates

- publisher final review is recorded for all 29 semantic records
- publisher PDF review is recorded for all 29 manuscripts; automated rendering also passed for all 674 pages
- all 63 claim-level source candidates were reviewed and accepted as contextual manuscript references, without misrepresenting them as independent empirical proof of modelled outputs

Dedicated plotting tables may still be added where useful, but every published figure now points to its registered machine-readable model-result dataset.

## Live deployment validation

The verified corpus was deployed to the Cloudflare Worker serving `greyscienx.com/*` and the `www.greyscienx.com` custom domain on 29 September 2026. The current deployed Worker version is `1aad0ded-431d-4ea0-a27c-958361e2625a`.

The repeatable live validator passed every test:

```text
29 of 29 live checks passed
530 unique sitemap URLs fetched successfully in the latest deployed corpus
Cloudflare apex DNS and nameservers resolved correctly
www.greyscienx.com resolves through Cloudflare and returns a permanent 308 redirect to the canonical apex URL
static SVG and PDF assets returned repeatable edge-cache HITs with stable ETags
the research API and hybrid search endpoint returned live results
JSON and Markdown content negotiation passed
MCP discovery, initialize, tools/list, tools/call and SSE delivery passed
robots.txt, five sitemap documents, RSS, llms.txt, the machine-readable research index, homepage canonical metadata and WebSite JSON-LD passed
the public IndexNow key was verified and all 531 canonical URLs were accepted by the IndexNow endpoint with HTTP 200
the Google Search Console HTML ownership file was fetched from the canonical production origin and matched its registered token
```

The live report is stored at `research/templates/semantic-twin/live-deployment-validation-report.json` and can be regenerated with `npm run deploy:validate`. The accepted IndexNow submission is recorded in `research/templates/semantic-twin/indexnow-submission-report.json` and can be repeated with `npm run indexnow:submit`.

Search-engine crawlability and IndexNow notification are verified. The canonical URL-prefix property `https://greyscienx.com/` is also ownership-verified in Google Search Console through the deployed HTML verification file. All five sitemap endpoints were submitted on 29 September 2026. Google immediately reported success for the main, research, series and datasets sitemaps. The standards sitemap was accepted twice by the submission flow but initially displayed `Couldn't fetch`; the live endpoint independently returned HTTP 200, valid XML and the correct `application/xml` content type to a Googlebot request, so this is recorded as a pending crawler retry rather than a live-site failure.

The Search Console verification and submission record is stored at `research/templates/semantic-twin/google-search-console-submission-report.json`.

Inclusion in third-party public indexes remains controlled by their crawlers and must be observed later.

## Deliberately human or deployment-bound gates

The following are not represented as completed machine checks because software cannot truthfully certify them on its own:

- judgement about whether a critique, fork, revision or new submission should be published
- empirical proof of third-party search-engine inclusion, which requires crawler ingestion and later observation or search-console data

These gates do not require another architecture. They use the review, versioning, verification and publication structures now present in the harness.

## OpenAI public-plugin submission readiness

GreyScienx is connected privately in ChatGPT and has been prepared for a separate public **With MCP** directory submission. The production release now includes:

- 22 MCP tools with explicit `readOnlyHint: true`, `openWorldHint: false` and `destructiveHint: false` annotations
- public privacy, terms and support pages
- a 512 × 512 production logo at `/brand/greyscienx-app-icon.png`
- a portable Agent Plugins 1.0 twin in `plugins/greyscienx/`
- a packaged archive at `plugins/greyscienx-plugin-1.0.0.zip`
- complete listing copy, starter prompts, five positive tests, three negative tests and release notes in `research/templates/semantic-twin/openai-public-plugin-submission.json`

The production build, lint, 14 research integrity tests and plugin-package checks pass. The live deployment validator passes 29 of 29 checks, all three policy pages and the logo return HTTP 200, and all 22 live tool annotations match the declared read-only behaviour.

The OpenAI Platform project `Personal / Greyscienx` has been created. Individual developer verification was completed through OpenAI's Persona flow and the organization now reports **Identity in review**. OpenAI continues to block public-draft creation until that review is approved. After approval, the prepared submission can be entered, domain-verified, scanned and submitted for review.
