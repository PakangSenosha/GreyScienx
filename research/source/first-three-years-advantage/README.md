# The First Three Years Advantage - reproducibility

This directory contains the complete model, inputs, results, manuscript, and figures for the GreyScienx paper.

## Rebuild

From this directory:

```powershell
python model.py
python build_pdf.py
python qa_check.py
```

The model writes deterministic CSV/JSON results to `results/` and five figures to `figures/`. The PDF builder writes the publication to `../../publications/the-first-three-years-advantage.pdf`.

All monetary values are constant 2026 rand. `inputs.json` separates cited observations from GreyScienx scenario assumptions. The central comparison holds life after age 25 constant, so strategy differences are caused by the first 36 months and their later compounding. It is a transparent counterfactual, not a forecast, recommendation, or claim that non-financial welfare can be reduced to money. `final-text.txt` is the layout-preserving extraction used for the final text audit; `results/qa_report.json` records metadata and machine checks.
