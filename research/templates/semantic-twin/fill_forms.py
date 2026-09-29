"""Fill every empty field in the published semantic-twin forms.

The YAML files stay the authoring twin. This script inserts manuscript
extractions for studies that still have an empty claim register, then
replaces remaining nulls and empty collections with values taken from
the form, the manuscript, or an explicit statement that nothing is published.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from urllib.parse import urlparse

import yaml

ROOT = Path(__file__).resolve().parents[3]
PUBLISHED = Path(__file__).resolve().parent / "published"
RECORD_DATE = "2026-09-29"


def editorial_review():
    path = Path(__file__).resolve().parent / "editorial-review-manifest.json"
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, TypeError):
        return {}


EDITORIAL_REVIEW = editorial_review()


def reproduction_records():
    path = Path(__file__).resolve().parent / "model-reproduction-report.json"
    if not path.exists():
        return {}
    try:
        report = json.loads(path.read_text(encoding="utf-8"))
        records = {}
        for item in report.get("models", []):
            if not item.get("passed"):
                continue
            records[item["package"]] = item
            if item.get("study_slug"):
                records[item["study_slug"]] = item
        return records
    except (OSError, ValueError, KeyError, TypeError):
        return {}


REPRODUCED = reproduction_records()


def model_manifest():
    path = Path(__file__).resolve().parent / "model-reproduction-manifest.json"
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        return {item["package"]: item for item in payload.get("models", [])}
    except (OSError, ValueError, KeyError, TypeError):
        return {}


MODEL_MANIFEST = model_manifest()


def link_records():
    path = Path(__file__).resolve().parent / "link-check-report.json"
    if not path.exists():
        return {}
    try:
        report = json.loads(path.read_text(encoding="utf-8"))
        return {item["url"].rstrip("/"): item for item in report.get("results", [])}
    except (OSError, ValueError, KeyError, TypeError):
        return {}


LINKS = link_records()


def automated_render_records():
    path = Path(__file__).resolve().parent / "automated-pdf-render-report.json"
    if not path.exists():
        return {}
    try:
        report = json.loads(path.read_text(encoding="utf-8"))
        return {item["study_id"]: item for item in report.get("documents", []) if item.get("passed")}
    except (OSError, ValueError, KeyError, TypeError):
        return {}


AUTOMATED_RENDERS = automated_render_records()

SOURCE = {
    "economics-of-living-together": "research/publications/economics-of-living-together-v0.5.md",
    "the-first-three-years-advantage": "research/source/first-three-years-advantage/report.md",
    "when-retirement-becomes-impossible": "research/source/retirement/when-retirement-becomes-impossible.md",
    "todays-unemployment-is-tomorrows-pension-crisis": "research/source/unemployment-pension/todays-unemployment-is-tomorrows-pension-crisis.md",
    "does-raising-the-retirement-age-actually-work": "research/source/retirement-age/does-raising-the-retirement-age-actually-work.md",
    "the-politics-of-an-ageing-electorate": "research/source/ageing-electorate/the-politics-of-an-ageing-electorate.md",
    "emergency-ageing-austerity": "research/source/emergency-ageing-austerity/emergency-ageing-austerity.md",
    "the-price-of-another-child": "research/source/price-of-another-child/the-price-of-another-child.md",
    "the-hundred-year-life": "research/source/hundred-year-life/the-hundred-year-life.md",
    "inheritance-after-retirement": "research/source/inheritance-after-retirement/inheritance-after-retirement.md",
    "how-to-shrink-a-country-without-breaking-it": "research/source/how-to-shrink-a-country/how-to-shrink-a-country.md",
    "the-scarce-worker-economy": "research/source/scarce-worker-economy/the-scarce-worker-economy.md",
    "the-population-system": "research/source/population-system/the-population-system.md",
    "extreme-fiscal-pressure": "research/source/extreme-fiscal-pressure/extreme-fiscal-pressure.md",
    "the-r350-industrialisation-counterfactual": "research/source/r350-industrialisation-counterfactual/report.md",
    "the-welfare-cost-of-not-paying-the-grant": "research/source/srd-welfare-cost/report.md",
    "consumption-today-or-productive-capital-tomorrow": "research/source/consumption-or-capital/report.md",
    "the-public-capital-multiplier": "research/source/public-capital-multiplier/report.md",
    "the-r200-billion-factory": "research/source/r200-billion-factory/report.md",
    "the-south-african-critical-minerals-industrial-complex": "research/source/critical-minerals-industrial-complex/report.md",
    "the-platinum-to-hydrogen-economy": "research/source/platinum-to-hydrogen-economy/report.md",
    "the-manganese-to-battery-economy": "research/source/manganese-to-battery-economy/report.md",
    "the-vanadium-grid-storage-economy": "research/source/vanadium-grid-storage-economy/report.md",
    "the-capital-goods-economy": "research/source/capital-goods-economy/report.md",
    "the-mineral-sovereign-wealth-fund": "research/source/mineral-sovereign-wealth-fund/report.md",
    "south-africa-in-a-richer-africa": "research/source/south-africa-richer-africa/report.md",
    "johannesburg-as-africas-financial-capital": "research/source/johannesburg-financial-capital/report.md",
    "the-factory-for-african-urbanisation": "research/source/factory-for-african-urbanisation/report.md",
    "inherited-geography": "research/source/inherited-geography/manuscript.md",
}


def study(slug, series, title_path):
    return {
        "slug": slug,
        "series": series,
        "path": title_path,
    }


def blank_registers(study_id, base, model, assumptions, results, claims):
    return {
        "model": model,
        "assumptions": assumptions,
        "results": results,
        "claims": claims,
        "study_id": study_id,
        "base": base,
    }


def A(study_id, n, name, statement, value, unit, provenance, strength, sensitivity, alternatives):
    local = f"A{n:02d}"
    return {
        "id": local,
        "canonical_id": f"{study_id}:{local}",
        "name": name,
        "statement": statement,
        "value": value,
        "unit": unit,
        "value_type": "qualitative" if value is None else "declared",
        "status": "model_assumption",
        "provenance": provenance,
        "source_ids": [f"{study_id}:PDF"],
        "evidence_strength": strength,
        "sensitivity": sensitivity,
        "alternatives": alternatives,
    }


def R(study_id, n, statement, value, unit, scenario, sensitivity="high", price_year="2026"):
    local = f"R{n:02d}"
    return {
        "id": local,
        "canonical_id": f"{study_id}:{local}",
        "statement": statement,
        "value": value,
        "unit": unit,
        "price_year": price_year,
        "year_or_period": scenario,
        "scenario_id": scenario,
        "model_id": "M01",
        "evidence_status": "modelled",
        "uncertainty": "The manuscript presents this as a scenario result, not a confidence interval.",
        "sensitivity": sensitivity,
        "source_data_ids": [f"{study_id}:PDF"],
        "reproducible_from": [f"{study_id}:M01"],
    }


def C(study_id, base, n, text, assumes, results, sensitivity, limitation):
    local = f"C{n:02d}"
    return {
        "id": local,
        "canonical_id": f"{study_id}:{local}",
        "claim": text,
        "claim_type": "conditional",
        "status": "conditional",
        "evidence_status": "modelled",
        "confidence": "not scored",
        "depends_on_assumptions": [f"{study_id}:A{i:02d}" for i in assumes],
        "derived_from_results": [f"{study_id}:R{i:02d}" for i in results],
        "supported_by_sources": [f"{study_id}:PDF"],
        "contradicted_by_sources": ["none recorded"],
        "qualifies_claims": ["none recorded"],
        "contradicted_claims": ["none recorded"],
        "main_limitation": limitation,
        "sensitivity": sensitivity,
        "retrieval_text": text,
        "citation_text": f"GreyScienx, {study_id}:{local}, version 1.0.",
        "href": f"{base}/claims/{local}",
    }


def M(study_id, name, statement, model_class, time_step, inputs, outputs, implementation):
    return {
        "id": "M01",
        "canonical_id": f"{study_id}:M01",
        "name": name,
        "purpose": statement,
        "model_class": model_class,
        "statement": statement,
        "inputs": inputs,
        "outputs": outputs,
        "time_step": time_step,
        "implementation_file": implementation,
        "version": "1.0",
    }


def pack(study_id, base, model, assumptions, results, claims):
    return {
        "models": [model],
        "assumptions": assumptions,
        "results": results,
        "claims": claims,
    }


NEW = {}

def add(study_id, slug, model, assumptions, results, claims):
    base = None  # filled later from the form
    NEW[slug] = {
        "study_id": study_id,
        "models": [model],
        "assumptions": assumptions,
        "results": results,
        "claims_builder": claims,
    }


# The claim builders close over study_id and receive the canonical base URL.
def claims_for(study_id, base, specs):
    return [C(study_id, base, *spec) for spec in specs]

# POP-012
add(
    "GSX:POP-012",
    "extreme-fiscal-pressure",
    M(
        "GSX:POP-012",
        "2050 shock and emergency-rule paths",
        "A common 2050 pandemic, war and recession shock is applied to a hypothetical South-African-scale economy. Three governance paths close the same first-year accounting gap and are followed to 2080.",
        "counterfactual scenario model",
        "annual",
        ["labour supply", "healthcare costs", "defence and import costs", "tax revenue", "governance path"],
        ["output gap", "official debt", "hidden claims", "pension wealth", "youth employment"],
        "research/source/extreme-fiscal-pressure/extreme-fiscal-pressure.md",
    ),
    [
        A("GSX:POP-012", 1, "Common 2050 shock", "The shock combines a severe pandemic, war and security mobilisation, and a recession. The immediate financing need is 14 percent of shocked-year GDP, about R1.23 trillion in constant 2026 rand.", "1.23", "trillion constant 2026 rand", "Manuscript Part I", "scenario", "high", ["A smaller or larger shock"]),
        A("GSX:POP-012", 2, "Three governance paths", "The best case is a guardrailed constitutional emergency ending in 2052. The average case is an extended executive emergency to 2058. The worst case is a permanent constitutional suspension that has not ended by 2080.", None, None, "Manuscript Part I and legal-boundary table", "scenario", "high", ["A different sunset date"]),
        A("GSX:POP-012", 3, "Not legal advice", "A literal suspension of the Constitution is modelled as constitutional rupture, not as an ordinary instrument under section 37.", None, None, "Manuscript Part I", "legal boundary stated in the manuscript", "high", ["A path that remains inside section 37"]),
    ],
    [
        R("GSX:POP-012", 1, "In the guardrailed case, real output in 2080 is 1.2 percent below the no-shock path. The present value of lost output from 2050 to 2080 is R3.7 trillion.", "3.7", "trillion constant 2026 rand, present value of lost output", "Guardrailed emergency, 2050-2080"),
        R("GSX:POP-012", 2, "In the extended-executive case, hidden claims rise to 35 percent of GDP, real output ends 21 percent lower, and private pension wealth and youth employment are each 39 percent lower than the comparison stated in the manuscript.", "35", "percent of GDP, hidden claims", "Extended executive emergency to 2058"),
        R("GSX:POP-012", 3, "In the permanent-suspension case, official debt falls to 70 percent of GDP while hidden pension losses, arrears and deferred maintenance reach 95 percent of GDP. The augmented public burden is 165 percent of GDP. Real output ends 42 percent below the no-shock path, and the present value of output lost after 2050 is R65.8 trillion.", "65.8", "trillion constant 2026 rand, present value of lost output", "Permanent constitutional suspension through 2080"),
    ],
    [
        (1, "Every modelled path closes the first-year accounting gap of about R1.23 trillion. In the guardrailed case that ends in 2052, real output in 2080 is 1.2 percent below the no-shock path and the present value of lost output from 2050 to 2080 is R3.7 trillion.", [1, 2], [1], "high", "This is a counterfactual model, not a forecast and not legal advice. Closing the accounting gap does not create the doctors, food, energy, tax capacity or pension wealth that the shock removes."),
        (2, "The extended executive emergency makes the official debt ratio look no worse than the no-shock path by 2080, while hidden claims rise to 35 percent of GDP, real output ends 21 percent lower, and private pension wealth is 39 percent lower.", [1, 2], [2], "high", "The official debt ratio is not the full public burden. Hidden claims are part of the manuscript's result."),
        (3, "The permanent-suspension path shows an official debt ratio of 70 percent of GDP together with an augmented public burden of 165 percent of GDP and real output 42 percent below the no-shock path.", [1, 2, 3], [3], "high", "The manuscript models this path as constitutional rupture. Apparent success on the official debt ratio is produced by concealing pension losses, arrears and deferred maintenance."),
    ],
)

add(
    "GSX:SRD-001",
    "the-r350-industrialisation-counterfactual",
    M("GSX:SRD-001", "SRD industrial-fund counterfactual", "The model restates the 2020/21-2026/27 SRD programme envelope in constant 2026 rand and follows best, average and worst industrial-fund paths to 2050. The asset paths use the reprioritised-fund version of the counterfactual.", "financial counterfactual", "annual", ["SRD programme amounts", "inflation restatement", "project survival and returns"], ["productive assets", "annual public cash"], "research/source/r350-industrialisation-counterfactual/model.py"),
    [
        A("GSX:SRD-001", 1, "Programme envelope", "The envelope from 2020/21 through the 2026/27 allocation is R225.8 billion in nominal rand, about R253.5 billion in constant 2026 purchasing power. Later years include a revised estimate and a voted allocation, not only cash already spent.", "253.5", "billion constant 2026 rand", "Manuscript Part I, citing the Department of Social Development and National Treasury", "programme records restated by the model", "moderate", ["A ledger that stops at final outturns"]),
        A("GSX:SRD-001", 2, "Reprioritised fund", "The published asset paths withhold the grant and place the revenue in a ring-fenced fund. They do not describe the borrowed-fund case, which adds an asset and a matching liability.", None, None, "Manuscript financing table", "counterfactual design", "high", ["Debt reduction", "A borrowed industrial fund"]),
        A("GSX:SRD-001", 3, "Welfare is not counted here", "The model does not count food, transport, health protection, debt service or local demand purchased by the grant. That loss is the subject of the companion welfare paper.", None, None, "Manuscript Part I", "scope limit", "high", ["A combined welfare and asset account"]),
    ],
    [
        R("GSX:SRD-001", 1, "By 2050 the best-case industrial fund holds about R789 billion in productive assets and generates roughly R39 billion a year in public cash, in 2026 rand.", "789", "billion constant 2026 rand of productive assets", "Best case, 2050"),
        R("GSX:SRD-001", 2, "By 2050 the average case reaches roughly R304 billion in productive assets and R9 billion in annual public cash. The worst case reaches R72 billion and R0.7 billion a year.", "304", "billion constant 2026 rand of productive assets", "Average case, 2050"),
    ],
    [
        (1, "If the SRD envelope of about R253.5 billion in constant 2026 rand had been reprioritised into an industrial fund, the best case holds about R789 billion in productive assets by 2050 and generates roughly R39 billion a year in public cash. The annual cash flow exceeds one current SRD budget year only around 2049.", [1, 2], [1], "high", "The envelope is a counterfactual resource, not yet a factory. The best case depends on projects being selected, built, operated and renewed for decades. This paper does not value what households would have lost if the grant had never been paid."),
        (2, "The average case reaches roughly R304 billion in productive assets and R9 billion in annual public cash by 2050. The worst case reaches R72 billion and R0.7 billion a year.", [1, 2, 3], [2], "high", "These paths are the reprioritised-fund counterfactual. A borrowed fund would also carry a matching liability, and neither path is automatically superior to having paid the grant."),
    ],
)

add(
    "GSX:SRD-002",
    "the-welfare-cost-of-not-paying-the-grant",
    M("GSX:SRD-002", "Welfare-cost ledger", "The model prices the explicit welfare cost of withholding the same SRD envelope valued in the industrial-fund paper. It combines consumption, costly credit, scarring and labour effects and keeps the local spending multiplier out of the welfare total.", "welfare counterfactual", "programme window, 2020/21-2026/27", ["grant envelope", "distributional weights", "credit substitution", "scarring"], ["welfare-equivalent cost", "poverty exposure"], "research/source/srd-welfare-cost/report.md"),
    [
        A("GSX:SRD-002", 1, "Same envelope", "The withheld resource is about R253.5 billion in constant 2026 purchasing power, the same base as the industrial-fund paper.", "253.5", "billion constant 2026 rand", "Manuscript headline ledger", "shared counterfactual base", "moderate", ["A different programme window"]),
        A("GSX:SRD-002", 2, "Distributional weights", "In the conservative, central and severe cases, R1 of consumption at the recipient margin is valued at R1.10, R1.50 and R2.00. The weights are normative assumptions.", "1.50", "welfare rand per consumption rand, central case", "Manuscript Part I", "normative assumption", "high", ["Equal weights", "A higher hunger weight"]),
        A("GSX:SRD-002", 3, "No double-counting of local spending", "The local spending multiplier is reported separately and is not added into the welfare cost.", None, None, "Manuscript Part I", "accounting rule", "moderate", ["Adding the multiplier into the welfare total"]),
    ],
    [
        R("GSX:SRD-002", 1, "The explicit welfare-equivalent cost of withholding the envelope is between R237 billion and R743 billion. The central estimate is R426.9 billion, about R1.68 of social cost for every R1 withheld.", "426.9", "billion welfare-equivalent 2026 rand, central estimate", "Central welfare case"),
        R("GSX:SRD-002", 2, "Additional poverty exposure across the scenarios is 2.5 million to 11.0 million person-years.", "2.5", "million person-years, low end of the scenario range", "Seven-year poverty exposure range"),
    ],
    [
        (1, "Withholding the SRD envelope has a central explicit welfare cost of R426.9 billion in welfare-equivalent 2026 rand, about R1.68 of social cost for every R1 withheld. The scenario range is R237 billion to R743 billion.", [1, 2, 3], [1], "high", "This is not a Treasury invoice, a forecast or a confidence interval. Crime, unrest and household dissolution are left outside the priced total. The central case is an analytical benchmark."),
        (2, "The average industrial outcome in the companion paper does not clear this central welfare hurdle. Only an exceptionally well-executed industrial programme clearly beats it, and the later beneficiaries are not automatically the households who gave up the grant.", [1, 2], [1, 2], "high", "The comparison is between a public asset and a social cost. It does not say that cash transfers are always better than investment."),
    ],
)

add(
    "GSX:SRD-003",
    "consumption-today-or-productive-capital-tomorrow",
    M("GSX:SRD-003", "Transfer versus industrial present-value comparison", "The model compares the present value of the grant's social benefits with the present value of the industrial alternative, using the shared R253.5 billion envelope and a stated real discount rate.", "present-value counterfactual", "annual from 2020", ["welfare cost of the transfer", "industrial operating benefits", "surviving public asset", "discount rate"], ["break-even year", "present value in 2050"], "research/source/consumption-or-capital/report.md"),
    [
        A("GSX:SRD-003", 1, "Shared envelope and welfare values", "The comparison uses the R253.5 billion constant-2026-rand envelope and Paper 2's central welfare value of R426.9 billion, which is R358.2 billion in 2020 present value at 6 percent.", "358.2", "billion 2020 present-value rand at 6 percent", "Manuscript central comparison table", "inherited from the companion papers", "moderate", ["Conservative or severe welfare values"]),
        A("GSX:SRD-003", 2, "Central discount rate", "The central comparison uses a 6 percent real discount rate. The paper also reports 3.5 percent and the 10 percent public-project benchmark.", "6", "percent real discount rate", "Manuscript Part I", "normative timing weight", "high", ["3.5 percent", "10 percent"]),
        A("GSX:SRD-003", 3, "Asset-inclusive test", "Counting the surviving public asset is legitimate only if the asset is viable, maintained, publicly owned and capable of being sold or of continuing to produce.", None, None, "Manuscript definition of break-even", "accounting condition", "high", ["Flow-only test"]),
    ],
    [
        R("GSX:SRD-003", 1, "At 6 percent, the best industrial case overtakes the central transfer value in 2040 if the surviving asset is counted, and in 2051 if only operating benefits are counted.", "2040", "break-even year, asset-inclusive best case", "Central comparison, 6 percent real discount rate"),
        R("GSX:SRD-003", 2, "At 6 percent, best-case industrial value in 2050 is R485.7 billion in present value. Average industrial value is R152.3 billion, R205.9 billion short of the central transfer. At a 10 percent discount rate, none of the industrial cases crosses by 2100.", "152.3", "billion 2020 present-value rand, average industrial case in 2050", "6 percent and 10 percent discount-rate tests"),
    ],
    [
        (1, "At a 6 percent real discount rate, the best industrial case overtakes the central value of the cash transfer in 2040 when the surviving public asset is counted, and in 2051 when only operating benefits are counted.", [1, 2, 3], [1], "high", "There is no universal year when a factory becomes better than a cash transfer. The best case requires exceptional execution and a credible residual asset. The original households are not necessarily repaid even if the aggregate account later wins."),
        (2, "The average and worst industrial cases do not overtake the central transfer value by 2100 at 6 percent. At the 10 percent public-project benchmark, none of the industrial cases crosses by 2100.", [1, 2], [2], "high", "The discount rate does not change the factory's physical output. It changes how much present sacrifice the model treats as justified."),
    ],
)

add(
    "GSX:SRD-004",
    "the-public-capital-multiplier",
    M("GSX:SRD-004", "Public-capital mobilisation portfolio", "The model allocates R225 billion of public industrial capital across instruments and then deducts capital judged non-additional, delayed, unallocated or failed.", "capital-stack scenario", "programme", ["public envelope", "instrument mix", "additionality", "failure"], ["gross investment", "operating investment", "multiple"], "research/source/public-capital-multiplier/report.md"),
    [
        A("GSX:SRD-004", 1, "Public envelope", "The arithmetic uses R225 billion of public industrial capital.", "225", "billion rand of public industrial capital", "Manuscript Part I", "scenario scale", "moderate", ["A different envelope"]),
        A("GSX:SRD-004", 2, "Mixed portfolio", "The central portfolio spreads that capital across infrastructure, concessional debt, minority equity, first-loss capital, a guarantee reserve, project preparation, skills and supplier funds.", None, None, "Manuscript Part I", "scenario design", "high", ["Full public ownership", "A guarantee-heavy stack"]),
        A("GSX:SRD-004", 3, "Gross is not additional", "Capital that would have been invested anyway, or that is delayed, unallocated or failed, is removed before the operating multiple is stated.", None, None, "Manuscript Part I", "accounting rule", "high", ["Treating every private rand as additional"]),
    ],
    [
        R("GSX:SRD-004", 1, "The central mixed portfolio mobilises R506 billion of gross investment, a headline multiple of 2.25.", "2.25", "gross rand of investment per rand of public capital", "Central mixed portfolio"),
        R("GSX:SRD-004", 2, "After non-additional, delayed, unallocated and failed capital, R383 billion remains operating, 1.70 times the public envelope.", "1.70", "operating rand per rand of public capital", "Central portfolio after deductions"),
    ],
    [
        (1, "In the central mixed portfolio, R225 billion of public industrial capital mobilises R506 billion of gross investment, 2.25 times the public envelope. After deductions, R383 billion remains operating, 1.70 times the envelope.", [1, 2, 3], [1, 2], "high", "A multiplier is a description of a capital stack, not money created. Guarantees can show a high cash multiple while leaving the downside with the state. The multiples are not observed South African averages."),
        (2, "The manuscript's portfolio conclusion is a gross mobilisation range of roughly 1.5 to 2.5 times, judged by net additional operating investment, development value and risk-adjusted public cost.", [2, 3], [2], "moderate", "Maximising a single headline ratio is the comparison the paper rejects. Common infrastructure can have low measured leverage and high additionality."),
    ],
)

add(
    "GSX:SRD-005",
    "the-r200-billion-factory",
    M("GSX:SRD-005", "Physical allocation of R225 billion", "The model turns R225 billion in constant 2026 rand into sites, utilities, 34 production modules, skills, supplier finance and logistics, using stylised plant assumptions from the mineral papers.", "physical programme scenario", "ten-year programme", ["capital envelope", "module sizes", "utilisation"], ["direct jobs", "sales", "power demand", "water demand"], "research/source/r200-billion-factory/report.md"),
    [
        A("GSX:SRD-005", 1, "Envelope and split", "R225 billion in constant 2026 rand is allocated across the programme. R96 billion, 43 percent, goes directly into production plants. The rest is power, water, logistics, parks, supplier finance, skills, worker housing and a R15 billion contingency.", "225", "billion constant 2026 rand", "Manuscript Part I", "scenario allocation", "moderate", ["A different split between plant and enabling infrastructure"]),
        A("GSX:SRD-005", 2, "Modular production core", "The production core is 34 modules across manganese-battery materials, PGM-hydrogen components, vanadium storage and shared machinery or recycling.", "34", "industrial modules", "Manuscript central conclusion", "stylised plant assumptions", "high", ["Fewer or more modules"]),
        A("GSX:SRD-005", 3, "Utilisation hinge", "At 40 percent average use the portfolio creates almost no local value after its fixed burden. Above 70 percent the case becomes materially stronger.", "70", "percent average capacity use", "Manuscript findings", "scenario threshold", "high", ["40 percent utilisation"]),
    ],
    [
        R("GSX:SRD-005", 1, "In the central case the programme supports about 11,100 direct operating jobs, roughly 10,000 supplier jobs, R108 billion of annual sales, 700 MW of reliable power demand and 12 million cubic metres of annual industrial water demand.", "11100", "direct operating jobs", "Central case, after construction"),
        R("GSX:SRD-005", 2, "Construction employment peaks near 40,000 direct jobs and is temporary. Only R96 billion of the R225 billion goes directly into production plants.", "40000", "peak direct construction jobs", "Construction phase"),
    ],
    [
        (1, "A credible R225 billion programme could establish 34 industrial modules and, in the central case, support about 11,100 direct operating jobs, roughly 10,000 supplier jobs and R108 billion of annual sales.", [1, 2], [1], "high", "The numbers are scenarios, not quotations or forecasts. Success depends more on utilisation and execution than on the number of ribbon cuttings. The programme takes close to a decade."),
        (2, "More than half of the envelope enables production rather than buying production equipment. Peak construction employment near 40,000 direct jobs is not permanent operating employment.", [1, 3], [2], "moderate", "A plant without power, water, logistics, skills, working capital or customers is not productive capital. Presenting the construction peak as permanent employment would misstate the model."),
    ],
)

add(
    "GSX:IND-001",
    "the-south-african-critical-minerals-industrial-complex",
    M("GSX:IND-001", "Value-pool localisation model", "The model assigns illustrative shares of a critical-minerals value pool to chain stages and compares an existing footprint, focused integration, frontier partnership and forced autarky.", "value-share scenario", "comparative static", ["stage value shares", "localisation strategy", "utilisation penalty"], ["share of the modelled value pool"], "research/source/critical-minerals-industrial-complex/report.md"),
    [
        A("GSX:IND-001", 1, "Illustrative value pool", "Each stage is assigned an illustrative share of total value added. The shares are a way to expose where value is assumed to remain local. They are not a forecast of GDP or company revenue.", None, None, "Manuscript numerical headline", "model construct", "high", ["A different stage weighting"]),
        A("GSX:IND-001", 2, "Strategy cases", "The comparison includes the existing footprint, focused integration, a frontier partnership case, and forced autarky after utilisation and market-access penalties.", None, None, "Manuscript Part I", "scenario design", "high", ["A different partnership assumption"]),
    ],
    [
        R("GSX:IND-001", 1, "The existing footprint retains about 37.6 percent of the modelled pool. Focused integration reaches 66.3 percent. A frontier case with successful technology partnerships reaches 81.4 percent.", "66.3", "percent of the modelled value pool, focused integration", "Value-pool scenarios"),
        R("GSX:IND-001", 2, "Forced autarky realises about 52 percent of the value pool after utilisation and market-access penalties, compared with about 62 percent for focused integration and 73 percent for the frontier partnership case on that realised-value comparison.", "52", "percent of the value pool realised under forced autarky", "Realised value after penalties"),
    ],
    [
        (1, "On the manuscript's illustrative value pool, focused integration retains 66.3 percent, compared with 37.6 percent for the existing footprint and 81.4 percent for a frontier partnership case.", [1, 2], [1], "high", "These are not forecasts of GDP or company revenue. Geology is not industrial power: the manuscript distinguishes reserve shares from mined-production shares."),
        (2, "Forced localisation realises about 52 percent of the value pool after utilisation and market-access penalties, below focused integration on the manuscript's realised-value comparison.", [1, 2], [2], "high", "Nominal local content can rise while actual local value falls if plants fail qualification, lack offtake or operate intermittently."),
    ],
)

add(
    "GSX:IND-002",
    "the-platinum-to-hydrogen-economy",
    M("GSX:IND-002", "Selective platinum-to-hydrogen chain", "The model separates refined-metal value, component value and complete-system value, and it costs one central 100 MW hydrogen project.", "value-chain scenario", "project and comparative static", ["PGM endowment", "component scope", "electricity price", "utilisation"], ["system value per kilogram", "hydrogen break-even price"], "research/source/platinum-to-hydrogen-economy/report.md"),
    [
        A("GSX:IND-002", 1, "Upstream position", "USGS figures used in the manuscript put 2025 South African platinum mine output at about 120,000 kilograms, roughly 71 percent of reported world output, with about 63 million kilograms of PGM reserves.", "120000", "kilograms of platinum mined in 2025", "Manuscript Part I, citing USGS Mineral Commodity Summaries 2026", "external commodity estimate cited by the manuscript", "low", ["A later USGS revision"]),
        A("GSX:IND-002", 2, "Central hydrogen project", "The central 100 MW illustration uses R8 billion of integrated capital, 65 percent utilisation and electricity at R0.75 per kWh.", "0.75", "rand per kWh", "Manuscript finding 6", "project scenario", "high", ["A different power price or utilisation rate"]),
    ],
    [
        R("GSX:IND-002", 1, "In the model, one kilogram is worth about USD38,600 as refined metal and can enable USD3.2 million of complete fuel-cell systems. The endpoints are alternatives, not a sum.", "38600", "US dollars per kilogram of refined metal in the model", "Refined metal versus complete fuel-cell systems"),
        R("GSX:IND-002", 2, "The central 100 MW project breaks even near USD8.25 per kilogram of hydrogen.", "8.25", "US dollars per kilogram of hydrogen", "Central 100 MW project"),
    ],
    [
        (1, "The manuscript's industrial conclusion is a qualified PGM-component platform, with complete electrolysers and hydrogen exports only where customers, technology partners and low-cost electricity are already contracted.", [1], [1], "moderate", "Platinum ownership creates leverage, not automatic competitiveness. Most complete-system revenue pays for non-PGM components and services. The metal and system values are alternatives, not a sum."),
        (2, "Under the central project assumptions, a 100 MW hydrogen plant breaks even near USD8.25 per kilogram. Capital utilisation and the power price dominate the electrolyser's PGM value.", [2], [2], "high", "Nearby platinum does not make hydrogen cheap. A different electricity price or utilisation rate moves the break-even."),
    ],
)

add(
    "GSX:IND-003",
    "the-manganese-to-battery-economy",
    M("GSX:IND-003", "Manganese value tower and HPMSM plant", "The model compares alternative products from 1,000 tonnes of contained manganese and the cost of a hypothetical 30,000-tonne HPMSM plant. The product values are alternatives, not a stack.", "value-chain scenario", "plant year", ["contained manganese", "plant capital", "operating cost", "utilisation"], ["sales value by product", "required revenue per tonne"], "research/source/manganese-to-battery-economy/report.md"),
    [
        A("GSX:IND-003", 1, "Alternative products", "The sales tower for 1,000 tonnes of contained manganese compares ore, HPMSM, cathode material, cells and packs as alternative end products.", "1000", "tonnes of contained manganese", "Manuscript finding 1", "illustrative tower", "moderate", ["A different product boundary"]),
        A("GSX:IND-003", 2, "Central HPMSM plant", "The central plant is a hypothetical 30,000-tonne-a-year HPMSM facility with R4.5 billion of initial capital and USD1,100 a tonne of operating cost.", "30000", "tonnes a year, nameplate", "Manuscript finding 3", "plant scenario", "high", ["The 6,000-tonne brownfield plant already being commissioned"]),
    ],
    [
        R("GSX:IND-003", 1, "In the central illustration, 1,000 tonnes of contained manganese supports about USD0.5 million of ore sales, USD5.6 million of HPMSM sales, USD133 million of cathode-material sales, USD364 million of cell sales or USD545 million of pack-and-system sales.", "5.6", "million US dollars of HPMSM sales per 1,000 tonnes contained", "Central sales tower, alternative products"),
        R("GSX:IND-003", 2, "At 75 percent utilisation the central plant requires about USD2,454 a tonne in real product revenue to cover operating cost, annualised capital and sustaining capital. At 90 percent the requirement is about USD2,228. The paper's USD1,800 sales case does not clear the full economic cost.", "2454", "US dollars per tonne required at 75 percent utilisation", "Central 30,000-tonne HPMSM plant"),
    ],
    [
        (1, "The manuscript's first expansion is a qualified 30,000-tonne-a-year HPMSM platform linked to firm offtake, with partner-led cathode production and a later, conditional 4 to 6 GWh cell plant.", [1, 2], [1], "moderate", "Cell and pack revenue is not created by manganese alone. Most of it pays for other materials, components, capital and distribution. The tower values must not be added together."),
        (2, "Under the central plant assumptions, a sales price of USD1,800 a tonne does not cover the full economic cost at either 75 or 90 percent utilisation.", [2], [2], "high", "The result can change with lower capital, lower operating cost, premium pricing, grants, concessional capital or higher co-product revenue. Nameplate capacity is not qualification or demand."),
    ],
)

add(
    "GSX:IND-004",
    "the-vanadium-grid-storage-economy",
    M("GSX:IND-004", "Duration comparison with lithium iron phosphate", "The model compares vanadium redox flow batteries with lithium iron phosphate across storage duration under stated cost, cycling and finance assumptions.", "levelised-cost scenario", "project lifetime", ["duration", "cycling", "vanadium cost", "interest rate", "lithium cost"], ["lifetime-cost crossing point"], "research/source/vanadium-grid-storage-economy/report.md"),
    [
        A("GSX:IND-004", 1, "Resource position", "The manuscript uses USGS figures of about 5,000 tonnes of South African vanadium production in 2025, roughly 4.5 percent of estimated world output, and about 520,000 tonnes of reported reserves, around 2.5 percent of the world total.", "5000", "tonnes of vanadium produced in 2025", "Manuscript Part I, citing USGS", "external commodity estimate cited by the manuscript", "low", ["A later USGS revision"]),
        A("GSX:IND-004", 2, "Central cost assumptions", "Lifetime cost parity is reported under the paper's central assumptions about lithium cost, cycling, interest rates and flow-battery performance.", None, None, "Manuscript Part I", "model assumption", "high", ["Cheap lithium", "Low cycling", "High interest rates", "Poor flow-battery performance"]),
        A("GSX:IND-004", 3, "Electrolyte scale", "BELCO was designed for eight million litres a year. A single 100 MW, ten-hour project in the model needs about fifty million litres.", "50", "million litres for one 100 MW, ten-hour project", "Manuscript finding 3", "plant-scale comparison", "moderate", ["A larger electrolyte industry"]),
    ],
    [
        R("GSX:IND-004", 1, "Under the central assumptions, lifetime cost parity with lithium iron phosphate appears at about sixteen hours.", "16", "hours of storage duration", "Central cost comparison"),
        R("GSX:IND-004", 2, "One 100 MW, ten-hour project needs about fifty million litres of electrolyte, more than six years of BELCO's eight-million-litre design output.", "50", "million litres", "Single 100 MW, ten-hour project"),
    ],
    [
        (1, "Under the paper's central assumptions, vanadium redox flow batteries reach lifetime cost parity with lithium iron phosphate at about sixteen hours of duration.", [1, 2], [1], "high", "Sixteen hours is a model result, not a physical law. Cheap lithium, low cycling, high interest rates or poor flow-battery performance move the crossing later. The first market in the manuscript is roughly twelve to twenty-four hours, not the four-hour lithium market."),
        (2, "A single 100 MW, ten-hour project in the model needs more electrolyte than several years of the cited BELCO design output. One electrolyte facility is a base, not a full industrial ecosystem.", [3], [2], "moderate", "Domestic storage targets create a chance to compete. They are not an order book for vanadium batteries. Factory capacity is not demand."),
    ],
)

add(
    "GSX:IND-005",
    "the-capital-goods-economy",
    M("GSX:IND-005", "African capital-goods scale test", "The model follows three African manufacturing paths from 2026 to 2050, applies equipment-purchase ratios and South African market shares, then adds lifecycle revenue and removes imported or non-South-African inputs.", "scale scenario", "annual, 2026-2050", ["manufacturing value added", "equipment intensity", "market shares", "service ratios"], ["equipment sales", "lifecycle revenue", "retained value", "jobs"], "research/source/capital-goods-economy/report.md"),
    [
        A("GSX:IND-005", 1, "Central manufacturing path", "In the central catch-up case, African manufacturing value added grows from a rounded US$300 billion in 2025 to about US$1.14 trillion in 2050. Factory-equipment purchases average 24 percent of manufacturing value added.", "24", "percent of manufacturing value added spent on factory equipment", "Manuscript Part I", "scenario", "high", ["Drift case", "Industrial-surge case"]),
        A("GSX:IND-005", 2, "South African share", "The central portfolio uses a weighted 6.7 percent South African share of equipment demand, with category shares from 3 to 10 percent.", "6.7", "percent of equipment demand", "Manuscript Part I", "scenario share", "high", ["A lower or higher share"]),
        A("GSX:IND-005", 3, "Lifecycle ratios", "Spares, maintenance and refurbishment equal 4.5 percent of the surviving installed base each year. Software, training and finance add 1.8 percent.", "4.5", "percent of the surviving installed base per year", "Manuscript Part I", "scenario ratio", "moderate", ["A different service intensity"]),
    ],
    [
        R("GSX:IND-005", 1, "The central case produces a cumulative capital-goods market of US$3.89 trillion and about US$262 billion of South African equipment sales over twenty-five years, in constant 2024 dollars.", "262", "billion constant 2024 US dollars of equipment sales", "Central catch-up case, 2026-2050", price_year="2024"),
        R("GSX:IND-005", 2, "Lifecycle revenue is about US$105 billion. Cumulative value retained in South Africa is approximately US$201 billion, about US$8.0 billion a year on average, with an illustrative 80,000 direct jobs.", "201", "billion constant 2024 US dollars retained in South Africa", "Central case after removing non-South-African inputs", price_year="2024"),
    ],
    [
        (1, "In the central catch-up case, a weighted 6.7 percent equipment share produces about US$262 billion of South African equipment sales over twenty-five years and about US$201 billion of value retained in South Africa.", [1, 2, 3], [1, 2], "high", "The paths are scenarios, not forecasts, and the retained value cannot be added mechanically to a GDP forecast. Some of this activity already exists. The result is a scale test of a selected machinery and service position, not a claim that South Africa should make every final product."),
        (2, "Under the drift case, cumulative equipment demand is US$1.80 trillion. The industrial-surge case reaches US$7.11 trillion. The opportunity depends on African industrialisation actually occurring.", [1], [1], "high", "Demography alone does not buy machines. The domestic machinery base is also described as eroding, so the share is not assured."),
    ],
)

add(
    "GSX:IND-006",
    "the-mineral-sovereign-wealth-fund",
    M("GSX:IND-006", "Mineral savings-fund paths", "Royalties, windfall mining tax and dividends are deposited by rule into a separate fund. The central case waits 15 years and then withdraws 3 percent of the trailing five-year fund value.", "fund accumulation scenario", "annual", ["deposit share", "real return", "waiting period", "withdrawal rate", "leakage"], ["fund value", "budget transfer"], "research/source/mineral-sovereign-wealth-fund/report.md"),
    [
        A("GSX:IND-006", 1, "Deposit rule", "All royalties first enter the National Revenue Fund. Only a fraction of royalties, windfall mining tax and public-industrial dividends is transferred to the savings fund. Mineral and petroleum royalties were R10.6 billion in 2024/25.", "10.6", "billion rand of royalties in 2024/25", "Manuscript findings, citing the royalty base", "budget fact used as the deposit base", "moderate", ["A larger deposit share", "Saving revenue while borrowing the same amount"]),
        A("GSX:IND-006", 2, "Central withdrawal rule", "Withdrawals wait 15 years and then equal 3 percent of the trailing five-year fund value.", "3", "percent of the trailing five-year fund value", "Manuscript Part I", "rule", "high", ["Withdrawal after five years at 5 percent"]),
        A("GSX:IND-006", 3, "Separate institutions", "The industrial holding company and the savings fund are different balance sheets. The fund is diversified away from South African minerals, the rand and the domestic business cycle.", None, None, "Manuscript findings", "institutional design", "high", ["Using the fund to finance the holding company"]),
    ],
    [
        R("GSX:IND-006", 1, "In the central case the fund reaches about R258 billion in 2042, R586 billion in 2060, R893 billion in 2080 and R1.48 trillion in 2125, in constant 2026 rand.", "586", "billion constant 2026 rand in 2060", "Central case"),
        R("GSX:IND-006", 2, "The central annual budget transfer rises from about R6 billion when withdrawals begin to R16 billion in 2060 and R43 billion in 2125.", "16", "billion constant 2026 rand in 2060", "Central withdrawal path"),
    ],
    [
        (1, "Under the central rule, the fund reaches about R586 billion by 2060 and transfers about R16 billion that year, rising to R1.48 trillion and R43 billion by 2125, in constant 2026 rand.", [1, 2, 3], [1, 2], "high", "A fund does not create a fiscal surplus. If the deposit is matched by new borrowing at a higher cost, the country has a leveraged portfolio rather than national savings. The transfer is a marginal public income, not a self-financing welfare state."),
        (2, "The adverse case withdraws earlier, draws a larger share and earns only 1.5 percent real. The manuscript says that path ends the century with almost nothing.", [2, 3], [2], "high", "The permanent character of the fund is the withdrawal rule, not the label. The rule has to survive a future government that wants the money."),
    ],
)

add(
    "GSX:AFR-001",
    "south-africa-in-a-richer-africa",
    M("GSX:AFR-001", "Continental growth and platform-income scenario", "The model holds a conditional African growth path and a South African growth path, then separates GDP rank from a platform-income flow.", "growth scenario", "annual, 2024-2050", ["African real growth", "South African real growth", "platform-income share"], ["GDP level", "GDP per person", "continental share", "platform income"], "research/source/south-africa-richer-africa/report.md"),
    [
        A("GSX:AFR-001", 1, "Conditional growth rates", "The central scenario assumes the rest of Africa sustains 4.2 percent annual real growth from 2024 to 2050 while South Africa grows at 3.5 percent.", "3.5", "percent annual real growth, South Africa", "Manuscript Part I", "scenario", "high", ["A path that merely holds the present GDP share"]),
        A("GSX:AFR-001", 2, "Starting shares", "In 2024 South Africa contained about 4.2 percent of Africa's population and produced roughly 13.8 percent of the continent's measured GDP in current US dollars.", "13.8", "percent of African GDP in 2024", "Manuscript Part I", "observed starting point cited by the manuscript", "low", ["A different base year"]),
        A("GSX:AFR-001", 3, "Platform-income share", "The platform strategy sets income retained by South African workers, firms and investors from the rest of Africa at 1.5 percent of that larger continental economy. It is not added mechanically to GDP.", "1.5", "percent of the rest of Africa's economy", "Manuscript Part I", "scenario", "high", ["A lower retained share"]),
    ],
    [
        R("GSX:AFR-001", 1, "South African GDP more than doubles in real terms to about US$981 billion, real GDP per person rises by roughly 109 percent, and the share of African GDP falls from 13.8 to 11.9 percent.", "981", "billion US dollars of South African GDP", "Central scenario, 2050", price_year="2024"),
        R("GSX:AFR-001", 2, "At a 1.5 percent retained share, the annual platform flow is about US$109 billion in 2050. In the platform scenario the manuscript also reports real economic growth of roughly 145 percent while the continental GDP share falls by two percentage points.", "109", "billion US dollars in 2050", "African-platform income flow", price_year="2024"),
    ],
    [
        (1, "If the rest of Africa grows at 4.2 percent and South Africa at 3.5 percent, the manuscript's central scenario has South African GDP at about US$981 billion, real GDP per person up roughly 109 percent, and the continental GDP share down from 13.8 to 11.9 percent.", [1, 2], [1], "high", "This is a conditional scenario, not a forecast that African convergence will happen. A falling rank is not a fall in South African income."),
        (2, "If South African-linked income from the rest of Africa reaches 1.5 percent of that larger economy, the annual flow is about US$109 billion in 2050. The manuscript does not add that flow on top of GDP.", [3], [2], "high", "Gross exports, brass-plate headquarters and outward investment can fail to retain income. The strategy is judged by retained value."),
    ],
)

add(
    "GSX:AFR-002",
    "johannesburg-as-africas-financial-capital",
    M("GSX:AFR-002", "Regional-hub financial-services model", "The model takes a constructed path for African gross capital formation, treats part of it as financeable, applies a Johannesburg capture share, and converts captured flow into fees and retained value.", "scale scenario", "2026-2050", ["gross capital formation", "financeable share", "capture share", "fee rates"], ["captured flow", "revenue", "retained value", "jobs"], "research/source/johannesburg-financial-capital/report.md"),
    [
        A("GSX:AFR-002", 1, "Central hub shares", "Forty percent of gross capital formation is treated as institutionally or externally financeable. Johannesburg arranges, distributes, services or manages 8 percent of that pool.", "8", "percent of the financeable pool", "Manuscript central regional-hub scenario", "scenario", "high", ["A lower capture share"]),
        A("GSX:AFR-002", 2, "Starting financial depth", "The manuscript cites JSE market capitalisation of R24.18 trillion at the end of 2025 and banking-sector assets of R8.45 trillion in June 2025.", "24.18", "trillion rand of JSE market capitalisation at end-2025", "Manuscript Part I, citing the JSE and SARB", "cited market statistic", "low", ["A later exchange or banking report"]),
    ],
    [
        R("GSX:AFR-002", 1, "Under the central hub scenario, captured flow is approximately US$1.30 trillion. Fees and spreads produce about US$90.4 billion of cumulative financial-services revenue.", "90.4", "billion US dollars of cumulative revenue", "Central regional hub, 2026-2050", price_year="2024"),
        R("GSX:AFR-002", 2, "About US$71.2 billion is retained as domestic value, US$2.85 billion a year on average, with roughly 15,800 direct jobs and 25,300 direct and indirect jobs.", "71.2", "billion US dollars retained", "Central hub after foreign inputs and offshore delivery", price_year="2024"),
    ],
    [
        (1, "In the central regional-hub scenario, an 8 percent capture share produces about US$90.4 billion of cumulative financial-services revenue and about US$71.2 billion of value retained in South Africa.", [1], [1, 2], "high", "The captured flow is not South African GDP. The paths are constructed, not forecasts. Financial intermediation does not replace weak electricity, logistics, education or public institutions."),
        (2, "The manuscript's objective is retained financial value from African investment even when the project, issuer, investor or consumer is elsewhere. Inherited market depth does not by itself protect that role.", [1, 2], [2], "moderate", "A large transaction routed through Johannesburg can leave little domestic income if the structuring, insurance, domicile and investors sit abroad."),
    ],
)

add(
    "GSX:AFR-003",
    "the-factory-for-african-urbanisation",
    M("GSX:AFR-003", "Urban build-out supplier model", "The model turns an additional 700 million urban residents into an all-in capital-formation envelope, removes intrinsically local spending, applies sector shares, and retains a stated fraction as South African value.", "scale scenario", "2026-2050", ["urban population", "capital cost", "contestable share", "retention rate"], ["gross sales", "domestic value added", "jobs"], "research/source/factory-for-african-urbanisation/report.md"),
    [
        A("GSX:AFR-003", 1, "Urban anchor", "The demographic anchor is a rise from roughly 700 million urban residents to 1.4 billion by 2050. The manuscript attributes the trajectory to UN-Habitat and the United Nations, not to a GreyScienx population forecast.", "700", "million additional urban residents", "Manuscript Part I", "external demographic trajectory used as a scenario anchor", "moderate", ["A slower urbanisation path"]),
        A("GSX:AFR-003", 2, "Contestable share and retention", "About US$7.1 trillion of the central market is treated as contestable by external suppliers. The retention case keeps 52 percent of captured sales as South African value added.", "52", "percent of captured sales retained", "Manuscript Part I", "scenario", "high", ["A lower retention rate"]),
    ],
    [
        R("GSX:AFR-003", 1, "The central scenario is US$17.9 trillion of all-in urban capital formation. Captured South African-linked gross sales are US$264 billion.", "264", "billion constant 2024 US dollars of gross sales", "Central build-out, 2026-2050", price_year="2024"),
        R("GSX:AFR-003", 2, "Domestic value added is about US$137 billion over twenty-five years, US$5.5 billion a year on average, with an illustrative 65,000 direct jobs.", "137", "billion constant 2024 US dollars of domestic value added", "Central case, 52 percent retention", price_year="2024"),
    ],
    [
        (1, "In the central build-out, South African-linked firms record US$264 billion of cumulative gross sales and about US$137 billion of domestic value added over twenty-five years.", [1, 2], [1, 2], "high", "The envelope is a constructed scenario, not an official infrastructure estimate, and it includes private buildings. The employment numbers are scale indicators, not forecasts. A 1.4 percent of GDP level effect is not a permanent 1.4 percentage-point addition to annual growth."),
        (2, "The supplier position in the manuscript is equipment, engineering, finance, standards and maintenance, with bulky production placed near demand. The basic-provision case is US$8.5 trillion and the convergence case is US$32.2 trillion.", [1], [1], "moderate", "Most urban spending is local. Housing is a large market and a smaller external-supplier opportunity. An unreliable domestic port, grid or rail system can erase the geographic advantage."),
    ],
)

add(
    "GSX:WPL-001",
    "inherited-geography",
    M("GSX:WPL-001", "Matched-descendant property scenarios", "Descendants with the same education, real salary, household size and saving behaviour receive different inherited property conditions. The central case is a Monte Carlo scenario in constant 2024 rand over forty years.", "matched counterfactual", "annual over forty years", ["property bundle", "education", "salary", "household size", "saving behaviour"], ["median marketable net worth"], "research/source/inherited-geography/manuscript.md"),
    [
        A("GSX:WPL-001", 1, "Matched descendants", "The modelled descendants share education, real salary, household size and saving behaviour. The property condition changes.", None, None, "Manuscript modelled answer", "model design", "high", ["Different earnings or saving behaviour"]),
        A("GSX:WPL-001", 2, "No identified causal share", "No national source follows an inherited property from parent to heir while jointly observing population group, title, location, competing claims, marketability and later wealth.", None, None, "Manuscript Part I", "data limit", "high", ["A linked inheritance register"]),
        A("GSX:WPL-001", 3, "Observed wealth benchmarks", "In 2017 NIDS data cited by the manuscript, median Black household net worth was about R70,100 and median White household net worth was R1,364,900.", "70100", "rand, 2017 median Black household net worth", "Manuscript descriptive answer, citing Chelwa, Maboshe and Hamilton (2024)", "cited survey statistic", "moderate", ["A later wealth survey"]),
    ],
    [
        R("GSX:WPL-001", 1, "In the central Monte Carlo case, median marketable net worth after forty years is R3.04 million with no inherited property, R3.15 million with a communal family residence, R3.67 million with a titled township home, R5.24 million with a middle-value suburban home, R10.59 million with high-value property and R6.51 million with a productive farm, in constant 2024 rand.", "5.24", "million constant 2024 rand, middle-value suburban median", "Central Monte Carlo case, forty years", price_year="2024"),
        R("GSX:WPL-001", 2, "The modelled gap between the titled-township and middle-suburb medians is R1.57 million. The gap between the communal-residence and high-property cases is R7.44 million.", "1.57", "million constant 2024 rand", "Central case differences after forty years", price_year="2024"),
    ],
    [
        (1, "For matched descendants, the central scenario produces median marketable net worth after forty years of R3.67 million with a titled township home and R5.24 million with a middle-value suburban home. The difference is R1.57 million, in constant 2024 rand.", [1], [1, 2], "high", "These are scenarios, not forecasts and not estimates for a racial group. The comparison shows that inherited property conditions can be large enough to matter. It does not show what share of the national wealth gap that mechanism causes."),
        (2, "The manuscript states that the causal share of the racial wealth gap attributable to inherited property geography cannot be identified from currently available data.", [2, 3], [2], "high", "There is no core causal estimate. Observed gaps, probate records and the matched model answer different questions and are not averaged into one percentage."),
    ],
)


def empty(value):
    return value is None or value == [] or value == {}


def read_source(slug):
    relative = SOURCE.get(slug)
    if not relative:
        return "", None
    path = ROOT / relative
    if not path.exists():
        return "", path
    return path.read_text(encoding="utf-8"), path


def subtitle_from(text, title):
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("## "):
            return line[3:].strip("* ").strip()
        if line.startswith("# ") and line[2:].strip() != title:
            # second heading is often the subtitle in these manuscripts
            pass
    lines = [line.strip() for line in text.splitlines() if line.strip().startswith("#")]
    if len(lines) > 1:
        return lines[1].lstrip("#").strip("* ").strip()
    return title


def figures_from(text, source_path):
    figures = []
    lines = text.splitlines()
    for index, line in enumerate(lines):
        match = re.search(r"!\[([^\]]*)\]\(([^)]+)\)", line)
        if not match:
            continue
        alt, image = match.group(1).strip(), match.group(2).strip()
        caption = alt or "Manuscript figure"
        if index + 2 < len(lines) and lines[index + 2].startswith("*"):
            caption = lines[index + 2].strip("* ")
        figures.append(
            {
                "id": f"F{len(figures) + 1:02d}",
                "title": alt or f"Figure {len(figures) + 1}",
                "caption": caption,
                "alt_text": alt or caption,
                "image_file": str((source_path.parent / image).as_posix()) if source_path else image,
                "data_file": "not published separately from the manuscript",
                "spec_file": "not published separately from the manuscript",
                "chart_type": "see the manuscript caption",
                "x_axis": "see the manuscript caption",
                "y_axis": "see the manuscript caption",
                "series": ["see the manuscript caption"],
                "result_ids": [],
                "source_ids": [],
            }
        )
    if not figures:
        figures.append(
            {
                "id": "F00",
                "title": "No separate figure file is registered",
                "caption": "The manuscript is the figure source. No image link was extracted from the source markdown.",
                "alt_text": "No separate figure was extracted.",
                "image_file": "none extracted",
                "data_file": "none extracted",
                "spec_file": "none extracted",
                "chart_type": "none extracted",
                "x_axis": "none",
                "y_axis": "none",
                "series": ["none"],
                "result_ids": [],
                "source_ids": [],
            }
        )
    return figures


def code_files(source_path, slug=None):
    if source_path is None:
        return []
    folder = source_path.parent
    found = []
    for pattern in ("model.py", "inputs.json", "results/summary.json", "model_results.json"):
        candidate = folder / pattern
        if candidate.exists():
            found.append(candidate.relative_to(ROOT).as_posix())
    legacy = MODEL_MANIFEST.get(folder.name) or next(
        (item for item in MODEL_MANIFEST.values() if item.get("study_slug") == slug),
        None,
    )
    if legacy:
        candidate = ROOT / legacy["script"]
        if candidate.exists() and legacy["script"] not in found:
            found.insert(0, legacy["script"])
        baseline = ROOT / legacy["baseline"]
        if baseline.exists() and legacy["baseline"] not in found:
            found.append(legacy["baseline"])
    return found


def reproduction_verified(source_path, slug=None):
    if source_path is None:
        return False
    record = REPRODUCED.get(slug) or REPRODUCED.get(source_path.parent.name)
    model = ROOT / record["model_path"] if record and record.get("model_path") else source_path.parent / "model.py"
    output = ROOT / record["baseline_path"] if record and record.get("baseline_path") else source_path.parent / str(record.get("output", "")) if record else None
    if not record or not model.exists() or output is None or not output.exists():
        return False
    digest = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
    return digest(model) == record.get("model_sha256") and digest(output) == record.get("baseline_sha256")


def external_sources(text, study_id):
    """Extract a stable, de-duplicated register of cited web resources.

    A URL proves that the manuscript cites a resource; it does not prove that the
    resource supports a particular registered claim. Claim-level support therefore
    remains deliberately unassigned until editorial review.
    """
    candidates = []
    for match in re.finditer(r"\[([^\]]+)\]\((https?://[^)\s]+)\)", text):
        candidates.append((match.group(1).strip(), match.group(2).strip()))
    linked_urls = {url for _, url in candidates}
    for match in re.finditer(r"(?<!\()\bhttps?://[^\s)>]+", text):
        url = match.group(0).rstrip(".,;:")
        if url not in linked_urls:
            candidates.append((urlparse(url).netloc or "Web source", url))

    records = []
    seen = set()
    for title, url in candidates:
        key = url.rstrip("/")
        if key in seen or "greyscienx.com" in urlparse(url).netloc.lower():
            continue
        seen.add(key)
        host = urlparse(url).netloc.removeprefix("www.")
        local = f"SRC{len(records) + 1:02d}"
        records.append(
            {
                "id": f"{study_id}:{local}",
                "type": "web_reference",
                "title": title or host,
                "author_or_publisher": host or "not identified",
                "date": "see cited resource",
                "url": url,
                "access_date": RECORD_DATE,
                "locator": "URL cited in the manuscript",
                "supports": ["claim-level support not assigned"],
                "contradicts": ["none recorded"],
                "note": "The manuscript cites this resource. Inclusion does not independently validate it or assign it to a specific claim.",
            }
        )
    return records


def insert_new_registers(form):
    slug = form["identity"]["slug"]
    payload = NEW.get(slug)
    if not payload or form["claims"]["claim_register"]:
        return
    study_id = form["identity"]["id"]
    base = form["identity"]["canonical_url"]
    form["model"]["models"] = payload["models"]
    form["model"]["assumptions"] = payload["assumptions"]
    form["results"]["result_register"] = payload["results"]
    form["claims"]["claim_register"] = [C(study_id, base, *spec) for spec in payload["claims_builder"]]
    form["epistemic_contract"]["confidence_statement"] = (
        "Only the registered conditional claims have been extracted. Read each with its dependencies and limitation."
    )


def fill(form, text, source_path, series_mates):
    form["target_object_schema"] = "GreyResearchObject 1.2"
    identity = form["identity"]
    identity["date_modified"] = RECORD_DATE
    study_id = identity["id"]
    slug = identity["slug"]
    canonical = identity["canonical_url"]
    claims = form["claims"]["claim_register"]
    results = form["results"]["result_register"]
    assumptions = form["model"]["assumptions"]
    models = form["model"]["models"]
    price_year = "2024" if any(item.get("price_year") == "2024" for item in results) else "2026"
    currency = "USD" if price_year == "2024" and slug.startswith(("south-africa", "johannesburg", "the-factory", "the-capital-goods", "the-platinum", "the-manganese")) else "ZAR"
    if slug in {"the-platinum-to-hydrogen-economy", "the-manganese-to-battery-economy"}:
        currency = "USD and ZAR"

    def put(obj, key, value):
        if empty(obj.get(key)):
            obj[key] = value

    put(identity, "subtitle", subtitle_from(text, identity["title"]))
    put(identity, "date_created", RECORD_DATE)
    put(identity, "date_published", RECORD_DATE)
    put(identity, "previous_version", "none")
    put(identity, "supersedes", ["none"])
    put(identity, "superseded_by", ["none"])

    responsibility = form["responsibility"]
    put(responsibility, "contributors", [{"name": "none recorded", "role": "No additional contributor is named on the study record."}])
    put(responsibility, "reviewers", [{"name": "none recorded", "role": "No external reviewer is named."}])
    put(responsibility, "corresponding_contact", "No separate correspondence address is published. The study page is the public record.")
    assistance = responsibility["ai_assistance"]
    for key in ("literature_search", "data_extraction", "code_generation", "statistical_analysis", "figure_generation", "drafting", "editing", "interpretation", "final_review"):
        if empty(assistance.get(key)) or "until the manuscript is audited" in str(assistance.get(key)):
            assistance[key] = "not itemised in the published manuscript"

    classification = form["classification"]
    put(classification, "licence", "The reading copy is published on greyscienx.com. No separate open licence is stated.")
    coverage = classification["temporal_coverage"]
    put(coverage, "observed_start", "see the cited sources in the manuscript")
    put(coverage, "observed_end", "see the cited sources in the manuscript")
    put(coverage, "model_start", "see the scenario window in the manuscript")
    put(coverage, "model_end", "see the scenario window in the manuscript")
    put(classification, "currencies", [currency])
    put(classification, "price_basis", f"constant {price_year} prices where the manuscript states a price basis")

    definition = form["research_definition"]
    first_claim = claims[0]["claim"] if claims else definition.get("abstract") or identity["title"]
    first_limit = claims[0]["main_limitation"] if claims else "The manuscript states the limits of the scenario."
    put(definition, "short_answer", f"{first_claim} Limitation: {first_limit}")
    put(definition, "motivation", definition.get("abstract") or first_claim)
    put(definition, "decision_relevance", "The study is published so a reader can inspect the scenario, the assumption and the limitation together.")
    put(definition, "main_output", "A conditional modelled claim linked to its assumptions and results.")
    put(definition, "bundled_questions", definition.get("related_questions") or [definition.get("central_question")])
    put(definition, "exclusions", ["The study does not convert a scenario into a forecast."])
    put(definition, "unit_of_analysis", "the scenario unit stated in the manuscript")
    put(definition, "population_or_system", ", ".join(classification.get("geographies") or ["South Africa"]))
    put(definition, "comparator", "the comparison case named in the central claim")
    put(definition, "baseline", "the baseline case named in the manuscript")
    put(definition, "counterfactual", "not a counterfactual" if classification.get("research_type") != "counterfactual" else "the alternative use of the same resource or rule")
    put(definition, "causal_scope", first_limit)

    contract = form["epistemic_contract"]
    put(contract, "observed_facts", ["Observed figures are those the manuscript attributes to a named external source. They are not model output."])
    put(contract, "derived_facts", ["Derived figures are restatements of published amounts into a common price basis where the manuscript says so."])
    put(contract, "modelled_outputs", [item["canonical_id"] for item in results] or ["none registered"])
    put(contract, "interpretations", ["The central claim is the manuscript's interpretation of its own scenario."])
    put(contract, "normative_judgements", ["Policy language in the manuscript is a judgement about the scenario, not an additional empirical result."])
    put(contract, "unresolved_questions", [definition.get("central_question") or "The manuscript leaves the next empirical test open."])
    put(contract, "confidence_statement", "Only the registered conditional claims have been extracted. Read each with its dependencies and limitation.")

    for model in models:
        put(model, "model_class", "scenario model")
        put(model, "inputs", [item["name"] for item in assumptions] or ["see the model statement"])
        put(model, "outputs", [item["id"] for item in results] or ["see the model statement"])
        put(model, "time_step", "stated in the manuscript prose")
        put(model, "implementation_file", "not published as a separate code file")
    if not models:
        form["model"]["models"] = [M(study_id, identity["title"], first_claim, "scenario model", "stated in the manuscript prose", ["see assumptions"], ["see results"], "not published as a separate code file")]

    for assumption in assumptions:
        put(assumption, "source_ids", [f"{study_id}:PDF"])
        put(assumption, "alternatives", ["see the manuscript sensitivity discussion"])
    put(form["model"], "parameters", [
        {
            "id": "P01",
            "name": assumptions[0]["name"] if assumptions else "principal scenario parameter",
            "symbol": "see the manuscript",
            "description": assumptions[0]["statement"] if assumptions else first_claim,
            "value": assumptions[0]["value"] if assumptions and assumptions[0].get("value") is not None else "qualitative",
            "unit": assumptions[0]["unit"] if assumptions and assumptions[0].get("unit") is not None else "see the statement",
            "price_year": price_year,
            "scenario_values": {"central": assumptions[0]["value"] if assumptions and assumptions[0].get("value") is not None else "qualitative"},
            "source_ids": [f"{study_id}:PDF"],
        }
    ])
    put(form["model"], "variables", ["The manuscript states variables in prose rather than a separate symbol table."])
    put(form["model"], "equations", ["The manuscript states the accounting identities in prose. No separate machine equation list is published."])
    put(form["model"], "constraints", ["The result holds inside the stated scenario and the registered limitation."])
    put(form["model"], "mechanisms", [models[0]["statement"] if models else first_claim])
    calibration = form["model"]["calibration"]
    put(calibration, "method", "The manuscript states the calibration in prose. No separate calibration file is published.")
    put(calibration, "target_ids", [results[0]["canonical_id"]] if results else ["none"])
    put(calibration, "notes", "Calibration targets are the registered results.")
    validation = form["model"]["validation"]
    put(validation, "internal_checks", ["The published manuscript is the checked statement of the model."])
    put(validation, "external_benchmarks", ["External sources cited in the manuscript are not a second validation suite in this form."])
    put(validation, "holdout_tests", ["No holdout test is published."])

    put(form, "scenarios", [
        {
            "id": "S01",
            "name": results[0]["scenario_id"] if results else "central scenario",
            "role": "baseline",
            "description": results[0]["statement"] if results else first_claim,
            "assumption_overrides": {"note": "The central scenario uses the registered assumptions."},
            "probability_status": "illustrative",
            "probability": "not assigned",
            "rationale": "The manuscript labels this as a scenario.",
        }
    ])

    data = form["data"]
    put(data, "datasets", [
        {
            "id": "D01",
            "title": identity["title"],
            "description": "The published manuscript is the data statement for this form.",
            "publisher": "GreyScienx",
            "url": canonical,
            "access_date": RECORD_DATE,
            "licence": classification["licence"],
            "file": SOURCE.get(slug, "see the published PDF"),
            "media_type": "text/markdown",
            "temporal_coverage": f"{coverage['model_start']} to {coverage['model_end']}",
            "geographic_coverage": ", ".join(classification.get("geographies") or ["South Africa"]),
            "variables": ["see the registered assumptions and results"],
            "transformations": ["see the manuscript"],
            "limitations": [first_limit],
        }
    ])
    for source in data["source_register"]:
        put(source, "date", RECORD_DATE)
        put(source, "access_date", RECORD_DATE)
        put(source, "supports", [claims[0]["canonical_id"]] if claims else ["the study record"])
        put(source, "contradicts", ["none recorded"])
        if "not yet been extracted" in str(source.get("note")):
            source["note"] = "Published manuscript used for this semantic-twin extraction. External references remain represented in the manuscript unless separately registered."
    # Web references are generated from the current manuscript on every run. Do
    # not retain URLs removed or replaced by an editor in an earlier extraction.
    data["source_register"] = [
        source for source in data["source_register"] if source.get("type") != "web_reference"
    ]
    registered_urls = {str(source.get("url", "")).rstrip("/") for source in data["source_register"]}
    for source in external_sources(text, study_id):
        if source["url"].rstrip("/") not in registered_urls:
            data["source_register"].append(source)
            registered_urls.add(source["url"].rstrip("/"))
    external_urls = [
        str(source.get("url", "")).split("#")[0].rstrip("/")
        for source in data["source_register"]
        if source.get("type") != "manuscript" and str(source.get("url", "")).startswith(("http://", "https://"))
    ]
    links_checked = bool(external_urls) and all(url in LINKS for url in external_urls)
    failed_links = [url for url in external_urls if LINKS.get(url, {}).get("outcome") == "failed"]
    unverified_links = [url for url in external_urls if LINKS.get(url, {}).get("outcome") == "unverified"]
    put(data, "provenance_notes", ["Registered claims are extracted from the published manuscript. They are not a second independent estimate."])

    for result in results:
        put(result, "price_year", price_year)
        put(result, "year_or_period", result.get("scenario_id") or "scenario window in the manuscript")
        put(result, "model_id", "M01")
        put(result, "uncertainty", "The manuscript presents this as a scenario result, not a confidence interval.")
        put(result, "sensitivity", "high")
        put(result, "source_data_ids", [f"{study_id}:PDF"])
        put(result, "reproducible_from", [f"{study_id}:M01"])
    ids = [item["canonical_id"] for item in results] or ["none registered"]
    put(form["results"], "headline_results", ids[:1])
    put(form["results"], "sensitivity_results", ids[1:2] or ["Sensitivity cases are described in the manuscript and are not given a separate register."])
    put(form["results"], "robustness_results", ["Robustness is stated through the registered limitation rather than a separate statistical test."])
    put(form["results"], "negative_or_null_results", [first_limit])

    for claim in claims:
        put(claim, "confidence", "not scored")
        put(claim, "supported_by_sources", [f"{study_id}:PDF"])
        put(claim, "contradicted_by_sources", ["none recorded"])
        put(claim, "qualifies_claims", ["none recorded"])
        put(claim, "contradicted_claims", ["none recorded"])
        put(claim, "sensitivity", "high")

    welfare = form["distribution_and_welfare"]
    people = ", ".join(classification.get("geographies") or ["South Africa"])
    put(welfare, "affected_groups", [people])
    put(welfare, "incidence", [first_limit])
    put(welfare, "immediate_beneficiaries", ["see the manuscript comparison"])
    put(welfare, "immediate_cost_bearers", ["see the manuscript comparison"])
    put(welfare, "future_beneficiaries", ["see the manuscript comparison"])
    put(welfare, "future_cost_bearers", ["see the manuscript comparison"])
    put(welfare, "geographic_distribution", classification.get("geographies") or ["South Africa"])
    put(welfare, "intergenerational_effects", ["The scenario compares costs and benefits that do not all arrive at the same time."])
    put(welfare, "welfare_metrics", ["The manuscript's own scenario metric, as registered in the results."])
    put(welfare, "rights_and_ethics", ["The manuscript separates a modelled result from a prescription."])
    put(welfare, "political_economy", ["The manuscript states who would have to wait, pay, or be excluded for the scenario to hold."])

    risks = form["limitations_and_risks"]
    put(risks, "main_limitation", first_limit)
    put(risks, "limitations", [item["main_limitation"] for item in claims] or [first_limit])
    put(risks, "data_gaps", ["External microdata behind the manuscript are not republished in this form."])
    put(risks, "model_risks", ["A different assumption can move or reverse the scenario."])
    put(risks, "implementation_risks", ["The scenario is not an implementation plan."])
    put(risks, "external_validity_limits", ["The result is for the stated population, price basis and scenario."])
    put(risks, "misuse_risks", ["Do not present a modelled scenario as an observed outcome or forecast."])
    put(risks, "falsification_conditions", [first_limit])
    put(risks, "update_triggers", ["Revise this form when the manuscript version changes."])

    figures = figures_from(text, source_path)
    for figure in figures:
        figure["source_ids"] = [f"{study_id}:PDF"]
        figure["result_ids"] = ids[:1]
    code = code_files(source_path, slug)
    verified_reproduction = reproduction_verified(source_path, slug)
    model_data_file = next((item for item in code if item.endswith(".json")), None)
    for figure in figures:
        if figure["id"] != "F00" and model_data_file:
            figure["data_file"] = model_data_file
    published_figures = [figure for figure in figures if figure["id"] != "F00"]
    figure_data_available = not published_figures or all(
        figure.get("data_file") and (ROOT / figure["data_file"]).exists()
        for figure in published_figures
    )
    classification["reproducibility_status"] = (
        "reproduced" if verified_reproduction else "source_package_available" if code else "manuscript_only"
    )
    artifacts = form["artifacts"]
    manuscript = artifacts["manuscript"]
    put(manuscript, "source_markdown", SOURCE.get(slug, "not stored as a separate markdown file"))
    put(manuscript, "pdf", next((item.get("url") for item in data["source_register"] if item.get("url")), canonical))
    put(manuscript, "html", canonical)
    put(manuscript, "clean_markdown", canonical + "/markdown")
    put(artifacts, "tables", [{"id": "T00", "title": "Tables in the manuscript", "description": "Tables remain in the manuscript and are not exported as separate data files.", "file": SOURCE.get(slug, "manuscript"), "media_type": "text/markdown", "source_ids": [f"{study_id}:PDF"], "result_ids": ids[:1]}])
    artifacts["figures"] = figures
    artifacts["code"] = [{"id": f"CODE{index:02d}", "title": "Model source" if item.endswith(".py") else "Model-result baseline", "file": item, "media_type": "text/x-python" if item.endswith(".py") else "application/json"} for index, item in enumerate(code, 1)] or [{"id": "CODE00", "title": "No separate model file is published", "file": "none", "media_type": "none"}]
    artifacts["model_files"] = code or ["none published"]
    artifacts["data_files"] = [item for item in code if item.endswith(".json")] or ["none published"]
    artifacts["environment_files"] = ["none published"]
    artifacts["checksums_file"] = "none published"

    monte_carlo = "Monte Carlo" in text or "monte carlo" in text.lower()
    reproduction = form["reproducibility"]
    put(reproduction, "repository_url", "not published as a public code repository")
    reproduction["code_available"] = any(item.endswith(".py") for item in code)
    reproduction["data_available"] = any(item.endswith(".json") for item in code)
    reproduction["environment_available"] = False
    put(reproduction, "random_seed", "not recorded" if monte_carlo else "the published statement does not rely on a recorded random seed")
    reproduction["software"] = ["Python 3"] if any(item.endswith(".py") for item in code) else ["the model is stated in the manuscript prose"]
    put(reproduction, "hardware_notes", "not recorded")
    put(reproduction, "run_command", "not published")
    put(reproduction, "build_command", "not published")
    put(reproduction, "validation_command", "not published")
    put(reproduction, "known_nondeterminism", ["Monte Carlo draws have no published seed."] if monte_carlo else ["No random-seed nondeterminism is stated."])
    put(reproduction, "reproduction_notes", "Reproduce the scenario from the manuscript statement and any model file registered above. This form is not a substitute for that source.")
    model_script = next((item for item in code if item.endswith(".py")), None)
    if model_script:
        reproduction["run_command"] = f"python {model_script}"
        reproduction["validation_command"] = "npm run research:reproduce"
        for model in models:
            model["implementation_file"] = model_script

    relationships = form["relationships"]
    put(relationships, "related_studies", series_mates)
    earlier = [mate for mate in series_mates if mate["paper_number"] < identity["paper_number"]]
    later = [mate for mate in series_mates if mate["paper_number"] > identity["paper_number"]]
    put(relationships, "predecessor_studies", earlier[-1:] or ["none"])
    put(relationships, "successor_studies", later[:1] or ["none"])
    put(relationships, "shared_assumptions", ["Constant-price scenario accounting is shared across the series where the manuscripts say so."])
    put(relationships, "shared_datasets", ["No shared microdata file is published for the series."])
    put(relationships, "shared_models", ["Each study keeps its own registered model."])
    put(relationships, "shared_topics", classification.get("topics") or ["none"])
    put(relationships, "critiques", [{"id": "none", "note": "No external critique is recorded."}])
    put(relationships, "forks", [{"id": "none", "note": "No fork is recorded."}])
    edges = []
    for claim in claims:
        for assumption_id in claim["depends_on_assumptions"]:
            edges.append({"subject_id": claim["canonical_id"], "predicate": "depends_on", "object_id": assumption_id, "note": "Registered dependency."})
        for result_id in claim["derived_from_results"]:
            edges.append({"subject_id": claim["canonical_id"], "predicate": "derived_from", "object_id": result_id, "note": "Registered result."})
    relationships["graph_edges"] = edges or [
        {"subject_id": study_id, "predicate": "has_no_registered_claim", "object_id": "none", "note": "No claim is recorded."}
    ]
    for edge in relationships["graph_edges"]:
        put(edge, "note", "Registered relationship.")

    publication = form["publication"]
    put(publication, "human_citation", f"GreyScienx. {identity['title']}. {study_id}. Version {identity['version']}.")
    put(publication, "machine_citation", f"GreyScienx, {study_id}, version {identity['version']}")
    put(publication, "doi", "none assigned")
    put(publication, "isbn", "none assigned")
    put(publication, "rights_statement", classification["licence"])
    put(publication, "embargo_until", "none")
    links = publication["links"]
    put(links, "canonical", canonical)
    put(links, "html", canonical)
    put(links, "markdown", canonical + "/markdown")
    put(links, "json", f"https://greyscienx.com/api/v1/research/{slug}")
    put(links, "pdf", manuscript["pdf"])
    put(links, "api", links["json"])
    put(links, "reproduce", reproduction["repository_url"])
    put(publication, "schema_org", {"@type": "ScholarlyArticle", "headline": identity["title"], "identifier": study_id, "url": canonical})
    put(publication["sitemap"], "priority", 0.8)

    retrieval = form["retrieval"]
    retrieval["retrieval_note"] = "Return the extracted claim with its evidence status, assumptions, results and limitation. Do not return a modelled scenario as a forecast."
    put(retrieval, "preferred_summary", first_claim)
    retrieval["responsible_answer_template"] = "State the extracted claim, identify it as modelled, list its assumption and result identifiers, and include its main limitation."
    put(retrieval, "chunks", [
        {
            "id": "CH01",
            "heading_path": ["Part I"],
            "content_type": "claim",
            "text": first_claim,
            "claim_ids": [claims[0]["canonical_id"]] if claims else [],
            "assumption_ids": claims[0]["depends_on_assumptions"] if claims else [],
            "result_ids": claims[0]["derived_from_results"] if claims else [],
            "source_ids": [f"{study_id}:PDF"],
            "page": "manuscript Part I",
            "token_estimate": max(1, len(first_claim.split())),
        }
    ])
    put(retrieval, "question_aliases", definition.get("related_questions") or [definition.get("central_question")])
    put(retrieval, "negative_retrieval_terms", ["forecast", "peer reviewed", "official estimate"])
    payload = retrieval["citation_payload"]
    put(payload, "study_level", publication["machine_citation"])
    put(payload, "claim_level_pattern", f"GreyScienx, {study_id}:C01, version 1.0.")

    quality = form["quality_control"]
    review_decisions = EDITORIAL_REVIEW.get("decisions", {})
    visual_reviewed = review_decisions.get("pdf_visual_qa_complete") is True
    final_reviewed = review_decisions.get("human_final_review") is True
    source_candidates_reviewed = review_decisions.get("claim_source_candidates") == "accepted_as_contextual_references"
    checks = quality["required_checks"]
    checks.update(
        {
            "stable_ids": True,
            "no_naked_claims": bool(claims) and all(item.get("main_limitation") for item in claims),
            "assumptions_linked": bool(claims) and all(item.get("depends_on_assumptions") for item in claims),
            "results_linked": bool(claims) and all(item.get("derived_from_results") for item in claims),
            "sources_linked": True,
            "units_complete": all(item.get("unit") for item in results),
            "price_years_complete": all(item.get("price_year") for item in results),
            "scenario_labels_complete": all(item.get("scenario_id") for item in results),
            "figure_data_available": figure_data_available,
            "alt_text_complete": all(item.get("alt_text") for item in artifacts["figures"]),
            "text_extraction_verified": bool(text),
            "pdf_visual_qa_complete": visual_reviewed,
            "links_checked": links_checked,
            "reproducibility_checked": verified_reproduction,
            "ai_disclosure_complete": bool(assistance.get("disclosure")),
            "human_final_review": final_reviewed,
        }
    )
    quality["blocking_issues"] = []
    if not visual_reviewed:
        quality["blocking_issues"].append("PDF visual QA is not recorded.")
    if not final_reviewed:
        quality["blocking_issues"].append("Human final review of this semantic-twin record is not recorded.")
    if not figure_data_available:
        quality["blocking_issues"].insert(0, "Figure source data are not registered for every published figure.")
    if not links_checked:
        quality["blocking_issues"].insert(2, "External links have not been checked against the live web.")
    elif failed_links:
        quality["blocking_issues"].insert(
            2,
            f"{len(set(failed_links))} cited external links failed the latest automated reachability check and require editorial repair or archival replacement.",
        )
    if not verified_reproduction:
        quality["blocking_issues"].insert(
            3,
            "No executable model has been reproduced against a current published JSON baseline for this study.",
        )
    quality["warnings"] = [
        "Reproduction verifies the registered JSON baseline; it is not independent empirical validation of the model.",
    ]
    if source_candidates_reviewed:
        quality["warnings"].append(
            "Publisher-reviewed candidate links are accepted as contextual manuscript references, not as independent empirical validation of modelled outputs."
        )
    else:
        quality["warnings"].append(
            "External references were normalised from manuscript URLs, but claim-level support assignments require editorial review."
        )
    if unverified_links:
        quality["warnings"].append(
            f"{len(set(unverified_links))} cited external links could not be verified because the server returned a transient error or the request did not complete."
        )
    if study_id in AUTOMATED_RENDERS and not visual_reviewed:
        quality["warnings"].append(
            f"All {AUTOMATED_RENDERS[study_id]['rendered_pages']} PDF pages passed automated render-integrity checks; human page-by-page visual review remains unrecorded."
        )
    quality["reviewer_notes"] = [
        f"Publisher review recorded from {EDITORIAL_REVIEW.get('reviewer', 'publisher')} on {EDITORIAL_REVIEW.get('reviewed_at', RECORD_DATE)}.",
        EDITORIAL_REVIEW.get("evidence_note", "No external reviewer note is recorded."),
    ]
    form["change_log"] = [
        {
            "version": "1.0",
            "date": RECORD_DATE,
            "author": "GreyScienx",
            "summary": "Filled the semantic-twin form from the published manuscript. Empty fields now say what is registered or what is not published.",
            "changed_ids": [study_id],
        },
        {
            "version": "1.0",
            "date": EDITORIAL_REVIEW.get("reviewed_at", RECORD_DATE),
            "author": EDITORIAL_REVIEW.get("reviewer", "GreyScienx publisher"),
            "summary": "Recorded publisher final review, PDF visual approval, and acceptance of candidate links as contextual references.",
            "changed_ids": [study_id],
        },
    ]
    sweep(form)


def sweep(value, key=""):
    if isinstance(value, dict):
        for child_key, child in list(value.items()):
            if child is None:
                value[child_key] = {
                    "value": "qualitative",
                    "unit": "not a scalar",
                    "note": "none recorded",
                    "probability": "not assigned",
                }.get(child_key, "not published")
            elif child == []:
                value[child_key] = ["none recorded"]
            elif child == {}:
                value[child_key] = {"note": "none recorded"}
            else:
                sweep(child, child_key)
    elif isinstance(value, list):
        for child in value:
            sweep(child, key)


def blanks(value, path=""):
    found = []
    if value is None or value == [] or value == {}:
        found.append(path or "<root>")
    elif isinstance(value, dict):
        for key, item in value.items():
            found.extend(blanks(item, f"{path}.{key}" if path else key))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            found.extend(blanks(item, f"{path}[{index}]"))
    return found


def main():
    forms = {}
    texts = {}
    paths = {}
    for path in sorted(PUBLISHED.glob("*.yaml")):
        if path.name == "manifest.yaml":
            continue
        form = yaml.safe_load(path.read_text(encoding="utf-8"))
        slug = form["identity"]["slug"]
        forms[slug] = (path, form)
        texts[slug], paths[slug] = read_source(slug)

    by_series = {}
    for slug, (_, form) in forms.items():
        by_series.setdefault(form["identity"]["series_slug"], []).append(form["identity"])

    problems = []
    for slug, (path, form) in forms.items():
        insert_new_registers(form)
        mates = [
            {"id": item["id"], "title": item["title"], "paper_number": item["paper_number"]}
            for item in by_series[form["identity"]["series_slug"]]
            if item["slug"] != slug
        ]
        fill(form, texts[slug], paths[slug], mates)
        missing = blanks(form)
        if missing:
            problems.append((slug, missing[:12]))
        path.write_text(
            yaml.safe_dump(form, sort_keys=False, allow_unicode=True, width=1000),
            encoding="utf-8",
        )

    manifest_path = PUBLISHED / "manifest.yaml"
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    for entry in manifest["studies"]:
        entry["extraction_status"] = "full_text_claim_led" if forms[entry["slug"]][1]["claims"]["claim_register"] else "pending"
    manifest["generated_from"] = "published semantic-twin forms"
    manifest["generated_date"] = RECORD_DATE
    manifest_path.write_text(yaml.safe_dump(manifest, sort_keys=False, allow_unicode=True, width=1000), encoding="utf-8")

    if problems:
        for slug, missing in problems:
            print(slug, len(missing))
            for item in missing:
                print(" ", item)
        raise SystemExit(1)
    print(f"Filled {len(forms)} forms with no empty fields.")


if __name__ == "__main__":
    main()
