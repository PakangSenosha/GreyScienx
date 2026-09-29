"""GreyScienx model for later retirement in a high-unemployment economy.

The model compares retirement at 60, 65, 70 and 75. It separates the private
pension arithmetic from the labour-market and public-finance channels: actual
older-worker retention, youth job displacement or complementarity, tax revenue,
old-age grant savings, disability substitution, work-related health costs and
productive output. All money values are constant 2026 rand. This is a
transparent scenario model, not a forecast or microsimulation.
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
WORK_DIR = ROOT / "work" / "retirement-age"
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
    fig.text(0.065, 0.917, field.upper(), color=CORAL, fontsize=8.5,
             fontweight="bold", ha="left", va="top")
    fig.text(0.065, 0.875, title, color=BLACK, fontsize=17,
             fontweight="bold", ha="left", va="top")
    fig.text(0.065, 0.823, subtitle, color=GREY_700, fontsize=8.4,
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


RETIREMENT_AGES = [60, 65, 70, 75]
FINAL_AGE = 100
REAL_RETURN = 0.03
REAL_WAGE_GROWTH = 0.015
CONTRIBUTION_RATE = 0.15
MONTHLY_WAGE_AT_25 = 30_000.0
POLICY_MONTHLY_WAGE_AT_60 = 22_000.0
OLDER_EFFECTIVE_TAX_SHARE = 0.16
YOUTH_MONTHLY_WAGE = 12_000.0
YOUTH_EFFECTIVE_TAX_SHARE = 0.08
YOUTH_EMPLOYED_BASE = 5_600_000
YOUTH_WAGE_RESPONSE = 0.45
POPULATION = 1_000_000
GRANT_ELIGIBLE_SHARE = 0.60
MONTHLY_PUBLIC_BENEFIT = 2_400.0
ANNUAL_PUBLIC_BENEFIT = MONTHLY_PUBLIC_BENEFIT * 12.0
ANNUAL_DISABILITY_HEALTH_COST = 12_000.0
YOUTH_BRIDGE_SUPPORT = 6_000.0


@dataclass(frozen=True)
class Occupation:
    key: str
    name: str
    share: float
    wage_multiplier: float
    disability_propensity: float
    work_health_cost: float
    retention_at_60: float
    annual_retention_decline: float
    flexible_conversion: float


OCCUPATIONS = [
    Occupation("professional", "Professional / desk", 0.35, 1.30, 0.08, 500.0, 0.90, 0.040, 0.42),
    Occupation("service", "Service / administrative", 0.30, 0.90, 0.16, 1_100.0, 0.80, 0.050, 0.40),
    Occupation("manual", "Manual / trades", 0.25, 0.78, 0.30, 2_600.0, 0.64, 0.055, 0.34),
    Occupation("strenuous", "Strenuous / hazardous", 0.10, 0.88, 0.45, 5_000.0, 0.46, 0.060, 0.28),
]


@dataclass(frozen=True)
class Scenario:
    key: str
    name: str
    employment_mode: str
    employment_scale: float
    old_worker_productivity: float
    net_youth_displacement: float
    disability_scale: float
    work_health_scale: float


SCENARIOS = [
    Scenario(
        "best", "Expansion + adapted jobs", "flexible", 1.05, 0.95,
        -0.05, 0.70, 0.75
    ),
    Scenario(
        "average", "Mixed labour market", "standard", 1.00, 0.85,
        0.15, 1.00, 1.00
    ),
    Scenario(
        "worst", "Stagnation + close competition", "standard", 0.75, 0.70,
        0.55, 1.25, 1.40
    ),
]


def potential_annual_wage(age: int) -> float:
    return MONTHLY_WAGE_AT_25 * 12.0 * (1.0 + REAL_WAGE_GROWTH) ** (age - 25)


def policy_annual_wage(age: int, occupation: Occupation) -> float:
    return (
        POLICY_MONTHLY_WAGE_AT_60 * 12.0
        * (1.0 + REAL_WAGE_GROWTH) ** (age - 60)
        * occupation.wage_multiplier
    )


def standard_retention(occupation: Occupation, age: int) -> float:
    years = max(0, age - 60)
    age_acceleration = 0.0025 * years * max(0, years - 5)
    return max(0.0, occupation.retention_at_60 - occupation.annual_retention_decline * years - age_acceleration)


def flexible_headcount(occupation: Occupation, age: int) -> float:
    standard = standard_retention(occupation, age)
    age_capacity = max(0.15, 1.0 - 0.04 * max(0, age - 60))
    return min(
        0.98,
        standard
        + (1.0 - standard) * occupation.flexible_conversion * age_capacity,
    )


def flexible_fte(occupation: Occupation, age: int) -> float:
    standard = standard_retention(occupation, age)
    added_headcount = flexible_headcount(occupation, age) - standard
    return min(1.0, standard + 0.62 * added_headcount)


def employment_fte(occupation: Occupation, scenario: Scenario, age: int) -> float:
    base = flexible_fte(occupation, age) if scenario.employment_mode == "flexible" else standard_retention(occupation, age)
    return min(1.0, base * scenario.employment_scale)


def annuity_factor(real_return: float, years: int) -> float:
    if abs(real_return) < 1e-12:
        return float(years)
    return (1.0 - (1.0 + real_return) ** (-years)) / real_return


def full_career_private_result(retirement_age: int) -> dict[str, float]:
    balance = 0.0
    for age in range(20, retirement_age):
        balance *= 1.0 + REAL_RETURN
        balance += potential_annual_wage(age) * CONTRIBUTION_RATE
    pension_years = FINAL_AGE - retirement_age + 1
    monthly_pension = balance / annuity_factor(REAL_RETURN, pension_years) / 12.0
    return {
        "wealth": balance,
        "monthly_pension": monthly_pension,
        "pension_years": pension_years,
    }


def expected_private_result(retirement_age: int, scenario: Scenario) -> dict[str, float]:
    base_at_60 = full_career_private_result(60)["wealth"]
    weighted_balance = 0.0
    for occupation in OCCUPATIONS:
        balance = base_at_60 * occupation.wage_multiplier
        for age in range(60, retirement_age):
            balance *= 1.0 + REAL_RETURN
            balance += (
                policy_annual_wage(age, occupation)
                * CONTRIBUTION_RATE
                * employment_fte(occupation, scenario, age)
            )
        weighted_balance += occupation.share * balance
    pension_years = FINAL_AGE - retirement_age + 1
    monthly_pension = weighted_balance / annuity_factor(REAL_RETURN, pension_years) / 12.0
    return {"wealth": weighted_balance, "monthly_pension": monthly_pension}


def model_policy(retirement_age: int, scenario: Scenario) -> dict:
    if retirement_age == 60:
        expected_private = expected_private_result(60, scenario)
        return {
            "retirement_age": 60,
            "scenario": asdict(scenario),
            "older_job_years": 0.0,
            "average_older_fte": 0.0,
            "youth_job_years_change": 0.0,
            "average_annual_youth_jobs_change": 0.0,
            "youth_wage_change_percent": 0.0,
            "grant_savings": 0.0,
            "older_tax_revenue": 0.0,
            "youth_tax_change": 0.0,
            "youth_support_cost": 0.0,
            "disability_claim_years": 0.0,
            "disability_cost": 0.0,
            "work_health_cost": 0.0,
            "unsupported_bridge_years": 0.0,
            "net_public_balance": 0.0,
            "net_output": 0.0,
            "expected_private_wealth": expected_private["wealth"],
            "expected_private_monthly_pension": expected_private["monthly_pension"],
        }

    older_job_years = 0.0
    youth_job_years_change = 0.0
    older_tax_revenue = 0.0
    disability_claim_years = 0.0
    unsupported_bridge_years = 0.0
    work_health_cost = 0.0
    older_output = 0.0

    for age in range(60, retirement_age):
        for occupation in OCCUPATIONS:
            people = POPULATION * occupation.share
            employed = people * employment_fte(occupation, scenario, age)
            nonemployed = people - employed
            wage = policy_annual_wage(age, occupation)
            older_job_years += employed
            older_tax_revenue += employed * wage * OLDER_EFFECTIVE_TAX_SHARE
            older_output += employed * wage * scenario.old_worker_productivity
            work_health_cost += employed * occupation.work_health_cost * scenario.work_health_scale

            age_claim_factor = min(1.8, 1.0 + 0.035 * (age - 60))
            claim_rate = min(
                0.90,
                occupation.disability_propensity
                * age_claim_factor
                * scenario.disability_scale,
            )
            claims = nonemployed * GRANT_ELIGIBLE_SHARE * claim_rate
            disability_claim_years += claims
            unsupported_bridge_years += (
                nonemployed * GRANT_ELIGIBLE_SHARE - claims
            )

    youth_job_years_change = -scenario.net_youth_displacement * older_job_years
    youth_tax_change = (
        youth_job_years_change
        * YOUTH_MONTHLY_WAGE * 12.0
        * YOUTH_EFFECTIVE_TAX_SHARE
    )
    youth_support_cost = (
        max(0.0, -youth_job_years_change) * YOUTH_BRIDGE_SUPPORT
    )
    youth_output_change = (
        youth_job_years_change * YOUTH_MONTHLY_WAGE * 12.0 * 0.90
    )
    delayed_years = retirement_age - 60
    average_annual_youth_jobs_change = youth_job_years_change / delayed_years
    youth_wage_change_percent = (
        100.0 * YOUTH_WAGE_RESPONSE
        * average_annual_youth_jobs_change / YOUTH_EMPLOYED_BASE
    )
    grant_savings = (
        POPULATION * GRANT_ELIGIBLE_SHARE
        * ANNUAL_PUBLIC_BENEFIT * delayed_years
    )
    disability_cost = disability_claim_years * (
        ANNUAL_PUBLIC_BENEFIT + ANNUAL_DISABILITY_HEALTH_COST
    )
    net_public_balance = (
        grant_savings + older_tax_revenue + youth_tax_change
        - youth_support_cost - disability_cost - work_health_cost
    )
    expected_private = expected_private_result(retirement_age, scenario)
    return {
        "retirement_age": retirement_age,
        "scenario": asdict(scenario),
        "older_job_years": older_job_years,
        "average_older_fte": older_job_years / delayed_years,
        "youth_job_years_change": youth_job_years_change,
        "average_annual_youth_jobs_change": average_annual_youth_jobs_change,
        "youth_wage_change_percent": youth_wage_change_percent,
        "grant_savings": grant_savings,
        "older_tax_revenue": older_tax_revenue,
        "youth_tax_change": youth_tax_change,
        "youth_support_cost": youth_support_cost,
        "disability_claim_years": disability_claim_years,
        "disability_cost": disability_cost,
        "work_health_cost": work_health_cost,
        "unsupported_bridge_years": unsupported_bridge_years,
        "net_public_balance": net_public_balance,
        "net_output": older_output + youth_output_change,
        "expected_private_wealth": expected_private["wealth"],
        "expected_private_monthly_pension": expected_private["monthly_pension"],
    }


def policy_grid() -> dict[str, list[dict]]:
    return {
        scenario.key: [model_policy(age, scenario) for age in RETIREMENT_AGES]
        for scenario in SCENARIOS
    }


def occupation_market() -> dict[str, dict[str, list[float]]]:
    ages = list(range(60, 80))
    output: dict[str, dict[str, list[float]]] = {"ages": ages}  # type: ignore
    for occupation in OCCUPATIONS:
        output[occupation.key] = {
            "standard": [standard_retention(occupation, age) for age in ages],
            "flexible_headcount": [flexible_headcount(occupation, age) for age in ages],
            "flexible_fte": [flexible_fte(occupation, age) for age in ages],
        }
    return output


def build_private_pension_figure(private: dict, policies: dict) -> Path:
    ages = np.array(RETIREMENT_AGES)
    full_wealth = np.array([private[str(age)]["wealth"] for age in ages]) / 1e6
    full_income = np.array([private[str(age)]["monthly_pension"] for age in ages]) / 1e3
    avg_wealth = np.array([
        policies["average"][idx]["expected_private_wealth"]
        for idx in range(len(ages))
    ]) / 1e6
    avg_income = np.array([
        policies["average"][idx]["expected_private_monthly_pension"]
        for idx in range(len(ages))
    ]) / 1e3

    fig, axes = plt.subplots(1, 2, figsize=(8.1, 4.2))
    fig.subplots_adjust(left=0.10, right=0.965, bottom=0.18, top=0.67, wspace=0.25)
    figure_header(
        fig,
        "Private pension arithmetic",
        "Later retirement makes the pension denominator smaller",
        "Full-career benchmark and expected mixed-occupation path, constant 2026 rand; private fund only.",
    )
    for ax, full, average, ylabel, title in [
        (axes[0], full_wealth, avg_wealth, "Private wealth (R million)", "Fund at retirement"),
        (axes[1], full_income, avg_income, "Monthly pension (R thousand)", "Income through age 100"),
    ]:
        ax.plot(ages, full, color=CORAL, linewidth=2.2, marker="o", label="Continuously employed")
        ax.plot(ages, average, color=TRUE_BLACK, linewidth=2.0, linestyle="--", marker="s", label="Expected retention")
        for x, y in zip(ages, average):
            ax.text(x, y + max(average) * 0.045, f"{y:.1f}", ha="center", fontsize=7.8)
        ax.set_title(title, fontsize=10.5, fontweight="bold")
        ax.set_xlabel("Retirement age")
        ax.set_ylabel(ylabel)
        ax.set_xticks(ages)
        ax.set_ylim(0, max(full) * 1.20)
        style_axis(ax)
    axes[0].legend(frameon=False, fontsize=7.8, loc="upper left")
    return save_figure(fig, "private-pension-dividend.png")


def build_fiscal_scenarios_figure(policies: dict) -> Path:
    fig, ax = plt.subplots(figsize=(8.1, 4.05))
    fig.subplots_adjust(left=0.12, right=0.965, bottom=0.18, top=0.68)
    figure_header(
        fig,
        "One-million-person cohort",
        "The budget usually improves - but the social route matters",
        "Cumulative public balance versus retirement at 60, R billion in constant 2026 rand; undiscounted.",
    )
    encodings = [
        ("best", CORAL, "-", "o"),
        ("average", TRUE_BLACK, "--", "s"),
        ("worst", GREY_500, ":", "D"),
    ]
    for key, color, line, marker in encodings:
        values = np.array([row["net_public_balance"] for row in policies[key]]) / 1e9
        label = policies[key][0]["scenario"]["name"]
        ax.plot(RETIREMENT_AGES, values, color=color, linestyle=line,
                marker=marker, linewidth=2.2, markersize=5.0, label=label)
        ax.text(75.4, values[-1], f"R{values[-1]:.0f}bn", va="center", fontsize=8.0, color=color)
    ax.axhline(0, color=BLACK, linewidth=0.9)
    ax.set_xlabel("Retirement age")
    ax.set_ylabel("Cumulative public balance (R billion)")
    ax.set_xticks(RETIREMENT_AGES)
    style_axis(ax)
    ax.legend(frameon=False, fontsize=8.0, loc="upper left")
    return save_figure(fig, "fiscal-scenarios.png")


def build_fiscal_decomposition_figure(policies: dict) -> Path:
    rows = policies["average"][1:]
    ages = np.array([row["retirement_age"] for row in rows])
    grant = np.array([row["grant_savings"] for row in rows]) / 1e9
    older_tax = np.array([row["older_tax_revenue"] for row in rows]) / 1e9
    youth_fiscal = np.array([
        row["youth_tax_change"] - row["youth_support_cost"] for row in rows
    ]) / 1e9
    disability = -np.array([row["disability_cost"] for row in rows]) / 1e9
    health = -np.array([row["work_health_cost"] for row in rows]) / 1e9
    net = np.array([row["net_public_balance"] for row in rows]) / 1e9

    fig, ax = plt.subplots(figsize=(8.1, 4.2))
    fig.subplots_adjust(left=0.12, right=0.965, bottom=0.18, top=0.66)
    figure_header(
        fig,
        "Average-case decomposition",
        "Grant savings and older-worker taxes do most of the fiscal work",
        "Cumulative change versus retirement at 60, R billion per one million people; undiscounted.",
    )
    x = np.arange(len(ages))
    width = 0.58
    ax.bar(x, grant, width, color=CORAL, label="Old-age grant saving")
    ax.bar(x, older_tax, width, bottom=grant, color=TRUE_BLACK, label="Older-worker tax")
    neg_bottom = np.zeros(len(ages))
    for values, color, label in [
        (disability, GREY_500, "Disability + health"),
        (youth_fiscal, GREY_300, "Youth tax + support"),
        (health, GREY_700, "Work-health cost"),
    ]:
        ax.bar(x, values, width, bottom=neg_bottom, color=color, label=label)
        neg_bottom += values
    ax.scatter(x, net, color=WHITE, edgecolor=TRUE_BLACK, marker="D", s=42,
               linewidth=1.2, zorder=4, label="Net public balance")
    for idx, value in enumerate(net):
        ax.text(idx, value + 18, f"R{value:.0f}bn", ha="center", fontsize=8.0,
                fontweight="bold", color=WHITE)
    ax.axhline(0, color=BLACK, linewidth=0.9)
    ax.set_xticks(x, [f"Retire at {age}" for age in ages])
    ax.set_ylabel("Cumulative public effect (R billion)")
    style_axis(ax)
    ax.legend(frameon=False, fontsize=7.4, loc="upper left", ncol=2)
    return save_figure(fig, "fiscal-decomposition.png")


def build_youth_effects_figure(policies: dict) -> Path:
    fig, axes = plt.subplots(1, 2, figsize=(8.1, 4.2))
    fig.subplots_adjust(left=0.11, right=0.965, bottom=0.18, top=0.66, wspace=0.27)
    figure_header(
        fig,
        "Youth labour market",
        "There is no fixed job count - but overlap can still hurt in a slump",
        "Cumulative youth job-years and modeled average wage effect while retirement is delayed; positive is better.",
    )
    encodings = [
        ("best", CORAL, "-", "o"),
        ("average", TRUE_BLACK, "--", "s"),
        ("worst", GREY_500, ":", "D"),
    ]
    for key, color, line, marker in encodings:
        jobs = np.array([
            row["youth_job_years_change"] for row in policies[key]
        ]) / 1e6
        wages = np.array([
            row["youth_wage_change_percent"] for row in policies[key]
        ])
        label = policies[key][0]["scenario"]["name"]
        axes[0].plot(RETIREMENT_AGES, jobs, color=color, linestyle=line,
                     marker=marker, linewidth=2.1, markersize=4.5, label=label)
        axes[1].plot(RETIREMENT_AGES, wages, color=color, linestyle=line,
                     marker=marker, linewidth=2.1, markersize=4.5)
    for ax in axes:
        ax.axhline(0, color=BLACK, linewidth=0.9)
        ax.set_xlabel("Retirement age")
        ax.set_xticks(RETIREMENT_AGES)
        style_axis(ax)
    axes[0].set_title("Youth jobs", fontsize=10.5, fontweight="bold")
    axes[0].set_ylabel("Cumulative change (million job-years)")
    axes[0].legend(frameon=False, fontsize=7.2, loc="lower left")
    axes[1].set_title("Youth wages", fontsize=10.5, fontweight="bold")
    axes[1].set_ylabel("Modeled average wage change (%)")
    return save_figure(fig, "youth-effects.png")


def build_occupation_market_figure(market: dict) -> Path:
    ages = np.array(market["ages"])
    fig, axes = plt.subplots(1, 2, figsize=(8.1, 4.3), sharey=True)
    fig.subplots_adjust(left=0.11, right=0.965, bottom=0.18, top=0.66, wspace=0.13)
    figure_header(
        fig,
        "Occupation and job design",
        "One retirement age cannot fit four different bodies of work",
        "Modeled share able to remain employed by age; the flexible market includes part-time and adapted roles.",
    )
    encodings = {
        "professional": (CORAL, "-", "o"),
        "service": (TRUE_BLACK, "--", "s"),
        "manual": (GREY_500, ":", "D"),
        "strenuous": (GREY_700, "-.", "^")
    }
    for ax, field, panel in [
        (axes[0], "standard", "Standard jobs"),
        (axes[1], "flexible_headcount", "Adapted retirement-job market"),
    ]:
        for occupation in OCCUPATIONS:
            color, line, marker = encodings[occupation.key]
            values = np.array(market[occupation.key][field]) * 100.0
            ax.plot(ages, values, color=color, linestyle=line, marker=marker,
                    markevery=3, linewidth=2.0, markersize=3.8, label=occupation.name)
        ax.axhline(50, color=GREY_300, linewidth=1.0)
        ax.set_title(panel, fontsize=10.5, fontweight="bold")
        ax.set_xlabel("Age")
        ax.set_xticks([60, 65, 70, 75, 79])
        ax.set_ylim(0, 105)
        style_axis(ax)
    axes[0].set_ylabel("Modeled employment capacity (%)")
    axes[1].legend(frameon=False, fontsize=7.1, loc="upper right")
    return save_figure(fig, "occupation-retirement-market.png")


def validate(results: dict) -> None:
    assert abs(sum(occupation.share for occupation in OCCUPATIONS) - 1.0) < 1e-12
    for key in ["best", "average", "worst"]:
        rows = results["policies"][key]
        assert [row["retirement_age"] for row in rows] == RETIREMENT_AGES
        assert all(rows[i]["net_public_balance"] <= rows[i + 1]["net_public_balance"] for i in range(3))
    assert results["policies"]["best"][-1]["net_public_balance"] > results["policies"]["average"][-1]["net_public_balance"]
    assert results["policies"]["average"][-1]["net_public_balance"] > results["policies"]["worst"][-1]["net_public_balance"]
    assert results["policies"]["best"][-1]["average_annual_youth_jobs_change"] > 0
    assert results["policies"]["average"][-1]["average_annual_youth_jobs_change"] < 0
    assert results["policies"]["worst"][-1]["average_annual_youth_jobs_change"] < results["policies"]["average"][-1]["average_annual_youth_jobs_change"]
    private = results["private_full_career"]
    assert all(private[str(a)]["wealth"] < private[str(b)]["wealth"] for a, b in zip(RETIREMENT_AGES, RETIREMENT_AGES[1:]))
    assert all(private[str(a)]["monthly_pension"] < private[str(b)]["monthly_pension"] for a, b in zip(RETIREMENT_AGES, RETIREMENT_AGES[1:]))
    for occupation in OCCUPATIONS:
        standard = results["occupation_market"][occupation.key]["standard"]
        flexible = results["occupation_market"][occupation.key]["flexible_headcount"]
        assert all(f >= s for f, s in zip(flexible, standard))


def main() -> None:
    set_plot_style()
    WORK_DIR.mkdir(parents=True, exist_ok=True)
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    private = {str(age): full_career_private_result(age) for age in RETIREMENT_AGES}
    policies = policy_grid()
    market = occupation_market()
    results = {
        "model_label": "Stylized retirement-age model, constant 2026 rand",
        "assumptions": {
            "retirement_ages": RETIREMENT_AGES,
            "final_age": FINAL_AGE,
            "real_return": REAL_RETURN,
            "real_wage_growth": REAL_WAGE_GROWTH,
            "contribution_rate": CONTRIBUTION_RATE,
            "monthly_wage_at_25": MONTHLY_WAGE_AT_25,
            "policy_monthly_wage_at_60": POLICY_MONTHLY_WAGE_AT_60,
            "older_effective_tax_share": OLDER_EFFECTIVE_TAX_SHARE,
            "youth_monthly_wage": YOUTH_MONTHLY_WAGE,
            "youth_effective_tax_share": YOUTH_EFFECTIVE_TAX_SHARE,
            "youth_employed_base": YOUTH_EMPLOYED_BASE,
            "population": POPULATION,
            "grant_eligible_share": GRANT_ELIGIBLE_SHARE,
            "monthly_public_benefit": MONTHLY_PUBLIC_BENEFIT,
        },
        "occupations": [asdict(occupation) for occupation in OCCUPATIONS],
        "scenarios": [asdict(scenario) for scenario in SCENARIOS],
        "private_full_career": private,
        "policies": policies,
        "occupation_market": market,
    }
    build_private_pension_figure(private, policies)
    build_fiscal_scenarios_figure(policies)
    build_fiscal_decomposition_figure(policies)
    build_youth_effects_figure(policies)
    build_occupation_market_figure(market)
    results["figures"] = {
        "private_pension": "assets/private-pension-dividend.png",
        "fiscal_scenarios": "assets/fiscal-scenarios.png",
        "fiscal_decomposition": "assets/fiscal-decomposition.png",
        "youth_effects": "assets/youth-effects.png",
        "occupation_market": "assets/occupation-retirement-market.png",
    }
    validate(results)
    RESULTS_PATH.write_text(json.dumps(results, indent=2), encoding="utf-8")

    print(f"Wrote {RESULTS_PATH}")
    for age in RETIREMENT_AGES:
        full = private[str(age)]
        average = policies["average"][RETIREMENT_AGES.index(age)]
        print(
            f"Retire {age}: full wealth R{full['wealth']/1e6:.2f}m; "
            f"full pension R{full['monthly_pension']:,.0f}/month; "
            f"average public balance R{average['net_public_balance']/1e9:.1f}bn; "
            f"youth jobs {average['average_annual_youth_jobs_change']/1e3:+.1f}k/year"
        )
    for scenario in SCENARIOS:
        row = policies[scenario.key][-1]
        print(
            f"{scenario.name}, age 75: public R{row['net_public_balance']/1e9:.1f}bn; "
            f"youth jobs {row['average_annual_youth_jobs_change']/1e3:+.1f}k/year; "
            f"wage {row['youth_wage_change_percent']:+.2f}%"
        )


if __name__ == "__main__":
    main()
