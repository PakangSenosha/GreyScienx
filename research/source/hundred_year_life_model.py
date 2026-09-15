"""GreyScienx armchair model for a 100-120 year life.

The model compares a conventional three-stage life with extended and multi-stage
alternatives. It tests work, recurring education, pension funding, long mortgages,
marriage duration and multigenerational care. It is a transparent scenario model,
not a forecast or recommendation. All money is constant 2026 rand.
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
WORK_DIR = ROOT / "work" / "hundred-year-life"
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


REAL_DISCOUNT = 0.03
REAL_WAGE_GROWTH = 0.012
START_MONTHLY_SALARY = 30_000
START_ANNUAL_SALARY = START_MONTHLY_SALARY * 12
TAX_SHARE = 0.25
PENSION_CONTRIBUTION = 0.15
PENSION_RETURN = 0.04


@dataclass(frozen=True)
class Stage:
    start: int
    end: int
    kind: str
    label: str
    work_fraction: float = 0.0


@dataclass(frozen=True)
class LifeDesign:
    key: str
    name: str
    stages: tuple[Stage, ...]


DESIGNS = [
    LifeDesign(
        "conventional", "Conventional three-stage",
        (
            Stage(20, 22, "Education", "University"),
            Stage(23, 64, "Full work", "One career", 1.0),
            Stage(65, 120, "Retirement", "Full retirement"),
        ),
    ),
    LifeDesign(
        "long_career", "Long career",
        (
            Stage(20, 22, "Education", "University"),
            Stage(23, 44, "Full work", "Career 1", 1.0),
            Stage(45, 45, "Education", "Retrain"),
            Stage(46, 69, "Full work", "Career 2", 1.0),
            Stage(70, 70, "Education", "Retrain"),
            Stage(71, 84, "Full work", "Career 3", 1.0),
            Stage(85, 94, "Phased work", "Half-time", 0.5),
            Stage(95, 120, "Retirement", "Retirement"),
        ),
    ),
    LifeDesign(
        "multi_stage", "Multi-stage life",
        (
            Stage(20, 24, "Education", "University"),
            Stage(25, 39, "Full work", "Career 1", 1.0),
            Stage(40, 42, "Education", "University at 40"),
            Stage(43, 59, "Full work", "Career 2", 1.0),
            Stage(60, 62, "Break", "Care / reset"),
            Stage(63, 64, "Education", "University at 60"),
            Stage(65, 79, "Full work", "Career 3", 1.0),
            Stage(80, 81, "Education", "University at 80"),
            Stage(82, 89, "Full work", "Career 4", 0.8),
            Stage(90, 99, "Phased work", "Portfolio work", 0.4),
            Stage(100, 120, "Retirement", "Late retirement"),
        ),
    ),
    LifeDesign(
        "portfolio", "Portfolio life",
        (
            Stage(20, 22, "Education", "University"),
            Stage(23, 34, "Full work", "Career 1", 1.0),
            Stage(35, 37, "Break", "Family / travel"),
            Stage(38, 54, "Full work", "Career 2", 1.0),
            Stage(55, 56, "Education", "Retrain"),
            Stage(57, 74, "Full work", "Career 3", 1.0),
            Stage(75, 99, "Phased work", "Flexible work", 0.5),
            Stage(100, 120, "Retirement", "Late retirement"),
        ),
    ),
]


def stage_at(design: LifeDesign, age: int) -> Stage | None:
    for stage in design.stages:
        if stage.start <= age <= stage.end:
            return stage
    return None


def skill_multiplier(design: LifeDesign, age: int) -> float:
    training_ends = [stage.end for stage in design.stages if stage.kind == "Education" and stage.end <= age]
    retraining_count = max(0, len(training_ends) - 1)
    boost = 1.0 + 0.10 * retraining_count
    last_training = max(training_ends) if training_ends else 22
    years_since = max(0, age - last_training - 12)
    decay = 0.992 ** years_since
    return boost * decay


def age_capacity(age: int) -> float:
    if age <= 69:
        return 1.0
    if age <= 84:
        return 1.0 - 0.010 * (age - 69)
    return max(0.55, 0.85 - 0.018 * (age - 84))


def annual_salary(design: LifeDesign, age: int) -> float:
    stage = stage_at(design, age)
    if stage is None or stage.work_fraction <= 0:
        return 0.0
    base = START_ANNUAL_SALARY * ((1 + REAL_WAGE_GROWTH) ** max(0, age - 25))
    return base * stage.work_fraction * skill_multiplier(design, age) * age_capacity(age)


def life_account(design: LifeDesign, death_age: int) -> dict[str, float]:
    pv_earnings = 0.0
    pv_taxes = 0.0
    pv_public = 0.0
    work_equivalent = 0.0
    education_years = 0.0
    break_years = 0.0
    retirement_years = 0.0
    for age in range(20, death_age):
        stage = stage_at(design, age)
        salary = annual_salary(design, age)
        discount = 1 / ((1 + REAL_DISCOUNT) ** (age - 20))
        pv_earnings += salary * discount
        pv_taxes += salary * TAX_SHARE * discount
        public_cost = 25_000
        if stage and stage.kind == "Education":
            public_cost += 72_000
            education_years += 1
        elif stage and stage.kind == "Break":
            public_cost += 18_000
            break_years += 1
        elif stage and stage.kind == "Retirement":
            public_cost += 58_000
            retirement_years += 1
        if stage:
            work_equivalent += stage.work_fraction
        pv_public += public_cost * discount
    return {
        "death_age": death_age,
        "work_equivalent_years": work_equivalent,
        "education_years": education_years,
        "break_years": break_years,
        "retirement_years": retirement_years,
        "pv_earnings": pv_earnings,
        "pv_taxes": pv_taxes,
        "pv_public_cost": pv_public,
        "net_fiscal": pv_taxes - pv_public,
    }


def pension_balance(retirement_age: int) -> tuple[float, float]:
    balance = 0.0
    final_salary = START_ANNUAL_SALARY
    for age in range(25, retirement_age):
        salary = START_ANNUAL_SALARY * ((1 + REAL_WAGE_GROWTH) ** (age - 25))
        balance = balance * (1 + PENSION_RETURN) + salary * PENSION_CONTRIBUTION
        final_salary = salary
    return balance, final_salary


def annuity_factor(years: int, rate: float) -> float:
    if years <= 0:
        return 0.0
    return (1 - (1 + rate) ** (-years)) / rate


def pension_matrix() -> dict[str, dict[str, float | None]]:
    output: dict[str, dict[str, float | None]] = {}
    for retirement_age in (65, 75, 85, 95):
        balance, final_salary = pension_balance(retirement_age)
        row: dict[str, float | None] = {}
        for death_age in (85, 100, 120):
            years = death_age - retirement_age
            if years <= 0:
                row[str(death_age)] = None
            else:
                required = 0.70 * final_salary * annuity_factor(years, 0.03)
                row[str(death_age)] = balance / required
        output[str(retirement_age)] = row
    return output


def retraining_return(training_age: int, work_end_age: int) -> dict[str, float]:
    wage = START_ANNUAL_SALARY * ((1 + REAL_WAGE_GROWTH) ** (training_age - 25))
    direct_cost = 2 * 120_000
    foregone_earnings = 2 * wage * 0.65
    total_cost = direct_cost + foregone_earnings
    benefit = 0.0
    payback = None
    cumulative = -total_cost
    for year, age in enumerate(range(training_age + 2, work_end_age), start=2):
        capacity = age_capacity(age)
        annual_gain = wage * 0.22 * ((1 + REAL_WAGE_GROWTH) ** (age - training_age)) * capacity
        discounted_gain = annual_gain / ((1 + 0.04) ** year)
        benefit += discounted_gain
        cumulative += discounted_gain
        if payback is None and cumulative >= 0:
            payback = year
    return {
        "training_age": training_age,
        "work_end_age": work_end_age,
        "total_cost": total_cost,
        "benefit": benefit,
        "net_value": benefit - total_cost,
        "payback_years": payback if payback is not None else -1,
    }


def mortgage_case(term_years: int) -> dict[str, float]:
    house_price = 1_800_000
    principal = house_price * 0.90
    monthly_rate = 0.035 / 12
    periods = term_years * 12
    payment = principal * monthly_rate / (1 - (1 + monthly_rate) ** (-periods))

    def balance_after(years: int) -> float:
        paid_periods = min(periods, years * 12)
        if paid_periods >= periods:
            return 0.0
        return principal * (1 + monthly_rate) ** paid_periods - payment * (
            ((1 + monthly_rate) ** paid_periods - 1) / monthly_rate
        )

    return {
        "term_years": term_years,
        "monthly_payment": payment,
        "total_interest": payment * periods - principal,
        "balance_age_65": balance_after(40),
        "balance_age_85": balance_after(60),
    }


def marriage_survival(years: int) -> float:
    probability = 1.0
    for year in range(1, years + 1):
        hazard = 0.020 if year <= 10 else 0.012
        probability *= 1 - hazard
    return probability


def adult_generations(lifespan: int, generation_gap: int) -> int:
    ages = [lifespan - generation_gap * index for index in range(8)]
    return sum(age >= 20 for age in ages)


def make_figures(
    accounts: dict[str, dict[str, dict[str, float]]],
    pensions: dict[str, dict[str, float | None]],
    retraining: list[dict[str, float]],
    mortgages: list[dict[str, float]],
) -> None:
    set_plot_style()

    stage_colors = {
        "Education": CORAL,
        "Full work": BLACK,
        "Phased work": GREY_500,
        "Break": GREY_300,
        "Retirement": GREY_100,
    }
    stage_hatches = {
        "Education": None,
        "Full work": None,
        "Phased work": "//",
        "Break": "xx",
        "Retirement": "..",
    }

    # Figure 1: life-course timelines.
    fig, ax = plt.subplots(figsize=(10.6, 5.3))
    figure_header(
        fig, "Figure 1", "A longer life needs more stages, not one longer retirement",
        "Illustrative lives from age 20 to 120; work intensity is encoded by fill and hatch."
    )
    for row, design in enumerate(DESIGNS):
        for stage in design.stages:
            width = stage.end - stage.start + 1
            ax.barh(row, width, left=stage.start, height=0.58,
                    color=stage_colors[stage.kind], hatch=stage_hatches[stage.kind],
                    edgecolor=BLACK if stage.kind in ("Break", "Retirement") else stage_colors[stage.kind],
                    linewidth=0.5)
            if width >= 8:
                label_color = WHITE if stage.kind == "Full work" else BLACK
                ax.text(stage.start + width / 2, row, stage.label, ha="center", va="center",
                        fontsize=7.5, color=label_color)
    ax.set_yticks(np.arange(len(DESIGNS)), [d.name for d in DESIGNS])
    ax.invert_yaxis()
    ax.set_xlim(20, 121)
    ax.set_xticks(np.arange(20, 121, 10))
    ax.set_xlabel("Age")
    style_axis(ax, grid_axis="x")
    handles = [plt.Rectangle((0, 0), 1, 1, facecolor=stage_colors[k], hatch=stage_hatches[k],
                             edgecolor=BLACK if k in ("Break", "Retirement") else stage_colors[k])
               for k in stage_colors]
    ax.legend(handles, list(stage_colors), loc="lower center", bbox_to_anchor=(0.5, -0.31),
              ncol=5, frameon=False)
    fig.subplots_adjust(left=0.23, right=0.97, bottom=0.25, top=0.72)
    save_figure(fig, "life-course-timelines.png")

    # Figure 2: time allocation at death age 120.
    fig, ax = plt.subplots(figsize=(10.6, 5.2))
    figure_header(
        fig, "Figure 2", "The conventional design turns longevity into dependency",
        "Adult years from 20 to 120; work is full-time-equivalent and breaks exclude formal education."
    )
    names = [d.name for d in DESIGNS]
    vals = accounts["120"]
    education = np.array([vals[d.key]["education_years"] for d in DESIGNS])
    work = np.array([vals[d.key]["work_equivalent_years"] for d in DESIGNS])
    breaks = np.array([vals[d.key]["break_years"] for d in DESIGNS])
    residual = 100 - education - work - breaks
    y = np.arange(len(names))
    left = np.zeros(len(names))
    for label, values, color, hatch in [
        ("Education", education, CORAL, None),
        ("Work-equivalent", work, BLACK, None),
        ("Breaks", breaks, GREY_300, "xx"),
        ("Retirement / non-work", residual, GREY_100, ".."),
    ]:
        ax.barh(y, values, left=left, height=0.58, color=color, hatch=hatch,
                edgecolor=BLACK if label in ("Breaks", "Retirement / non-work") else color,
                linewidth=0.5, label=label)
        left += values
    for idx, value in enumerate(work):
        ax.text(education[idx] + value / 2, idx, f"{value:.0f} work-years", ha="center", va="center",
                fontsize=8, color=WHITE)
    ax.set_yticks(y, names)
    ax.invert_yaxis()
    ax.set_xlim(0, 100)
    ax.set_xlabel("Years between ages 20 and 120")
    style_axis(ax, grid_axis="x")
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.28), ncol=4, frameon=False)
    fig.subplots_adjust(left=0.23, right=0.97, bottom=0.24, top=0.72)
    save_figure(fig, "adult-time-allocation.png")

    # Figure 3: retraining economics.
    fig, ax = plt.subplots(figsize=(10.6, 5.2))
    figure_header(
        fig, "Figure 3", "University at 80 works only when useful work remains",
        "Present value at the training age; two study years, a 22 percent earnings uplift and a 4 percent discount rate."
    )
    ages = [item["training_age"] for item in retraining]
    costs = np.array([item["total_cost"] for item in retraining]) / 1e6
    benefits = np.array([item["benefit"] for item in retraining]) / 1e6
    x = np.arange(len(ages))
    width = 0.34
    ax.bar(x - width / 2, costs, width, color=GREY_300, label="Study and foregone earnings")
    ax.bar(x + width / 2, benefits, width, color=CORAL, label="Later earnings gain")
    for idx, item in enumerate(retraining):
        net = item["net_value"] / 1e6
        payback = int(item["payback_years"])
        label = f"Net R{net:+.2f}m"
        if payback > 0:
            label += f" | payback {payback}y"
        else:
            label += " | no payback"
        ax.text(idx, max(costs[idx], benefits[idx]) + 0.08, label, ha="center", fontsize=8, color=BLACK)
    ax.set_xticks(x, [f"Retrain at {age}" for age in ages])
    ax.set_ylabel("R million, present value")
    style_axis(ax)
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.24), ncol=2, frameon=False)
    fig.subplots_adjust(left=0.09, right=0.97, bottom=0.21, top=0.72)
    save_figure(fig, "retraining-returns.png")

    # Figure 4: pension adequacy matrix.
    retirement_ages = [65, 75, 85, 95]
    death_ages = [85, 100, 120]
    matrix = np.full((len(retirement_ages), len(death_ages)), np.nan)
    for i, retirement_age in enumerate(retirement_ages):
        for j, death_age in enumerate(death_ages):
            value = pensions[str(retirement_age)][str(death_age)]
            matrix[i, j] = np.nan if value is None else value
    fig, ax = plt.subplots(figsize=(9.2, 5.4))
    figure_header(
        fig, "Figure 4", "A pension age of 65 does not finance a 120-year life",
        "Funded ratio for a steady worker saving 15 percent; 100 percent funds 70 percent of final pay until death."
    )
    masked = np.ma.masked_invalid(matrix)
    cmap = plt.matplotlib.colors.ListedColormap([GREY_100, GREY_300, CORAL, BLACK])
    bounds = [0, 0.6, 0.9, 1.2, 10]
    norm = plt.matplotlib.colors.BoundaryNorm(bounds, cmap.N)
    ax.imshow(masked, cmap=cmap, norm=norm, aspect="auto")
    for i, retirement_age in enumerate(retirement_ages):
        for j, death_age in enumerate(death_ages):
            value = matrix[i, j]
            if np.isnan(value):
                label = "Not applicable"
                color = GREY_500
            else:
                label = f"{100 * value:.0f}% funded"
                color = WHITE if value >= 1.2 else BLACK
            ax.text(j, i, label, ha="center", va="center", color=color, fontsize=10,
                    fontweight="bold")
    ax.set_xticks(np.arange(len(death_ages)), [f"Lives to {age}" for age in death_ages])
    ax.set_yticks(np.arange(len(retirement_ages)), [f"Retires at {age}" for age in retirement_ages])
    ax.set_xlabel("Longevity scenario")
    ax.set_ylabel("Retirement age")
    ax.grid(False)
    for spine in ax.spines.values():
        spine.set_visible(False)
    fig.subplots_adjust(left=0.18, right=0.96, bottom=0.15, top=0.72)
    save_figure(fig, "pension-adequacy-map.png")

    # Figure 5: mortgage trade-offs.
    fig, axes = plt.subplots(1, 2, figsize=(10.6, 5.2))
    figure_header(
        fig, "Figure 5", "A 60-year mortgage lowers the instalment and lengthens the trap",
        "R1.8m home, 10 percent deposit and 3.5 percent real interest; loan begins at age 25."
    )
    terms = [item["term_years"] for item in mortgages]
    payments = np.array([item["monthly_payment"] for item in mortgages]) / 1000
    interest = np.array([item["total_interest"] for item in mortgages]) / 1e6
    debt65 = np.array([item["balance_age_65"] for item in mortgages]) / 1e6
    x = np.arange(len(terms))
    axes[0].bar(x, payments, color=[CORAL, GREY_500, BLACK], width=0.58)
    for idx, value in enumerate(payments):
        axes[0].text(idx, value + 0.18, f"R{value:.1f}k", ha="center", fontsize=8)
    axes[0].set_title("Monthly payment", fontsize=10, fontweight="bold")
    axes[0].set_ylabel("R thousand per month")
    axes[1].bar(x - 0.17, interest, width=0.34, color=CORAL, label="Total real interest")
    axes[1].bar(x + 0.17, debt65, width=0.34, color=GREY_500, label="Debt remaining at 65")
    axes[1].set_title("Lifetime price of patience", fontsize=10, fontweight="bold")
    axes[1].set_ylabel("R million")
    for ax in axes:
        ax.set_xticks(x, [f"{term}-year" for term in terms])
        ax.set_xlabel("Mortgage term")
        style_axis(ax)
    axes[1].legend(loc="lower center", bbox_to_anchor=(0.5, -0.28), ncol=2, frameon=False)
    fig.subplots_adjust(left=0.08, right=0.97, bottom=0.22, top=0.71, wspace=0.23)
    save_figure(fig, "mortgage-tradeoffs.png")

    # Figure 6: care ages and overlapping generations.
    fig, axes = plt.subplots(1, 2, figsize=(10.6, 5.2))
    figure_header(
        fig, "Figure 6", "Longevity makes old age a relationship between old people",
        "Caregiver ages are mechanical examples; generation counts require all listed generations to be alive."
    )
    parent_ages = np.array([90, 100, 110])
    for birth_age, color, marker, style in [(25, CORAL, "o", "-"), (35, BLACK, "s", "--")]:
        child_ages = parent_ages - birth_age
        axes[0].plot(parent_ages, child_ages, color=color, marker=marker, linestyle=style,
                     linewidth=2.2, label=f"Parenthood at {birth_age}")
        for xval, yval in zip(parent_ages, child_ages):
            axes[0].text(xval + 0.7, yval, f"child {yval}", va="center", fontsize=8)
    axes[0].set_title("Age of the caregiving child", fontsize=10, fontweight="bold")
    axes[0].set_xlabel("Age of extremely old parent")
    axes[0].set_ylabel("Age of adult child")
    axes[0].set_xticks(parent_ages)
    style_axis(axes[0])
    axes[0].legend(loc="lower center", bbox_to_anchor=(0.5, -0.28), ncol=2, frameon=False)

    lifespans = [85, 100, 120]
    gap25 = [adult_generations(age, 25) for age in lifespans]
    gap32 = [adult_generations(age, 32) for age in lifespans]
    x = np.arange(len(lifespans))
    axes[1].bar(x - 0.17, gap25, width=0.34, color=CORAL, label="25-year generation gap")
    axes[1].bar(x + 0.17, gap32, width=0.34, color=GREY_500, label="32-year generation gap")
    for idx, value in enumerate(gap25):
        axes[1].text(idx - 0.17, value + 0.08, str(value), ha="center", fontsize=8)
    for idx, value in enumerate(gap32):
        axes[1].text(idx + 0.17, value + 0.08, str(value), ha="center", fontsize=8)
    axes[1].set_title("Adult generations alive together", fontsize=10, fontweight="bold")
    axes[1].set_xticks(x, [f"Life to {age}" for age in lifespans])
    axes[1].set_ylabel("Adult generations")
    axes[1].set_ylim(0, 5.7)
    style_axis(axes[1])
    axes[1].legend(loc="lower center", bbox_to_anchor=(0.5, -0.28), ncol=1, frameon=False)
    fig.subplots_adjust(left=0.08, right=0.97, bottom=0.23, top=0.71, wspace=0.24)
    save_figure(fig, "care-and-generations.png")


def main() -> None:
    WORK_DIR.mkdir(parents=True, exist_ok=True)
    accounts = {
        str(death_age): {design.key: life_account(design, death_age) for design in DESIGNS}
        for death_age in (85, 100, 120)
    }
    pensions = pension_matrix()
    retraining = [retraining_return(age, 95) for age in (40, 60, 80)]
    mortgages = [mortgage_case(term) for term in (20, 40, 60)]
    marriages = {str(years): marriage_survival(years) for years in (20, 40, 60, 80, 90)}
    generations = {
        str(lifespan): {str(gap): adult_generations(lifespan, gap) for gap in (25, 32)}
        for lifespan in (85, 100, 120)
    }
    payload = {
        "study": "The Hundred-Year Life",
        "prices": "constant 2026 rand",
        "core_assumptions": {
            "start_monthly_salary": START_MONTHLY_SALARY,
            "real_wage_growth": REAL_WAGE_GROWTH,
            "tax_share": TAX_SHARE,
            "real_discount_rate": REAL_DISCOUNT,
            "pension_contribution": PENSION_CONTRIBUTION,
            "pension_real_return": PENSION_RETURN,
        },
        "designs": [
            {"key": design.key, "name": design.name, "stages": [asdict(stage) for stage in design.stages]}
            for design in DESIGNS
        ],
        "life_accounts": accounts,
        "pension_funded_ratios": pensions,
        "retraining": retraining,
        "mortgages": mortgages,
        "marriage_survival_examples": marriages,
        "adult_generations": generations,
        "warnings": [
            "Living to 100 or 120 is a hypothetical scenario, not a South African forecast.",
            "Marriage survival is a mechanical hazard illustration, not a prediction.",
            "The mortgage uses a constant real rate and excludes fees, taxes, maintenance and default.",
            "The pension matrix assumes uninterrupted contributions and deterministic death ages.",
        ],
    }
    RESULTS_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    make_figures(accounts, pensions, retraining, mortgages)

    display = {
        "accounts_to_120": {
            design.name: {
                "work_equivalent_years": round(accounts["120"][design.key]["work_equivalent_years"], 1),
                "education_years": round(accounts["120"][design.key]["education_years"], 1),
                "retirement_years": round(accounts["120"][design.key]["retirement_years"], 1),
                "pv_earnings_m": round(accounts["120"][design.key]["pv_earnings"] / 1e6, 2),
                "net_fiscal_m": round(accounts["120"][design.key]["net_fiscal"] / 1e6, 2),
            }
            for design in DESIGNS
        },
        "pensions_pct": {
            retirement: {death: None if ratio is None else round(100 * ratio)
                         for death, ratio in row.items()}
            for retirement, row in pensions.items()
        },
        "retraining_m": [
            {
                "age": item["training_age"],
                "cost": round(item["total_cost"] / 1e6, 2),
                "benefit": round(item["benefit"] / 1e6, 2),
                "net": round(item["net_value"] / 1e6, 2),
                "payback": int(item["payback_years"]),
            }
            for item in retraining
        ],
        "mortgages": [
            {
                "term": item["term_years"],
                "payment": round(item["monthly_payment"]),
                "interest_m": round(item["total_interest"] / 1e6, 2),
                "debt65_m": round(item["balance_age_65"] / 1e6, 2),
            }
            for item in mortgages
        ],
        "marriage_survival_pct": {k: round(100 * v, 1) for k, v in marriages.items()},
        "generations": generations,
    }
    print(json.dumps(display, indent=2))


if __name__ == "__main__":
    main()
