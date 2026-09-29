# Inherited Geography research package

This directory contains the reproducible evidence, model, figures and manuscript for **Inherited Geography: The Racial Property-Wealth Dividend**.

## Contents

- `model.py` - deterministic Monte Carlo model (seed `20260920`, 100,000 draws per scenario).
- `parameters.csv` - machine-readable model parameters and their evidentiary status.
- `model_results.json` - complete distributional results.
- `sources.md` - verified source ledger, exact claims used, and limitations.
- `data-notes.md` - model design, identification boundary, and parameter rationale.
- `citations.json` - structured citation catalogue.
- `manuscript.md` - publication source.
- `figures/` - eight GreyScienx-styled analytical figures.
- `sources/` - locally archived public PDFs and extracted text where download access permitted.
- `extracted-text.txt` - final-PDF text extraction generated during QA.
- `qa/` - final metadata, checksums, render inventory and visual-review log.

## Reproduce

From the repository root:

```powershell
python research/source/inherited-geography/model.py
python .agents/skills/greyscienx-editorial-pdf/scripts/build_report.py `
  research/source/inherited-geography/manuscript.md `
  research/publications/inherited-geography-racial-property-wealth-dividend.pdf `
  --css app/globals.css `
  --title "Inherited Geography" `
  --title-accent "The Racial Property-Wealth Dividend" `
  --subtitle "Thirty years after apartheid ended, how much of its property geography is still compounding?" `
  --author "GreyScienx" `
  --subject "South African property inheritance, spatial inequality and intergenerational wealth" `
  --header-title "Inherited Geography" `
  --footer-meta "GREYSCIENX / RESEARCH PAPER / 2026"
```

The model is a scale-and-distribution experiment, not a forecast, valuation service, or causal estimate. Population-group scenarios are aggregate historical calibrations and must not be used to infer an individual's wealth.

