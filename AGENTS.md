<!-- BEGIN:nextjs-agent-rules -->

# This is NOT the Next.js you know

This version has breaking changes — APIs, conventions, and file structure may all differ from your training data. Read the relevant guide in `node_modules/next/dist/docs/` (resolved from this file's directory; in monorepos the `next` package may not be visible from the repo root) before writing any code. Heed deprecation notices.

This block is written and re-added by `next dev` — verify at `node_modules/next/dist/server/lib/generate-agent-files.js`. Removing it from a diff only re-creates the uncommitted change; committing it with your work keeps the tree clean.

<!-- END:nextjs-agent-rules -->

# GreyScienx project guidance

GreyScienx is a neutral, multidisciplinary research publication. Keep the website and publication language institutional rather than personal unless the user explicitly requests author biography content.

## Sources of truth

- `lib/catalog.ts` defines the published series, paper titles, slugs, summaries, and public URLs.
- `research/publications/` contains the public manuscripts.
- `research/source/` contains model code, model results, report text, and figures that may support a manuscript. Search by paper slug or distinctive title words; do not assume a source folder exists.
- `.agents/skills/greyscienx-x-editorial/` defines the required workflow for X/Twitter publication campaigns.
- `app/globals.css` is the visual reference for the GreyScienx website. Social cards use the stricter visual system bundled with the social skill.

## Social publication campaigns

Treat one paper's campaign as one distinct deliverable and normally one distinct Codex task. Do not combine several papers into one campaign unless the user explicitly asks for a cross-paper series.

For a paper with slug `<paper-slug>`, place all campaign outputs in `social/x/<paper-slug>/`. Keep changes inside that campaign directory unless a shared skill fix is genuinely required. Do not edit the manuscript, its models, the website, or another campaign as a side effect.

Every campaign must invoke `$greyscienx-x-editorial`, read the complete manuscript and relevant model evidence, and meet that skill's claim-ledger, post-count, visual, accessibility, and validation requirements. Model results must be described as modeled results, scenarios, estimates, or counterfactuals as appropriate. Never silently turn cohabitation into marriage, household results into individual results, absolute differences into multiples, or scenarios into forecasts.

Use the paper's canonical public article URL from `lib/catalog.ts`. Do not invent a URL from the PDF filename. Generate and validate the complete pack, but do not publish or schedule posts without a separate explicit instruction.

## Campaign task prompt

When opening a new task for one paper, use this shape:

> Use `$greyscienx-x-editorial` to create the complete X campaign for `<paper title>`. The canonical paper entry is in `lib/catalog.ts`. Read the full manuscript in `research/publications/` and inspect relevant evidence in `research/source/`. Write all outputs to `social/x/<paper-slug>/`, validate the pack, and stop before publishing or scheduling anything.
