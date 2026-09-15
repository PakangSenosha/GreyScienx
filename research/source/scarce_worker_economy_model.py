"""GreyScienx armchair model for a scarce-worker economy.

The model follows a hypothetical South-African-scale economy from 2026 to
2076. It asks how productivity, automation, older workers and immigration can
substitute for a shrinking resident workforce, and where headcount still
matters. All money is constant 2026 rand. Results are scenarios, not forecasts.
"""

from __future__ import annotations

import json
import math
import re
import sys
from pathlib import Path

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
WORK_DIR = ROOT / "work" / "scarce-worker-economy"
ASSET_DIR = WORK_DIR / "assets"
RESULTS_PATH = WORK_DIR / "model_results.json"
CSS_PATH = Path(r"C:\Users\Deriv\Desktop\GreyScienx\app\globals.css")
STYLE_HELPER = Path(
    r"C:\Users\Deriv\Desktop\GreyScienx\skills\greyscienx-editorial-pdf\scripts"
)
if str(STYLE_HELPER) not in sys.path:
    sys.path.insert(0, str(STYLE_HELPER))

try:
    from greyscienx_style import configure_matplotlib  # type: ignore
except Exception:
    configure_matplotlib = None


def load_brand_tokens() -> dict[str, str]:
    defaults = {
        "black": "#131200",
        "true-black": "#000000",
        "coral": "#f26157",
        "white": "#fbfffe",
        "grey-100": "#f0f1f2",
        "grey-300": "#cccccc",
        "grey-500": "#777777",
        "grey-700": "#3d3d3d",
    }
    if CSS_PATH.exists():
        css = CSS_PATH.read_text(encoding="utf-8")
        for key in list(defaults):
            match = re.search(rf"--{re.escape(key)}\s*:\s*(#[0-9a-fA-F]{{6}})", css)
            if match:
                defaults[key] = match.group(1)
    return defaults


TOKENS = load_brand_tokens()
BLACK = TOKENS["black"]
TRUE_BLACK = TOKENS["true-black"]
CORAL = TOKENS["coral"]
WHITE = TOKENS["white"]
GREY_100 = TOKENS["grey-100"]
GREY_300 = TOKENS["grey-300"]
GREY_500 = TOKENS["grey-500"]
GREY_700 = TOKENS["grey-700"]


def set_plot_style() -> None:
    configured = False
    if configure_matplotlib is not None:
        try:
            configure_matplotlib(CSS_PATH)
            configured = True
        except Exception:
            pass
    if not configured:
        plt.rcParams.update(
            {
                "font.family": "sans-serif",
                "font.sans-serif": ["Segoe UI", "Arial", "DejaVu Sans"],
                "font.size": 9.0,
                "axes.edgecolor": BLACK,
                "axes.labelcolor": BLACK,
                "axes.titlecolor": BLACK,
                "xtick.color": BLACK,
                "ytick.color": BLACK,
                "text.color": BLACK,
                "figure.facecolor": WHITE,
                "axes.facecolor": WHITE,
                "savefig.facecolor": WHITE,
            }
        )
    plt.rcParams["axes.unicode_minus"] = False


def figure_header(fig: plt.Figure, field: str, title: str, subtitle: str) -> None:
    fig.add_artist(
        plt.Line2D(
            [0.065, 0.965], [0.955, 0.955], transform=fig.transFigure,
            color=CORAL, linewidth=4.0, solid_capstyle="butt"
        )
    )
    fig.text(0.065, 0.918, field.upper(), color=CORAL, fontsize=8.5,
             fontweight="bold", ha="left", va="top")
    fig.text(0.065, 0.878, title, color=BLACK, fontsize=17,
             fontweight="bold", ha="left", va="top")
    fig.text(0.065, 0.826, subtitle, color=GREY_700, fontsize=8.4,
             ha="left", va="top")


def style_axis(ax: plt.Axes, grid_axis: str = "y") -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(BLACK)
    ax.spines["bottom"].set_color(BLACK)
    ax.grid(axis=grid_axis, color=GREY_300, linewidth=0.6)
    ax.grid(axis="x" if grid_axis == "y" else "y", visible=False)
    ax.set_axisbelow(True)


def save_figure(fig: plt.Figure, name: str) -> Path:
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    path = ASSET_DIR / name
    fig.savefig(path, dpi=280, bbox_inches="tight", facecolor=WHITE)
    plt.close(fig)
    return path


START_YEAR = 2026
END_YEAR = 2076
YEARS = np.arange(START_YEAR, END_YEAR + 1)
T = YEARS - START_YEAR
WORKERS_0 = 12_000_000.0
RETIREES_0 = 3_000_000.0
POPULATION_0 = 22_000_000.0
OUTPUT_PER_WORKER_0 = 420_000.0
WAGE_0 = 300_000.0
RETIREE_COST_0 = 100_000.0
RETIREMENT_AGE = 67
MIGRANT_AGE = 25
INTEGRATION_LAG = 2
WORKING_COHORT_YEARS = RETIREMENT_AGE - MIGRANT_AGE - INTEGRATION_LAG


SCENARIOS = {
    "Worst": {
        "worker_decline": -0.0085,
        "population_decline": -0.0060,
        "retirees_2076": 6_600_000.0,
        "organic_productivity": 0.0030,
        "automation_productivity": 0.0010,
        "annual_immigrants": 20_000.0,
        "migrant_employment": 0.68,
        "migrant_retention": 0.70,
        "older_workers_2076": 250_000.0,
    },
    "Average": {
        "worker_decline": -0.0060,
        "population_decline": -0.0035,
        "retirees_2076": 6_000_000.0,
        "organic_productivity": 0.0060,
        "automation_productivity": 0.0030,
        "annual_immigrants": 75_000.0,
        "migrant_employment": 0.84,
        "migrant_retention": 0.80,
        "older_workers_2076": 700_000.0,
    },
    "Best": {
        "worker_decline": -0.0035,
        "population_decline": -0.0020,
        "retirees_2076": 5_400_000.0,
        "organic_productivity": 0.0090,
        "automation_productivity": 0.0050,
        "annual_immigrants": 110_000.0,
        "migrant_employment": 0.90,
        "migrant_retention": 0.86,
        "older_workers_2076": 1_100_000.0,
    },
}


def migrant_paths(annual_arrivals: float, employment: float, retention: float) -> dict[str, np.ndarray]:
    workers = np.zeros(len(YEARS))
    retirees = np.zeros(len(YEARS))
    residents = np.zeros(len(YEARS))
    for i, year in enumerate(YEARS):
        for arrival_year in range(START_YEAR + 1, int(year) + 1):
            age = MIGRANT_AGE + (int(year) - arrival_year)
            years_since_arrival = int(year) - arrival_year
            retained = annual_arrivals * retention
            if age < 90:
                residents[i] += retained
            if years_since_arrival >= INTEGRATION_LAG and age < RETIREMENT_AGE:
                workers[i] += retained * employment
            elif RETIREMENT_AGE <= age < 90:
                retirees[i] += retained
    return {"workers": workers, "retirees": retirees, "residents": residents}


def scenario_path(name: str, params: dict[str, float]) -> dict[str, np.ndarray | float]:
    native_workers = WORKERS_0 * ((1 + params["worker_decline"]) ** T)
    native_population = POPULATION_0 * ((1 + params["population_decline"]) ** T)
    native_retirees = np.linspace(RETIREES_0, params["retirees_2076"], len(YEARS))
    older_workers = params["older_workers_2076"] * (T / T[-1]) ** 1.25
    migration = migrant_paths(
        params["annual_immigrants"],
        params["migrant_employment"],
        params["migrant_retention"],
    )
    workers = native_workers + older_workers + migration["workers"]
    retirees = native_retirees + migration["retirees"]
    total_productivity_rate = params["organic_productivity"] + params["automation_productivity"]
    productivity = (1 + total_productivity_rate) ** T
    organic = (1 + params["organic_productivity"]) ** T
    automation = (1 + params["automation_productivity"]) ** T
    gdp = workers * OUTPUT_PER_WORKER_0 * productivity
    population = native_population + migration["residents"] * 1.15
    gdp_per_capita = gdp / population
    wage_productivity = (1 + 0.65 * total_productivity_rate) ** T
    retiree_cost = RETIREE_COST_0 * (1.004 ** T)
    contribution_rate = retirees * retiree_cost / (workers * WAGE_0 * wage_productivity)

    needed_annual = max(
        0.0,
        (WORKERS_0 - native_workers[-1] - older_workers[-1])
        / (WORKING_COHORT_YEARS * params["migrant_employment"] * params["migrant_retention"]),
    )
    organic_equivalent = workers[-1] * (organic[-1] - 1)
    automation_equivalent = workers[-1] * organic[-1] * (automation[-1] - 1)
    return {
        "name": name,
        "native_workers": native_workers,
        "older_workers": older_workers,
        "migrant_workers": migration["workers"],
        "migrant_retirees": migration["retirees"],
        "migrant_residents": migration["residents"],
        "workers": workers,
        "retirees": retirees,
        "support_ratio": workers / retirees,
        "productivity": productivity,
        "organic_productivity": organic,
        "automation_productivity": automation,
        "gdp": gdp,
        "population": population,
        "gdp_per_capita": gdp_per_capita,
        "contribution_rate": contribution_rate,
        "needed_annual_immigrants": needed_annual,
        "organic_equivalent_2076": organic_equivalent,
        "automation_equivalent_2076": automation_equivalent,
    }


PATHS = {name: scenario_path(name, params) for name, params in SCENARIOS.items()}


SECTORS = [
    "Digital and admin",
    "Manufacturing and logistics",
    "Construction and maintenance",
    "Health and care",
    "Education, safety and public services",
    "Food, agriculture and personal services",
]
SECTOR_BASE_SHARES = np.array([0.24, 0.20, 0.12, 0.16, 0.16, 0.12])
SECTOR_DEMAND_2076 = np.array([0.95, 0.90, 0.95, 1.75, 1.00, 1.05])
SECTOR_PRODUCTIVITY_2076 = np.array([2.30, 1.95, 1.45, 1.25, 1.40, 1.30])
SECTOR_AVAILABLE_2076 = np.array([1.80, 1.55, 0.82, 1.95, 1.25, 1.15]) * 1e6
SECTOR_REQUIRED_2076 = WORKERS_0 * SECTOR_BASE_SHARES * SECTOR_DEMAND_2076 / SECTOR_PRODUCTIVITY_2076
SECTOR_GAP_2076 = SECTOR_REQUIRED_2076 - SECTOR_AVAILABLE_2076
SECTOR_WAGE_PRESSURE = np.clip(SECTOR_GAP_2076 / SECTOR_AVAILABLE_2076 * 0.60, -0.10, 0.35)


def productivity_hurdle(worker_ratio: np.ndarray, retiree_ratio: np.ndarray | float = 1.0) -> np.ndarray:
    cost_growth = 1.004 ** (END_YEAR - START_YEAR)
    return ((np.asarray(retiree_ratio) * cost_growth / worker_ratio) ** (1 / (END_YEAR - START_YEAR)) - 1) * 100


def fiscal_value(
    wage: float,
    employment: float,
    retention: float,
    tax_rate: float,
    wage_growth: float,
    integration_cost: float,
    annual_services: float = 45_000.0,
    retirement_cost: float = 125_000.0,
    discount: float = 0.03,
) -> float:
    pv = -integration_cost
    for year in range(0, 65):
        age = MIGRANT_AGE + year
        if year < INTEGRATION_LAG:
            net = -annual_services
        elif age < RETIREMENT_AGE:
            earnings = wage * ((1 + wage_growth) ** year)
            net = employment * earnings * tax_rate - annual_services
        elif age < 90:
            net = -retirement_cost * (1.004 ** max(0, age - RETIREMENT_AGE))
        else:
            net = 0.0
        pv += retention * net / ((1 + discount) ** year)
    return pv


FISCAL_CASES = {
    "Weak integration": fiscal_value(260_000, 0.68, 0.70, 0.23, 0.005, 180_000),
    "Skilled, average": fiscal_value(420_000, 0.84, 0.80, 0.27, 0.010, 150_000),
    "Skilled, strong": fiscal_value(550_000, 0.90, 0.86, 0.30, 0.014, 120_000),
}


def fiscal_value_birth() -> float:
    discount = 0.03
    pv = -250_000.0
    for year in range(0, 90):
        age = year
        if age < 22:
            annual_cost = 28_000.0 if age < 6 else 40_000.0
            pv -= annual_cost / ((1 + discount) ** year)
        elif age < 67:
            earnings = 350_000.0 * (1.01 ** (age - 22))
            net = 0.78 * earnings * 0.24 - 45_000.0
            pv += net / ((1 + discount) ** year)
        else:
            pv -= 125_000.0 * (1.004 ** (age - 67)) / ((1 + discount) ** year)
    return pv


BIRTH_FISCAL_VALUE = fiscal_value_birth()


def make_support_figure() -> None:
    avg = PATHS["Average"]
    fig, axes = plt.subplots(1, 2, figsize=(10.6, 5.2), gridspec_kw={"wspace": 0.28})
    figure_header(
        fig, "Figure 01 / support arithmetic", "More retirees, fewer resident workers",
        "Average case for a hypothetical South-African-scale economy; people in millions"
    )
    ax = axes[0]
    ax.plot(YEARS, np.asarray(avg["native_workers"]) / 1e6, color=BLACK, linewidth=2.5,
            linestyle="--", label="Resident workers")
    ax.plot(YEARS, np.asarray(avg["workers"]) / 1e6, color=CORAL, linewidth=2.8,
            label="Workers after immigration and later work")
    ax.plot(YEARS, np.asarray(avg["retirees"]) / 1e6, color=GREY_500, linewidth=2.3,
            linestyle=":", label="Retirees")
    style_axis(ax)
    ax.set_ylabel("People (millions)")
    ax.set_xlabel("Year")
    ax.legend(frameon=False, loc="best", fontsize=7.8)

    ax = axes[1]
    no_response_ratio = np.asarray(avg["native_workers"]) / np.linspace(RETIREES_0, 6_000_000, len(YEARS))
    ax.plot(YEARS, no_response_ratio, color=BLACK, linewidth=2.4, linestyle="--",
            label="Resident workers only")
    ax.plot(YEARS, np.asarray(avg["support_ratio"]), color=CORAL, linewidth=2.8,
            label="Average response")
    ax.axhline(2.0, color=GREY_500, linewidth=1.0, linestyle=":")
    ax.text(2074.5, 2.07, "2 workers per retiree", color=GREY_700, ha="right", fontsize=7.5)
    style_axis(ax)
    ax.set_ylabel("Workers per retiree")
    ax.set_xlabel("Year")
    ax.legend(frameon=False, loc="upper right", fontsize=7.8)
    fig.subplots_adjust(top=0.76, bottom=0.14, left=0.08, right=0.97)
    save_figure(fig, "support-arithmetic.png")


def make_hurdle_figure() -> None:
    fig, axes = plt.subplots(1, 2, figsize=(10.6, 5.35), gridspec_kw={"wspace": 0.34})
    figure_header(
        fig, "Figure 02 / productivity hurdle", "The small GDP hurdle hides a larger fiscal hurdle",
        "Annual real productivity growth required over fifty years; percentages"
    )
    ax = axes[0]
    decline = np.linspace(0, 45, 181)
    wr = 1 - decline / 100
    gdp_hurdle = ((1 / wr) ** (1 / 50) - 1) * 100
    ax.plot(decline, gdp_hurdle, color=CORAL, linewidth=2.8)
    central_decline = (1 - np.asarray(PATHS["Average"]["native_workers"])[-1] / WORKERS_0) * 100
    central_hurdle = ((1 / (1 - central_decline / 100)) ** (1 / 50) - 1) * 100
    ax.scatter([central_decline], [central_hurdle], color=BLACK, s=34, zorder=4)
    ax.annotate(f"Average case: {central_hurdle:.2f}% a year", (central_decline, central_hurdle),
                xytext=(8, 13), textcoords="offset points", fontsize=7.8, color=BLACK)
    style_axis(ax)
    ax.set_xlabel("Resident workforce decline by 2076 (%)")
    ax.set_ylabel("Growth needed to hold GDP flat (% a year)")

    ax = axes[1]
    worker_ratios = np.linspace(0.55, 1.00, 160)
    retiree_ratios = np.linspace(1.0, 2.4, 160)
    X, Y = np.meshgrid(worker_ratios, retiree_ratios)
    Z = productivity_hurdle(X, Y)
    cmap = mcolors.LinearSegmentedColormap.from_list("greycoral", [WHITE, GREY_300, CORAL, TRUE_BLACK])
    mesh = ax.pcolormesh(X * 100, Y, Z, cmap=cmap, shading="auto", vmin=0.5, vmax=2.8)
    contours = ax.contour(X * 100, Y, Z, levels=[1.0, 1.5, 2.0, 2.5], colors=BLACK, linewidths=0.65)
    ax.clabel(contours, inline=True, fontsize=7, fmt="%.1f%%")
    avg_wr = np.asarray(PATHS["Average"]["native_workers"])[-1] / WORKERS_0
    avg_rr = 6_000_000 / RETIREES_0
    ax.scatter([avg_wr * 100], [avg_rr], color=WHITE, edgecolor=BLACK, s=45, linewidth=1.1, zorder=5)
    ax.annotate("Average demographic case", (avg_wr * 100, avg_rr), xytext=(-56, 10),
                textcoords="offset points", fontsize=7.5, color=WHITE, fontweight="bold")
    ax.set_xlabel("Resident workforce remaining in 2076 (%)")
    ax.set_ylabel("Retirees relative to 2026")
    cbar = fig.colorbar(mesh, ax=ax, fraction=0.048, pad=0.03)
    cbar.set_label("Required wage productivity (% a year)", fontsize=7.6)
    cbar.ax.tick_params(labelsize=7)
    fig.subplots_adjust(top=0.75, bottom=0.15, left=0.08, right=0.96)
    save_figure(fig, "productivity-hurdle.png")


def make_substitution_figure() -> None:
    names = list(SCENARIOS)
    missing = np.array([WORKERS_0 - np.asarray(PATHS[n]["native_workers"])[-1] for n in names]) / 1e6
    older = np.array([np.asarray(PATHS[n]["older_workers"])[-1] for n in names]) / 1e6
    migrants = np.array([np.asarray(PATHS[n]["migrant_workers"])[-1] for n in names]) / 1e6
    organic = np.array([float(PATHS[n]["organic_equivalent_2076"]) for n in names]) / 1e6
    automation = np.array([float(PATHS[n]["automation_equivalent_2076"]) for n in names]) / 1e6

    fig, ax = plt.subplots(figsize=(10.6, 5.3))
    figure_header(
        fig, "Figure 03 / substitution", "Four levers can close an output gap - but only two add people",
        "2076 worker-equivalent contribution versus missing resident workers; millions"
    )
    x = np.arange(len(names))
    width = 0.58
    bottoms = np.zeros(len(names))
    components = [
        (older, "Older workers", CORAL, None),
        (migrants, "Employed immigrants", BLACK, "//"),
        (organic, "General productivity", GREY_500, None),
        (automation, "Automation and AI", GREY_300, ".."),
    ]
    for values, label, color, hatch in components:
        ax.bar(x, values, width, bottom=bottoms, color=color, label=label, hatch=hatch,
               edgecolor=WHITE if hatch else color, linewidth=0.5)
        bottoms += values
    for i, target in enumerate(missing):
        ax.hlines(target, i - width / 2 - 0.06, i + width / 2 + 0.06, color=CORAL,
                  linewidth=3.0, zorder=5)
        ax.text(i, target + 0.15, f"missing {target:.1f}m", ha="center", va="bottom",
                fontsize=7.6, color=CORAL, fontweight="bold")
    style_axis(ax)
    ax.set_xticks(x, names)
    ax.set_ylabel("Worker-equivalent contribution (millions)")
    ax.set_xlabel("Scenario")
    ax.legend(frameon=False, ncol=4, loc="upper left", fontsize=7.4)
    ax.set_ylim(0, max(bottoms) * 1.15)
    fig.subplots_adjust(top=0.75, bottom=0.14, left=0.08, right=0.97)
    save_figure(fig, "workforce-substitution.png")


def make_staffing_figure() -> None:
    order = np.arange(len(SECTORS))[::-1]
    required = SECTOR_REQUIRED_2076[order] / 1e6
    available = SECTOR_AVAILABLE_2076[order] / 1e6
    wage = SECTOR_WAGE_PRESSURE[order] * 100
    labels = [SECTORS[i] for i in order]

    fig, axes = plt.subplots(1, 2, figsize=(10.6, 5.8), gridspec_kw={"width_ratios": [1.55, 0.8], "wspace": 0.30})
    figure_header(
        fig, "Figure 04 / staffing frontier", "Automation cannot move a spreadsheet into a hospital ward",
        "Average case in 2076; worker requirements, available workers and modelled wage pressure"
    )
    y = np.arange(len(labels))
    ax = axes[0]
    ax.barh(y - 0.17, required, height=0.31, color=CORAL, label="Workers required")
    ax.barh(y + 0.17, available, height=0.31, color=BLACK, label="Workers available")
    style_axis(ax, "x")
    ax.set_yticks(y, labels)
    ax.set_xlabel("Workers (millions)")
    ax.legend(frameon=False, loc="lower right", fontsize=7.6)
    for yy, req, avail in zip(y, required, available):
        if req > avail:
            ax.text(max(req, avail) + 0.04, yy, f"gap {req-avail:.2f}m", va="center",
                    fontsize=7.2, color=CORAL, fontweight="bold")

    ax = axes[1]
    colors = [CORAL if val > 0 else GREY_500 for val in wage]
    ax.barh(y, wage, color=colors, height=0.48)
    ax.axvline(0, color=BLACK, linewidth=0.8)
    style_axis(ax, "x")
    ax.set_yticks(y, [])
    ax.set_xlabel("Real wage pressure versus baseline (%)")
    for yy, val in zip(y, wage):
        ax.text(val + (0.7 if val >= 0 else -0.7), yy, f"{val:+.0f}%",
                va="center", ha="left" if val >= 0 else "right", fontsize=7.4, color=BLACK)
    ax.set_xlim(min(-12, wage.min() - 3), max(28, wage.max() + 4))
    fig.subplots_adjust(top=0.74, bottom=0.14, left=0.23, right=0.97)
    save_figure(fig, "staffing-bottlenecks.png")


def make_migration_figure() -> None:
    names = list(SCENARIOS)
    actual = np.array([SCENARIOS[n]["annual_immigrants"] for n in names]) / 1e3
    needed = np.array([float(PATHS[n]["needed_annual_immigrants"]) for n in names]) / 1e3

    fig, axes = plt.subplots(1, 2, figsize=(10.6, 5.4), gridspec_kw={"wspace": 0.34})
    figure_header(
        fig, "Figure 05 / migration", "A young immigrant is a bridge, not demographic immortality",
        "Annual inflows required for headcount stability and lifetime direct fiscal value"
    )
    ax = axes[0]
    x = np.arange(len(names))
    ax.bar(x - 0.18, actual, width=0.36, color=CORAL, label="Modelled annual inflow")
    ax.bar(x + 0.18, needed, width=0.36, color=BLACK, label="Needed to hold 12m workers")
    style_axis(ax)
    ax.set_xticks(x, names)
    ax.set_ylabel("Young working-age arrivals (thousands a year)")
    ax.set_xlabel("Scenario")
    ax.legend(frameon=False, fontsize=7.5, loc="upper right")

    ax = axes[1]
    labels = list(FISCAL_CASES) + ["Additional birth"]
    values = np.array(list(FISCAL_CASES.values()) + [BIRTH_FISCAL_VALUE]) / 1e6
    colors = [GREY_500, CORAL, BLACK, GREY_300]
    bars = ax.barh(np.arange(len(labels))[::-1], values, color=colors)
    ax.axvline(0, color=BLACK, linewidth=0.9)
    style_axis(ax, "x")
    ax.set_yticks(np.arange(len(labels))[::-1], labels)
    ax.set_xlabel("Lifetime direct fiscal value (R millions, PV at age 25 or birth)")
    lim = max(abs(values.min()), abs(values.max())) * 1.24
    ax.set_xlim(-lim, lim)
    for bar, val in zip(bars, values):
        ax.text(val + (0.045 if val >= 0 else -0.045), bar.get_y() + bar.get_height() / 2,
                f"{val:+.2f}", va="center", ha="left" if val >= 0 else "right",
                fontsize=7.4, color=BLACK)
    fig.subplots_adjust(top=0.74, bottom=0.15, left=0.11, right=0.97)
    save_figure(fig, "migration-and-fiscal-value.png")


def make_gdp_figure() -> None:
    avg = PATHS["Average"]
    no_response_prod = 1.004 ** T
    no_response_gdp = np.asarray(avg["native_workers"]) * OUTPUT_PER_WORKER_0 * no_response_prod
    no_response_pop = POPULATION_0 * ((1 - 0.0035) ** T)
    no_response_pc = no_response_gdp / no_response_pop

    fig, axes = plt.subplots(1, 2, figsize=(10.6, 5.2), gridspec_kw={"wspace": 0.28})
    figure_header(
        fig, "Figure 06 / growth", "A country can shrink while living standards rise",
        "Real GDP and GDP per person, indexed to 100 in 2026"
    )
    style_map = {
        "No adaptation": (BLACK, "--"),
        "Worst": (GREY_500, ":"),
        "Average": (CORAL, "-"),
        "Best": (BLACK, "-"),
    }
    for ax, metric, no_response in [
        (axes[0], "gdp", no_response_gdp),
        (axes[1], "gdp_per_capita", no_response_pc),
    ]:
        ax.plot(YEARS, no_response / no_response[0] * 100,
                color=style_map["No adaptation"][0], linestyle=style_map["No adaptation"][1],
                linewidth=2.0, label="No adaptation")
        for name in ["Worst", "Average", "Best"]:
            values = np.asarray(PATHS[name][metric])
            ax.plot(YEARS, values / values[0] * 100, color=style_map[name][0],
                    linestyle=style_map[name][1], linewidth=2.5, label=name)
        style_axis(ax)
        ax.set_xlabel("Year")
        ax.set_ylabel("Index (2026 = 100)")
    axes[0].set_title("Total GDP", fontsize=10, fontweight="bold", loc="left")
    axes[1].set_title("GDP per person", fontsize=10, fontweight="bold", loc="left")
    axes[0].legend(frameon=False, fontsize=7.5, loc="upper left")
    fig.subplots_adjust(top=0.75, bottom=0.14, left=0.08, right=0.97)
    save_figure(fig, "gdp-and-gdp-per-capita.png")


def serialise_array(value: np.ndarray) -> list[float]:
    return [round(float(v), 3) for v in value]


def build_results() -> dict[str, object]:
    scenario_results: dict[str, object] = {}
    for name, path in PATHS.items():
        scenario_results[name] = {
            "assumptions": SCENARIOS[name],
            "workers": serialise_array(np.asarray(path["workers"])),
            "native_workers": serialise_array(np.asarray(path["native_workers"])),
            "migrant_workers": serialise_array(np.asarray(path["migrant_workers"])),
            "retirees": serialise_array(np.asarray(path["retirees"])),
            "support_ratio": serialise_array(np.asarray(path["support_ratio"])),
            "gdp_index": serialise_array(np.asarray(path["gdp"]) / np.asarray(path["gdp"])[0] * 100),
            "gdp_per_capita_index": serialise_array(
                np.asarray(path["gdp_per_capita"]) / np.asarray(path["gdp_per_capita"])[0] * 100
            ),
            "contribution_rate": serialise_array(np.asarray(path["contribution_rate"]) * 100),
            "needed_annual_immigrants": round(float(path["needed_annual_immigrants"])),
            "organic_worker_equivalent_2076": round(float(path["organic_equivalent_2076"])),
            "automation_worker_equivalent_2076": round(float(path["automation_equivalent_2076"])),
        }
    return {
        "study": "The Scarce-Worker Economy",
        "prices": "constant 2026 rand",
        "years": [int(y) for y in YEARS],
        "core_assumptions": {
            "workers_2026": WORKERS_0,
            "retirees_2026": RETIREES_0,
            "population_2026": POPULATION_0,
            "output_per_worker_2026": OUTPUT_PER_WORKER_0,
            "annual_wage_2026": WAGE_0,
            "annual_age_related_cost_per_retiree_2026": RETIREE_COST_0,
            "retirement_age": RETIREMENT_AGE,
            "migrant_arrival_age": MIGRANT_AGE,
            "integration_lag_years": INTEGRATION_LAG,
        },
        "scenarios": scenario_results,
        "sectors": {
            "names": SECTORS,
            "required_workers_2076": serialise_array(SECTOR_REQUIRED_2076),
            "available_workers_2076": serialise_array(SECTOR_AVAILABLE_2076),
            "worker_gap_2076": serialise_array(SECTOR_GAP_2076),
            "wage_pressure_percent": serialise_array(SECTOR_WAGE_PRESSURE * 100),
        },
        "fiscal_values_present_value_rand": {
            **{name: round(value) for name, value in FISCAL_CASES.items()},
            "Additional birth": round(BIRTH_FISCAL_VALUE),
        },
        "warnings": [
            "The economy is hypothetical and is not a forecast for South Africa or Gauteng.",
            "Migration, employment, productivity and demographic paths are declared scenarios.",
            "Automation worker-equivalents describe output capacity, not people or tax contributors.",
            "Sector staffing and wage responses are teaching assumptions, not occupational forecasts.",
            "Fiscal values exclude wider spillovers, descendants, remittances and distributional effects.",
        ],
    }


def validate() -> None:
    assert math.isclose(SECTOR_BASE_SHARES.sum(), 1.0)
    assert PATHS["Average"]["support_ratio"][0] == WORKERS_0 / RETIREES_0
    assert np.asarray(PATHS["Average"]["native_workers"])[-1] < WORKERS_0
    assert np.asarray(PATHS["Average"]["retirees"])[-1] > RETIREES_0
    assert SECTOR_GAP_2076[3] > 500_000
    assert SECTOR_WAGE_PRESSURE[3] > 0.20
    assert FISCAL_CASES["Skilled, strong"] > FISCAL_CASES["Skilled, average"]
    assert FISCAL_CASES["Skilled, average"] > FISCAL_CASES["Weak integration"]
    assert float(PATHS["Worst"]["needed_annual_immigrants"]) > float(PATHS["Average"]["needed_annual_immigrants"])
    assert float(PATHS["Average"]["needed_annual_immigrants"]) > float(PATHS["Best"]["needed_annual_immigrants"])


def main() -> None:
    set_plot_style()
    validate()
    WORK_DIR.mkdir(parents=True, exist_ok=True)
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    make_support_figure()
    make_hurdle_figure()
    make_substitution_figure()
    make_staffing_figure()
    make_migration_figure()
    make_gdp_figure()
    RESULTS_PATH.write_text(json.dumps(build_results(), indent=2), encoding="utf-8")
    print(f"Wrote {RESULTS_PATH}")
    for name, path in PATHS.items():
        print(
            f"{name}: workers {np.asarray(path['workers'])[-1]/1e6:.2f}m, "
            f"retirees {np.asarray(path['retirees'])[-1]/1e6:.2f}m, "
            f"support {np.asarray(path['support_ratio'])[-1]:.2f}, "
            f"GDP index {np.asarray(path['gdp'])[-1]/np.asarray(path['gdp'])[0]*100:.1f}, "
            f"GDP pc index {np.asarray(path['gdp_per_capita'])[-1]/np.asarray(path['gdp_per_capita'])[0]*100:.1f}, "
            f"age rate {np.asarray(path['contribution_rate'])[-1]*100:.1f}%"
        )
    print("Fiscal PV:", {k: round(v / 1e6, 2) for k, v in FISCAL_CASES.items()}, "birth", round(BIRTH_FISCAL_VALUE / 1e6, 2))


if __name__ == "__main__":
    main()
