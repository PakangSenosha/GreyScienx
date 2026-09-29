"""Transparent scenario model for GreyScienx African Convergence Paper 1.

All GDP values are constant 2024 US dollars. This is a conditional scenario
model, not a forecast. It separates economic scale from continental relevance.
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, Rectangle


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
YEARS = np.arange(2024, 2051)

# 2024 World Bank Open Data, summed across 54 African states. GDP excludes
# Eritrea and South Sudan because 2024 observations were unavailable.
AFRICA_GDP_2024 = 2902.0  # US$bn
SA_GDP_2024 = 401.1  # US$bn
REST_GDP_2024 = AFRICA_GDP_2024 - SA_GDP_2024
AFRICA_POP_2024 = 1512.0  # millions
SA_POP_2024 = 64.0  # millions
AFRICA_POP_2050 = 2500.0  # conditional series premise
SA_POP_2050 = 75.0  # stylised assumption, not a demographic forecast

SCENARIOS = {
    "Commodity drift": {
        "sa_growth": 0.015,
        "rest_growth": 0.042,
        "capture_rate": 0.004,
        "scores": [50, 42, 30, 55, 42, 32],
    },
    "Domestic repair": {
        "sa_growth": 0.025,
        "rest_growth": 0.042,
        "capture_rate": 0.008,
        "scores": [65, 60, 52, 70, 60, 62],
    },
    "African platform": {
        "sa_growth": 0.035,
        "rest_growth": 0.042,
        "capture_rate": 0.015,
        "scores": [80, 82, 82, 86, 78, 80],
    },
}

DIMENSIONS = [
    "Productivity",
    "Tradable\ncapability",
    "Africa-linked\nearnings",
    "Capital and\nownership",
    "Knowledge\nexports",
    "Network\nreliability",
]
WEIGHTS = np.array([0.25, 0.20, 0.20, 0.15, 0.10, 0.10])
BASELINE_SCORES = np.array([55, 60, 45, 75, 55, 45])


def compound(base: float, growth: float) -> np.ndarray:
    return base * (1 + growth) ** (YEARS - YEARS[0])


def simulate(config: dict) -> dict[str, np.ndarray | float]:
    sa_gdp = compound(SA_GDP_2024, config["sa_growth"])
    rest_gdp = compound(REST_GDP_2024, config["rest_growth"])
    total_gdp = sa_gdp + rest_gdp
    share = 100 * sa_gdp / total_gdp
    sa_pop = SA_POP_2024 * (SA_POP_2050 / SA_POP_2024) ** ((YEARS - 2024) / 26)
    africa_pop = AFRICA_POP_2024 * (AFRICA_POP_2050 / AFRICA_POP_2024) ** ((YEARS - 2024) / 26)
    sa_gdp_pc_index = 100 * (sa_gdp / sa_pop) / (sa_gdp[0] / sa_pop[0])
    africa_gdp_pc_index = 100 * (total_gdp / africa_pop) / (total_gdp[0] / africa_pop[0])
    captured_income = rest_gdp * config["capture_rate"]
    score = float(np.dot(np.array(config["scores"]), WEIGHTS))
    return {
        "sa_gdp": sa_gdp,
        "rest_gdp": rest_gdp,
        "total_gdp": total_gdp,
        "share": share,
        "sa_pop": sa_pop,
        "africa_pop": africa_pop,
        "sa_gdp_pc_index": sa_gdp_pc_index,
        "africa_gdp_pc_index": africa_gdp_pc_index,
        "captured_income": captured_income,
        "score": score,
    }


RESULTS = {name: simulate(config) for name, config in SCENARIOS.items()}
BASELINE_RELEVANCE = float(np.dot(BASELINE_SCORES, WEIGHTS))


def new_figure(title: str, subtitle: str, field: str, height: float = 4.55):
    fig = plt.figure(figsize=(7.2, height))
    add_figure_header(fig, title, subtitle, field=field, tokens=TOKENS)
    return fig


def save(fig, name: str):
    ASSETS.mkdir(parents=True, exist_ok=True)
    save_figure(fig, ASSETS / name, dpi=260)
    plt.close(fig)


def figure_scale_relevance():
    fig = new_figure(
        "GDP rank is not continental relevance",
        "The platform case loses GDP share but raises the diagnostic relevance score.",
        "GREYSCIENX / CENTRAL RESULT",
    )
    ax = fig.add_axes([0.11, 0.17, 0.84, 0.58])
    ax.axhline(BASELINE_RELEVANCE, color=TOKENS["grey-300"], linewidth=1.0)
    ax.axvline(100 * SA_GDP_2024 / AFRICA_GDP_2024, color=TOKENS["grey-300"], linewidth=1.0)
    ax.scatter([100 * SA_GDP_2024 / AFRICA_GDP_2024], [BASELINE_RELEVANCE], s=105, color=TOKENS["black"], marker="s", zorder=5)
    ax.annotate("2024 baseline", (13.82, BASELINE_RELEVANCE), xytext=(8, 8), textcoords="offset points", fontsize=8, fontweight="bold")
    styles = {
        "Commodity drift": (TOKENS["grey-500"], "D"),
        "Domestic repair": (TOKENS["black"], "s"),
        "African platform": (TOKENS["coral"], "o"),
    }
    for name, result in RESULTS.items():
        colour, marker = styles[name]
        x = result["share"][-1]
        y = result["score"]
        ax.scatter([x], [y], s=120, color=colour, marker=marker, zorder=5)
        offset = (8, -13) if name == "Commodity drift" else (8, 8)
        ax.annotate(name, (x, y), xytext=offset, textcoords="offset points", fontsize=8, color=colour, fontweight="bold")
    style_axis(ax, TOKENS)
    ax.set_xlabel("South Africa's share of African GDP in 2050 (%)")
    ax.set_ylabel("Continental relevance score (0-100)")
    ax.set_xlim(5.5, 15.0)
    ax.set_ylim(30, 90)
    ax.text(14.7, 88, "large and relevant", ha="right", fontsize=7.4, color=TOKENS["grey-500"])
    ax.text(5.8, 32, "smaller and peripheral", fontsize=7.4, color=TOKENS["grey-500"])
    save(fig, "scale-relevance.png")


def figure_population_market():
    fig = new_figure(
        "Africa's market grows as its population expands",
        "Population is not destiny, but it changes the scale of the opportunity outside the country.",
        "GREYSCIENX / DEMOGRAPHIC PREMISE",
        4.7,
    )
    ax1 = fig.add_axes([0.09, 0.18, 0.38, 0.56])
    pop = [AFRICA_POP_2024 / 1000, AFRICA_POP_2050 / 1000]
    bars = ax1.bar([0, 1], pop, color=[TOKENS["grey-700"], TOKENS["coral"]], width=0.58)
    style_axis(ax1, TOKENS)
    ax1.set_xticks([0, 1], ["2024", "2050"])
    ax1.set_ylabel("African population (billions)")
    ax1.set_ylim(0, 2.8)
    for b, v in zip(bars, pop):
        ax1.text(b.get_x() + b.get_width() / 2, v + 0.08, f"{v:.2f}bn", ha="center", fontsize=8.3, fontweight="bold")

    ax2 = fig.add_axes([0.58, 0.18, 0.37, 0.56])
    platform = RESULTS["African platform"]
    values = [AFRICA_GDP_2024 / 1000, platform["total_gdp"][-1] / 1000]
    bars2 = ax2.bar([0, 1], values, color=[TOKENS["grey-700"], TOKENS["coral"]], width=0.58)
    style_axis(ax2, TOKENS)
    ax2.set_xticks([0, 1], ["2024", "2050"])
    ax2.set_ylabel("African GDP (constant 2024 US$tn)")
    ax2.set_ylim(0, 9.4)
    for b, v in zip(bars2, values):
        ax2.text(b.get_x() + b.get_width() / 2, v + 0.25, f"${v:.1f}tn", ha="center", fontsize=8.3, fontweight="bold")
    fig.text(0.50, 0.08, "South Africa's population share: 4.2% in 2024 -> 3.0% in 2050 (stylised)", ha="center", fontsize=8, color=TOKENS["grey-700"])
    save(fig, "population-market.png")


def figure_gdp_share_paths():
    fig = new_figure(
        "Faster African growth reduces South Africa's GDP share",
        "Maintaining rank requires matching continental growth; relevance does not.",
        "GREYSCIENX / RELATIVE SCALE",
    )
    ax = fig.add_axes([0.11, 0.16, 0.84, 0.59])
    for i, (name, result) in enumerate(RESULTS.items()):
        enc = [ENC[2], ENC[1], ENC[0]][i]
        ax.plot(YEARS, result["share"], label=name, **enc)
        ax.text(2050.4, result["share"][-1], f"{result['share'][-1]:.1f}%", va="center", fontsize=7.7, color=enc["color"], fontweight="bold")
    style_axis(ax, TOKENS)
    ax.set_xlabel("Year")
    ax.set_ylabel("South Africa's share of African GDP (%)")
    ax.set_xlim(2024, 2053)
    ax.set_ylim(5, 15)
    ax.legend(loc="lower left", frameon=False, ncol=3, fontsize=7.5)
    save(fig, "gdp-share-paths.png")


def figure_absolute_income():
    fig = new_figure(
        "A country can grow richer while its continental share falls",
        "The welfare question is productivity and income per person, not continental rank alone.",
        "GREYSCIENX / ABSOLUTE PROSPERITY",
        4.7,
    )
    ax = fig.add_axes([0.10, 0.18, 0.49, 0.56])
    names = list(RESULTS)
    values = [RESULTS[n]["sa_gdp"][-1] for n in names]
    colours = [TOKENS["grey-500"], TOKENS["black"], TOKENS["coral"]]
    bars = ax.barh(np.arange(3), values, color=colours, height=0.56)
    style_axis(ax, TOKENS)
    ax.set_yticks(np.arange(3), names)
    ax.set_xlabel("South African GDP in 2050 (constant 2024 US$bn)")
    ax.set_xlim(0, 1100)
    for b, v in zip(bars, values):
        ax.text(v + 18, b.get_y() + b.get_height() / 2, f"${v:,.0f}bn", va="center", fontsize=8, fontweight="bold")

    ax2 = fig.add_axes([0.70, 0.18, 0.25, 0.56])
    pc = [RESULTS[n]["sa_gdp_pc_index"][-1] - 100 for n in names]
    bars2 = ax2.bar(np.arange(3), pc, color=colours, width=0.58)
    style_axis(ax2, TOKENS)
    ax2.set_xticks(np.arange(3), ["Drift", "Repair", "Platform"], rotation=25, ha="right")
    ax2.set_ylabel("Real GDP per person gain, 2024-50 (%)")
    ax2.set_ylim(0, 130)
    for b, v in zip(bars2, pc):
        ax2.text(b.get_x() + b.get_width() / 2, v + 4, f"+{v:.0f}%", ha="center", fontsize=8, fontweight="bold")
    save(fig, "absolute-income.png")


def figure_relevance_index():
    fig = new_figure(
        "Continental relevance is a portfolio, not a single ranking",
        "Scores are transparent diagnostics; the weights are judgement calls, not observed facts.",
        "GREYSCIENX / RELEVANCE INDEX",
        5.0,
    )
    ax = fig.add_axes([0.16, 0.19, 0.79, 0.56])
    matrix = np.vstack([
        BASELINE_SCORES,
        SCENARIOS["Commodity drift"]["scores"],
        SCENARIOS["Domestic repair"]["scores"],
        SCENARIOS["African platform"]["scores"],
    ])
    labels = ["2024 baseline", "2050 drift", "2050 repair", "2050 platform"]
    im = ax.imshow(matrix, cmap=plt.matplotlib.colors.LinearSegmentedColormap.from_list("gsx", [TOKENS["grey-100"], TOKENS["grey-500"], TOKENS["coral"]]), vmin=20, vmax=90, aspect="auto")
    ax.set_xticks(np.arange(len(DIMENSIONS)), DIMENSIONS, fontsize=7.4)
    ax.set_yticks(np.arange(4), labels, fontsize=8)
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            colour = TOKENS["white"] if matrix[i, j] >= 67 else TOKENS["black"]
            ax.text(j, i, f"{matrix[i, j]:.0f}", ha="center", va="center", color=colour, fontsize=8, fontweight="bold")
    for spine in ax.spines.values():
        spine.set_visible(False)
    fig.text(0.16, 0.105, "Weights: productivity 25%; tradable capability 20%; Africa-linked earnings 20%; capital 15%; knowledge 10%; networks 10%.", fontsize=7.4, color=TOKENS["grey-700"])
    save(fig, "relevance-index.png")


def figure_platform_functions():
    fig = new_figure(
        "African growth activates South African capabilities",
        "The strategy is to own and operate high-value functions around other countries' expansion.",
        "GREYSCIENX / PLATFORM ARCHITECTURE",
        4.55,
    )
    ax = fig.add_axes([0.05, 0.12, 0.90, 0.63])
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 60)
    ax.axis("off")
    ax.add_patch(Rectangle((1, 20), 20, 22, facecolor=TOKENS["coral"], edgecolor="none"))
    ax.text(11, 33, "AFRICAN\nGROWTH", ha="center", va="center", fontsize=12, fontweight="bold", color=TOKENS["black"])
    ax.text(11, 24, "cities + firms + incomes", ha="center", va="center", fontsize=7.2, color=TOKENS["black"])
    functions = [
        (28, 36, "MACHINERY", "capital goods"),
        (51, 36, "CAPITAL", "finance + insurance"),
        (74, 36, "SYSTEMS", "energy + logistics"),
        (28, 13, "KNOWLEDGE", "science + skills"),
        (51, 13, "SERVICES", "legal + digital"),
        (74, 13, "OWNERSHIP", "African assets"),
    ]
    for x, y, title, note in functions:
        ax.add_patch(Rectangle((x, y), 19, 16, facecolor=TOKENS["true-black"], edgecolor="none"))
        ax.text(x + 9.5, y + 10.0, title, ha="center", va="center", fontsize=8.6, fontweight="bold", color=TOKENS["white"])
        ax.text(x + 9.5, y + 4.1, note, ha="center", va="center", fontsize=6.8, color=TOKENS["grey-300"])
        ax.add_patch(FancyArrowPatch((21, 31), (x, y + 8), arrowstyle="-|>", mutation_scale=10, linewidth=1.0, color=TOKENS["grey-500"]))
    ax.add_patch(Rectangle((94, 20), 5, 22, facecolor=TOKENS["coral"], edgecolor="none"))
    ax.text(96.5, 31, "SA\nINCOME", rotation=90, ha="center", va="center", fontsize=8.5, fontweight="bold")
    save(fig, "platform-functions.png")


def figure_capture_income():
    fig = new_figure(
        "A small market claim can become a major income stream",
        "Illustrative domestic income retained from exports, services, fees and African-owned assets in 2050.",
        "GREYSCIENX / MARKET CAPTURE",
    )
    ax = fig.add_axes([0.11, 0.17, 0.84, 0.58])
    rest_2050 = RESULTS["African platform"]["rest_gdp"][-1]
    rates = np.array([0.25, 0.5, 1.0, 1.5, 2.0, 3.0])
    income = rest_2050 * rates / 100
    bars = ax.bar(rates, income, width=0.28, color=[TOKENS["grey-500"]] * 3 + [TOKENS["coral"]] * 3)
    style_axis(ax, TOKENS)
    ax.set_xlabel("Domestic income captured as a share of the rest of Africa's GDP (%)")
    ax.set_ylabel("Annual South African income (constant 2024 US$bn)")
    ax.set_xticks(rates, [f"{r:g}%" for r in rates])
    for b, v in zip(bars, income):
        ax.text(b.get_x() + b.get_width() / 2, v + 3.0, f"${v:,.0f}bn", ha="center", fontsize=7.8, fontweight="bold")
    ax.text(1.5, income[3] * 0.55, "central platform case", ha="center", fontsize=7.4, color=TOKENS["black"], fontweight="bold")
    save(fig, "capture-income.png")


def figure_sensitivity():
    fig = new_figure(
        "Future GDP share depends on the growth differential",
        "2050 share under combinations of South African and rest-of-Africa real growth.",
        "GREYSCIENX / SENSITIVITY MAP",
        4.9,
    )
    sa_rates = np.arange(1.0, 5.1, 0.5)
    rest_rates = np.arange(3.0, 6.1, 0.5)
    grid = np.zeros((len(rest_rates), len(sa_rates)))
    for i, rg in enumerate(rest_rates):
        for j, sg in enumerate(sa_rates):
            sa = SA_GDP_2024 * (1 + sg / 100) ** 26
            rest = REST_GDP_2024 * (1 + rg / 100) ** 26
            grid[i, j] = 100 * sa / (sa + rest)
    ax = fig.add_axes([0.13, 0.18, 0.74, 0.57])
    cmap = plt.matplotlib.colors.LinearSegmentedColormap.from_list("gsx_heat", [TOKENS["grey-100"], TOKENS["grey-500"], TOKENS["coral"]])
    ax.imshow(grid, origin="lower", aspect="auto", cmap=cmap, vmin=5, vmax=20)
    ax.set_xticks(np.arange(len(sa_rates)), [f"{x:.1f}%" for x in sa_rates], fontsize=7.2)
    ax.set_yticks(np.arange(len(rest_rates)), [f"{x:.1f}%" for x in rest_rates], fontsize=7.2)
    ax.set_xlabel("South African annual real GDP growth")
    ax.set_ylabel("Rest-of-Africa annual real GDP growth")
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            colour = TOKENS["white"] if grid[i, j] > 13 else TOKENS["black"]
            ax.text(j, i, f"{grid[i, j]:.1f}", ha="center", va="center", fontsize=6.5, color=colour)
    fig.text(0.89, 0.47, "cell = SA share\nof African GDP (%)", fontsize=7.3, color=TOKENS["grey-700"], va="center")
    save(fig, "sensitivity-map.png")


def figure_priority_matrix():
    fig = new_figure(
        "High-value functions still depend on reliable foundations",
        "Illustrative priorities combine continental upside with South Africa's present readiness.",
        "GREYSCIENX / STRATEGIC PRIORITIES",
        4.85,
    )
    ax = fig.add_axes([0.10, 0.17, 0.85, 0.58])
    items = {
        "Capital goods": (74, 72, 520),
        "Finance": (82, 78, 460),
        "Engineering": (78, 70, 430),
        "Knowledge": (70, 62, 380),
        "Headquarters": (67, 58, 330),
        "Logistics gateway": (88, 38, 540),
        "Digital services": (72, 66, 360),
        "Basic mass industry": (52, 48, 300),
    }
    for label, (impact, readiness, size) in items.items():
        colour = TOKENS["coral"] if impact >= 75 else TOKENS["black"]
        ax.scatter(impact, readiness, s=size, color=colour, alpha=0.88, edgecolor=TOKENS["white"], linewidth=0.8)
        ax.annotate(label, (impact, readiness), xytext=(5, 5), textcoords="offset points", fontsize=7.2, fontweight="bold", color=colour)
    ax.axvline(70, color=TOKENS["grey-300"], linewidth=1)
    ax.axhline(60, color=TOKENS["grey-300"], linewidth=1)
    style_axis(ax, TOKENS)
    ax.set_xlabel("Potential continental value (illustrative score)")
    ax.set_ylabel("Current South African readiness (illustrative score)")
    ax.set_xlim(45, 95)
    ax.set_ylim(30, 88)
    ax.text(93, 33, "high upside, weak base", ha="right", fontsize=7.2, color=TOKENS["grey-500"])
    ax.text(93, 84, "build and scale", ha="right", fontsize=7.2, color=TOKENS["grey-500"])
    save(fig, "priority-matrix.png")


def figure_scorecard():
    fig = new_figure(
        "The strategy needs gates that can fail",
        "A relevance strategy is credible only if outcomes can be measured and abandoned when they do not work.",
        "GREYSCIENX / 2050 SCORECARD",
        4.75,
    )
    ax = fig.add_axes([0.05, 0.13, 0.90, 0.63])
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 55)
    ax.axis("off")
    years = [2026, 2030, 2035, 2040, 2050]
    titles = ["MEASURE", "REPAIR", "EXPAND", "OWN", "COMPOUND"]
    notes = [
        "publish the\nrelevance ledger",
        "power, ports,\nvisas, skills",
        "double African\nmarket depth",
        "grow African\nasset income",
        "raise income\nwithout rank obsession",
    ]
    xs = np.linspace(4, 82, 5)
    ax.plot([8, 90], [27, 27], color=TOKENS["grey-300"], linewidth=2)
    for i, (x, year, title, note) in enumerate(zip(xs, years, titles, notes)):
        fill = TOKENS["coral"] if i in (0, 4) else TOKENS["true-black"]
        txt = TOKENS["black"] if i in (0, 4) else TOKENS["white"]
        ax.add_patch(Rectangle((x, 18), 15, 19, facecolor=fill, edgecolor="none"))
        ax.text(x + 7.5, 33, str(year), ha="center", va="center", fontsize=8, fontweight="bold", color=txt)
        ax.text(x + 7.5, 27, title, ha="center", va="center", fontsize=8.2, fontweight="bold", color=txt)
        ax.text(x + 7.5, 21.7, note, ha="center", va="center", fontsize=6.5, color=txt)
    ax.text(50, 7.5, "Every gate is judged by exports, retained income, productivity, reliability and employment - not announcements.", ha="center", fontsize=8.0, fontweight="bold")
    save(fig, "scorecard.png")


def main():
    figure_scale_relevance()
    figure_population_market()
    figure_gdp_share_paths()
    figure_absolute_income()
    figure_relevance_index()
    figure_platform_functions()
    figure_capture_income()
    figure_sensitivity()
    figure_priority_matrix()
    figure_scorecard()

    summary = {
        "units": "constant 2024 US$ billions unless stated",
        "baseline": {
            "africa_gdp": AFRICA_GDP_2024,
            "south_africa_gdp": SA_GDP_2024,
            "south_africa_gdp_share_pct": 100 * SA_GDP_2024 / AFRICA_GDP_2024,
            "africa_population_m": AFRICA_POP_2024,
            "south_africa_population_m": SA_POP_2024,
            "south_africa_population_share_pct": 100 * SA_POP_2024 / AFRICA_POP_2024,
            "relevance_score": BASELINE_RELEVANCE,
        },
        "scenarios_2050": {},
    }
    for name, result in RESULTS.items():
        summary["scenarios_2050"][name] = {
            "sa_real_growth_pct": 100 * SCENARIOS[name]["sa_growth"],
            "rest_africa_real_growth_pct": 100 * SCENARIOS[name]["rest_growth"],
            "sa_gdp": float(result["sa_gdp"][-1]),
            "africa_gdp": float(result["total_gdp"][-1]),
            "sa_gdp_share_pct": float(result["share"][-1]),
            "sa_gdp_per_capita_index": float(result["sa_gdp_pc_index"][-1]),
            "africa_gdp_per_capita_index": float(result["africa_gdp_pc_index"][-1]),
            "africa_linked_income": float(result["captured_income"][-1]),
            "relevance_score": float(result["score"]),
        }
    target_share = 0.138
    required_growth = ((target_share / (1 - target_share)) * (REST_GDP_2024 * (1.042 ** 26)) / SA_GDP_2024) ** (1 / 26) - 1
    summary["growth_needed_to_hold_2024_share_pct"] = 100 * required_growth
    (ROOT / "model_results.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
