# GreyScienx X editorial standard

## Contents

- Campaign architecture
- Honest clickbait
- Long post
- Short-post angles
- Claim ledger
- Manifest contract
- Release sequence

## Campaign architecture

A publication pack is a small editorial campaign, not a repeated announcement. Use the ten-post minimum to reveal different mechanisms, time horizons, sensitivities, trade-offs, and limits in the same paper.

Every post must work independently for a reader who has not seen the others. Each includes the stable full-paper URL and a useful visual. Avoid “Part 4” dependence except in an explicit thread variant.

## Honest clickbait

Write like a sober newspaper front page: concrete subject, active verb, striking number or conflict, and no throat-clearing. The headline earns the click; the first qualification earns trust.

Strong patterns:

- **Number with boundary:** “Living together at 25 adds almost R4 million in modelled household wealth by 75.”
- **Timing:** “Ten years of duplicated housing costs can still be visible half a century later.”
- **Counterfactual:** “The same salaries. The same children. One household decision—and a R4 million gap.”
- **Reversal:** “The cheaper option can lower measured GDP while leaving households better off.”
- **Threshold:** “At 24 hours, the expensive battery becomes the cheaper one in this model.”
- **Trade-off:** “R225 billion can build factories—or disappear into the infrastructure they need.”

Rejected transformations:

| Source finding | Reject | Why |
|---|---|---|
| Early cohabitation produces R3.972m more household wealth in the average scenario | “Marriage at 25 makes you 4× richer” | Changes the institution, unit, magnitude, and certainty |
| A policy closes 40% of a modelled fiscal gap | “This policy solves the pension crisis” | Converts a partial scenario result into a universal causal claim |
| An estimate is in constant 2026 rand | Omitting the price year where inflation matters | Makes unlike values look directly comparable |

Use surprise, not deception. “Can”, “could”, “in the model”, and “under central assumptions” are useful when they are the true epistemic status, not timid filler.

## Long post

Target 1,200–2,500 characters unless the paper needs less. X currently permits longer posts for eligible Premium accounts, but the format is difficult to schedule and platform limits change. Keep a thread fallback.

Structure:

1. **Lead:** the central tension or strongest result in one or two lines.
2. **Experiment:** who or what is compared, over what period, and under which scenario.
3. **Three findings:** use short paragraphs; connect the number to its mechanism.
4. **Counterweight:** the strongest caveat or case in which the result weakens.
5. **Why it matters:** the wider economic, political, scientific, or social implication.
6. **Link:** “Read the full paper:” plus the stable URL.

Do not paste an abstract. The long post should tell a compact story with a beginning, mechanism, and boundary.

## Nine short-post angles

Choose at least nine from this bank, and add a new angle when the paper suggests a better one:

1. Headline result or threshold.
2. Baseline versus alternative.
3. The mechanism behind the headline.
4. A time-path or compounding result.
5. Best, average, and worst cases.
6. A sensitivity that changes the answer.
7. A distributional winner and loser.
8. A common intuition the model overturns.
9. A constraint, bottleneck, or implementation failure.
10. A policy lever and its cost.
11. A “what the model does not say” credibility post.
12. A cross-paper connection inside the same research series.

Do not use filler questions (“Thoughts?”), engagement bait, invented controversy, unexplained acronyms, or more than two useful hashtags. Prefer no hashtag when the copy is clearer without one. Emojis are opt-in, not the house voice.

## Claim ledger

Create `claims.csv` with these columns:

```text
claim_id,claim_type,source_location,source_text,social_wording,qualifier,visual_source,checked
```

- `claim_type`: observed, external-source, model-result, scenario, assumption, or interpretation.
- `source_location`: paper page plus figure/table/section, or an exact model-output path and key.
- `source_text`: concise faithful extraction, not a rewritten hook.
- `social_wording`: the strongest wording the evidence supports.
- `qualifier`: price year, geography, sample, scenario, counterfactual, uncertainty, or other governing boundary.
- `visual_source`: original figure, regenerated data file, or `none`.
- `checked`: `yes` only after values, units, labels, and arithmetic have been verified.

Each post cites at least one claim ID in `manifest.json`. Each number on a card must be represented in the ledger.

## Manifest contract

Use this shape for `manifest.json`:

```json
{
  "publication": {
    "title": "Publication title",
    "url": "https://greyscienx.com/research/series/paper.pdf"
  },
  "posts": [
    {
      "id": "01",
      "type": "long",
      "angle": "flagship",
      "copy": "Post copy with full URL",
      "image": "cards/01-flagship.png",
      "alt": "What the visual shows and the relevant values.",
      "claim_ids": ["C01", "C02"]
    }
  ],
  "claims": [
    {
      "id": "C01",
      "type": "model-result",
      "source": "p. 14, Table 3",
      "checked": true
    }
  ]
}
```

The validator accepts more fields but requires the fields shown above. Keep `posts.md` human-readable and `manifest.json` machine-checkable.

## Release sequence

A useful default cadence is three weeks:

- Day 1: flagship long post, pinned temporarily.
- Days 2–5: headline number, mechanism, and best/average/worst comparison.
- Week 2: sensitivity, distribution, and policy posts.
- Week 3: limitation post, cross-paper connection, and a final “one chart” recap.

Do not schedule this automatically. Adjust cadence to news relevance and avoid posting two near-identical cards consecutively.

