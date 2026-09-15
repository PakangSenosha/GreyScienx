"""GreyScienx simulator for an ageing-related fiscal emergency.

The model compares politically plausible mixes of taxes, pension reforms,
service reductions and borrowing. It closes a hypothetical R150 billion annual
gap in constant 2026 rand and distributes the modelled welfare loss among
workers, pensioners, children and future taxpayers. It is a transparent stress
test, not a forecast or official costing.
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import linprog


ROOT = Path(__file__).resolve().parents[1]
WORK_DIR = ROOT / "work" / "emergency-ageing-austerity"
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


GAP_BN = 150.0
GROUPS = ["Workers", "Pensioners", "Children", "Future taxpayers"]
TRANCHES = 5
WELFARE_CURVE = np.array([0.70, 0.85, 1.05, 1.35, 1.75])
POLITICAL_CURVE = np.array([0.76, 0.88, 1.00, 1.16, 1.38])


@dataclass(frozen=True)
class Intervention:
    key: str
    name: str
    policy_unit: str
    maximum: str
    mature_yield_bn: float
    first_year_share: float
    maturity_year: int
    welfare_cost: float
    political_cost: float
    burden: tuple[float, float, float, float]
    vulnerable_pensioner_share: float
    group: str


INTERVENTIONS = [
    Intervention("income_tax", "Worker income-tax surcharge", "+3 percentage points", "+3 pp", 100, 1.00, 1, 1.02, 1.25, (0.78, 0.05, 0.12, 0.05), 0.02, "Current taxes"),
    Intervention("consumption_tax", "Broad consumption-tax increase", "+2 percentage points", "+2 pp", 55, 1.00, 1, 1.28, 1.30, (0.45, 0.20, 0.25, 0.10), 0.18, "Current taxes"),
    Intervention("contributions", "Higher retirement contributions", "+4 percentage points", "+4 pp", 24, 0.10, 10, 0.48, 0.72, (0.85, 0.05, 0.08, 0.02), 0.02, "Pre-funding"),
    Intervention("retirement_age", "Raise pension and grant age", "+5 years", "+5 years", 55, 0.18, 6, 0.88, 1.70, (0.27, 0.63, 0.06, 0.04), 0.78, "Work longer"),
    Intervention("benefit_cut", "Reduce pension benefits", "-10 percent", "-10%", 36, 1.00, 1, 1.58, 2.15, (0.04, 0.91, 0.03, 0.02), 0.92, "Broad pension restraint"),
    Intervention("means_test", "Means-test affluent pensioners", "Top quarter targeted", "Top 25%", 30, 0.72, 2, 0.54, 1.32, (0.03, 0.93, 0.01, 0.03), 0.12, "Targeted pension measures"),
    Intervention("solidarity_tax", "Solidarity tax on high pensions", "+5 percentage points", "+5 pp", 18, 1.00, 1, 0.46, 0.82, (0.02, 0.95, 0.00, 0.03), 0.04, "Targeted pension measures"),
    Intervention("pension_wealth_tax", "Tax private pension wealth", "0.5 percent annually", "0.5%", 25, 0.85, 2, 0.66, 1.46, (0.05, 0.90, 0.00, 0.05), 0.05, "Targeted pension measures"),
    Intervention("indexation", "Index benefits below inflation", "3 points below CPI", "-3 pp", 28, 0.32, 5, 1.12, 1.02, (0.03, 0.92, 0.02, 0.03), 0.78, "Broad pension restraint"),
    Intervention("inflation", "Inflation surprise", "+5 percentage points", "+5 pp", 42, 1.00, 1, 1.82, 0.62, (0.43, 0.30, 0.16, 0.11), 0.62, "Broad pension restraint"),
    Intervention("health_cut", "Reduce age-related healthcare", "-10 percent", "-10%", 35, 1.00, 1, 2.05, 2.05, (0.20, 0.59, 0.16, 0.05), 0.88, "Service cuts"),
    Intervention("non_age_cut", "Cut non-age government spending", "-5 percent", "-5%", 80, 1.00, 1, 1.62, 0.78, (0.38, 0.06, 0.46, 0.10), 0.05, "Service cuts"),
    Intervention("borrowing", "Additional annual borrowing", "R75 billion", "R75bn", 75, 1.00, 1, 1.30, 0.32, (0.04, 0.01, 0.05, 0.90), 0.02, "Borrowing"),
]

INDEX = {item.key: index for index, item in enumerate(INTERVENTIONS)}


def tranche_arrays() -> dict[str, np.ndarray]:
    yields = []
    welfare = []
    politics = []
    groups = [[] for _ in GROUPS]
    vulnerable = []
    immediate = []
    for item in INTERVENTIONS:
        tranche_yield = item.mature_yield_bn / TRANCHES
        for tranche in range(TRANCHES):
            yields.append(tranche_yield)
            welfare_piece = tranche_yield * item.welfare_cost * WELFARE_CURVE[tranche]
            welfare.append(welfare_piece)
            politics.append(tranche_yield * item.political_cost * POLITICAL_CURVE[tranche])
            for group_index, share in enumerate(item.burden):
                groups[group_index].append(welfare_piece * share)
            vulnerable.append(welfare_piece * item.vulnerable_pensioner_share)
            immediate.append(tranche_yield * item.first_year_share)
    return {
        "yield": np.array(yields),
        "welfare": np.array(welfare),
        "politics": np.array(politics),
        "groups": np.array(groups),
        "vulnerable": np.array(vulnerable),
        "immediate": np.array(immediate),
    }


ARRAYS = tranche_arrays()


def lever_slice(key: str) -> slice:
    start = INDEX[key] * TRANCHES
    return slice(start, start + TRANCHES)


def solve_package(
    name: str,
    welfare_weight: float = 1.0,
    political_weight: float = 0.0,
    group_weights: tuple[float, float, float, float] = (0, 0, 0, 0),
    vulnerable_weight: float = 0.0,
    caps: dict[str, float] | None = None,
    immediate_floor: float | None = None,
) -> dict[str, object]:
    caps = caps or {}
    objective = welfare_weight * ARRAYS["welfare"] + political_weight * ARRAYS["politics"]
    for index, weight in enumerate(group_weights):
        objective = objective + weight * ARRAYS["groups"][index]
    objective = objective + vulnerable_weight * ARRAYS["vulnerable"]

    rows = [-ARRAYS["yield"]]
    rhs = [-GAP_BN]
    # Later tranches cannot be used before earlier ones.
    for intervention_index in range(len(INTERVENTIONS)):
        for tranche in range(TRANCHES - 1):
            row = np.zeros(len(objective))
            start = intervention_index * TRANCHES
            row[start + tranche + 1] = 1
            row[start + tranche] = -1
            rows.append(row)
            rhs.append(0.0)
    for key, cap in caps.items():
        row = np.zeros(len(objective))
        row[lever_slice(key)] = 1
        rows.append(row)
        rhs.append(TRANCHES * cap)
    if immediate_floor is not None:
        rows.append(-ARRAYS["immediate"])
        rhs.append(-immediate_floor)

    solution = linprog(
        objective,
        A_ub=np.array(rows),
        b_ub=np.array(rhs),
        bounds=[(0, 1)] * len(objective),
        method="highs",
    )
    if not solution.success:
        raise RuntimeError(f"Package {name} is infeasible: {solution.message}")
    x = np.clip(solution.x, 0, 1)
    levels = {
        item.key: float(x[lever_slice(item.key)].sum() / TRANCHES)
        for item in INTERVENTIONS
    }
    closure_by_intervention = {
        item.key: float(np.dot(x[lever_slice(item.key)], ARRAYS["yield"][lever_slice(item.key)]))
        for item in INTERVENTIONS
    }
    group_loss = ARRAYS["groups"] @ x
    welfare_loss = float(ARRAYS["welfare"] @ x)
    political_cost = float(ARRAYS["politics"] @ x)
    mature_closure = float(ARRAYS["yield"] @ x)
    first_year_closure = float(ARRAYS["immediate"] @ x)
    return {
        "name": name,
        "levels": levels,
        "closure_by_intervention": closure_by_intervention,
        "mature_closure_bn": mature_closure,
        "first_year_closure_bn": first_year_closure,
        "welfare_index": 100.0 * welfare_loss / GAP_BN,
        "political_resistance_index": 100.0 * political_cost / GAP_BN,
        "group_loss": {group: float(group_loss[i]) for i, group in enumerate(GROUPS)},
        "group_loss_share": {
            group: float(100 * group_loss[i] / group_loss.sum()) for i, group in enumerate(GROUPS)
        },
        "vulnerable_pensioner_loss": float(ARRAYS["vulnerable"] @ x),
    }


PACKAGE_CONFIGS = [
    {
        "name": "Balanced transition",
        "welfare_weight": 1.0,
        "political_weight": 0.15,
        "caps": {"borrowing": 0.20, "inflation": 0.0, "health_cut": 0.20, "non_age_cut": 0.30,
                 "benefit_cut": 0.45, "retirement_age": 0.60},
    },
    {
        "name": "Targeted solidarity",
        "welfare_weight": 1.0,
        "political_weight": 0.12,
        "vulnerable_weight": 1.8,
        "caps": {"income_tax": 0.45, "consumption_tax": 0.15, "borrowing": 0.15, "inflation": 0.0,
                 "health_cut": 0.10, "non_age_cut": 0.20, "benefit_cut": 0.20, "retirement_age": 0.35},
    },
    {
        "name": "Work-and-save transition",
        "welfare_weight": 0.85,
        "political_weight": 0.30,
        "caps": {"contributions": 1.0, "retirement_age": 1.0, "income_tax": 0.45,
                 "consumption_tax": 0.15, "benefit_cut": 0.15, "indexation": 0.25, "inflation": 0.0,
                 "health_cut": 0.10, "non_age_cut": 0.20, "borrowing": 0.12},
    },
    {
        "name": "Protect basic benefits",
        "welfare_weight": 1.0,
        "political_weight": 0.22,
        "vulnerable_weight": 3.0,
        "caps": {"benefit_cut": 0.0, "indexation": 0.0, "retirement_age": 0.15, "inflation": 0.0,
                 "health_cut": 0.0, "consumption_tax": 0.45, "non_age_cut": 0.35, "borrowing": 0.28},
    },
    {
        "name": "Low visible pain",
        "welfare_weight": 0.35,
        "political_weight": 1.65,
        "caps": {"borrowing": 0.70, "inflation": 0.55, "health_cut": 0.45,
                 "non_age_cut": 0.70, "benefit_cut": 0.45},
    },
]


def group_closure(package: dict[str, object]) -> dict[str, float]:
    closure = package["closure_by_intervention"]
    output: dict[str, float] = {}
    for item in INTERVENTIONS:
        output[item.group] = output.get(item.group, 0.0) + float(closure[item.key])
    return output


def annual_path(package: dict[str, object], years: int = 10) -> dict[str, list[float]]:
    closure = package["closure_by_intervention"]
    structural = []
    borrowing = []
    debt = []
    debt_stock = 0.0
    for year in range(1, years + 1):
        structural_closure = 0.0
        for item in INTERVENTIONS:
            if item.key == "borrowing":
                continue
            ramp = item.first_year_share
            if item.maturity_year > 1:
                ramp += (1.0 - item.first_year_share) * min(year - 1, item.maturity_year - 1) / (item.maturity_year - 1)
            else:
                ramp = 1.0
            structural_closure += float(closure[item.key]) * ramp
        annual_borrow = max(0.0, GAP_BN - structural_closure)
        debt_stock = debt_stock * 1.03 + annual_borrow
        structural.append(structural_closure)
        borrowing.append(annual_borrow)
        debt.append(debt_stock)
    return {"structural_closure": structural, "annual_borrowing": borrowing, "debt_stock": debt}


def frontier_points() -> list[dict[str, float]]:
    points = []
    generic_caps = {"borrowing": 0.50, "inflation": 0.50, "health_cut": 0.60, "non_age_cut": 0.70}
    for political_weight in np.linspace(0, 3.2, 41):
        package = solve_package(
            name=f"frontier-{political_weight:.2f}",
            welfare_weight=1.0,
            political_weight=float(political_weight),
            caps=generic_caps,
        )
        points.append(
            {
                "welfare_index": float(package["welfare_index"]),
                "political_resistance_index": float(package["political_resistance_index"]),
            }
        )
    unique = []
    seen = set()
    for point in points:
        key = (round(point["welfare_index"], 4), round(point["political_resistance_index"], 4))
        if key not in seen:
            unique.append(point)
            seen.add(key)
    return sorted(unique, key=lambda point: point["political_resistance_index"])


def make_figures(packages: list[dict[str, object]], frontier: list[dict[str, float]]) -> None:
    set_plot_style()

    # Figure 1: fiscal capacity and timing of each lever.
    fig, ax = plt.subplots(figsize=(10.6, 6.4))
    figure_header(
        fig, "Figure 1", "No single humane lever is large enough",
        "Maximum annual fiscal contribution under the study's policy bounds, in constant 2026 rand."
    )
    names = [item.name for item in INTERVENTIONS][::-1]
    mature = np.array([item.mature_yield_bn for item in INTERVENTIONS])[::-1]
    immediate = np.array([item.mature_yield_bn * item.first_year_share for item in INTERVENTIONS])[::-1]
    y = np.arange(len(names))
    ax.barh(y, mature, color=GREY_300, height=0.64, label="Mature annual effect")
    ax.barh(y, immediate, color=CORAL, height=0.36, label="First-year effect")
    for index, value in enumerate(mature):
        ax.text(value + 1.8, index, f"R{value:.0f}bn", va="center", ha="left", fontsize=8, color=BLACK)
    ax.set_yticks(y, names)
    ax.set_xlim(0, 112)
    ax.set_xlabel("Annual fiscal gap closed (R billion)")
    style_axis(ax, grid_axis="x")
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.22), ncol=2, frameon=False)
    fig.subplots_adjust(left=0.31, right=0.95, bottom=0.22, top=0.76)
    save_figure(fig, "intervention-capacity.png")

    # Figure 2: mature policy composition of each package.
    package_names = [p["name"] for p in packages]
    grouped = [group_closure(p) for p in packages]
    group_order = ["Current taxes", "Pre-funding", "Work longer", "Targeted pension measures",
                   "Broad pension restraint", "Service cuts", "Borrowing"]
    palette = [CORAL, BLACK, GREY_500, GREY_300, GREY_700, GREY_100, WHITE]
    hatches = [None, "//", "..", "xx", "\\\\", "++", "oo"]
    fig, ax = plt.subplots(figsize=(10.6, 5.4))
    figure_header(
        fig, "Figure 2", "Efficient packages combine instruments instead of maxing out one",
        "Mature annual contribution to the R150bn gap; borrowing is the portion never structurally closed."
    )
    left = np.zeros(len(packages))
    for index, group in enumerate(group_order):
        values = np.array([item.get(group, 0.0) for item in grouped])
        ax.barh(np.arange(len(packages)), values, left=left, color=palette[index], hatch=hatches[index],
                edgecolor=BLACK if index in (5, 6) else palette[index], linewidth=0.5,
                height=0.58, label=group)
        left += values
    ax.set_yticks(np.arange(len(packages)), package_names)
    ax.invert_yaxis()
    ax.set_xlim(0, 155)
    ax.set_xlabel("Annual gap closed (R billion)")
    style_axis(ax, grid_axis="x")
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.49), ncol=3, frameon=False)
    fig.subplots_adjust(left=0.24, right=0.96, bottom=0.36, top=0.74)
    save_figure(fig, "package-composition.png")

    # Figure 3: welfare burden distribution.
    fig, ax = plt.subplots(figsize=(10.6, 5.0))
    figure_header(
        fig, "Figure 3", "Every package protects someone by shifting cost to someone else",
        "Share of modelled welfare loss, not share of fiscal revenue raised."
    )
    colors = [CORAL, BLACK, GREY_500, GREY_300]
    left = np.zeros(len(packages))
    for index, group in enumerate(GROUPS):
        values = np.array([p["group_loss_share"][group] for p in packages])
        ax.barh(np.arange(len(packages)), values, left=left, color=colors[index], height=0.58, label=group)
        for row, value in enumerate(values):
            if value >= 10:
                label_color = WHITE if index in (0, 1, 2) else BLACK
                ax.text(left[row] + value / 2, row, f"{value:.0f}%", ha="center", va="center",
                        fontsize=8, fontweight="bold", color=label_color)
        left += values
    ax.set_yticks(np.arange(len(packages)), package_names)
    ax.invert_yaxis()
    ax.set_xlim(0, 100)
    ax.set_xlabel("Share of package welfare loss (%)")
    style_axis(ax, grid_axis="x")
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.27), ncol=4, frameon=False)
    fig.subplots_adjust(left=0.24, right=0.96, bottom=0.25, top=0.73)
    save_figure(fig, "distributional-incidence.png")

    # Figure 4: political-welfare frontier and named packages.
    fig, ax = plt.subplots(figsize=(10.6, 5.3))
    figure_header(
        fig, "Figure 4", "Political ease and social efficiency point in different directions",
        "Lower-left is better. The line traces optimal mixes as political resistance receives more weight."
    )
    fx = np.array([p["political_resistance_index"] for p in frontier])
    fy = np.array([p["welfare_index"] for p in frontier])
    ax.plot(fx, fy, color=GREY_500, linewidth=2.2, marker="o", markersize=3.5,
            label="Efficient frontier")
    for index, package in enumerate(packages):
        x = package["political_resistance_index"]
        yv = package["welfare_index"]
        ax.scatter([x], [yv], s=65, color=CORAL if index == 0 else BLACK,
                   marker="o" if index == 0 else "s", zorder=5)
        short_labels = ["Balanced", "Targeted solidarity", "Work-and-save", "Basic benefits", "Low visible pain"]
        offsets = [(8, -12), (8, 8), (-118, -1), (-106, 11), (8, 8)]
        ax.annotate(short_labels[index], (x, yv), xytext=offsets[index], textcoords="offset points",
                    fontsize=8, color=BLACK)
    all_x = np.concatenate([fx, np.array([p["political_resistance_index"] for p in packages])])
    all_y = np.concatenate([fy, np.array([p["welfare_index"] for p in packages])])
    ax.set_xlim(max(0, all_x.min() - 4), all_x.max() + 6)
    ax.set_ylim(max(0, all_y.min() - 5), all_y.max() + 7)
    ax.set_xlabel("Political resistance index")
    ax.set_ylabel("Total welfare-loss index")
    style_axis(ax)
    fig.subplots_adjust(left=0.10, right=0.96, bottom=0.15, top=0.73)
    save_figure(fig, "efficiency-frontier.png")

    # Figure 5: transition borrowing and debt stock.
    fig, axes = plt.subplots(1, 2, figsize=(10.6, 5.0))
    figure_header(
        fig, "Figure 5", "Slow reforms still need a financing bridge",
        "Structural closure ramps in; annual shortfalls are borrowed at a 3 percent real rate."
    )
    line_styles = ["-", "--", "-.", ":", (0, (5, 2, 1, 2))]
    colors = [CORAL, BLACK, GREY_500, GREY_700, GREY_300]
    years = np.arange(1, 11)
    for index, package in enumerate(packages):
        path = package["annual_path"]
        axes[0].plot(years, path["annual_borrowing"], color=colors[index], linestyle=line_styles[index],
                     linewidth=2.2, label=package["name"])
        axes[1].plot(years, path["debt_stock"], color=colors[index], linestyle=line_styles[index],
                     linewidth=2.2)
    axes[0].set_title("Annual bridge borrowing", fontsize=10, fontweight="bold")
    axes[1].set_title("Accumulated emergency debt", fontsize=10, fontweight="bold")
    axes[0].set_ylabel("R billion per year")
    axes[1].set_ylabel("R billion, constant 2026 rand")
    for ax in axes:
        ax.set_xlabel("Year of package")
        ax.set_xticks([1, 3, 5, 7, 10])
        style_axis(ax)
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", bbox_to_anchor=(0.5, -0.005), ncol=3, frameon=False)
    fig.subplots_adjust(left=0.09, right=0.97, bottom=0.22, top=0.72, wspace=0.20)
    save_figure(fig, "transition-borrowing.png")


def main() -> None:
    WORK_DIR.mkdir(parents=True, exist_ok=True)
    packages = [solve_package(**config) for config in PACKAGE_CONFIGS]
    for package in packages:
        package["annual_path"] = annual_path(package)
        package["grouped_closure"] = group_closure(package)
    frontier = frontier_points()
    payload = {
        "gap_bn": GAP_BN,
        "groups": GROUPS,
        "interventions": [asdict(item) for item in INTERVENTIONS],
        "packages": packages,
        "frontier": frontier,
        "notes": {
            "prices": "constant 2026 rand",
            "real_interest_rate": 0.03,
            "welfare_index": "Modelled welfare loss divided by the R150bn gap and multiplied by 100.",
            "political_index": "Modelled resistance cost divided by the R150bn gap and multiplied by 100.",
        },
    }
    RESULTS_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    make_figures(packages, frontier)
    summary = []
    for package in packages:
        summary.append(
            {
                "name": package["name"],
                "first_year_closure_bn": round(package["first_year_closure_bn"], 1),
                "welfare_index": round(package["welfare_index"], 1),
                "political_index": round(package["political_resistance_index"], 1),
                "year_10_debt_bn": round(package["annual_path"]["debt_stock"][-1], 1),
                "burden_share": {k: round(v, 1) for k, v in package["group_loss_share"].items()},
                "closure": {k: round(v, 1) for k, v in package["grouped_closure"].items()},
            }
        )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
