---
name: greyscienx-x-editorial
description: Turn a GreyScienx publication into a verified X/Twitter campaign with one long post, at least nine short posts, research-linked visual cards, alt text, and a claim ledger. Use for drafting, revising, or rendering social promotion for a paper; do not use to publish posts without separate user authorization.
---

# GreyScienx X editorial

Create a publication pack that is arresting enough to earn attention and precise enough to survive scrutiny. The source paper—not the desired hook—is the authority.

Before writing, read [references/editorial-standard.md](references/editorial-standard.md). When producing images, also read [references/visual-system.md](references/visual-system.md).

## Required output

For every publication, create at least ten standalone posts:

- Post 01: one long-form flagship post, normally 1,200–2,500 characters. Keep it below X's current long-post limit. If long posts are unavailable on the target account, provide a numbered 280-character thread variant as well.
- Posts 02–10: at least nine distinct short posts, each no more than 280 characters including the visible paper URL.
- One unique 1080 × 1350 PNG card and useful alt text for every post.
- A claim ledger linking every factual or modelled assertion to a paper page, figure, table, model output, or explicit assumption.
- A release-order suggestion. Do not post or schedule anything unless the user separately asks and authorizes that external action.

Store a completed pack beside the publication or in the user-specified location:

```text
social/x/
|-- manifest.json
|-- posts.md
|-- claims.csv
`-- cards/
    |-- 01-flagship.png
    `-- 02-...png
```

## Workflow

1. Read the complete paper, its figures, model outputs, and stable public URL. Do not draft from the abstract alone when the full paper is available.
2. Build the claim ledger before writing hooks. Distinguish observed evidence, sourced external facts, model results, scenarios, and opinion.
3. Choose ten genuinely different angles. Prefer one strong idea per post over ten rewrites of the headline result.
4. Draft the long post and nine short posts using the editorial standard. Put the decisive idea early and the qualification close enough to govern interpretation.
5. Design one card per post. Reuse a paper figure only when it remains legible at social size; otherwise redraw a simplified, traceable version.
6. Render cards with `scripts/render_card.py`, then inspect every PNG at full size and as a phone-sized thumbnail.
7. Run `scripts/validate_pack.py manifest.json`. Fix claim gaps, duplicate angles, character overruns, missing URLs, missing alt text, unreadable cards, and any wording stronger than the paper.

## Rendering

```powershell
python skills/greyscienx-x-editorial/scripts/render_card.py card.json cards/02-head-start.png
```

The renderer accepts `chartImage`, `stat`, or `bars` visual data. Use the CSS-derived GreyScienx template in `assets/social-card.html`; do not recreate the Legible poster's rounded, gradient-heavy product style. Preserve the bundled outlined wordmarks in `assets/greyscienx-logo.svg` and `assets/greyscienx-logo-inverse.svg`. The renderer embeds them as data URIs so cards have no external logo or font dependency. Run `scripts/build_logo.py` only when intentionally rebuilding the saved vector sources.

## Non-negotiable integrity rules

- Use “in this model”, “under these assumptions”, or equivalent language for hypothetical results. A model result is not a forecast.
- Never change “R4 million more” into “4× more”, “living together” into “marriage”, or household wealth into an individual's wealth.
- Preserve units, price year, time horizon, comparison group, and scenario name when they materially constrain the claim.
- Honest clickbait may sharpen contrast or curiosity; it may not manufacture causality, certainty, universality, or a larger number.
- Put the paper URL in every final post. Cards also carry the short display URL, but the image is not a substitute for a clickable link.
- Do not hide qualifications in alt text or a later reply.
