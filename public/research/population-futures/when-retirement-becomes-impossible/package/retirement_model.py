"""Stylized retirement sustainability model and GreyScienx figures.

All monetary values are expressed in constant 2026 rand. The model is a
transparent scenario engine, not a forecast of South Africa or any pension
fund. It links an individual funded account to a steady-state pay-as-you-go
population model so that financial and demographic pressure can be compared
without presenting equations in the publication.
"""

from __future__ import annotations

import json
import math
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
WORK_DIR = ROOT / "work" / "retirement"
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
    if not CSS_PATH.exists():
        return defaults
    text = CSS_PATH.read_text(encoding="utf-8")
    for key in list(defaults):
        match = re.search(rf"--{re.escape(key)}\s*:\s*(#[0-9a-fA-F]{{6}})", text)
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
        except TypeError:
            try:
                configure_matplotlib()
                configured = True
            except Exception:
                pass
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
            "axes.grid": True,
            "grid.color": GREY_300,
            "grid.linewidth": 0.6,
            "axes.spines.top": False,
                "axes.spines.right": False,
            }
        )
    plt.rcParams["axes.unicode_minus"] = False


def figure_header(fig: plt.Figure, field: str, title: str, subtitle: str) -> None:
    fig.add_artist(
        plt.Line2D([0.065, 0.965], [0.955, 0.955], transform=fig.transFigure,
                   color=CORAL, linewidth=4.0, solid_capstyle="butt")
    )
    fig.text(0.065, 0.917, field.upper(), color=CORAL, fontsize=8.5,
             fontweight="bold", ha="left", va="top")
    fig.text(0.065, 0.875, title, color=BLACK, fontsize=17,
             fontweight="bold", ha="left", va="top")
    fig.text(0.065, 0.825, subtitle, color=GREY_700, fontsize=8.5,
             ha="left", va="top")


def save_figure(fig: plt.Figure, name: str) -> Path:
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    path = ASSET_DIR / name
    fig.savefig(path, dpi=280, bbox_inches="tight", facecolor=WHITE)
    plt.close(fig)
    return path


def style_axis(ax: plt.Axes) -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(BLACK)
    ax.spines["bottom"].set_color(BLACK)
    ax.grid(axis="y", color=GREY_300, linewidth=0.6)
    ax.grid(axis="x", visible=False)
    ax.set_axisbelow(True)


@dataclass(frozen=True)
class FundedScenario:
    name: str
    retirement_age: int
    longevity: int
    contribution_rate: float
    real_return: float
    productivity_growth: float
    replacement_rate: float
    benefit_indexation: float


def funded_path(
    scenario: FundedScenario,
    start_age: int = 25,
    starting_monthly_salary: float = 30_000.0,
) -> dict:
    balance = 0.0
    annual_salary = starting_monthly_salary * 12.0
    final_salary = None
    depletion_age = None
    ages: list[int] = []
    balances: list[float] = []
    withdrawals: list[float] = []

    for age in range(start_age, scenario.longevity + 1):
        balance *= 1.0 + scenario.real_return
        withdrawal = 0.0
        if age < scenario.retirement_age:
            balance += annual_salary * scenario.contribution_rate
            if age == scenario.retirement_age - 1:
                final_salary = annual_salary
            annual_salary *= 1.0 + scenario.productivity_growth
        else:
            if final_salary is None:
                final_salary = annual_salary
            years_retired = age - scenario.retirement_age
            withdrawal = (
                final_salary
                * scenario.replacement_rate
                * (1.0 + scenario.benefit_indexation) ** years_retired
            )
            balance -= withdrawal
            if balance < 0 and depletion_age is None:
                depletion_age = age

        ages.append(age)
        balances.append(balance)
        withdrawals.append(withdrawal)

    return {
        "scenario": asdict(scenario),
        "ages": ages,
        "balances": balances,
        "withdrawals": withdrawals,
        "depletion_age": depletion_age,
        "final_balance": balances[-1],
        "balance_at_retirement": balances[scenario.retirement_age - start_age - 1],
        "final_annual_salary": final_salary,
        "first_year_pension": (final_salary or 0.0) * scenario.replacement_rate,
    }


def supported_replacement_rate(
    retirement_age: int,
    longevity: int,
    contribution_rate: float,
    real_return: float,
    productivity_growth: float = 0.015,
    benefit_indexation: float = 0.0,
    start_age: int = 25,
    starting_monthly_salary: float = 30_000.0,
) -> float:
    annual_salary = starting_monthly_salary * 12.0
    balance = 0.0
    for age in range(start_age, retirement_age):
        balance *= 1.0 + real_return
        balance += annual_salary * contribution_rate
        if age < retirement_age - 1:
            annual_salary *= 1.0 + productivity_growth
    final_salary = annual_salary
    discount_sum = 0.0
    years_retired = longevity - retirement_age + 1
    for year in range(years_retired):
        discount_sum += (1.0 + benefit_indexation) ** year / (1.0 + real_return) ** (year + 1)
    if final_salary <= 0 or discount_sum <= 0:
        return 0.0
    return max(0.0, balance / (final_salary * discount_sum))


def stable_population(tfr: float, longevity: int, years: int = 260) -> np.ndarray:
    """Return a stylized stable age distribution with rectangular survival."""
    max_age = 111
    population = np.zeros(max_age, dtype=float)
    population[: min(longevity, max_age)] = 1.0
    population /= population.sum()

    for _ in range(years):
        births = population[20:40].sum() * 0.5 * tfr / 20.0
        next_population = np.zeros_like(population)
        next_population[0] = births
        upper = min(longevity, max_age)
        next_population[1:upper] = population[: upper - 1]
        total = next_population.sum()
        if total > 0:
            population = next_population / total
    return population


def payg_metrics(
    retirement_age: int,
    longevity: int,
    tfr: float,
    productivity_growth: float = 0.015,
    public_replacement_rate: float = 0.40,
    contributor_coverage: float = 0.80,
    wage_indexed: bool = False,
) -> dict:
    population = stable_population(tfr, longevity)
    workers = population[20:retirement_age].sum()
    retiree_ages = np.arange(retirement_age, min(longevity, len(population)))
    retirees_by_age = population[retirement_age: min(longevity, len(population))]
    retirees = retirees_by_age.sum()
    contributors = workers * contributor_coverage

    if wage_indexed:
        relative_benefit = np.ones_like(retirees_by_age)
    else:
        years_since_retirement = retiree_ages - retirement_age
        relative_benefit = 1.0 / (1.0 + productivity_growth) ** years_since_retirement
    benefit_bill = public_replacement_rate * np.sum(retirees_by_age * relative_benefit)
    tax_rate = benefit_bill / contributors if contributors > 0 else math.inf
    dependency_ratio = retirees / workers if workers > 0 else math.inf
    workers_per_retiree = workers / retirees if retirees > 0 else math.inf
    max_dependency_at_20pct = (
        0.20 * contributor_coverage / public_replacement_rate
        if wage_indexed
        else None
    )
    return {
        "workers_share": workers,
        "retirees_share": retirees,
        "contributors_share": contributors,
        "workers_per_retiree": workers_per_retiree,
        "dependency_ratio": dependency_ratio,
        "required_payroll_rate": tax_rate,
        "max_dependency_at_20pct": max_dependency_at_20pct,
    }


def required_retirement_age(
    longevity: int,
    tfr: float,
    productivity_growth: float,
    public_replacement_rate: float,
    contributor_coverage: float,
    ceiling: float = 0.20,
    wage_indexed: bool = False,
) -> int | None:
    for retirement_age in range(55, 81):
        metric = payg_metrics(
            retirement_age,
            longevity,
            tfr,
            productivity_growth,
            public_replacement_rate,
            contributor_coverage,
            wage_indexed,
        )
        if metric["required_payroll_rate"] <= ceiling:
            return retirement_age
    return None


def fmt_rand(value: float) -> str:
    sign = "-" if value < 0 else ""
    return f"{sign}R{abs(value) / 1_000_000:.1f}m"


def build_funded_paths_figure(paths: list[dict]) -> Path:
    fig, ax = plt.subplots(figsize=(8.1, 4.15))
    fig.subplots_adjust(left=0.12, right=0.965, bottom=0.17, top=0.73)
    figure_header(
        fig,
        "Funded account",
        "A 60 percent pension promise can outlive the pot",
        "Balance after each year's saving or withdrawal, constant 2026 rand; negative values are funding shortfalls.",
    )
    encodings = [
        (CORAL, "-", "o"),
        (TRUE_BLACK, "--", "s"),
        (GREY_500, ":", "D"),
        (CORAL, "-.", "^"),
    ]
    for result, (color, linestyle, marker) in zip(paths, encodings):
        ages = np.array(result["ages"])
        balances = np.array(result["balances"]) / 1_000_000.0
        label = result["scenario"]["name"]
        mark_every = max(1, len(ages) // 9)
        ax.plot(
            ages,
            balances,
            color=color,
            linestyle=linestyle,
            linewidth=2.1,
            marker=marker,
            markersize=4.3,
            markevery=mark_every,
            label=label,
        )
    ax.axhline(0, color=BLACK, linewidth=1.1)
    ax.axvline(60, color=GREY_300, linewidth=0.9)
    ax.text(60.5, ax.get_ylim()[1] * 0.92, "age 60", color=GREY_700, fontsize=8)
    ax.set_xlabel("Age")
    ax.set_ylabel("Fund balance (R million)")
    style_axis(ax)
    ax.legend(loc="lower left", frameon=False, ncol=2, fontsize=8.0)
    return save_figure(fig, "funded-account-paths.png")


def build_funded_map_figure() -> tuple[Path, list[list[float]]]:
    contribution_rates = [0.06, 0.09, 0.12, 0.15, 0.18, 0.21, 0.24, 0.27, 0.30]
    returns = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06]
    values = np.array(
        [
            [
                supported_replacement_rate(60, 90, contribution, ret, 0.015, 0.0)
                for contribution in contribution_rates
            ]
            for ret in returns
        ]
    )
    cmap = mcolors.LinearSegmentedColormap.from_list(
        "greyscienx", [WHITE, GREY_100, GREY_300, CORAL, TRUE_BLACK]
    )
    norm = mcolors.Normalize(vmin=0.15, vmax=0.75)
    fig, ax = plt.subplots(figsize=(8.1, 4.25))
    fig.subplots_adjust(left=0.12, right=0.92, bottom=0.18, top=0.70)
    figure_header(
        fig,
        "Sustainability map A",
        "What retirement at 60 can actually replace",
        "Maximum lifelong pension as a share of final salary; retire at 60, live to 90, price-indexed benefits.",
    )
    im = ax.imshow(values, cmap=cmap, norm=norm, aspect="auto", origin="lower")
    ax.set_xticks(np.arange(len(contribution_rates)), [f"{x:.0%}" for x in contribution_rates])
    ax.set_yticks(np.arange(len(returns)), [f"{x:.0%}" for x in returns])
    ax.set_xlabel("Contribution rate of salary")
    ax.set_ylabel("Net real investment return")
    for row in range(values.shape[0]):
        for col in range(values.shape[1]):
            value = values[row, col]
            color = WHITE if value >= 0.52 else BLACK
            ax.text(col, row, f"{value:.0%}", ha="center", va="center", color=color, fontsize=7.7,
                    fontweight="bold" if value >= 0.60 else "normal")
    cbar = fig.colorbar(im, ax=ax, fraction=0.045, pad=0.035)
    cbar.set_label("Sustainable replacement rate")
    cbar.ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{x:.0%}"))
    ax.tick_params(length=0)
    return save_figure(fig, "funded-replacement-map.png"), values.tolist()


def build_payg_map_figure() -> tuple[Path, dict[str, list[list[float]]]]:
    retirement_ages = [60, 65, 70, 75]
    longevities = [80, 85, 90, 95, 100]
    fertility_levels = [1.3, 1.7, 2.1]
    matrices: dict[str, list[list[float]]] = {}
    cmap = mcolors.LinearSegmentedColormap.from_list(
        "greyscienx_tax", [WHITE, GREY_100, GREY_300, CORAL, TRUE_BLACK]
    )
    norm = mcolors.Normalize(vmin=0.08, vmax=0.50)
    fig, axes = plt.subplots(1, 3, figsize=(8.2, 4.9), sharey=True)
    fig.subplots_adjust(left=0.085, right=0.94, bottom=0.17, top=0.70, wspace=0.16)
    figure_header(
        fig,
        "Sustainability map B",
        "Low fertility turns a long retirement into a payroll problem",
        "Required pension-only payroll rate for a 40 percent public benefit; 80 percent contributor coverage, 1.5 percent productivity, price indexation.",
    )
    for ax, fertility in zip(axes, fertility_levels):
        matrix = np.array(
            [
                [
                    payg_metrics(retirement, longevity, fertility)["required_payroll_rate"]
                    for retirement in retirement_ages
                ]
                for longevity in longevities
            ]
        )
        matrices[f"tfr_{fertility:.1f}"] = matrix.tolist()
        ax.imshow(matrix, cmap=cmap, norm=norm, aspect="auto", origin="lower")
        ax.set_title(f"Fertility {fertility:.1f}", fontsize=10.5, fontweight="bold", pad=8)
        ax.set_xticks(np.arange(len(retirement_ages)), retirement_ages)
        ax.set_xlabel("Retirement age")
        ax.set_yticks(np.arange(len(longevities)), longevities)
        ax.tick_params(length=0)
        for row in range(matrix.shape[0]):
            for col in range(matrix.shape[1]):
                value = matrix[row, col]
                text_color = WHITE if value >= 0.36 else BLACK
                ax.text(col, row, f"{value:.0%}", ha="center", va="center",
                        color=text_color, fontsize=7.7,
                        fontweight="bold" if value <= 0.20 else "normal")
    axes[0].set_ylabel("Longevity assumption (age)")
    cbar_ax = fig.add_axes([0.952, 0.17, 0.018, 0.53])
    colorbar = fig.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=cmap), cax=cbar_ax)
    colorbar.set_label("Required rate")
    colorbar.ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{x:.0%}"))
    return save_figure(fig, "public-pension-sustainability-map.png"), matrices


def build_indexation_figure() -> tuple[Path, dict[str, list[float]]]:
    growth_rates = np.array([0.0, 0.005, 0.01, 0.015, 0.02, 0.025])
    price_rates = np.array(
        [payg_metrics(60, 95, 1.7, g, wage_indexed=False)["required_payroll_rate"] for g in growth_rates]
    )
    wage_rates = np.array(
        [payg_metrics(60, 95, 1.7, g, wage_indexed=True)["required_payroll_rate"] for g in growth_rates]
    )
    fig, ax = plt.subplots(figsize=(8.1, 3.9))
    fig.subplots_adjust(left=0.12, right=0.965, bottom=0.19, top=0.68)
    figure_header(
        fig,
        "Indexation",
        "Productivity helps only when benefits do not chase wages",
        "Required pension-only payroll rate; retire at 60, longevity 95, fertility 1.7, 40 percent initial benefit.",
    )
    ax.plot(growth_rates * 100, price_rates * 100, color=CORAL, linewidth=2.2,
            marker="o", markersize=5, label="Benefits rise with prices")
    ax.plot(growth_rates * 100, wage_rates * 100, color=TRUE_BLACK, linewidth=2.0,
            linestyle="--", marker="s", markersize=4.5, label="Benefits rise with wages")
    ax.axhline(20, color=GREY_500, linewidth=1.0, linestyle=":")
    ax.text(growth_rates[-1] * 100, 20.5, "20% policy ceiling", color=GREY_700,
            fontsize=8, ha="right")
    ax.set_xlabel("Real productivity growth per year (%)")
    ax.set_ylabel("Required payroll rate (%)")
    ax.set_xticks(growth_rates * 100, [f"{g:.1f}" for g in growth_rates * 100])
    style_axis(ax)
    ax.legend(frameon=False, loc="lower left")
    return save_figure(fig, "indexation-productivity.png"), {
        "growth_rates": growth_rates.tolist(),
        "price_indexed_rates": price_rates.tolist(),
        "wage_indexed_rates": wage_rates.tolist(),
    }


def build_occupation_figure() -> tuple[Path, dict[str, int | None]]:
    longevities = np.arange(80, 101, 5)
    required = [
        required_retirement_age(
            int(longevity), 1.7, 0.015, 0.40, 0.80, 0.20, wage_indexed=False
        )
        for longevity in longevities
    ]
    plotted = [value if value is not None else 81 for value in required]
    fig, ax = plt.subplots(figsize=(8.1, 3.9))
    fig.subplots_adjust(left=0.12, right=0.965, bottom=0.19, top=0.68)
    figure_header(
        fig,
        "Healthspan and work",
        "A uniform pension age can be fiscally neat and physically unfair",
        "Minimum retirement age needed to keep the modeled payroll rate at or below 20 percent; fertility 1.7, price-indexed benefit.",
    )
    ax.plot(longevities, plotted, color=CORAL, linewidth=2.3, marker="o", markersize=5.0,
            label="Fiscal retirement age")
    occupation_lines = [
        (60, "Heavy physical work: hypothetical feasible limit 60", TRUE_BLACK, "--"),
        (65, "Mixed or frontline work: hypothetical limit 65", GREY_500, ":"),
        (70, "Desk or knowledge work: hypothetical limit 70", BLACK, "-."),
    ]
    for level, label, color, line in occupation_lines:
        ax.axhline(level, color=color, linewidth=1.2, linestyle=line, label=label)
    ax.set_xlabel("Longevity assumption (age)")
    ax.set_ylabel("Retirement age")
    ax.set_xticks(longevities)
    ax.set_ylim(55, 82)
    style_axis(ax)
    ax.legend(frameon=False, loc="upper left", fontsize=7.7)
    return save_figure(fig, "occupation-healthspan-frontier.png"), {
        str(int(longevity)): value for longevity, value in zip(longevities, required)
    }


def run() -> None:
    set_plot_style()
    WORK_DIR.mkdir(parents=True, exist_ok=True)
    ASSET_DIR.mkdir(parents=True, exist_ok=True)

    scenarios = [
        FundedScenario("Favourable", 65, 85, 0.18, 0.05, 0.015, 0.60, 0.0),
        FundedScenario("Middle", 65, 90, 0.15, 0.03, 0.015, 0.60, 0.0),
        FundedScenario("Retire at 60", 60, 90, 0.12, 0.03, 0.015, 0.60, 0.0),
        FundedScenario("Adverse", 60, 100, 0.08, 0.01, 0.005, 0.60, 0.005),
    ]
    paths = [funded_path(scenario) for scenario in scenarios]
    funded_paths_path = build_funded_paths_figure(paths)
    funded_map_path, funded_map = build_funded_map_figure()
    payg_map_path, payg_map = build_payg_map_figure()
    indexation_path, indexation = build_indexation_figure()
    occupation_path, occupation = build_occupation_figure()

    focal_public = {}
    for label, retirement, longevity, fertility in [
        ("short_retirement", 65, 85, 2.1),
        ("ageing_squeeze", 60, 95, 1.7),
        ("century_life", 60, 100, 1.3),
        ("reformed_century_life", 70, 100, 1.3),
    ]:
        focal_public[label] = payg_metrics(retirement, longevity, fertility)

    results = {
        "model_label": "Stylized scenario model, constant 2026 rand",
        "starting_monthly_salary": 30_000,
        "funded_scenarios": paths,
        "funded_replacement_map": funded_map,
        "public_sustainability_map": payg_map,
        "indexation": indexation,
        "occupation_frontier": occupation,
        "focal_public_scenarios": focal_public,
        "figures": {
            "funded_paths": str(funded_paths_path),
            "funded_map": str(funded_map_path),
            "payg_map": str(payg_map_path),
            "indexation": str(indexation_path),
            "occupation": str(occupation_path),
        },
    }
    RESULTS_PATH.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(json.dumps({
        "results": str(RESULTS_PATH),
        "figures": results["figures"],
        "funded_summary": [
            {
                "name": p["scenario"]["name"],
                "depletion_age": p["depletion_age"],
                "retirement_balance": round(p["balance_at_retirement"]),
                "final_balance": round(p["final_balance"]),
            }
            for p in paths
        ],
        "public_summary": {
            k: {
                "workers_per_retiree": round(v["workers_per_retiree"], 2),
                "required_payroll_rate": round(v["required_payroll_rate"], 4),
            }
            for k, v in focal_public.items()
        },
        "occupation_frontier": occupation,
    }, indent=2))


if __name__ == "__main__":
    run()
