"""GreyScienx political-demographic model for an ageing electorate.

This is a transparent scenario model, not a forecast. It follows South Africa's
age structure from 2025 to 2100, converts adults into voters with the Electoral
Commission's 2024 age-turnout pattern, and maps the resulting electorate into
stylised spending preferences, austerity choices and youth support for the
welfare state.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
WORK_DIR = ROOT / "work" / "ageing-electorate"
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


YEARS = np.arange(2025, 2101)
AGES = np.arange(101)
RETIREMENT_AGE = 60

# Official 2024 turnout by age band from the Electoral Commission report.
TURNOUT_BANDS = [
    (18, 19, 0.45),
    (20, 29, 0.48),
    (30, 39, 0.49),
    (40, 49, 0.56),
    (50, 59, 0.66),
    (60, 69, 0.78),
    (70, 79, 0.82),
    (80, 100, 0.68),
]

PREFERENCE_BANDS = [
    (18, 29, np.array([18, 20, 28, 29, 5], dtype=float)),
    (30, 44, np.array([20, 22, 30, 23, 5], dtype=float)),
    (45, 59, np.array([28, 27, 24, 16, 5], dtype=float)),
    (60, 74, np.array([42, 32, 14, 7, 5], dtype=float)),
    (75, 100, np.array([47, 35, 9, 4, 5], dtype=float)),
]
CATEGORIES = ["Old-age income", "Health", "Education", "Housing and youth", "Other"]
BASELINE_ALLOCATION = np.array([24, 26, 27, 18, 5], dtype=float)

SCENARIOS = {
    "Renewal": {
        "tfr_end": 2.05,
        "tfr_year": 2070,
        "mortality_improvement": 0.18,
        "migration_per_thousand": 1.8,
    },
    "Baseline ageing": {
        "tfr_end": 1.70,
        "tfr_year": 2070,
        "mortality_improvement": 0.28,
        "migration_per_thousand": 0.6,
    },
    "Accelerated ageing": {
        "tfr_end": 1.30,
        "tfr_year": 2050,
        "mortality_improvement": 0.42,
        "migration_per_thousand": 0.0,
    },
}


def distribute(total: float, start: int, end: int, slope: float = 0.0) -> np.ndarray:
    count = end - start + 1
    weights = np.exp(np.linspace(-slope, slope, count))
    values = total * weights / weights.sum()
    out = np.zeros(101)
    out[start : end + 1] = values
    return out


def initial_population() -> np.ndarray:
    # Rounded 2025 calibration: 63.1m people and 6.6m aged 60 or older.
    pop = np.zeros(101)
    pop += distribute(19.3e6, 0, 17, slope=0.08)
    pop += distribute(12.8e6, 18, 29, slope=-0.03)
    pop += distribute(13.9e6, 30, 44, slope=-0.10)
    pop += distribute(10.4e6, 45, 59, slope=-0.20)
    pop += distribute(5.3e6, 60, 74, slope=-0.38)
    pop += distribute(1.3e6, 75, 100, slope=-1.15)
    return pop * (63.1e6 / pop.sum())


def base_mortality() -> np.ndarray:
    q = np.zeros(101)
    q[0] = 0.015
    q[1:15] = 0.00035
    q[15:30] = 0.0008
    q[30:45] = 0.0017
    q[45:60] = 0.0045
    q[60:70] = np.linspace(0.011, 0.022, 10)
    q[70:80] = np.linspace(0.027, 0.055, 10)
    q[80:90] = np.linspace(0.070, 0.145, 10)
    q[90:101] = np.linspace(0.175, 0.360, 11)
    return q


def turnout_by_age() -> np.ndarray:
    turnout = np.zeros(101)
    for start, end, rate in TURNOUT_BANDS:
        turnout[start : end + 1] = rate
    return turnout


BASE_TURNOUT = turnout_by_age()


def weighted_median_age(weights: np.ndarray, minimum_age: int = 18) -> float:
    local = weights.copy()
    local[:minimum_age] = 0
    total = local.sum()
    if total <= 0:
        return float("nan")
    cumulative = np.cumsum(local)
    return float(np.searchsorted(cumulative, total / 2))


def interpolate(start: float, end: float, year: int, end_year: int) -> float:
    share = np.clip((year - 2025) / max(1, end_year - 2025), 0.0, 1.0)
    return float(start + (end - start) * share)


def simulate_population(spec: dict[str, float]) -> np.ndarray:
    populations = np.zeros((len(YEARS), len(AGES)))
    populations[0] = initial_population()
    q0 = base_mortality()
    migration_weights = np.zeros(101)
    migration_weights[18:45] = np.exp(-((AGES[18:45] - 29) / 9.5) ** 2)
    migration_weights /= migration_weights.sum()

    for index, year in enumerate(YEARS[:-1]):
        pop = populations[index]
        mortality_improvement = interpolate(
            0.0, spec["mortality_improvement"], int(year), 2100
        )
        mortality = np.clip(q0 * (1.0 - mortality_improvement), 0.00015, 0.42)
        next_pop = np.zeros(101)
        next_pop[1:100] = pop[:99] * (1.0 - mortality[:99])
        next_pop[100] = pop[99] * (1.0 - mortality[99]) + pop[100] * (1.0 - mortality[100])

        tfr = interpolate(2.21, spec["tfr_end"], int(year), int(spec["tfr_year"]))
        women_20_39 = pop[20:40].sum() * 0.5
        births = women_20_39 * tfr / 20.0
        next_pop[0] = births * (1.0 - mortality[0])

        net_migration = pop.sum() * spec["migration_per_thousand"] / 1000.0
        next_pop += net_migration * migration_weights
        populations[index + 1] = next_pop
    return populations


def preference_by_age() -> np.ndarray:
    matrix = np.zeros((101, len(CATEGORIES)))
    for start, end, values in PREFERENCE_BANDS:
        matrix[start : end + 1] = values
    return matrix


PREFERENCES = preference_by_age()


def allocation_from_votes(pop: np.ndarray, turnout: np.ndarray) -> np.ndarray:
    votes = pop * turnout
    adult_votes = votes[18:].sum()
    preference = (votes[:, None] * PREFERENCES).sum(axis=0) / adult_votes
    responsiveness = 0.62
    allocation = (1.0 - responsiveness) * BASELINE_ALLOCATION + responsiveness * preference
    return allocation * (100.0 / allocation.sum())


def electorate_metrics(populations: np.ndarray, feedback: bool) -> dict[str, list[float]]:
    output = {
        "adult_median": [],
        "voter_median": [],
        "older_adult_share": [],
        "older_vote_share": [],
        "young_adult_share": [],
        "young_vote_share": [],
        "youth_support": [],
        "allocation": [],
    }
    support_state = 72.0
    for pop in populations:
        turnout = BASE_TURNOUT.copy()
        if feedback:
            youth_multiplier = np.clip(0.78 + 0.0030 * support_state, 0.84, 1.02)
            turnout[18:35] *= youth_multiplier
            turnout[60:] *= 1.035
            turnout = np.minimum(turnout, 0.90)

        votes = pop * turnout
        adults = pop[18:].sum()
        all_votes = votes[18:].sum()
        older_adult_share = pop[60:].sum() / adults
        older_vote_share = votes[60:].sum() / all_votes
        young_adult_share = pop[18:35].sum() / adults
        young_vote_share = votes[18:35].sum() / all_votes
        allocation = allocation_from_votes(pop, turnout)
        old_services = allocation[0] + 0.62 * allocation[1]
        support_target = 72.0 - 1.35 * max(0.0, old_services - 40.5) - 62.0 * max(
            0.0, 0.245 - young_vote_share
        )
        support_target = float(np.clip(support_target, 32.0, 78.0))
        support_state = 0.86 * support_state + 0.14 * support_target

        output["adult_median"].append(weighted_median_age(pop))
        output["voter_median"].append(weighted_median_age(votes))
        output["older_adult_share"].append(100 * older_adult_share)
        output["older_vote_share"].append(100 * older_vote_share)
        output["young_adult_share"].append(100 * young_adult_share)
        output["young_vote_share"].append(100 * young_vote_share)
        output["youth_support"].append(support_state)
        output["allocation"].append(allocation.tolist())
    return output


def first_year(condition: np.ndarray) -> int | None:
    indices = np.flatnonzero(condition)
    return int(YEARS[indices[0]]) if len(indices) else None


def austerity_cuts(allocation: np.ndarray, older_vote_share: float, young_vote_share: float) -> np.ndarray:
    older = older_vote_share / 100.0
    young = young_vote_share / 100.0
    protection = np.array(
        [
            min(0.96, 0.54 + 1.08 * older),
            min(0.90, 0.48 + 0.64 * older),
            min(0.82, 0.28 + 1.35 * young),
            min(0.72, 0.12 + 1.30 * young),
            0.18,
        ]
    )
    exposure = allocation * (1.0 - protection)
    return 10.0 * exposure / exposure.sum()


def make_figures(results: dict[str, dict[str, list[float]]]) -> None:
    set_plot_style()

    # Figure 1: the demographic median and the actual median voter.
    fig, axes = plt.subplots(1, 3, figsize=(10.6, 4.7), sharey=True)
    figure_header(
        fig, "Figure 1", "The median voter ages before the median adult",
        "Age-turnout differences amplify demographic ageing; the 60-year line marks a retired median voter."
    )
    for ax, scenario in zip(axes, SCENARIOS):
        data = results[scenario]["status_quo"]
        ax.plot(YEARS, data["adult_median"], color=GREY_500, linewidth=2.0, label="Median adult")
        ax.plot(YEARS, data["voter_median"], color=CORAL, linewidth=2.8, label="Median voter")
        ax.axhline(60, color=BLACK, linewidth=1.0, linestyle=(0, (4, 3)))
        ax.set_title(scenario, fontsize=10, fontweight="bold")
        ax.set_xlim(2025, 2100)
        ax.set_xticks([2025, 2050, 2075, 2100])
        ax.set_ylim(34, 64)
        ax.set_xlabel("Year")
        style_axis(ax)
    axes[0].set_ylabel("Age")
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=2, frameon=False, bbox_to_anchor=(0.5, 0.005))
    fig.subplots_adjust(left=0.07, right=0.97, bottom=0.19, top=0.74, wspace=0.16)
    save_figure(fig, "median-voter-age.png")

    # Figure 2: older and younger voting blocs under fixed and feedback turnout.
    scenario = "Baseline ageing"
    fig, axes = plt.subplots(1, 2, figsize=(10.6, 4.8), sharey=True)
    figure_header(
        fig, "Figure 2", "Older voters can overtake young adults without becoming a majority",
        "Share of votes cast by people aged 60+ and 18-34 in the baseline demographic path."
    )
    for ax, regime, title in zip(
        axes,
        ["status_quo", "feedback"],
        ["2024 turnout pattern held constant", "Political feedback lowers youth turnout"],
    ):
        data = results[scenario][regime]
        ax.plot(YEARS, data["older_vote_share"], color=CORAL, linewidth=2.8, label="Age 60+")
        ax.plot(YEARS, data["young_vote_share"], color=BLACK, linewidth=2.3, label="Age 18-34")
        cross = first_year(np.array(data["older_vote_share"]) >= np.array(data["young_vote_share"]))
        if cross is not None:
            y = np.interp(cross, YEARS, data["older_vote_share"])
            ax.scatter([cross], [y], s=45, facecolor=WHITE, edgecolor=CORAL, linewidth=1.7, zorder=5)
            ax.annotate(f"Crosses in {cross}", (cross, y), xytext=(6, 13), textcoords="offset points",
                        fontsize=8, color=BLACK)
        ax.set_title(title, fontsize=10, fontweight="bold")
        ax.set_xlim(2025, 2100)
        ax.set_xticks([2025, 2050, 2075, 2100])
        ax.set_ylim(5, 50)
        ax.set_xlabel("Year")
        style_axis(ax)
    axes[0].set_ylabel("Share of votes cast (%)")
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=2, frameon=False, bbox_to_anchor=(0.5, 0.005))
    fig.subplots_adjust(left=0.08, right=0.97, bottom=0.18, top=0.74, wspace=0.15)
    save_figure(fig, "voting-bloc-crossover.png")

    # Figure 3: budget allocation under three electorates.
    scenario = "Accelerated ageing"
    years_to_plot = [2025, 2050, 2075, 2100]
    positions = [int(np.where(YEARS == year)[0][0]) for year in years_to_plot]
    allocation = np.array(results[scenario]["feedback"]["allocation"])[positions]
    colors = [CORAL, BLACK, GREY_500, GREY_300, GREY_100]
    fig, ax = plt.subplots(figsize=(10.6, 4.9))
    figure_header(
        fig, "Figure 3", "A decisive older bloc changes priorities gradually, then persistently",
        "Modelled allocation of each R100 in the accelerated-ageing feedback case."
    )
    left = np.zeros(len(years_to_plot))
    for index, category in enumerate(CATEGORIES):
        ax.barh(range(len(years_to_plot)), allocation[:, index], left=left,
                color=colors[index], height=0.55, label=category)
        for row, value in enumerate(allocation[:, index]):
            if value >= 8:
                label_color = WHITE if index in (0, 1) else BLACK
                ax.text(left[row] + value / 2, row, f"{value:.0f}", ha="center", va="center",
                        color=label_color, fontsize=8, fontweight="bold")
        left += allocation[:, index]
    ax.set_yticks(range(len(years_to_plot)), [str(y) for y in years_to_plot])
    ax.invert_yaxis()
    ax.set_xlim(0, 100)
    ax.set_xlabel("Allocation per R100")
    ax.set_ylabel("Year")
    style_axis(ax, grid_axis="x")
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.38), ncol=3, frameon=False)
    fig.subplots_adjust(left=0.10, right=0.97, bottom=0.28, top=0.73)
    save_figure(fig, "political-budget-allocation.png")

    # Figure 4: distribution of a R10 austerity package.
    data = results[scenario]["feedback"]
    cuts = []
    for index in positions:
        cuts.append(
            austerity_cuts(
                np.array(data["allocation"][index]),
                data["older_vote_share"][index],
                data["young_vote_share"][index],
            )
        )
    cuts = np.array(cuts)
    fig, ax = plt.subplots(figsize=(10.6, 5.0))
    figure_header(
        fig, "Figure 4", "Austerity follows the path of least electoral resistance",
        "Who absorbs a R10 consolidation when protection rises with voting power."
    )
    x = np.arange(len(years_to_plot))
    bottom = np.zeros(len(years_to_plot))
    for index, category in enumerate(CATEGORIES):
        ax.bar(x, cuts[:, index], bottom=bottom, color=colors[index], width=0.62, label=category)
        for row, value in enumerate(cuts[:, index]):
            if value >= 1.2:
                label_color = WHITE if index in (0, 1) else BLACK
                ax.text(row, bottom[row] + value / 2, f"{value:.1f}", ha="center", va="center",
                        color=label_color, fontsize=8, fontweight="bold")
        bottom += cuts[:, index]
    ax.set_xticks(x, [str(y) for y in years_to_plot])
    ax.set_ylim(0, 10)
    ax.set_xlabel("Year")
    ax.set_ylabel("Share of R10 cut")
    style_axis(ax)
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.38), ncol=3, frameon=False)
    fig.subplots_adjust(left=0.09, right=0.97, bottom=0.29, top=0.73)
    save_figure(fig, "austerity-incidence.png")

    # Figure 5: the feedback loop as three linked trajectories.
    fig, axes = plt.subplots(3, 1, figsize=(10.6, 7.2), sharex=True)
    figure_header(
        fig, "Figure 5", "The gerontocracy risk is a feedback loop, not an age threshold",
        "Baseline ageing with fixed turnout compared with the stylised political-feedback case."
    )
    status = results["Baseline ageing"]["status_quo"]
    feedback = results["Baseline ageing"]["feedback"]
    panels = [
        ("older_vote_share", "Age 60+ vote (%)"),
        (None, "Older-focused allocation\n(R per R100)"),
        ("youth_support", "Youth support index\n(0-100)"),
    ]
    for row, (key, ylabel) in enumerate(panels):
        ax = axes[row]
        if key is None:
            status_values = np.array(status["allocation"])[:, 0] + np.array(status["allocation"])[:, 1]
            feedback_values = np.array(feedback["allocation"])[:, 0] + np.array(feedback["allocation"])[:, 1]
        else:
            status_values = np.array(status[key])
            feedback_values = np.array(feedback[key])
        ax.plot(YEARS, status_values, color=GREY_500, linewidth=2.0,
                label="Fixed turnout" if row == 0 else None)
        ax.plot(YEARS, feedback_values, color=CORAL, linewidth=2.7,
                label="Political feedback" if row == 0 else None)
        ax.set_ylabel(ylabel)
        style_axis(ax)
    axes[-1].set_xlabel("Year")
    axes[-1].set_xticks([2025, 2050, 2075, 2100])
    axes[0].legend(loc="upper left", ncol=2, frameon=False)
    fig.subplots_adjust(left=0.12, right=0.97, bottom=0.10, top=0.78, hspace=0.28)
    save_figure(fig, "fiscal-gerontocracy-feedback.png")


def main() -> None:
    WORK_DIR.mkdir(parents=True, exist_ok=True)
    results: dict[str, dict[str, list[float]]] = {}
    summary: dict[str, dict[str, object]] = {}
    for scenario, spec in SCENARIOS.items():
        populations = simulate_population(spec)
        status = electorate_metrics(populations, feedback=False)
        feedback = electorate_metrics(populations, feedback=True)
        results[scenario] = {"status_quo": status, "feedback": feedback}
        summary[scenario] = {}
        for regime, data in results[scenario].items():
            older = np.array(data["older_vote_share"])
            young = np.array(data["young_vote_share"])
            median = np.array(data["voter_median"])
            summary[scenario][regime] = {
                "older_overtakes_young": first_year(older >= young),
                "median_voter_reaches_60": first_year(median >= 60),
                "metrics_2025": {key: value[0] for key, value in data.items() if key != "allocation"},
                "metrics_2100": {key: value[-1] for key, value in data.items() if key != "allocation"},
                "allocation_2025": data["allocation"][0],
                "allocation_2100": data["allocation"][-1],
            }

    payload = {
        "assumptions": {
            "retirement_age": RETIREMENT_AGE,
            "initial_population_millions": round(initial_population().sum() / 1e6, 3),
            "initial_age_60_plus_millions": round(initial_population()[60:].sum() / 1e6, 3),
            "turnout_bands": TURNOUT_BANDS,
            "baseline_allocation": BASELINE_ALLOCATION.tolist(),
            "categories": CATEGORIES,
            "scenarios": SCENARIOS,
        },
        "summary": summary,
        "results": results,
    }
    RESULTS_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    make_figures(results)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
