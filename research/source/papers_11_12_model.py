"""Build the quantitative exhibits for GreyScienx papers 11 and 12.

Paper 11 is a synthesis of the ten preceding thought experiments. Paper 12
introduces a common 2050 pandemic-war-recession shock and varies the way in
which emergency power is governed. The calculations are scenarios, not
forecasts. All monetary values are constant 2026 rand unless stated otherwise.
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import FancyArrowPatch, Rectangle


ROOT = Path(__file__).resolve().parents[1]
CSS = Path(r"C:\Users\Deriv\Desktop\GreyScienx\app\globals.css")
STYLE_DIR = Path(
    r"C:\Users\Deriv\Desktop\GreyScienx\skills\greyscienx-editorial-pdf\scripts"
)
sys.path.insert(0, str(STYLE_DIR))

from greyscienx_style import (  # noqa: E402
    add_figure_header,
    configure_matplotlib,
    line_encodings,
    save_figure,
    style_axis,
)


TOKENS = configure_matplotlib(CSS)
CORAL = TOKENS["coral"]
BLACK = TOKENS["black"]
TRUE_BLACK = TOKENS["true-black"]
WHITE = TOKENS["white"]
G100 = TOKENS["grey-100"]
G300 = TOKENS["grey-300"]
G500 = TOKENS["grey-500"]
G700 = TOKENS["grey-700"]
ENC = line_encodings(TOKENS)

SYN_DIR = ROOT / "work" / "population-system"
SYN_ASSETS = SYN_DIR / "assets"
EFP_DIR = ROOT / "work" / "extreme-fiscal-pressure"
EFP_ASSETS = EFP_DIR / "assets"
for directory in (SYN_ASSETS, EFP_ASSETS):
    directory.mkdir(parents=True, exist_ok=True)


def _clean_axes(ax):
    ax.set_facecolor(WHITE)
    ax.tick_params(labelsize=8)


def _header(fig, title, subtitle, field):
    add_figure_header(fig, title, subtitle, field=field, tokens=TOKENS)


def _save(fig, path):
    fig.subplots_adjust(top=0.78, left=0.095, right=0.96, bottom=0.13)
    save_figure(fig, path, dpi=260)
    plt.close(fig)


STUDIES = [
    {
        "n": 1,
        "short": "Retirement\nsustainability",
        "title": "When Retirement Becomes Impossible",
        "metric": "27%",
        "meaning": "Sustainable replacement at 60 in the base private-pension case",
        "horizon": "40-70 years",
        "risk": 78,
    },
    {
        "n": 2,
        "short": "Youth work ->\nold-age income",
        "title": "Today's Unemployment Is Tomorrow's Pension Crisis",
        "metric": "R0.15m",
        "meaning": "Wealth at 60 after persistent exclusion, versus R4.84m in stable work",
        "horizon": "40-80 years",
        "risk": 88,
    },
    {
        "n": 3,
        "short": "Later\nretirement",
        "title": "Does Raising the Retirement Age Actually Work?",
        "metric": "R213bn",
        "meaning": "Public gain for a one-million-person cohort moving from 60 to 65",
        "horizon": "5-45 years",
        "risk": 59,
    },
    {
        "n": 4,
        "short": "Ageing\nelectorate",
        "title": "The Politics of an Ageing Electorate",
        "metric": "2039",
        "meaning": "Baseline year age 60+ voters overtake voters aged 18-34",
        "horizon": "10-75 years",
        "risk": 73,
    },
    {
        "n": 5,
        "short": "Ageing\nausterity",
        "title": "Emergency Ageing Austerity",
        "metric": "R150bn",
        "meaning": "Annual fiscal gap allocated across politically plausible packages",
        "horizon": "0-15 years",
        "risk": 82,
    },
    {
        "n": 6,
        "short": "Cost of an\nextra birth",
        "title": "The Price of Another Child",
        "metric": "R780k",
        "meaning": "Median cost per additional birth for the modelled family bundle",
        "horizon": "20-90 years",
        "risk": 69,
    },
    {
        "n": 7,
        "short": "Hundred-year\nlife",
        "title": "The Hundred-Year Life",
        "metric": "57.4",
        "meaning": "Work-equivalent years in the modelled multi-stage life",
        "horizon": "0-95 years",
        "risk": 65,
    },
    {
        "n": 8,
        "short": "Late\ninheritance",
        "title": "Inheritance After Retirement",
        "metric": "R3.24m",
        "meaning": "Value at 100 of R1m inherited at 70, at 4% real growth",
        "horizon": "20-75 years",
        "risk": 54,
    },
    {
        "n": 9,
        "short": "Managed\nshrinkage",
        "title": "How to Shrink a Country Without Breaking It",
        "metric": "+3.5%",
        "meaning": "Households by 2076 even while population falls 22.2%",
        "horizon": "10-50 years",
        "risk": 75,
    },
    {
        "n": 10,
        "short": "Scarce-worker\neconomy",
        "title": "The Scarce-Worker Economy",
        "metric": "738k",
        "meaning": "Unfilled health and care jobs in the 2076 average case",
        "horizon": "10-50 years",
        "risk": 86,
    },
]


def make_synthesis_system_map():
    fig, ax = plt.subplots(figsize=(9.2, 6.1))
    fig.subplots_adjust(top=0.80, left=0.03, right=0.97, bottom=0.04)
    _header(
        fig,
        "Ten studies, one population system",
        "Flows run through lives, households, the economy, the budget and politics",
        "GREYSCIENX / PAPER 11",
    )
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)
    ax.axis("off")

    nodes = {
        "fertility": (0.7, 5.3, "6 / Fertility\nNew cohorts"),
        "youth": (2.8, 5.3, "2 / Youth work\nContribution histories"),
        "life": (5.0, 5.3, "7 / Longer lives\nMulti-stage careers"),
        "retire": (7.2, 5.3, "1 + 3 / Retirement\nAge and adequacy"),
        "fiscal": (9.2, 3.5, "5 / Fiscal balance\nTaxes and benefits"),
        "politics": (7.2, 1.5, "4 / Politics\nWho decides"),
        "workers": (5.0, 1.5, "10 / Workers\nAI and migration"),
        "places": (2.8, 1.5, "9 / Places\nHousing and networks"),
        "wealth": (0.7, 3.5, "8 / Wealth\nInheritance timing"),
    }
    for key, (x, y, label) in nodes.items():
        is_central = key == "fiscal"
        width, height = (1.55, 0.92) if not is_central else (1.6, 1.0)
        face = TRUE_BLACK if is_central else WHITE
        edge = CORAL if is_central else BLACK
        text_color = WHITE if is_central else BLACK
        rect = Rectangle(
            (x - width / 2, y - height / 2), width, height,
            linewidth=1.6 if is_central else 1.0, edgecolor=edge, facecolor=face,
        )
        ax.add_patch(rect)
        ax.text(x, y, label, ha="center", va="center", fontsize=8.3,
                fontweight="bold", color=text_color, linespacing=1.25)

    links = [
        ("fertility", "youth"), ("youth", "life"), ("life", "retire"),
        ("retire", "fiscal"), ("fiscal", "politics"), ("politics", "workers"),
        ("workers", "places"), ("places", "wealth"), ("wealth", "fertility"),
        ("workers", "fiscal"), ("youth", "workers"), ("places", "fiscal"),
        ("politics", "retire"),
    ]
    for a, b in links:
        x1, y1, _ = nodes[a]
        x2, y2, _ = nodes[b]
        arrow = FancyArrowPatch(
            (x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=10,
            connectionstyle="arc3,rad=0.08", linewidth=1.0,
            color=G500, alpha=0.85, shrinkA=33, shrinkB=33,
        )
        ax.add_patch(arrow)

    ax.text(
        4.97, 3.48,
        "HOUSEHOLD FORMATION\nThe prequel: sharing changes\nconsumption, housing and resilience",
        ha="center", va="center", fontsize=9.4, fontweight="bold", color=CORAL,
        bbox=dict(boxstyle="square,pad=0.55", facecolor=G100, edgecolor=CORAL, linewidth=1.3),
    )
    save_figure(fig, SYN_ASSETS / "ten-studies-one-system.png", dpi=260)
    plt.close(fig)


def make_synthesis_headline_metrics():
    fig, axes = plt.subplots(2, 5, figsize=(10.2, 5.6))
    fig.subplots_adjust(top=0.77, left=0.035, right=0.985, bottom=0.06, wspace=0.16, hspace=0.28)
    _header(
        fig,
        "The ten headline results",
        "Selected outputs from the preceding hypothetical models; units and denominators differ",
        "GREYSCIENX / PAPER 11",
    )
    for ax, study in zip(axes.flat, STUDIES):
        ax.axis("off")
        ax.add_patch(Rectangle((0, 0), 1, 1, transform=ax.transAxes, facecolor=WHITE,
                               edgecolor=G300, linewidth=1.0))
        ax.add_patch(Rectangle((0, 0.90), 1, 0.10, transform=ax.transAxes,
                               facecolor=CORAL, edgecolor="none"))
        ax.text(0.06, 0.82, f"{study['n']:02d}", transform=ax.transAxes,
                color=CORAL, fontsize=9, fontweight="bold")
        ax.text(0.06, 0.58, study["metric"], transform=ax.transAxes,
                color=BLACK, fontsize=19, fontweight="bold")
        ax.text(0.06, 0.40, study["short"].replace("\n", " "), transform=ax.transAxes,
                color=BLACK, fontsize=8.1, fontweight="bold", va="top", wrap=True)
        words = study["meaning"].split()
        lines, current = [], ""
        for word in words:
            trial = f"{current} {word}".strip()
            if len(trial) <= 28:
                current = trial
            else:
                lines.append(current)
                current = word
        if current:
            lines.append(current)
        ax.text(0.06, 0.29, "\n".join(lines[:4]), transform=ax.transAxes,
                color=G500, fontsize=6.8, va="top", linespacing=1.22)
    save_figure(fig, SYN_ASSETS / "ten-headline-results.png", dpi=260)
    plt.close(fig)


def make_synthesis_policy_clock():
    fig, ax = plt.subplots(figsize=(9.2, 5.7))
    _header(
        fig,
        "The policy clock",
        "Some levers buy months; others require a generation before they change the contributor base",
        "GREYSCIENX / PAPER 11",
    )
    actions = [
        ("Targeted transfers and temporary tax", 0.1, 2, "Now"),
        ("Managed infrastructure consolidation", 2, 18, "Places"),
        ("Older-worker job redesign", 2, 15, "Work"),
        ("Migration and qualification recognition", 1, 12, "People"),
        ("Training pipelines for care and trades", 3, 15, "Skills"),
        ("Pension contribution and indexation reform", 1, 30, "Finance"),
        ("Multi-stage career and healthspan reform", 8, 45, "Lives"),
        ("Fertility and family formation policy", 20, 55, "Births"),
        ("Living-transfer and inheritance reform", 3, 50, "Wealth"),
    ]
    y = np.arange(len(actions))[::-1]
    for idx, (label, start, end, _) in enumerate(actions):
        yi = y[idx]
        ax.barh(yi, end - start, left=start, height=0.58,
                color=CORAL if idx in (0, 3, 7) else G700, alpha=0.95)
        ax.scatter([start], [yi], color=BLACK, s=18, zorder=4)
        ax.text(-1.2, yi, label, ha="right", va="center", fontsize=8.2,
                fontweight="bold" if idx in (0, 7) else "normal")
        ax.text(end + 0.8, yi, f"{end:g}y", ha="left", va="center", fontsize=7.5, color=G500)
    for marker, label in [(0, "crisis"), (5, "term"), (20, "new worker"), (40, "retirement")]:
        ax.axvline(marker, color=G300, linewidth=0.8, zorder=0)
        ax.text(marker, len(actions) - 0.25, label, ha="center", va="bottom", fontsize=7.2, color=G500)
    ax.set_xlim(-0.5, 60)
    ax.set_yticks([])
    ax.set_xlabel("Years before the lever is substantially effective")
    style_axis(ax, TOKENS, grid_axis="x")
    fig.subplots_adjust(top=0.78, left=0.31, right=0.96, bottom=0.13)
    save_figure(fig, SYN_ASSETS / "policy-clock.png", dpi=260)
    plt.close(fig)


def make_synthesis_matrix():
    levers = [
        "Jobs", "Healthspan", "Retirement", "Family policy", "Housing",
        "Transfers", "Productivity", "Migration", "Institutions",
    ]
    matrix = np.array([
        [1, 2, 3, 0, 0, 2, 2, 1, 2],
        [3, 1, 2, 1, 1, 2, 2, 1, 2],
        [2, 3, 3, 0, 0, 2, 2, 1, 2],
        [1, 1, 2, 1, 1, 2, 1, 1, 3],
        [2, 2, 3, 1, 1, 3, 2, 1, 3],
        [2, 1, 0, 3, 3, 3, 1, 1, 2],
        [3, 3, 3, 1, 2, 2, 3, 1, 3],
        [2, 1, 1, 1, 3, 3, 2, 0, 3],
        [2, 1, 1, 2, 3, 2, 2, 2, 3],
        [3, 3, 2, 1, 2, 2, 3, 3, 3],
    ])
    cmap = LinearSegmentedColormap.from_list("gs", [WHITE, G300, G700, CORAL])
    fig, ax = plt.subplots(figsize=(9.7, 6.3))
    _header(
        fig,
        "No paper has a one-lever solution",
        "Model dependency: 0 = peripheral, 1 = useful, 2 = important, 3 = binding",
        "GREYSCIENX / PAPER 11",
    )
    ax.imshow(matrix, aspect="auto", cmap=cmap, vmin=0, vmax=3)
    ax.set_xticks(np.arange(len(levers)), levers, rotation=38, ha="right", fontsize=7.5)
    ax.set_yticks(np.arange(10), [f"{s['n']:02d}  {s['short'].replace(chr(10), ' ')}" for s in STUDIES], fontsize=7.5)
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            val = matrix[i, j]
            ax.text(j, i, str(val), ha="center", va="center", fontsize=7,
                    color=WHITE if val >= 2 else BLACK, fontweight="bold")
    ax.set_xticks(np.arange(-0.5, len(levers), 1), minor=True)
    ax.set_yticks(np.arange(-0.5, 10, 1), minor=True)
    ax.grid(which="minor", color=WHITE, linewidth=1.2)
    ax.tick_params(which="minor", bottom=False, left=False)
    for spine in ax.spines.values():
        spine.set_visible(False)
    fig.subplots_adjust(top=0.78, left=0.27, right=0.97, bottom=0.18)
    save_figure(fig, SYN_ASSETS / "intervention-matrix.png", dpi=260)
    plt.close(fig)


def make_synthesis_delay_curve():
    years = np.arange(2026, 2081)
    t = years - 2026
    early = 22 + 0.42 * t + 4 * np.sin(t / 13)
    delayed = 22 + 0.75 * t + 0.035 * np.maximum(years - 2040, 0) ** 2
    crisis = delayed.copy()
    crisis += np.where(years >= 2050, 22 * (1 - np.exp(-(years - 2050) / 5)), 0)
    fig, ax = plt.subplots(figsize=(9.2, 5.5))
    _header(
        fig,
        "Delay converts adjustment into emergency",
        "A synthetic system-pressure index combining fiscal, labour, household and spatial stress",
        "GREYSCIENX / PAPER 11",
    )
    for series, label, enc in [
        (early, "Early portfolio reform", ENC[0]),
        (delayed, "Delayed adjustment", ENC[1]),
        (crisis, "Delayed plus 2050 shock", ENC[2]),
    ]:
        ax.plot(years, series, label=label, linewidth=2.0, markevery=8, markersize=4, **enc)
        ax.text(years[-1] + 0.5, series[-1], f"{series[-1]:.0f}", va="center", fontsize=8, color=enc["color"])
    ax.axvline(2050, color=CORAL, linewidth=1.0, alpha=0.8)
    ax.text(2050.5, ax.get_ylim()[1] * 0.92, "2050 shock", color=CORAL, fontsize=8, fontweight="bold")
    ax.set_ylabel("System pressure, synthetic index")
    ax.set_xlabel("Year")
    ax.legend(frameon=False, loc="upper left", fontsize=8)
    style_axis(ax, TOKENS)
    _save(fig, SYN_ASSETS / "cost-of-delay.png")


def make_synthesis():
    make_synthesis_system_map()
    make_synthesis_headline_metrics()
    make_synthesis_policy_clock()
    make_synthesis_matrix()
    make_synthesis_delay_curve()
    out = {
        "scope": "Synthesis of ten preceding GreyScienx hypothetical models",
        "monetary_unit": "constant 2026 South African rand",
        "studies": STUDIES,
        "synthetic_pressure_index": {
            "warning": "Normalised illustration; components are not directly commensurable",
            "early_reform_2080": 22 + 0.42 * 54 + 4 * math.sin(54 / 13),
            "delayed_2080": 22 + 0.75 * 54 + 0.035 * 40 ** 2,
        },
    }
    (SYN_DIR / "model_results.json").write_text(json.dumps(out, indent=2), encoding="utf-8")


# ----------------------- Paper 12 model -----------------------


YEARS = np.arange(2026, 2081)
BASELINE_GDP_2026 = 6.5  # R trillion, constant 2026 rand


def interp(points):
    xp, fp = zip(*points)
    return np.interp(YEARS, xp, fp)


def baseline_series():
    gdp = np.zeros(len(YEARS))
    gdp[0] = BASELINE_GDP_2026
    for i in range(1, len(YEARS)):
        year = YEARS[i]
        growth = np.interp(year, [2027, 2050, 2080], [0.018, 0.015, 0.012])
        gdp[i] = gdp[i - 1] * (1 + growth)
    population = interp([(2026, 64.0), (2040, 67.7), (2050, 68.4), (2080, 63.8)])
    contributors = interp([(2026, 18.0), (2050, 17.2), (2080, 15.0)])
    retirees = interp([(2026, 6.0), (2050, 9.0), (2080, 13.0)])
    youth_employment = interp([(2026, 42), (2050, 47), (2080, 52)])
    tfr = interp([(2026, 2.15), (2050, 1.80), (2080, 1.65)])
    household_size = interp([(2026, 3.25), (2050, 2.80), (2080, 2.45)])
    trust = interp([(2026, 50), (2050, 48), (2080, 48)])
    debt = interp([(2026, 73), (2049, 85), (2050, 86), (2060, 98), (2070, 107), (2080, 116)])
    hidden = interp([(2026, 4), (2050, 7), (2080, 12)])
    pension = np.full(len(YEARS), 100.0)
    inheritance = np.full(len(YEARS), 100.0)
    maintenance = interp([(2026, 100), (2050, 108), (2080, 124)])
    return {
        "gdp": gdp,
        "population": population,
        "contributors": contributors,
        "retirees": retirees,
        "youth_employment": youth_employment,
        "tfr": tfr,
        "household_size": household_size,
        "trust": trust,
        "debt": debt,
        "hidden": hidden,
        "pension": pension,
        "inheritance": inheritance,
        "maintenance": maintenance,
    }


BASE = baseline_series()

SCENARIO_POINTS = {
    "Guardrailed emergency": {
        "gdp_gap": [(2026, 0), (2049, 0), (2050, -9), (2051, -6), (2052, -3), (2055, -0.8), (2065, -0.7), (2080, -1.2)],
        "contrib_gap": [(2026, 0), (2049, 0), (2050, -5), (2053, -2), (2060, -1), (2080, -2)],
        "retiree_gap": [(2026, 0), (2080, 0)],
        "youth": [(2026, 42), (2049, 47), (2050, 37), (2053, 45), (2060, 48), (2080, 50)],
        "tfr": [(2026, 2.15), (2049, 1.81), (2051, 1.64), (2056, 1.75), (2080, 1.60)],
        "household": [(2026, 3.25), (2049, 2.81), (2052, 2.94), (2060, 2.72), (2080, 2.52)],
        "trust": [(2026, 50), (2049, 48), (2050, 44), (2053, 48), (2060, 51), (2080, 50)],
        "debt": [(2026, 73), (2049, 85), (2050, 95), (2053, 108), (2060, 112), (2070, 116), (2080, 120)],
        "hidden": [(2026, 4), (2049, 7), (2053, 10), (2060, 8), (2080, 6)],
        "pension": [(2026, 100), (2049, 100), (2052, 94), (2080, 93)],
        "inheritance": [(2026, 100), (2049, 100), (2052, 96), (2080, 94)],
        "maintenance": [(2026, 100), (2049, 108), (2053, 121), (2060, 116), (2080, 135)],
        "skilled_migration_2080": -0.2,
        "regime_end": 2052,
        "coral": True,
    },
    "Extended executive emergency": {
        "gdp_gap": [(2026, 0), (2049, 0), (2050, -9), (2053, -10), (2058, -13), (2065, -15), (2080, -21)],
        "contrib_gap": [(2026, 0), (2049, 0), (2050, -5), (2058, -10), (2080, -15)],
        "retiree_gap": [(2026, 0), (2049, 0), (2060, -1), (2080, -2)],
        "youth": [(2026, 42), (2049, 47), (2050, 34), (2058, 36), (2080, 39)],
        "tfr": [(2026, 2.15), (2049, 1.81), (2053, 1.48), (2060, 1.43), (2080, 1.40)],
        "household": [(2026, 3.25), (2049, 2.81), (2055, 3.02), (2080, 2.70)],
        "trust": [(2026, 50), (2049, 48), (2051, 36), (2058, 31), (2065, 34), (2080, 35)],
        "debt": [(2026, 73), (2049, 85), (2050, 93), (2053, 103), (2060, 99), (2070, 106), (2080, 115)],
        "hidden": [(2026, 4), (2049, 7), (2053, 19), (2060, 31), (2070, 34), (2080, 35)],
        "pension": [(2026, 100), (2049, 100), (2053, 79), (2060, 67), (2080, 61)],
        "inheritance": [(2026, 100), (2049, 100), (2053, 82), (2060, 69), (2080, 58)],
        "maintenance": [(2026, 100), (2049, 108), (2058, 150), (2080, 192)],
        "skilled_migration_2080": -1.9,
        "regime_end": 2058,
        "coral": False,
    },
    "Permanent constitutional suspension": {
        "gdp_gap": [(2026, 0), (2049, 0), (2050, -9), (2053, -16), (2058, -23), (2065, -31), (2080, -42)],
        "contrib_gap": [(2026, 0), (2049, 0), (2050, -6), (2058, -18), (2065, -25), (2080, -37)],
        "retiree_gap": [(2026, 0), (2049, 0), (2060, -2), (2080, -5)],
        "youth": [(2026, 42), (2049, 47), (2050, 32), (2058, 29), (2080, 26)],
        "tfr": [(2026, 2.15), (2049, 1.81), (2053, 1.38), (2065, 1.23), (2080, 1.18)],
        "household": [(2026, 3.25), (2049, 2.81), (2055, 3.18), (2080, 2.95)],
        "trust": [(2026, 50), (2049, 48), (2051, 29), (2058, 23), (2080, 18)],
        "debt": [(2026, 73), (2049, 85), (2050, 92), (2055, 97), (2060, 88), (2070, 76), (2080, 70)],
        "hidden": [(2026, 4), (2049, 7), (2053, 27), (2060, 54), (2070, 78), (2080, 95)],
        "pension": [(2026, 100), (2049, 100), (2053, 69), (2060, 48), (2080, 29)],
        "inheritance": [(2026, 100), (2049, 100), (2053, 72), (2060, 51), (2080, 27)],
        "maintenance": [(2026, 100), (2049, 108), (2058, 173), (2080, 278)],
        "skilled_migration_2080": -4.8,
        "regime_end": 2080,
        "coral": False,
    },
}


def build_scenarios():
    result = {"No 2050 shock": BASE}
    for name, cfg in SCENARIO_POINTS.items():
        gap = interp(cfg["gdp_gap"])
        contributor_gap = interp(cfg["contrib_gap"])
        retiree_gap = interp(cfg["retiree_gap"])
        result[name] = {
            "gdp": BASE["gdp"] * (1 + gap / 100),
            "population": BASE["population"] * (1 + 0.42 * contributor_gap / 100),
            "contributors": BASE["contributors"] * (1 + contributor_gap / 100),
            "retirees": BASE["retirees"] * (1 + retiree_gap / 100),
            "youth_employment": interp(cfg["youth"]),
            "tfr": interp(cfg["tfr"]),
            "household_size": interp(cfg["household"]),
            "trust": interp(cfg["trust"]),
            "debt": interp(cfg["debt"]),
            "hidden": interp(cfg["hidden"]),
            "pension": interp(cfg["pension"]),
            "inheritance": interp(cfg["inheritance"]),
            "maintenance": interp(cfg["maintenance"]),
        }
    return result


SCENARIOS = build_scenarios()

SCENARIO_STYLE = {
    "No 2050 shock": {"color": G300, "linestyle": "-", "marker": None},
    "Guardrailed emergency": {"color": CORAL, "linestyle": "-", "marker": "o"},
    "Extended executive emergency": {"color": BLACK, "linestyle": (0, (5, 3)), "marker": "s"},
    "Permanent constitutional suspension": {"color": G500, "linestyle": (0, (1, 2)), "marker": "D"},
}


def plot_lines(ax, key, labels=True, endpoint_format="{:.0f}", markevery=8):
    for name, values in SCENARIOS.items():
        style = SCENARIO_STYLE[name]
        ax.plot(YEARS, values[key], label=name, linewidth=2.0,
                color=style["color"], linestyle=style["linestyle"],
                marker=style["marker"], markevery=markevery, markersize=3.5)
        if labels:
            ax.text(2080.6, values[key][-1], endpoint_format.format(values[key][-1]),
                    color=style["color"], fontsize=7.2, va="center")


def make_regime_timeline():
    fig, ax = plt.subplots(figsize=(9.5, 5.6))
    _header(
        fig,
        "The same 2050 shock, three governance paths",
        "The experiment changes emergency duration and safeguards, not the initial pandemic-war-recession hit",
        "GREYSCIENX / PAPER 12",
    )
    rows = [
        ("Guardrailed emergency", 2050, 2053, CORAL, "21-day start; reviewed; sunset; full institutions"),
        ("Extended executive emergency", 2050, 2059, BLACK, "Emergency decrees; weak review; elections delayed"),
        ("Permanent constitutional suspension", 2050, 2080, G500, "Constitutional rupture; command finance becomes permanent"),
    ]
    ys = [2.6, 1.6, 0.6]
    for (name, start, end, colour, note), y in zip(rows, ys):
        ax.barh(y, end - start, left=start, height=0.42, color=colour, zorder=2)
        ax.scatter([start], [y], s=52, color=CORAL, edgecolor=BLACK, linewidth=0.8, zorder=3)
        ax.text(2049.2, y, name, ha="right", va="center", fontsize=8.6, fontweight="bold")
        ax.text(start + 0.6, y - 0.34, note, ha="left", va="top", fontsize=7.4, color=G500)
    ax.axvspan(2050, 2052, color=CORAL, alpha=0.08)
    ax.text(2051, 3.12, "Acute shock", ha="center", va="bottom", fontsize=8, color=CORAL, fontweight="bold")
    ax.set_xlim(2048, 2082)
    ax.set_ylim(0, 3.45)
    ax.set_yticks([])
    ax.set_xlabel("Year")
    style_axis(ax, TOKENS, grid_axis="x")
    fig.subplots_adjust(top=0.78, left=0.29, right=0.96, bottom=0.13)
    save_figure(fig, EFP_ASSETS / "regime-timeline.png", dpi=260)
    plt.close(fig)


def make_gdp_debt():
    fig, axes = plt.subplots(1, 2, figsize=(10.1, 5.2))
    _header(
        fig,
        "Command can compress the deficit while shrinking the economy",
        "Real output and official debt; hidden claims include pension losses, arrears and deferred maintenance",
        "GREYSCIENX / PAPER 12",
    )
    ax = axes[0]
    for name, values in SCENARIOS.items():
        s = SCENARIO_STYLE[name]
        index = values["gdp"] / BASE["gdp"][YEARS == 2049][0] * 100
        ax.plot(YEARS, index, label=name, linewidth=2, color=s["color"], linestyle=s["linestyle"],
                marker=s["marker"], markevery=8, markersize=3)
        ax.text(2080.5, index[-1], f"{index[-1]:.0f}", va="center", fontsize=7, color=s["color"])
    ax.axvline(2050, color=CORAL, linewidth=0.9)
    ax.set_title("Real GDP index")
    ax.set_ylabel("2049 = 100")
    ax.set_xlabel("Year")
    style_axis(ax, TOKENS)

    ax = axes[1]
    for name, values in SCENARIOS.items():
        s = SCENARIO_STYLE[name]
        ax.plot(YEARS, values["debt"], linewidth=2, color=s["color"], linestyle=s["linestyle"],
                marker=s["marker"], markevery=8, markersize=3)
    for name in ("Extended executive emergency", "Permanent constitutional suspension"):
        values = SCENARIOS[name]
        s = SCENARIO_STYLE[name]
        augmented = values["debt"] + values["hidden"]
        ax.plot(YEARS, augmented, linewidth=1.2, color=s["color"], linestyle="-", alpha=0.45)
        ax.fill_between(YEARS, values["debt"], augmented, color=s["color"], alpha=0.08)
    ax.axvline(2050, color=CORAL, linewidth=0.9)
    ax.set_title("Debt and hidden public burden")
    ax.set_ylabel("Percent of GDP")
    ax.set_xlabel("Year")
    style_axis(ax, TOKENS)
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, frameon=False, fontsize=7.3, ncol=2,
               loc="lower center", bbox_to_anchor=(0.5, 0.015))
    fig.subplots_adjust(top=0.76, left=0.08, right=0.97, bottom=0.18, wspace=0.25)
    save_figure(fig, EFP_ASSETS / "gdp-and-public-burden.png", dpi=260)
    plt.close(fig)


FISCAL_COMPONENTS = {
    "Guardrailed emergency": {
        "Temporary progressive levy": 2.5,
        "Transparent reprioritisation": 2.0,
        "Contingency reserves": 1.0,
        "Emergency borrowing": 6.0,
        "Limited pension indexation": 0.5,
        "Guarantees / liquidity": 2.0,
    },
    "Extended executive emergency": {
        "Broad compulsory levy": 4.0,
        "Service cuts": 3.0,
        "Forced pension holdings": 3.0,
        "Monetary finance": 2.5,
        "Rationing and arrears": 1.5,
    },
    "Permanent constitutional suspension": {
        "Confiscatory levies": 3.5,
        "Pension conversion": 4.0,
        "Monetary repression": 3.0,
        "Service rationing": 2.5,
        "Arrears / default": 1.0,
    },
}


def make_fiscal_composition():
    fig, axes = plt.subplots(1, 3, figsize=(12.2, 5.8), sharey=False)
    _header(
        fig,
        "How the first-year fiscal hole is made to disappear",
        "Each case allocates a 14% of GDP 2050 emergency need; incidence differs radically",
        "GREYSCIENX / PAPER 12",
    )
    for ax, (scenario, components) in zip(axes, FISCAL_COMPONENTS.items()):
        labels = list(components)
        vals = list(components.values())
        y = np.arange(len(labels))[::-1]
        colours = [CORAL] + [BLACK if i % 2 else G500 for i in range(1, len(vals))]
        ax.barh(y, vals, color=colours, height=0.58)
        for yi, val in zip(y, vals):
            ax.text(val + 0.08, yi, f"{val:.1f}", va="center", fontsize=7.2, fontweight="bold")
        ax.set_yticks(y, labels, fontsize=6.9)
        ax.set_title(scenario.replace(" emergency", "\nemergency"), fontsize=9.2)
        ax.set_xlabel("% of GDP")
        ax.set_xlim(0, 6.8)
        style_axis(ax, TOKENS, grid_axis="x")
    fig.subplots_adjust(top=0.76, left=0.12, right=0.98, bottom=0.13, wspace=0.90)
    save_figure(fig, EFP_ASSETS / "first-year-fiscal-closure.png", dpi=260)
    plt.close(fig)


DOMAIN_DAMAGE = {
    "Household security / cohabitation": [5, 18, 42],
    "Retirement adequacy": [4, 24, 51],
    "Youth lifetime pensions": [6, 28, 58],
    "Feasible later retirement": [3, 17, 38],
    "Fiscal-democratic balance": [2, 34, 72],
    "Austerity welfare loss": [8, 30, 65],
    "Fertility-policy effectiveness": [4, 22, 46],
    "Hundred-year-life adaptability": [3, 20, 49],
    "Useful early wealth transfers": [2, 26, 55],
    "Managed urban shrinkage": [5, 31, 62],
    "Essential-worker capacity": [4, 27, 59],
}


def make_domain_heatmap():
    matrix = np.array(list(DOMAIN_DAMAGE.values()))
    cmap = LinearSegmentedColormap.from_list("damage", [WHITE, G300, G700, CORAL])
    fig, ax = plt.subplots(figsize=(8.9, 6.4))
    _header(
        fig,
        "The 2050 regime reaches every previous study",
        "Modelled 2070 damage relative to the no-shock path; 0 = none, 100 = extreme",
        "GREYSCIENX / PAPER 12",
    )
    ax.imshow(matrix, aspect="auto", cmap=cmap, vmin=0, vmax=75)
    col_labels = ["Guardrailed", "Extended", "Permanent"]
    ax.set_xticks(range(3), col_labels, fontsize=8.4)
    ax.set_yticks(range(len(DOMAIN_DAMAGE)), list(DOMAIN_DAMAGE), fontsize=7.8)
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            value = matrix[i, j]
            ax.text(j, i, f"{value}", ha="center", va="center", fontsize=7.5,
                    color=WHITE if value > 28 else BLACK, fontweight="bold")
    ax.set_xticks(np.arange(-0.5, 3, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, len(DOMAIN_DAMAGE), 1), minor=True)
    ax.grid(which="minor", color=WHITE, linewidth=1.3)
    ax.tick_params(which="minor", bottom=False, left=False)
    for spine in ax.spines.values():
        spine.set_visible(False)
    fig.subplots_adjust(top=0.78, left=0.34, right=0.97, bottom=0.13)
    save_figure(fig, EFP_ASSETS / "cross-study-damage.png", dpi=260)
    plt.close(fig)


def make_people_pathways():
    fig, axes = plt.subplots(2, 2, figsize=(10.0, 7.2))
    _header(
        fig,
        "The emergency is carried through people's lives",
        "Employment, contribution support, funded wealth and fertility after the common 2050 shock",
        "GREYSCIENX / PAPER 12",
    )
    specs = [
        ("youth_employment", "Youth employment rate", "%", "{:.0f}%"),
        ("ratio", "Contributors per retiree", "ratio", "{:.2f}"),
        ("pension", "Private pension wealth", "2049 = 100", "{:.0f}"),
        ("tfr", "Total fertility rate", "births per woman", "{:.2f}"),
    ]
    for ax, (key, title, ylabel, fmt) in zip(axes.flat, specs):
        for name, values in SCENARIOS.items():
            s = SCENARIO_STYLE[name]
            series = values["contributors"] / values["retirees"] if key == "ratio" else values[key]
            ax.plot(YEARS, series, linewidth=1.8, color=s["color"], linestyle=s["linestyle"],
                    marker=s["marker"], markevery=9, markersize=3)
            ax.text(2080.5, series[-1], fmt.format(series[-1]), color=s["color"], fontsize=6.8, va="center")
        ax.axvline(2050, color=CORAL, linewidth=0.8)
        ax.set_title(title, fontsize=9.5)
        ax.set_ylabel(ylabel, fontsize=7.8)
        ax.set_xlabel("Year", fontsize=7.8)
        style_axis(ax, TOKENS)
    handles = [plt.Line2D([0], [0], color=SCENARIO_STYLE[name]["color"],
                          linestyle=SCENARIO_STYLE[name]["linestyle"], linewidth=2,
                          label=name) for name in SCENARIOS]
    fig.legend(handles=handles, frameon=False, fontsize=7.2, ncol=2,
               loc="lower center", bbox_to_anchor=(0.5, 0.01))
    fig.subplots_adjust(top=0.80, left=0.08, right=0.96, bottom=0.12, hspace=0.38, wspace=0.26)
    save_figure(fig, EFP_ASSETS / "people-pathways.png", dpi=260)
    plt.close(fig)


def make_places_wealth():
    fig, axes = plt.subplots(1, 3, figsize=(10.5, 5.25))
    _header(
        fig,
        "Forced stability moves losses off budget",
        "Household crowding, infrastructure backlog and the purchasing power of private wealth",
        "GREYSCIENX / PAPER 12",
    )
    for ax, key, title, ylabel, fmt in [
        (axes[0], "household_size", "Average household size", "People", "{:.2f}"),
        (axes[1], "maintenance", "Maintenance backlog", "2026 = 100", "{:.0f}"),
        (axes[2], "inheritance", "Real inheritance value", "2049 = 100", "{:.0f}"),
    ]:
        for name, values in SCENARIOS.items():
            s = SCENARIO_STYLE[name]
            ax.plot(YEARS, values[key], linewidth=1.9, color=s["color"], linestyle=s["linestyle"],
                    marker=s["marker"], markevery=9, markersize=3)
            ax.text(2080.5, values[key][-1], fmt.format(values[key][-1]), color=s["color"], fontsize=6.7, va="center")
        ax.axvline(2050, color=CORAL, linewidth=0.8)
        ax.set_title(title, fontsize=9.2)
        ax.set_ylabel(ylabel, fontsize=7.8)
        ax.set_xlabel("Year", fontsize=7.8)
        style_axis(ax, TOKENS)
    fig.subplots_adjust(top=0.76, left=0.07, right=0.97, bottom=0.12, wspace=0.30)
    save_figure(fig, EFP_ASSETS / "households-places-wealth.png", dpi=260)
    plt.close(fig)


def make_trust_output():
    fig, ax = plt.subplots(figsize=(9.2, 5.45))
    _header(
        fig,
        "Emergency legitimacy is an economic asset",
        "The model links lower trust to weaker compliance, investment, migration retention and reform capacity",
        "GREYSCIENX / PAPER 12",
    )
    for name, values in SCENARIOS.items():
        s = SCENARIO_STYLE[name]
        ax.plot(YEARS, values["trust"], linewidth=2.1, color=s["color"], linestyle=s["linestyle"],
                marker=s["marker"], markevery=8, markersize=3.5, label=name)
        ax.text(2080.5, values["trust"][-1], f"{values['trust'][-1]:.0f}", color=s["color"], fontsize=7.2, va="center")
    ax.axvspan(2050, 2052, color=CORAL, alpha=0.08)
    ax.set_ylabel("Institutional trust, 0-100 index")
    ax.set_xlabel("Year")
    ax.legend(frameon=False, fontsize=7.4, loc="lower left")
    style_axis(ax, TOKENS)
    _save(fig, EFP_ASSETS / "trust-paths.png")


MEASURE_FRONTIER = [
    ("Health logistics\nand targeted relief", 86, 12, 82),
    ("Temporary progressive\nsolidarity levy", 72, 19, 72),
    ("Emergency borrowing\nwith fiscal anchor", 78, 25, 77),
    ("Time-limited rationing\nof true shortages", 64, 33, 58),
    ("Forced pension-fund\nbond purchases", 60, 66, 34),
    ("Open-ended price\nand wage controls", 51, 75, 26),
    ("Suspended elections\nand judicial review", 18, 94, 8),
]


def make_safeguard_frontier():
    fig, ax = plt.subplots(figsize=(9.2, 5.8))
    _header(
        fig,
        "Emergency power has a safeguard frontier",
        "Response capacity versus long-run institutional damage; bubble size is modelled public legitimacy",
        "GREYSCIENX / PAPER 12",
    )
    label_positions = {
        "Health logistics\nand targeted relief": (90, 13, "left"),
        "Temporary progressive\nsolidarity levy": (74, 14, "left"),
        "Emergency borrowing\nwith fiscal anchor": (76, 29, "right"),
        "Time-limited rationing\nof true shortages": (66, 36, "left"),
        "Forced pension-fund\nbond purchases": (62, 68, "left"),
        "Open-ended price\nand wage controls": (53, 72, "left"),
        "Suspended elections\nand judicial review": (20, 96, "left"),
    }
    for label, capacity, damage, legitimacy in MEASURE_FRONTIER:
        colour = CORAL if damage < 35 else (BLACK if damage < 70 else G500)
        ax.scatter(capacity, damage, s=legitimacy * 4.2, color=colour, alpha=0.82,
                   edgecolor=BLACK, linewidth=0.7)
        label_x, label_y, ha = label_positions[label]
        ax.annotate(
            label,
            xy=(capacity, damage),
            xytext=(label_x, label_y),
            fontsize=7.1,
            ha=ha,
            va="center",
            color=BLACK,
            arrowprops={"arrowstyle": "-", "color": G500, "linewidth": 0.55},
        )
    ax.axhspan(0, 35, color=CORAL, alpha=0.06)
    ax.text(98, 5, "High capacity, bounded damage", ha="right", fontsize=7.5,
            color=CORAL, fontweight="bold")
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_xlabel("Immediate response capacity, index")
    ax.set_ylabel("Long-run institutional damage, index")
    style_axis(ax, TOKENS, grid_axis="both")
    _save(fig, EFP_ASSETS / "safeguard-frontier.png")


def scenario_summary():
    idx_2049 = int(np.where(YEARS == 2049)[0][0])
    idx_2050 = int(np.where(YEARS == 2050)[0][0])
    idx_2070 = int(np.where(YEARS == 2070)[0][0])
    idx_2080 = int(np.where(YEARS == 2080)[0][0])
    base_pv = 0.0
    summaries = {}
    for name, values in SCENARIOS.items():
        gap = BASE["gdp"] - values["gdp"]
        after = YEARS >= 2050
        discount = 1 / (1.03 ** (YEARS[after] - 2050))
        pv_loss = float(np.sum(gap[after] * discount))
        if name == "No 2050 shock":
            base_pv = pv_loss
        summaries[name] = {
            "gdp_2049_r_trillion": round(float(values["gdp"][idx_2049]), 3),
            "gdp_2050_r_trillion": round(float(values["gdp"][idx_2050]), 3),
            "gdp_2080_r_trillion": round(float(values["gdp"][idx_2080]), 3),
            "gdp_gap_2080_percent": round(float((values["gdp"][idx_2080] / BASE["gdp"][idx_2080] - 1) * 100), 1),
            "pv_output_loss_2050_2080_r_trillion": round(pv_loss, 2),
            "official_debt_2080_percent_gdp": round(float(values["debt"][idx_2080]), 1),
            "hidden_claims_2080_percent_gdp": round(float(values["hidden"][idx_2080]), 1),
            "augmented_burden_2080_percent_gdp": round(float(values["debt"][idx_2080] + values["hidden"][idx_2080]), 1),
            "contributors_per_retiree_2080": round(float(values["contributors"][idx_2080] / values["retirees"][idx_2080]), 2),
            "youth_employment_2080_percent": round(float(values["youth_employment"][idx_2080]), 1),
            "tfr_2080": round(float(values["tfr"][idx_2080]), 2),
            "pension_wealth_2080_index": round(float(values["pension"][idx_2080]), 1),
            "inheritance_value_2080_index": round(float(values["inheritance"][idx_2080]), 1),
            "trust_2070_index": round(float(values["trust"][idx_2070]), 1),
            "trust_2080_index": round(float(values["trust"][idx_2080]), 1),
        }
        if name in SCENARIO_POINTS:
            summaries[name]["net_skilled_migration_loss_2080_millions"] = SCENARIO_POINTS[name]["skilled_migration_2080"]
    return summaries


def make_extreme_fiscal_pressure():
    make_regime_timeline()
    make_gdp_debt()
    make_fiscal_composition()
    make_domain_heatmap()
    make_people_pathways()
    make_places_wealth()
    make_trust_output()
    make_safeguard_frontier()
    result = {
        "warning": "Hypothetical scenario model, not a forecast or a legal opinion",
        "currency": "constant 2026 South African rand",
        "horizon": "2026-2080",
        "initial_2050_emergency_need_percent_gdp": 14,
        "same_initial_shock": "pandemic, war/security mobilisation and recession",
        "scenarios": scenario_summary(),
        "first_year_gap_closure_percent_gdp": FISCAL_COMPONENTS,
        "cross_study_damage_2070_index": DOMAIN_DAMAGE,
        "measure_frontier": [
            {"measure": a, "response_capacity": b, "institutional_damage": c, "legitimacy": d}
            for a, b, c, d in MEASURE_FRONTIER
        ],
        "key_assumptions": {
            "baseline_gdp_2026_r_trillion": BASELINE_GDP_2026,
            "baseline_population_2026_millions": 64,
            "baseline_contributors_2026_millions": 18,
            "baseline_retirees_2026_millions": 6,
            "discount_rate_real": 0.03,
            "guardrailed_emergency_end": 2052,
            "extended_emergency_end": 2058,
            "permanent_suspension_end": "not restored by 2080",
        },
    }
    (EFP_DIR / "model_results.json").write_text(json.dumps(result, indent=2), encoding="utf-8")


if __name__ == "__main__":
    make_synthesis()
    make_extreme_fiscal_pressure()
    print(SYN_DIR / "model_results.json")
    print(EFP_DIR / "model_results.json")
