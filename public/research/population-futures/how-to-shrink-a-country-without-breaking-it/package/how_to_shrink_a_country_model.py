"""GreyScienx armchair model for demographic and urban contraction.

The model follows a hypothetical Gauteng city-region from 2026 to 2076.
It links population, household size, housing, municipal infrastructure,
schools, universities and regional property values. It compares managed
shrinkage with delayed adjustment. All money is constant 2026 rand and all
results are scenarios rather than forecasts or municipal engineering advice.
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
WORK_DIR = ROOT / "work" / "how-to-shrink-a-country"
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
POPULATION_0 = 1_200_000.0
HOUSEHOLD_SIZE_0 = 2.86
HOUSEHOLDS_0 = POPULATION_0 / HOUSEHOLD_SIZE_0
HABITABLE_HOMES_0 = 430_000.0
CENTRAL_POP_DECLINE = -0.005

ZONE_NAMES = ["Central corridor", "Inner suburbs", "Outer edge", "Satellite town"]
ZONE_POP_0 = np.array([240_000.0, 360_000.0, 420_000.0, 180_000.0])
ZONE_HH_SIZE_0 = np.array([2.40, 2.75, 3.00, 3.60])
ZONE_HH_SIZE_2076 = np.array([1.80, 2.00, 2.25, 2.75])
ZONE_FIXED_OM_BN = np.array([0.25, 0.42, 0.50, 0.19])
ZONE_COLLECTION = np.array([0.97, 0.92, 0.85, 0.78])
MAINTENANCE_REVENUE_PER_HH = 6_200.0
VARIABLE_OM_PER_PERSON = 700.0


def population_path(rate: float) -> np.ndarray:
    return POPULATION_0 * ((1 + rate) ** T)


def household_size_path(end_size: float) -> np.ndarray:
    return np.linspace(HOUSEHOLD_SIZE_0, end_size, len(YEARS))


def household_path(pop_rate: float, end_size: float) -> np.ndarray:
    return population_path(pop_rate) / household_size_path(end_size)


def housing_stock_paths(households: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    delayed = np.zeros(len(YEARS))
    managed = np.zeros(len(YEARS))
    delayed[0] = HABITABLE_HOMES_0
    managed[0] = HABITABLE_HOMES_0
    for i in range(1, len(YEARS)):
        delayed_build = 2_500.0 if YEARS[i] <= 2035 else 500.0
        delayed[i] = delayed[i - 1] * (1 - 0.0045) + delayed_build

        target = households[i] / 0.95
        required_after_decay = target - managed[i - 1] * (1 - 0.0025)
        managed_build = max(600.0, min(2_400.0, required_after_decay))
        managed[i] = managed[i - 1] * (1 - 0.0025) + managed_build
    return delayed, managed


def regional_paths() -> dict[str, np.ndarray]:
    delayed_rates = np.array([-0.002, -0.004, -0.0065, -0.012])
    delayed_pop = np.stack(
        [ZONE_POP_0[z] * ((1 + delayed_rates[z]) ** T) for z in range(4)], axis=1
    )

    total_managed = population_path(CENTRAL_POP_DECLINE)
    start_shares = ZONE_POP_0 / ZONE_POP_0.sum()
    end_shares = np.array([0.28, 0.34, 0.26, 0.12])
    managed_shares = np.stack(
        [np.linspace(start_shares[z], end_shares[z], len(YEARS)) for z in range(4)],
        axis=1,
    )
    managed_pop = total_managed[:, None] * managed_shares

    hh_sizes = np.stack(
        [np.linspace(ZONE_HH_SIZE_0[z], ZONE_HH_SIZE_2076[z], len(YEARS)) for z in range(4)],
        axis=1,
    )
    delayed_hh = delayed_pop / hh_sizes
    managed_hh = managed_pop / hh_sizes

    age_factor_delayed = 1.004 ** T
    delayed_cost = (
        ZONE_FIXED_OM_BN[None, :] * age_factor_delayed[:, None]
        + delayed_pop * VARIABLE_OM_PER_PERSON / 1e9
    )
    collection_decay = np.stack(
        [np.linspace(1.0, end, len(YEARS)) for end in (0.98, 0.93, 0.83, 0.72)],
        axis=1,
    )
    delayed_revenue = (
        delayed_hh * MAINTENANCE_REVENUE_PER_HH
        * ZONE_COLLECTION[None, :] * collection_decay / 1e9
    )
    delayed_coverage = delayed_revenue / delayed_cost

    retirement_end = np.array([0.97, 0.84, 0.64, 0.52])
    retirement_start_year = np.array([2046, 2041, 2036, 2031])
    fixed_multipliers = np.ones_like(managed_pop)
    for z in range(4):
        span = max(1, END_YEAR - retirement_start_year[z])
        progress = np.clip((YEARS - retirement_start_year[z]) / span, 0, 1)
        fixed_multipliers[:, z] = 1 - progress * (1 - retirement_end[z])
    managed_cost = (
        ZONE_FIXED_OM_BN[None, :] * (1.0015 ** T)[:, None] * fixed_multipliers
        + managed_pop * VARIABLE_OM_PER_PERSON / 1e9
    )
    collection_gain = np.stack(
        [np.linspace(1.0, end, len(YEARS)) for end in (1.02, 1.03, 1.02, 1.00)],
        axis=1,
    )
    managed_revenue = (
        managed_hh * MAINTENANCE_REVENUE_PER_HH
        * ZONE_COLLECTION[None, :] * collection_gain / 1e9
    )
    managed_coverage = managed_revenue / managed_cost

    return {
        "delayed_pop": delayed_pop,
        "managed_pop": managed_pop,
        "hh_sizes": hh_sizes,
        "delayed_hh": delayed_hh,
        "managed_hh": managed_hh,
        "delayed_cost": delayed_cost,
        "managed_cost": managed_cost,
        "delayed_revenue": delayed_revenue,
        "managed_revenue": managed_revenue,
        "delayed_coverage": delayed_coverage,
        "managed_coverage": managed_coverage,
    }


def first_year_below(values: np.ndarray, threshold: float) -> int | None:
    hits = np.where(values < threshold)[0]
    return int(YEARS[hits[0]]) if len(hits) else None


def education_paths() -> dict[str, np.ndarray]:
    pop = population_path(CENTRAL_POP_DECLINE)
    learners = 0.18 * POPULATION_0 * ((1 + CENTRAL_POP_DECLINE - 0.008) ** T)
    schools_delayed = np.full(len(YEARS), 240.0)
    after_2045 = YEARS >= 2046
    schools_delayed[after_2045] = np.linspace(240, 216, after_2045.sum())
    schools_managed = np.maximum(120.0, np.ceil(learners / 900.0))
    capacity_delayed = schools_delayed * 1_100.0
    capacity_managed = schools_managed * 1_100.0
    school_cost_delayed = schools_delayed * 14e6 + learners * 25_000.0
    school_cost_managed = schools_managed * 14e6 + learners * 27_000.0

    university_students = 45_000.0 * ((1 - 0.008) ** T)
    university_fixed_delayed = np.full(len(YEARS), 1.8e9)
    campus_progress = np.clip((YEARS - 2036) / 20, 0, 1)
    university_fixed_managed = 1.8e9 - 0.55e9 * campus_progress
    university_cost_delayed = university_fixed_delayed + university_students * 55_000.0
    university_cost_managed = university_fixed_managed + university_students * 58_000.0

    return {
        "population": pop,
        "learners": learners,
        "schools_delayed": schools_delayed,
        "schools_managed": schools_managed,
        "school_util_delayed": learners / capacity_delayed,
        "school_util_managed": learners / capacity_managed,
        "school_cost_delayed": school_cost_delayed,
        "school_cost_managed": school_cost_managed,
        "school_cost_per_learner_delayed": school_cost_delayed / learners,
        "school_cost_per_learner_managed": school_cost_managed / learners,
        "university_students": university_students,
        "university_cost_delayed": university_cost_delayed,
        "university_cost_managed": university_cost_managed,
    }


def housing_price_indices(regional: dict[str, np.ndarray]) -> dict[str, np.ndarray]:
    initial_hh = regional["delayed_hh"][0]
    initial_stock = initial_hh / 0.95
    delayed_stock = np.zeros_like(regional["delayed_hh"])
    delayed_stock[0] = initial_stock
    build_rates = np.array([0.0040, 0.0030, 0.0025, 0.0010])
    decay_rates = np.array([0.0015, 0.0020, 0.0035, 0.0050])
    for i in range(1, len(YEARS)):
        build_scale = 1.0 if YEARS[i] <= 2035 else 0.20
        delayed_stock[i] = (
            delayed_stock[i - 1] * (1 - decay_rates)
            + initial_stock * build_rates * build_scale
        )

    managed_target_vacancy = np.stack(
        [np.linspace(0.05, end, len(YEARS)) for end in (0.04, 0.05, 0.08, 0.12)],
        axis=1,
    )
    managed_stock = regional["managed_hh"] / (1 - managed_target_vacancy)

    delayed_occupancy = np.clip(regional["delayed_hh"] / delayed_stock, 0.45, 1.08)
    managed_occupancy = np.clip(regional["managed_hh"] / managed_stock, 0.45, 1.08)
    delayed_service = np.clip(
        regional["delayed_coverage"] / regional["delayed_coverage"][0], 0.45, 1.10
    )
    managed_service = np.clip(
        regional["managed_coverage"] / regional["managed_coverage"][0], 0.65, 1.20
    )
    amenity_end = np.array([1.12, 1.03, 0.92, 0.82])
    amenity = np.stack(
        [np.linspace(1.0, amenity_end[z], len(YEARS)) for z in range(4)], axis=1
    )
    delayed_price = 100 * (delayed_occupancy / 0.95) ** 3.0 * delayed_service ** 1.2
    managed_price = 100 * (managed_occupancy / 0.95) ** 2.0 * managed_service ** 0.8 * amenity

    return {
        "delayed_stock": delayed_stock,
        "managed_stock": managed_stock,
        "delayed_vacancy": 1 - regional["delayed_hh"] / delayed_stock,
        "managed_vacancy": managed_target_vacancy,
        "delayed_price": delayed_price,
        "managed_price": managed_price,
    }


def present_value(series: np.ndarray, rate: float = 0.03) -> float:
    return float(np.sum(series / ((1 + rate) ** T)))


def strategy_costs(
    regional: dict[str, np.ndarray], education: dict[str, np.ndarray], prices: dict[str, np.ndarray]
) -> dict[str, dict[str, float]]:
    delayed_coverage_gap = np.clip(0.90 - regional["delayed_coverage"], 0, None)
    managed_coverage_gap = np.clip(0.90 - regional["managed_coverage"], 0, None)
    delayed_infra_annual = regional["delayed_cost"].sum(axis=1) * (
        1 + 1.8 * delayed_coverage_gap.mean(axis=1)
    )
    managed_infra_annual = regional["managed_cost"].sum(axis=1) * (
        1 + 0.8 * managed_coverage_gap.mean(axis=1)
    )

    delayed_empty_homes = np.clip(
        prices["delayed_stock"] - regional["delayed_hh"], 0, None
    ).sum(axis=1)
    managed_empty_homes = np.clip(
        prices["managed_stock"] - regional["managed_hh"], 0, None
    ).sum(axis=1)
    delayed_housing_annual = delayed_empty_homes * 12_000.0 / 1e9
    managed_housing_annual = managed_empty_homes * 5_000.0 / 1e9

    delayed_education_annual = (
        education["school_cost_delayed"] + education["university_cost_delayed"]
    ) / 1e9
    managed_education_annual = (
        education["school_cost_managed"] + education["university_cost_managed"]
    ) / 1e9

    adaptation_managed = np.zeros(len(YEARS))
    for year, amount in ((2031, 2.5), (2036, 5.0), (2041, 3.5), (2046, 2.0)):
        adaptation_managed[YEARS == year] = amount
    adaptation_delayed = np.zeros(len(YEARS))
    for year, amount in ((2051, 2.5), (2061, 4.0), (2071, 3.0)):
        adaptation_delayed[YEARS == year] = amount

    delayed = {
        "Infrastructure": present_value(delayed_infra_annual),
        "Education": present_value(delayed_education_annual),
        "Vacancy and decline": present_value(delayed_housing_annual),
        "Late emergency works": present_value(adaptation_delayed),
    }
    managed = {
        "Infrastructure": present_value(managed_infra_annual),
        "Education": present_value(managed_education_annual),
        "Vacancy and decline": present_value(managed_housing_annual),
        "Early adaptation": present_value(adaptation_managed),
    }
    return {"delayed": delayed, "managed": managed}


def make_results() -> dict:
    household_cases = {
        "reconsolidation": household_path(CENTRAL_POP_DECLINE, 3.00),
        "stable_size": household_path(CENTRAL_POP_DECLINE, HOUSEHOLD_SIZE_0),
        "moderate_fragmentation": household_path(CENTRAL_POP_DECLINE, 2.45),
        "strong_fragmentation": household_path(CENTRAL_POP_DECLINE, 2.15),
    }
    central_households = household_cases["strong_fragmentation"]
    housing_delayed, housing_managed = housing_stock_paths(central_households)
    regional = regional_paths()
    education = education_paths()
    prices = housing_price_indices(regional)
    costs = strategy_costs(regional, education, prices)

    threshold_years = {
        ZONE_NAMES[z]: first_year_below(regional["delayed_coverage"][:, z], 0.90)
        for z in range(4)
    }

    def arr(values: np.ndarray, digits: int = 3) -> list[float]:
        return [round(float(v), digits) for v in values]

    return {
        "study": "How to Shrink a Country Without Breaking It",
        "prices": "constant 2026 rand",
        "years": [int(y) for y in YEARS],
        "core_assumptions": {
            "population_2026": POPULATION_0,
            "household_size_2026": HOUSEHOLD_SIZE_0,
            "households_2026": HOUSEHOLDS_0,
            "habitable_homes_2026": HABITABLE_HOMES_0,
            "central_annual_population_change": CENTRAL_POP_DECLINE,
            "strong_fragmentation_household_size_2076": 2.15,
            "school_capacity": 1100,
            "discount_rate": 0.03,
        },
        "population": arr(population_path(CENTRAL_POP_DECLINE), 0),
        "household_cases": {key: arr(value, 0) for key, value in household_cases.items()},
        "housing": {
            "delayed_stock": arr(housing_delayed, 0),
            "managed_stock": arr(housing_managed, 0),
            "central_households": arr(central_households, 0),
        },
        "regional": {
            "zones": ZONE_NAMES,
            "delayed_population": regional["delayed_pop"].round(0).tolist(),
            "managed_population": regional["managed_pop"].round(0).tolist(),
            "delayed_households": regional["delayed_hh"].round(0).tolist(),
            "managed_households": regional["managed_hh"].round(0).tolist(),
            "delayed_coverage": regional["delayed_coverage"].round(3).tolist(),
            "managed_coverage": regional["managed_coverage"].round(3).tolist(),
            "first_year_below_90pct": threshold_years,
            "delayed_price_index": prices["delayed_price"].round(1).tolist(),
            "managed_price_index": prices["managed_price"].round(1).tolist(),
        },
        "education": {
            "learners": arr(education["learners"], 0),
            "schools_delayed": arr(education["schools_delayed"], 0),
            "schools_managed": arr(education["schools_managed"], 0),
            "school_util_delayed": arr(education["school_util_delayed"], 3),
            "school_util_managed": arr(education["school_util_managed"], 3),
            "school_cost_per_learner_delayed": arr(
                education["school_cost_per_learner_delayed"], 0
            ),
            "school_cost_per_learner_managed": arr(
                education["school_cost_per_learner_managed"], 0
            ),
            "university_students": arr(education["university_students"], 0),
        },
        "strategy_costs_pv_bn": costs,
        "warnings": [
            "The city-region is hypothetical and is not a forecast for Gauteng or any municipality.",
            "Household-size, migration and regional location paths are declared scenarios.",
            "Municipal, school, university and housing cost relationships are teaching assumptions.",
            "Price indices show relative directional pressure, not appraisals or investable forecasts.",
        ],
    }


def make_figures(data: dict) -> None:
    set_plot_style()
    years = np.array(data["years"])
    population = np.array(data["population"], dtype=float)

    # Figure 1: population and household count.
    fig, ax = plt.subplots(figsize=(10.6, 5.5))
    figure_header(
        fig, "Figure 1", "A smaller population can still form more households",
        "Hypothetical city-region; all series indexed to 2026 = 100; population falls 0.5 percent a year."
    )
    pop_index = population / population[0] * 100
    ax.plot(years, pop_index, color=BLACK, linestyle="--", marker="s",
            markevery=10, linewidth=2.0,
            label="Population / households if size stays 2.86")
    line_specs = [
        ("moderate_fragmentation", GREY_700, "-.", "^", "Households: size falls to 2.45"),
        ("strong_fragmentation", CORAL, "-", "o", "Households: size falls to 2.15"),
    ]
    for key, color, linestyle, marker, label in line_specs:
        values = np.array(data["household_cases"][key], dtype=float)
        ax.plot(years, values / values[0] * 100, color=color, linestyle=linestyle,
                marker=marker, markevery=10, linewidth=2.0, label=label)
    ax.axhline(100, color=GREY_300, linewidth=0.8)
    ax.set_xlabel("Year")
    ax.set_ylabel("Index, 2026 = 100")
    ax.set_xlim(years[0], years[-1])
    style_axis(ax)
    ax.legend(loc="lower left", frameon=False, ncol=2)
    fig.subplots_adjust(left=0.09, right=0.97, bottom=0.14, top=0.74)
    save_figure(fig, "population-households.png")

    # Figure 2: contraction map.
    fig, ax = plt.subplots(figsize=(10.6, 5.7))
    figure_header(
        fig, "Figure 2", "Housing demand depends on people per home, not people alone",
        "Change in household count after 50 years across population and household-size scenarios."
    )
    rates = np.linspace(-0.015, 0.005, 121)
    end_sizes = np.linspace(1.8, 3.2, 99)
    change = np.zeros((len(end_sizes), len(rates)))
    for i, end_size in enumerate(end_sizes):
        final_pop = POPULATION_0 * ((1 + rates) ** 50)
        final_hh = final_pop / end_size
        change[i] = (final_hh / HOUSEHOLDS_0 - 1) * 100
    cmap = mcolors.LinearSegmentedColormap.from_list(
        "greyscienx_div", [GREY_700, GREY_100, WHITE, CORAL]
    )
    mesh = ax.pcolormesh(rates * 100, end_sizes, change, cmap=cmap, shading="auto",
                         vmin=-45, vmax=45)
    contour = ax.contour(rates * 100, end_sizes, change, levels=[0], colors=[BLACK], linewidths=1.8)
    ax.clabel(contour, fmt={0: "no change in households"}, fontsize=8, inline=True)
    ax.scatter([CENTRAL_POP_DECLINE * 100], [2.15], s=70, color=CORAL,
               edgecolor=BLACK, linewidth=0.8, zorder=4)
    ax.annotate("central case", xy=(CENTRAL_POP_DECLINE * 100, 2.15),
                xytext=(-0.18, 1.98), arrowprops={"arrowstyle": "-", "color": BLACK},
                fontsize=8)
    ax.set_xlabel("Annual population change")
    ax.set_ylabel("Average household size in 2076")
    ax.set_xticks([-1.5, -1.0, -0.5, 0.0, 0.5], ["-1.5%", "-1.0%", "-0.5%", "0%", "+0.5%"])
    cbar = fig.colorbar(mesh, ax=ax, pad=0.02)
    cbar.set_label("Change in households by 2076")
    cbar.set_ticks([-40, -20, 0, 20, 40])
    cbar.set_ticklabels(["-40%", "-20%", "0%", "+20%", "+40%"])
    fig.subplots_adjust(left=0.10, right=0.91, bottom=0.15, top=0.72)
    save_figure(fig, "contraction-map.png")

    # Figure 3: housing shortage despite population decline.
    fig, ax = plt.subplots(figsize=(10.6, 5.5))
    figure_header(
        fig, "Figure 3", "Housing can become scarce while the city loses people",
        "Strong household fragmentation; habitable stock erodes faster when adjustment and maintenance are delayed."
    )
    households = np.array(data["housing"]["central_households"]) / 1_000
    delayed = np.array(data["housing"]["delayed_stock"]) / 1_000
    managed = np.array(data["housing"]["managed_stock"]) / 1_000
    ax.plot(years, households, color=CORAL, linewidth=2.4, marker="o", markevery=10,
            label="Households needing homes")
    ax.plot(years, delayed, color=BLACK, linewidth=2.1, linestyle="--", marker="s",
            markevery=10, label="Habitable homes: delayed")
    ax.plot(years, managed, color=GREY_500, linewidth=2.1, linestyle=":", marker="D",
            markevery=10, label="Habitable homes: managed")
    ax.fill_between(years, delayed, households, where=households > delayed,
                    color=CORAL, alpha=0.22, label="Shortfall")
    ax.set_xlabel("Year")
    ax.set_ylabel("Homes or households, thousands")
    ax.set_xlim(years[0], years[-1])
    style_axis(ax)
    ax.legend(loc="upper left", frameon=False, ncol=2)
    fig.subplots_adjust(left=0.10, right=0.97, bottom=0.14, top=0.72)
    save_figure(fig, "housing-shortfall.png")

    # Figure 4: regional municipal viability.
    fig, ax = plt.subplots(figsize=(10.6, 5.6))
    figure_header(
        fig, "Figure 4", "The satellite town fails first; the outer edge follows",
        "Maintenance revenue divided by modelled network operating cost under delayed adjustment; 0.90 is the warning line."
    )
    coverage = np.array(data["regional"]["delayed_coverage"])
    styles = [
        (CORAL, "-", "o"),
        (BLACK, "--", "s"),
        (GREY_700, "-.", "^"),
        (GREY_500, ":", "D"),
    ]
    for z, name in enumerate(ZONE_NAMES):
        color, linestyle, marker = styles[z]
        ax.plot(years, coverage[:, z], color=color, linestyle=linestyle,
                marker=marker, markevery=10, linewidth=2.0, label=name)
    ax.axhline(0.90, color=BLACK, linewidth=1.2, linestyle=":")
    ax.text(END_YEAR, 0.915, "90% warning threshold", ha="right", va="bottom", fontsize=8)
    ax.set_xlabel("Year")
    ax.set_ylabel("Revenue coverage of network cost")
    ax.set_xlim(years[0], years[-1])
    ax.set_ylim(0.35, 1.55)
    ax.set_yticks([0.4, 0.6, 0.8, 0.9, 1.0, 1.2, 1.4],
                  ["40%", "60%", "80%", "90%", "100%", "120%", "140%"])
    style_axis(ax)
    ax.legend(loc="upper right", frameon=False, ncol=2)
    fig.subplots_adjust(left=0.10, right=0.97, bottom=0.14, top=0.72)
    save_figure(fig, "regional-viability.png")

    # Figure 5: school adaptation.
    fig, axes = plt.subplots(1, 2, figsize=(10.6, 5.4))
    figure_header(
        fig, "Figure 5", "Empty classrooms are not free classrooms",
        "The learner population falls faster than the total population; managed mergers keep more schools near efficient scale."
    )
    util_delayed = np.array(data["education"]["school_util_delayed"]) * 100
    util_managed = np.array(data["education"]["school_util_managed"]) * 100
    cost_delayed = np.array(data["education"]["school_cost_per_learner_delayed"]) / 1_000
    cost_managed = np.array(data["education"]["school_cost_per_learner_managed"]) / 1_000
    axes[0].plot(years, util_delayed, color=BLACK, linestyle="--", linewidth=2.0,
                 marker="s", markevery=10, label="Delayed")
    axes[0].plot(years, util_managed, color=CORAL, linestyle="-", linewidth=2.2,
                 marker="o", markevery=10, label="Managed")
    axes[0].axhline(65, color=GREY_500, linestyle=":", linewidth=1.1)
    axes[0].set_title("School-seat use")
    axes[0].set_xlabel("Year")
    axes[0].set_ylabel("Occupied capacity")
    axes[0].set_ylim(35, 95)
    axes[0].set_yticks([40, 50, 60, 65, 70, 80, 90], ["40%", "50%", "60%", "65%", "70%", "80%", "90%"])
    axes[0].legend(frameon=False, loc="lower left")
    style_axis(axes[0])

    axes[1].plot(years, cost_delayed, color=BLACK, linestyle="--", linewidth=2.0,
                 marker="s", markevery=10, label="Delayed")
    axes[1].plot(years, cost_managed, color=CORAL, linestyle="-", linewidth=2.2,
                 marker="o", markevery=10, label="Managed")
    axes[1].set_title("Annual cost per learner")
    axes[1].set_xlabel("Year")
    axes[1].set_ylabel("R thousand, constant 2026 rand")
    axes[1].legend(frameon=False, loc="upper left")
    style_axis(axes[1])
    fig.subplots_adjust(left=0.08, right=0.97, bottom=0.15, top=0.69, wspace=0.27)
    save_figure(fig, "education-capacity.png")

    # Figure 6: strategy costs.
    fig, ax = plt.subplots(figsize=(10.6, 5.5))
    figure_header(
        fig, "Figure 6", "Managed shrinkage buys a smaller bill and a functioning city",
        "Fifty-year present value at 3 percent; constant 2026 rand; illustrative system costs."
    )
    delayed = data["strategy_costs_pv_bn"]["delayed"]
    managed = data["strategy_costs_pv_bn"]["managed"]
    delayed_order = ["Infrastructure", "Education", "Vacancy and decline", "Late emergency works"]
    managed_order = ["Infrastructure", "Education", "Vacancy and decline", "Early adaptation"]
    colors = [BLACK, GREY_500, GREY_300, CORAL]
    hatches = [None, "//", "..", "xx"]
    bottoms = [0.0, 0.0]
    for i in range(4):
        vals = [delayed[delayed_order[i]], managed[managed_order[i]]]
        ax.bar([0, 1], vals, bottom=bottoms, color=colors[i], width=0.58,
               hatch=hatches[i], edgecolor=BLACK if hatches[i] else colors[i],
               linewidth=0.5 if hatches[i] else 0,
               label=["Infrastructure", "Education", "Vacancy / decline", "Adaptation works"][i])
        bottoms = [bottoms[j] + vals[j] for j in range(2)]
    for x, total in enumerate(bottoms):
        ax.text(x, total + 2.0, f"R{total:.0f}bn", ha="center", fontsize=10, fontweight="bold")
    ax.set_xticks([0, 1], ["Delayed adjustment", "Managed shrinkage"])
    ax.set_ylabel("Present value, R billion")
    style_axis(ax)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.16), ncol=4, frameon=False)
    fig.subplots_adjust(left=0.10, right=0.97, bottom=0.25, top=0.72)
    save_figure(fig, "strategy-costs.png")


def main() -> None:
    WORK_DIR.mkdir(parents=True, exist_ok=True)
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    data = make_results()
    RESULTS_PATH.write_text(json.dumps(data, indent=2), encoding="utf-8")
    make_figures(data)

    start_pop = data["core_assumptions"]["population_2026"]
    end_pop = data["population"][-1]
    start_hh = data["core_assumptions"]["households_2026"]
    end_hh = data["household_cases"]["strong_fragmentation"][-1]
    delayed_total = sum(data["strategy_costs_pv_bn"]["delayed"].values())
    managed_total = sum(data["strategy_costs_pv_bn"]["managed"].values())
    display = {
        "population_change_pct": round((end_pop / start_pop - 1) * 100, 1),
        "household_change_pct": round((end_hh / start_hh - 1) * 100, 1),
        "delayed_housing_gap_2076": round(
            data["housing"]["central_households"][-1] - data["housing"]["delayed_stock"][-1]
        ),
        "first_below_90pct": data["regional"]["first_year_below_90pct"],
        "school_utilisation_2076_pct": {
            "delayed": round(data["education"]["school_util_delayed"][-1] * 100, 1),
            "managed": round(data["education"]["school_util_managed"][-1] * 100, 1),
        },
        "strategy_pv_bn": {
            "delayed": round(delayed_total, 1),
            "managed": round(managed_total, 1),
            "saving": round(delayed_total - managed_total, 1),
        },
        "price_index_2076": {
            "delayed": {
                zone: data["regional"]["delayed_price_index"][-1][i]
                for i, zone in enumerate(ZONE_NAMES)
            },
            "managed": {
                zone: data["regional"]["managed_price_index"][-1][i]
                for i, zone in enumerate(ZONE_NAMES)
            },
        },
    }
    print(json.dumps(display, indent=2))


if __name__ == "__main__":
    main()
