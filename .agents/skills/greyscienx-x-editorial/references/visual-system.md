# GreyScienx social visual system

Use `app/globals.css` as the brand source of truth. Reload its custom properties when the site changes.

## Canvas and safe area

- Primary card: 1080 × 1350 px (4:5). It falls within X's currently supported full-display single-image range and also works well on other feeds.
- Keep essential type at least 64 px from every edge.
- Export PNG or JPEG below 5 MB for ordinary X posting.
- Inspect at 270 × 338 px as well as at full size. If a label disappears at thumbnail size, simplify the visual.

## Editorial character

The cards are research front pages, not product ads:

- Warm white or true-black ground.
- A strong coral top rule and restrained coral emphasis.
- Oversized, tightly set headline.
- Sharp rectangular figure frame; no rounded cards, gradients, glass effects, generic stock imagery, or soft shadows.
- Segoe UI or another neutral sans serif available locally.
- Wordmark, series label, paper number, source line, and display URL.
- Use the bundled outlined GreyScienx SVG wordmark. Do not typeset or redraw the logo inside an individual card.
- One dominant visual claim per card.

The supplied `assets/social-card.html` deliberately improves on the Legible reference by using a sharper newspaper hierarchy, a larger evidence area, real figure captions, explicit model-status labels, and a source footer.

## Card families

Use varied layouts across a campaign:

1. **Chart desk:** simplified chart or cropped research figure with a one-sentence caption.
2. **Number front:** one large number, what it measures, and its comparison base.
3. **Before/after:** two or three bars with direct labels and the delta highlighted.
4. **Scenario strip:** best, central, and adverse outcomes with no false single-number precision.
5. **Threshold:** emphasise the point where one option crosses another.
6. **Mechanism:** compact sequence such as “shared rent → monthly saving → compounding”.
7. **Fine print:** a strong “What this does not mean” card that earns credibility.

At least four of ten cards should show data when the paper contains sufficient quantitative material. The rest may explain mechanisms, assumptions, or limitations. Avoid decorative graphs with no analytical payload.

## Chart rules

- Redraw dense paper figures rather than shrinking them blindly.
- Use coral for the primary case, black for the comparator, and grey for a third case. Add direct labels or distinct line/marker styles so colour is not the only encoding.
- Start bars at zero. If an axis is truncated for a line chart, label it plainly.
- Include units, price year, scenario, and source in the card itself when omission could mislead.
- A chart caption interprets the result; it does not repeat the headline.
- Negative model balances may represent a funding shortfall rather than literal debt. Label that distinction.

## Copy-image division

The image should carry the headline, evidence, caption, and display URL. The post copy carries context, a qualification, and the clickable full URL. Do not place a paragraph of body copy on the image.

Alt text should state the visual form, axes or categories, decisive values, and the main comparison. Do not use alt text as a dumping ground for caveats omitted from the visible card.
