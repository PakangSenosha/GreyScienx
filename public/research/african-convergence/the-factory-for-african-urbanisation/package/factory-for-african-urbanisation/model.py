"""Scenario model and figures for GreyScienx African Convergence Paper 2.

This is a transparent conditional model, not a forecast. All monetary values
are constant 2024 US dollars. The model separates total African urban capital
formation, the share contestable by external suppliers, gross sales by South
African-linked firms, and domestic value added retained in South Africa.
"""

from __future__ import annotations

import json
import sys
import textwrap
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch, Rectangle


ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
CSS = Path(r"C:\Users\Deriv\Desktop\GreyScienx\app\globals.css")
STYLE_DIR = Path(r"C:\Users\Deriv\Desktop\GreyScienx\skills\greyscienx-editorial-pdf\scripts")
sys.path.insert(0, str(STYLE_DIR))

from greyscienx_style import (  # noqa: E402
    add_figure_header,
    configure_matplotlib,
    line_encodings,
    save_figure,
    style_axis,
)


TOKENS = configure_matplotlib(CSS)
ENC = line_encodings(TOKENS)
YEARS = np.arange(2026, 2051)

# Demographic anchor: approximately 700 million African urban residents today,
# rising to 1.4 billion in 2050 (UN-Habitat / UN OSAA, 2026).
URBAN_POP_START = 700.0  # millions
URBAN_POP_END = 1400.0  # millions
NEW_URBAN_RESIDENTS = np.linspace(20.0, 36.0, len(YEARS))  # sums to 700m
URBAN_POP = URBAN_POP_START + np.cumsum(NEW_URBAN_RESIDENTS)

# All-in urban capital per additional resident. These constructed assumptions
# cover housing, networks, transport, utilities, public facilities and related
# industrial systems; they are not an official forecast.
DEMAND_CASES = {
    "Provision floor": np.linspace(10.0, 14.0, len(YEARS)),
    "Build-out": np.linspace(20.0, 30.0, len(YEARS)),
    "Convergence": np.linspace(36.0, 54.0, len(YEARS)),
}

SECTORS = [
    "Housing and\nbuildings",
    "Transport and\nlogistics",
    "Power",
    "Water and\nsanitation",
    "Telecom and\ndigital",
    "Waste and\ncircular systems",
    "Public and\nsocial facilities",
    "Industrial and\nmunicipal systems",
]
SECTOR_SHARES = np.array([0.31, 0.20, 0.16, 0.12, 0.07, 0.05, 0.05, 0.04])
ADDRESSABLE_SHARES = np.array([0.20, 0.45, 0.55, 0.45, 0.60, 0.45, 0.30, 0.65])
SA_CAPTURE_SHARES = np.array([0.02, 0.04, 0.05, 0.04, 0.02, 0.03, 0.02, 0.06])

SA_GDP_2024 = 401.1  # US$bn, World Bank current-dollar anchor
DOMESTIC_VALUE_ADDED_SHARE = 0.52
DIRECT_VA_PER_JOB = 0.085  # US$bn per thousand jobs = US$85,000 per job
EMPLOYMENT_MULTIPLIER = 1.60  # illustrative direct + indirect support


def demand_path(case: str) -> np.ndarray:
    return NEW_URBAN_RESIDENTS * DEMAND_CASES[case]


TOTAL_DEMAND = {name: demand_path(name) for name in DEMAND_CASES}
CENTRAL_TOTAL = float(TOTAL_DEMAND["Build-out"].sum())
SECTOR_DEMAND = CENTRAL_TOTAL * SECTOR_SHARES
ADDRESSABLE = SECTOR_DEMAND * ADDRESSABLE_SHARES
SA_SALES_BY_SECTOR = ADDRESSABLE * SA_CAPTURE_SHARES
SA_SALES = float(SA_SALES_BY_SECTOR.sum())
SA_CAPTURE_WEIGHTED = SA_SALES / float(ADDRESSABLE.sum())
SA_DVA = SA_SALES * DOMESTIC_VALUE_ADDED_SHARE
AVG_ANNUAL_DVA = SA_DVA / len(YEARS)
DIRECT_JOBS_K = AVG_ANNUAL_DVA / DIRECT_VA_PER_JOB
SUPPORTED_JOBS_K = DIRECT_JOBS_K * EMPLOYMENT_MULTIPLIER

CAPTURE_SCENARIOS = {
    "Bypass": {"capture": 0.01, "dva": 0.35},
    "Supplier": {"capture": SA_CAPTURE_WEIGHTED, "dva": 0.52},
    "Systems platform": {"capture": 0.07, "dva": 0.65},
}


def new_figure(title: str, subtitle: str, field: str, height: float = 4.7):
    fig = plt.figure(figsize=(7.2, height))
    add_figure_header(fig, title, subtitle, field=field, tokens=TOKENS)
    return fig


def save(fig, name: str):
    ASSETS.mkdir(parents=True, exist_ok=True)
    save_figure(fig, ASSETS / name, dpi=260)
    plt.close(fig)


def figure_urban_wave():
    fig = new_figure(
        "Africa adds another urban continent",
        "The model starts with the UN-Habitat trajectory: roughly 700 million urban residents today and 1.4 billion by 2050.",
        "GREYSCIENX / DEMOGRAPHIC ANCHOR",
    )
    ax = fig.add_axes([0.10, 0.18, 0.84, 0.56])
    ax.fill_between(YEARS, URBAN_POP_START, URBAN_POP, color=TOKENS["coral"], alpha=0.18)
    ax.plot(YEARS, URBAN_POP, color=TOKENS["coral"], linewidth=2.4)
    ax.axhline(URBAN_POP_START, color=TOKENS["grey-500"], linewidth=1.1, linestyle="--")
    ax.text(2026.2, 715, "~700m existing urban residents", fontsize=8, color=TOKENS["grey-700"])
    ax.text(2049.6, 1416, "1.4bn", ha="right", fontsize=10, fontweight="bold", color=TOKENS["coral"])
    ax.text(2038, 1020, "+700m residents", fontsize=12, fontweight="bold", color=TOKENS["coral"])
    ax.text(2038, 978, "housing, pipes, roads, power, schools and systems", fontsize=7.8, color=TOKENS["grey-700"])
    style_axis(ax, TOKENS)
    ax.set_xlabel("Year")
    ax.set_ylabel("African urban population (millions)")
    ax.set_xlim(2026, 2050)
    ax.set_ylim(650, 1490)
    save(fig, "urban-wave.png")


def figure_demand_paths():
    fig = new_figure(
        "The annual market depends on the standard of build-out",
        "Three constructed cost envelopes translate each year's new urban residents into constant-dollar capital demand.",
        "GREYSCIENX / SCENARIO RANGE",
    )
    ax = fig.add_axes([0.10, 0.17, 0.84, 0.58])
    order = ["Provision floor", "Build-out", "Convergence"]
    styles = [ENC[2], ENC[1], ENC[0]]
    for name, enc in zip(order, styles):
        y = TOTAL_DEMAND[name]
        ax.plot(YEARS, y, label=f"{name}: US${y.sum()/1000:.1f}tn cumulative", **enc)
        ax.text(2050.3, y[-1], f"${y[-1]:.0f}bn", va="center", fontsize=7.8, color=enc["color"], fontweight="bold")
    style_axis(ax, TOKENS)
    ax.set_xlim(2026, 2053)
    ax.set_ylim(0, 2100)
    ax.set_xlabel("Year")
    ax.set_ylabel("Annual urban capital demand (US$bn, 2024 prices)")
    ax.legend(loc="upper left", frameon=False, fontsize=7.5)
    save(fig, "demand-paths.png")


def figure_sector_market():
    fig = new_figure(
        "Buildings dominate; systems carry the tradable margin",
        "Central build-out case, cumulative 2026-2050 capital demand by sector.",
        "GREYSCIENX / US$17.5TN CENTRAL CASE",
        5.1,
    )
    ax = fig.add_axes([0.27, 0.12, 0.67, 0.65])
    order = np.arange(len(SECTORS))[::-1]
    vals = SECTOR_DEMAND / 1000
    colors = [TOKENS["coral"] if i in (1, 2, 3, 7) else TOKENS["grey-500"] for i in range(len(SECTORS))]
    ax.barh(order, vals[::-1], color=colors[::-1], height=0.64)
    ax.set_yticks(order, [s.replace("\n", " ") for s in SECTORS[::-1]], fontsize=7.6)
    for y, v in zip(order, vals[::-1]):
        ax.text(v + 0.07, y, f"${v:.2f}tn", va="center", fontsize=7.4, fontweight="bold")
    style_axis(ax, TOKENS)
    ax.set_xlabel("Cumulative capital demand (US$tn, 2024 prices)")
    ax.set_xlim(0, 6.3)
    save(fig, "sector-market.png")


def figure_funnel():
    fig = new_figure(
        "Most urban spending never becomes a South African order",
        "The central-case funnel removes locally supplied construction, competing imports and foreign content before counting domestic value added.",
        "GREYSCIENX / CAPTURE FUNNEL",
        4.9,
    )
    ax = fig.add_axes([0.06, 0.13, 0.88, 0.64])
    ax.axis("off")
    stages = [
        ("Total African urban\ncapital formation", CENTRAL_TOTAL / 1000, 0.92, TOKENS["grey-100"]),
        ("Contestable equipment,\nsystems and services", float(ADDRESSABLE.sum()) / 1000, 0.64, TOKENS["grey-300"]),
        ("South African-linked\ngross sales", SA_SALES / 1000, 0.34, TOKENS["grey-700"]),
        ("Value retained in\nSouth Africa", SA_DVA / 1000, 0.20, TOKENS["coral"]),
    ]
    y_positions = [0.76, 0.54, 0.32, 0.10]
    for (label, value, width, color), y in zip(stages, y_positions):
        x = 0.5 - width / 2
        box = FancyBboxPatch((x, y), width, 0.14, boxstyle="round,pad=0.01,rounding_size=0.012", facecolor=color, edgecolor="none")
        ax.add_patch(box)
        txt_color = TOKENS["white"] if color in (TOKENS["grey-700"], TOKENS["coral"]) else TOKENS["black"]
        ax.text(x + 0.025, y + 0.07, label, va="center", fontsize=8, color=txt_color, fontweight="bold")
        ax.text(x + width - 0.025, y + 0.07, f"US${value:.2f}tn", ha="right", va="center", fontsize=10, color=txt_color, fontweight="bold")
    ax.text(0.50, 0.01, f"Weighted South African share of the contestable market: {SA_CAPTURE_WEIGHTED*100:.1f}%", ha="center", fontsize=8.2, color=TOKENS["grey-700"])
    save(fig, "capture-funnel.png")


def figure_sector_capture():
    fig = new_figure(
        "Power, transport and water carry most captured sales",
        "Sector assumptions combine market size, external-supplier addressability and a conservative South African share.",
        "GREYSCIENX / CENTRAL CAPTURE",
        5.0,
    )
    ax = fig.add_axes([0.27, 0.13, 0.66, 0.63])
    order = np.argsort(SA_SALES_BY_SECTOR)
    vals = SA_SALES_BY_SECTOR[order]
    labels = [SECTORS[i].replace("\n", " ") for i in order]
    colors = [TOKENS["coral"] if i >= len(vals) - 3 else TOKENS["grey-500"] for i in range(len(vals))]
    ax.barh(np.arange(len(vals)), vals, color=colors, height=0.62)
    ax.set_yticks(np.arange(len(vals)), labels, fontsize=7.5)
    for y, v in enumerate(vals):
        ax.text(v + 1.5, y, f"${v:.0f}bn", va="center", fontsize=7.3, fontweight="bold")
    style_axis(ax, TOKENS)
    ax.set_xlabel("Cumulative South African-linked sales (US$bn)")
    ax.set_xlim(0, 90)
    save(fig, "sector-capture.png")


def figure_capture_scenarios():
    fig = new_figure(
        "Market share matters; retained value matters twice",
        "Gross sales can be large while little production, engineering or intellectual property remains in South Africa.",
        "GREYSCIENX / THREE INDUSTRIAL OUTCOMES",
        5.0,
    )
    ax = fig.add_axes([0.12, 0.18, 0.80, 0.56])
    names = list(CAPTURE_SCENARIOS)
    total_addr = float(ADDRESSABLE.sum())
    sales = [total_addr * CAPTURE_SCENARIOS[n]["capture"] for n in names]
    dva = [sales[i] * CAPTURE_SCENARIOS[n]["dva"] for i, n in enumerate(names)]
    x = np.arange(3)
    w = 0.34
    b1 = ax.bar(x - w/2, sales, width=w, color=TOKENS["grey-500"], label="Gross African sales")
    b2 = ax.bar(x + w/2, dva, width=w, color=TOKENS["coral"], label="Domestic value added")
    for bars in (b1, b2):
        for b in bars:
            ax.text(b.get_x()+b.get_width()/2, b.get_height()+10, f"${b.get_height():.0f}bn", ha="center", fontsize=7.6, fontweight="bold")
    style_axis(ax, TOKENS)
    ax.set_xticks(x, names)
    ax.set_ylabel("Cumulative 2026-2050 value (US$bn)")
    ax.set_ylim(0, 560)
    ax.legend(frameon=False, loc="upper left", fontsize=7.5)
    save(fig, "capture-scenarios.png")


def figure_share_jobs():
    fig = new_figure(
        "A supplier position supports tens of thousands of jobs",
        "Illustrative average annual domestic value added and direct employment at different shares of the contestable market.",
        "GREYSCIENX / SCALE TEST",
    )
    ax = fig.add_axes([0.10, 0.18, 0.62, 0.56])
    shares = np.linspace(0, 0.08, 81)
    annual_dva = float(ADDRESSABLE.sum()) * shares * DOMESTIC_VALUE_ADDED_SHARE / len(YEARS)
    jobs = annual_dva / DIRECT_VA_PER_JOB
    ax.plot(shares * 100, jobs, color=TOKENS["coral"], linewidth=2.4)
    ax.scatter([SA_CAPTURE_WEIGHTED*100], [DIRECT_JOBS_K], s=80, color=TOKENS["black"], zorder=5)
    ax.annotate(f"Central supplier case\n{DIRECT_JOBS_K:.0f}k direct jobs", (SA_CAPTURE_WEIGHTED*100, DIRECT_JOBS_K), xytext=(12, 10), textcoords="offset points", fontsize=8, fontweight="bold")
    style_axis(ax, TOKENS)
    ax.set_xlabel("South African share of contestable market (%)")
    ax.set_ylabel("Average direct jobs (thousands)")
    ax.set_xlim(0, 8)
    ax.set_ylim(0, 180)
    ax2 = ax.twinx()
    ax2.set_ylim(0, 180 * DIRECT_VA_PER_JOB)
    ax2.set_ylabel("Annual domestic value added (US$bn)")
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_color(TOKENS["grey-300"])
    ax2.tick_params(colors=TOKENS["grey-500"], labelsize=7)
    save(fig, "share-jobs.png")


def figure_product_map():
    fig = new_figure(
        "Bulk materials stay local; systems travel",
        "Bulky materials favour local African production; complex equipment and systems can carry more South African knowledge and value.",
        "GREYSCIENX / PRODUCT ECONOMICS",
        5.1,
    )
    ax = fig.add_axes([0.12, 0.17, 0.81, 0.59])
    products = {
        "Cement": (18, 18), "Aggregates": (10, 10), "Precast housing": (32, 34),
        "Steel structures": (43, 42), "Pumps": (68, 62), "Transformers": (72, 72),
        "Rail systems": (61, 78), "Water treatment": (76, 81), "Mining machinery": (81, 75),
        "Control software": (94, 93), "Engineering services": (92, 86), "Buses and trucks": (58, 61),
    }
    ax.axvspan(0, 50, color=TOKENS["grey-100"], alpha=0.7)
    ax.axhspan(50, 100, color=TOKENS["coral"], alpha=0.06)
    for name, (x, y) in products.items():
        c = TOKENS["coral"] if x >= 60 and y >= 60 else TOKENS["grey-700"]
        ax.scatter(x, y, s=38, color=c)
        ax.annotate(name, (x, y), xytext=(4, 4), textcoords="offset points", fontsize=6.8, color=c)
    style_axis(ax, TOKENS)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_xlabel("Ease of cross-border trade / remote delivery")
    ax.set_ylabel("South African knowledge and systems intensity")
    ax.text(4, 95, "LOCAL PRODUCTION\nWITH SA OWNERSHIP", fontsize=7.2, fontweight="bold", color=TOKENS["grey-500"], va="top")
    ax.text(96, 5, "DIRECT EXPORT", fontsize=7.2, fontweight="bold", color=TOKENS["grey-500"], ha="right")
    ax.text(96, 95, "SYSTEMS PLATFORM", fontsize=7.2, fontweight="bold", color=TOKENS["coral"], ha="right", va="top")
    save(fig, "product-map.png")


def figure_delivery_modes():
    fig = new_figure(
        "Three ways to retain South African value",
        "The correct operating model changes with freight cost, local-content rules, maintenance needs and intellectual-property intensity.",
        "GREYSCIENX / BUSINESS ARCHITECTURE",
        4.8,
    )
    ax = fig.add_axes([0.04, 0.12, 0.92, 0.64])
    ax.axis("off")
    cards = [
        (0.02, "1", "EXPORT", "Transformers, pumps, vehicles, specialist machinery and modular components shipped from South Africa.", "Best when value-to-weight is high and standards travel."),
        (0.35, "2", "BUILD LOCALLY", "African plants for cement, steel products, precast systems and maintenance, with South African capital and operating know-how.", "Best when freight is expensive or procurement requires local value."),
        (0.68, "3", "ORCHESTRATE", "Design, project finance, software, standards, engineering, training, spares and lifecycle service managed from a South African hub.", "Best when complexity and uptime matter more than tonnes shipped."),
    ]
    for x, num, title, body, footer in cards:
        ax.add_patch(FancyBboxPatch((x, 0.10), 0.29, 0.78, boxstyle="round,pad=0.015,rounding_size=0.012", facecolor=TOKENS["white"], edgecolor=TOKENS["grey-300"], linewidth=1.0))
        ax.add_patch(Rectangle((x, 0.73), 0.29, 0.15, color=TOKENS["coral"] if num == "3" else TOKENS["black"]))
        ax.text(x+0.025, 0.805, num, color=TOKENS["white"], fontsize=13, fontweight="bold", va="center")
        ax.text(x+0.072, 0.805, title, color=TOKENS["white"], fontsize=8.6, fontweight="bold", va="center")
        ax.text(x+0.025, 0.65, textwrap.fill(body, 29), fontsize=7.1, color=TOKENS["black"], va="top", linespacing=1.28)
        ax.text(x+0.025, 0.18, textwrap.fill(footer, 31), fontsize=6.6, color=TOKENS["grey-500"], va="bottom", style="italic", linespacing=1.22)
    save(fig, "delivery-modes.png")


def figure_roadmap():
    fig = new_figure(
        "The window is long; the capability build is sequential",
        "South Africa has to earn platform status before the steepest part of the urban build-out.",
        "GREYSCIENX / 2026-2050 ROADMAP",
        4.7,
    )
    ax = fig.add_axes([0.05, 0.14, 0.90, 0.62])
    ax.axis("off")
    stages = [
        (0.10, "2026-30", "Repair the base", "Power, ports, rail, skills; product standards; export finance."),
        (0.38, "2031-36", "Win reference projects", "Regional tenders; maintenance networks; bankable local partners."),
        (0.66, "2037-43", "Localise across Africa", "Plants near demand; supplier development; lifecycle contracts."),
        (0.90, "2044-50", "Operate the systems", "Software, finance, standards, retrofits and continental service."),
    ]
    for i, (x, date, title, body) in enumerate(stages):
        color = TOKENS["coral"] if i == 3 else TOKENS["black"]
        left = 0.005 + i * 0.248
        ax.add_patch(FancyBboxPatch((left, 0.16), 0.225, 0.66, boxstyle="round,pad=0.012,rounding_size=0.012", facecolor=TOKENS["white"], edgecolor=TOKENS["grey-300"], linewidth=1.0))
        ax.add_patch(Rectangle((left, 0.70), 0.225, 0.12, color=color))
        ax.text(left + 0.018, 0.76, date, color=TOKENS["white"], fontsize=8.3, fontweight="bold", va="center")
        ax.text(left + 0.018, 0.61, textwrap.fill(title, 18), fontsize=8.2, fontweight="bold", va="top", linespacing=1.15)
        ax.text(left + 0.018, 0.41, textwrap.fill(body, 25), fontsize=6.8, color=TOKENS["grey-700"], va="top", linespacing=1.25)
        if i < 3:
            ax.annotate("", xy=(left + 0.25, 0.49), xytext=(left + 0.232, 0.49), arrowprops=dict(arrowstyle="->", color=TOKENS["coral"], lw=1.2))
    save(fig, "roadmap.png")


def export_results():
    scenario_rows = {}
    total_addr = float(ADDRESSABLE.sum())
    for name, config in CAPTURE_SCENARIOS.items():
        sales = total_addr * config["capture"]
        dva = sales * config["dva"]
        scenario_rows[name] = {
            "capture_percent": round(100 * config["capture"], 2),
            "domestic_value_added_share_percent": round(100 * config["dva"], 1),
            "cumulative_sales_usd_bn": round(sales, 1),
            "cumulative_domestic_value_added_usd_bn": round(dva, 1),
            "average_annual_domestic_value_added_usd_bn": round(dva / len(YEARS), 2),
            "average_direct_jobs_thousands": round((dva / len(YEARS)) / DIRECT_VA_PER_JOB, 1),
        }
    results = {
        "years": [int(YEARS[0]), int(YEARS[-1])],
        "new_urban_residents_millions": round(float(NEW_URBAN_RESIDENTS.sum()), 1),
        "cumulative_demand_usd_trillion": {k: round(float(v.sum()) / 1000, 2) for k, v in TOTAL_DEMAND.items()},
        "central_total_usd_trillion": round(CENTRAL_TOTAL / 1000, 2),
        "central_addressable_usd_trillion": round(float(ADDRESSABLE.sum()) / 1000, 2),
        "central_sa_sales_usd_bn": round(SA_SALES, 1),
        "central_sa_capture_percent": round(100 * SA_CAPTURE_WEIGHTED, 2),
        "central_domestic_value_added_usd_bn": round(SA_DVA, 1),
        "central_average_annual_domestic_value_added_usd_bn": round(AVG_ANNUAL_DVA, 2),
        "central_direct_jobs_thousands": round(DIRECT_JOBS_K, 1),
        "central_supported_jobs_thousands": round(SUPPORTED_JOBS_K, 1),
        "central_annual_dva_percent_2024_sa_gdp": round(100 * AVG_ANNUAL_DVA / SA_GDP_2024, 2),
        "scenarios": scenario_rows,
        "sector_rows": [
            {
                "sector": SECTORS[i].replace("\n", " "),
                "total_demand_usd_bn": round(float(SECTOR_DEMAND[i]), 1),
                "addressable_share_percent": round(float(ADDRESSABLE_SHARES[i] * 100), 1),
                "sa_capture_percent": round(float(SA_CAPTURE_SHARES[i] * 100), 1),
                "sa_sales_usd_bn": round(float(SA_SALES_BY_SECTOR[i]), 1),
            }
            for i in range(len(SECTORS))
        ],
    }
    (ROOT / "model_results.json").write_text(json.dumps(results, indent=2), encoding="utf-8")


def main():
    figure_urban_wave()
    figure_demand_paths()
    figure_sector_market()
    figure_funnel()
    figure_sector_capture()
    figure_capture_scenarios()
    figure_share_jobs()
    figure_product_map()
    figure_delivery_modes()
    figure_roadmap()
    export_results()
    print(f"Generated 10 figures in {ASSETS}")
    print(f"Central demand: US${CENTRAL_TOTAL/1000:.2f}tn")
    print(f"Addressable market: US${ADDRESSABLE.sum()/1000:.2f}tn")
    print(f"SA-linked sales: US${SA_SALES:.1f}bn")
    print(f"Domestic value added: US${SA_DVA:.1f}bn")
    print(f"Average direct jobs: {DIRECT_JOBS_K:.0f}k")


if __name__ == "__main__":
    main()
