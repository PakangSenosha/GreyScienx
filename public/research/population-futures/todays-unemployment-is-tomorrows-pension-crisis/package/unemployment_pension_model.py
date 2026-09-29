"""GreyScienx cohort model for unemployment as a delayed pension crisis.

The model follows six stylized labour-market histories from age 20 to 100. It
tracks earnings, private retirement contributions, pension wealth, a modeled
old-age grant, public healthcare cost and tax contribution in constant 2026
rand. It is a transparent scenario model, not a forecast or microsimulation.
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
WORK_DIR = ROOT / "work" / "unemployment-pension"
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


AGE_START = 20
RETIREMENT_AGE = 60
FINAL_AGE = 100
REAL_WAGE_GROWTH = 0.015
REAL_RETURN = 0.03
MONTHLY_WAGE_AT_25 = 30_000.0
MAX_GRANT_MONTHLY = 2_400.0
GRANT_FULL_BELOW = 10_000.0
GRANT_ZERO_ABOVE = 15_000.0


@dataclass(frozen=True)
class Profile:
    key: str
    name: str
    description: str
    contribution_rate: float
    formal_tax_rate: float
    informal_tax_rate: float


PROFILES = [
    Profile("stable", "Stable formal", "Formal work from 20 to 59", 0.15, 0.20, 0.05),
    Profile("temporary", "Five-year shock", "Unemployed 20-24, then catches up", 0.15, 0.20, 0.05),
    Profile("delayed", "Entry at 30", "Unemployed 20-29, wage scar fades", 0.15, 0.20, 0.05),
    Profile("interrupted", "Interrupted career", "Formal work, ten-year mid-career gap", 0.15, 0.20, 0.05),
    Profile("informal", "Mostly informal", "Works four years in five at 70% wage", 0.05, 0.20, 0.05),
    Profile("persistent", "Persistent exclusion", "Works one year in four at 60% wage", 0.03, 0.20, 0.03),
]


def potential_annual_wage(age: int) -> float:
    return MONTHLY_WAGE_AT_25 * 12.0 * (1.0 + REAL_WAGE_GROWTH) ** (age - 25)


def labour_state(profile: Profile, age: int) -> tuple[str, float]:
    """Return sector and fraction of the age-specific benchmark wage."""
    if profile.key == "stable":
        return "formal", 1.0
    if profile.key == "temporary":
        if age < 25:
            return "unemployed", 0.0
        return "formal", min(1.0, 0.90 + 0.01 * (age - 25))
    if profile.key == "delayed":
        if age < 30:
            return "unemployed", 0.0
        return "formal", min(1.0, 0.80 + 0.01 * (age - 30))
    if profile.key == "interrupted":
        if 30 <= age < 40:
            return "unemployed", 0.0
        if age >= 40:
            return "formal", min(1.0, 0.80 + 0.01 * (age - 40))
        return "formal", 1.0
    if profile.key == "informal":
        if (age - AGE_START) % 5 == 4:
            return "unemployed", 0.0
        return "informal", 0.70
    if profile.key == "persistent":
        if (age - AGE_START) % 4 == 0:
            return "informal", 0.60
        return "unemployed", 0.0
    raise ValueError(profile.key)


def public_health_cost(age: int) -> float:
    """Illustrative annual public healthcare cost in constant 2026 rand."""
    if age < 60:
        return 3_000.0
    if age < 70:
        return 10_000.0
    if age < 80:
        return 18_000.0
    if age < 90:
        return 32_000.0
    return 52_000.0


def annuity_factor(real_return: float, years: int) -> float:
    if abs(real_return) < 1e-12:
        return float(years)
    return (1.0 - (1.0 + real_return) ** (-years)) / real_return


def modeled_monthly_grant(private_monthly_pension: float) -> float:
    """Stylized phased top-up, not the legal SASSA means test."""
    if private_monthly_pension <= GRANT_FULL_BELOW:
        return MAX_GRANT_MONTHLY
    if private_monthly_pension >= GRANT_ZERO_ABOVE:
        return 0.0
    share = (GRANT_ZERO_ABOVE - private_monthly_pension) / (
        GRANT_ZERO_ABOVE - GRANT_FULL_BELOW
    )
    return MAX_GRANT_MONTHLY * share


def simulate_profile(profile: Profile, real_return: float = REAL_RETURN) -> dict:
    ages = list(range(AGE_START, FINAL_AGE + 1))
    balance = 0.0
    balances: list[float] = []
    earnings_by_age: list[float] = []
    taxes_by_age: list[float] = []
    health_by_age: list[float] = []
    grants_by_age: list[float] = []
    fiscal_flow_by_age: list[float] = []
    employment_years = 0
    formal_years = 0
    informal_years = 0

    for age in range(AGE_START, RETIREMENT_AGE):
        balance *= 1.0 + real_return
        sector, wage_fraction = labour_state(profile, age)
        earnings = potential_annual_wage(age) * wage_fraction
        contribution = earnings * profile.contribution_rate
        tax_rate = 0.0
        if sector == "formal":
            tax_rate = profile.formal_tax_rate
            employment_years += 1
            formal_years += 1
        elif sector == "informal":
            tax_rate = profile.informal_tax_rate
            employment_years += 1
            informal_years += 1
        taxes = earnings * tax_rate
        health = public_health_cost(age)
        balance += contribution
        balances.append(balance)
        earnings_by_age.append(earnings)
        taxes_by_age.append(taxes)
        health_by_age.append(health)
        grants_by_age.append(0.0)
        fiscal_flow_by_age.append(taxes - health)

    wealth_at_60 = balance
    retirement_years = FINAL_AGE - RETIREMENT_AGE + 1
    private_annual_pension = wealth_at_60 / annuity_factor(real_return, retirement_years)
    private_monthly_pension = private_annual_pension / 12.0
    monthly_grant = modeled_monthly_grant(private_monthly_pension)
    annual_grant = monthly_grant * 12.0

    for age in range(RETIREMENT_AGE, FINAL_AGE + 1):
        balance *= 1.0 + real_return
        balance -= private_annual_pension
        health = public_health_cost(age)
        balances.append(balance)
        earnings_by_age.append(0.0)
        taxes_by_age.append(0.0)
        health_by_age.append(health)
        grants_by_age.append(annual_grant)
        fiscal_flow_by_age.append(-health - annual_grant)

    final_benchmark_monthly = potential_annual_wage(RETIREMENT_AGE - 1) / 12.0
    target_monthly_income = 0.60 * final_benchmark_monthly
    retirement_income = private_monthly_pension + monthly_grant
    grant_share = monthly_grant / retirement_income if retirement_income > 0 else 0.0
    lifetime_taxes = float(sum(taxes_by_age))
    lifetime_health = float(sum(health_by_age))
    lifetime_grants = float(sum(grants_by_age))

    return {
        "profile": asdict(profile),
        "ages": ages,
        "balances": balances,
        "earnings_by_age": earnings_by_age,
        "taxes_by_age": taxes_by_age,
        "health_by_age": health_by_age,
        "grants_by_age": grants_by_age,
        "fiscal_flow_by_age": fiscal_flow_by_age,
        "employment_years": employment_years,
        "formal_years": formal_years,
        "informal_years": informal_years,
        "wealth_at_60": wealth_at_60,
        "private_monthly_pension": private_monthly_pension,
        "monthly_grant": monthly_grant,
        "grant_share_of_cash_income": grant_share,
        "target_monthly_income": target_monthly_income,
        "retirement_income_ratio": retirement_income / target_monthly_income,
        "lifetime_earnings": float(sum(earnings_by_age)),
        "lifetime_taxes": lifetime_taxes,
        "lifetime_health": lifetime_health,
        "lifetime_grants": lifetime_grants,
        "lifetime_net_fiscal": lifetime_taxes - lifetime_health - lifetime_grants,
        "ending_balance": balance,
    }


def wealth_for_entry_age(entry_age: int, contribution_rate: float, real_return: float) -> float:
    balance = 0.0
    initial_scar = max(0.50, 1.0 - 0.02 * (entry_age - AGE_START))
    for age in range(AGE_START, RETIREMENT_AGE):
        balance *= 1.0 + real_return
        if age >= entry_age:
            wage_fraction = min(1.0, initial_scar + 0.01 * (age - entry_age))
            balance += potential_annual_wage(age) * wage_fraction * contribution_rate
    return balance


def catchup_rates() -> dict[str, list[float]]:
    entry_ages = [20, 25, 30, 35, 40, 45]
    output: dict[str, list[float]] = {"entry_ages": entry_ages}
    for real_return in [0.01, 0.03, 0.05]:
        target = wealth_for_entry_age(20, 0.15, real_return)
        rates = []
        for entry_age in entry_ages:
            wealth_at_full_rate = wealth_for_entry_age(entry_age, 1.0, real_return)
            rates.append(target / wealth_at_full_rate if wealth_at_full_rate > 0 else float("inf"))
        output[f"return_{real_return:.2f}"] = rates
    return output


COHORT_MIXES = {
    "secure": {
        "stable": 0.60,
        "temporary": 0.25,
        "delayed": 0.08,
        "interrupted": 0.05,
        "informal": 0.02,
        "persistent": 0.00,
    },
    "excluded": {
        "stable": 0.15,
        "temporary": 0.15,
        "delayed": 0.20,
        "interrupted": 0.15,
        "informal": 0.25,
        "persistent": 0.10,
    },
}


def cohort_summary(results_by_key: dict[str, dict], mix: dict[str, float]) -> dict:
    count = 1_000_000
    ages = results_by_key["stable"]["ages"]

    def weighted(metric: str) -> float:
        return sum(mix[key] * results_by_key[key][metric] for key in mix)

    fiscal_flow = [
        count * sum(
            mix[key] * results_by_key[key]["fiscal_flow_by_age"][index]
            for key in mix
        )
        for index in range(len(ages))
    ]
    grant_reliant_share = sum(
        share for key, share in mix.items() if results_by_key[key]["monthly_grant"] > 0
    )
    return {
        "population": count,
        "ages": ages,
        "fiscal_flow_by_age": fiscal_flow,
        "average_wealth_at_60": weighted("wealth_at_60"),
        "average_private_monthly_pension": weighted("private_monthly_pension"),
        "average_monthly_grant": weighted("monthly_grant"),
        "grant_reliant_share": grant_reliant_share,
        "lifetime_taxes": count * weighted("lifetime_taxes"),
        "lifetime_health": count * weighted("lifetime_health"),
        "lifetime_grants": count * weighted("lifetime_grants"),
        "lifetime_net_fiscal": count * weighted("lifetime_net_fiscal"),
    }


def build_wealth_paths_figure(results: list[dict]) -> Path:
    fig, axes = plt.subplots(1, 2, figsize=(8.1, 4.2), sharey=True)
    fig.subplots_adjust(left=0.10, right=0.965, bottom=0.17, top=0.67, wspace=0.13)
    figure_header(
        fig,
        "Private retirement wealth",
        "The pension gap is laid down decades before retirement",
        "Private fund balance from age 20 to 100, constant 2026 rand; retirement begins at 60.",
    )
    panels = [
        (["stable", "temporary", "delayed"], "Youth entry"),
        (["interrupted", "informal", "persistent"], "Interrupted and excluded"),
    ]
    encoding = {
        "stable": (CORAL, "-", "o"),
        "temporary": (TRUE_BLACK, "--", "s"),
        "delayed": (GREY_500, ":", "D"),
        "interrupted": (CORAL, "-.", "^"),
        "informal": (TRUE_BLACK, "--", "s"),
        "persistent": (GREY_500, ":", "D"),
    }
    result_map = {r["profile"]["key"]: r for r in results}
    for ax, (keys, panel_title) in zip(axes, panels):
        for key in keys:
            result = result_map[key]
            color, line, marker = encoding[key]
            ax.plot(
                result["ages"], np.array(result["balances"]) / 1_000_000.0,
                color=color, linestyle=line, linewidth=2.0, marker=marker,
                markersize=3.5, markevery=10, label=result["profile"]["name"]
            )
        ax.axvline(RETIREMENT_AGE, color=GREY_300, linewidth=0.9)
        ax.axhline(0, color=BLACK, linewidth=0.9)
        ax.set_title(panel_title, fontsize=10.5, fontweight="bold")
        ax.set_xlabel("Age")
        style_axis(ax)
        ax.legend(frameon=False, fontsize=7.5, loc="upper right")
    axes[0].set_ylabel("Private fund balance (R million)")
    return save_figure(fig, "private-wealth-paths.png")


def build_income_ladder_figure(results: list[dict]) -> Path:
    names = [r["profile"]["name"] for r in results]
    private = np.array([r["private_monthly_pension"] for r in results]) / 1_000.0
    grants = np.array([r["monthly_grant"] for r in results]) / 1_000.0
    target = results[0]["target_monthly_income"] / 1_000.0
    y = np.arange(len(names))
    fig, ax = plt.subplots(figsize=(8.1, 4.2))
    fig.subplots_adjust(left=0.23, right=0.965, bottom=0.15, top=0.70)
    figure_header(
        fig,
        "Retirement income",
        "The state cushions the floor; it does not replace the missing career",
        "Modeled monthly income from age 60, constant 2026 rand; the grant is a simplified analytical top-up.",
    )
    ax.barh(y, private, color=TRUE_BLACK, height=0.58, label="Private pension")
    ax.barh(y, grants, left=private, color=CORAL, height=0.58, label="Modeled grant")
    ax.axvline(target, color=GREY_500, linestyle=":", linewidth=1.2,
               label=f"60% benchmark target: R{target:.1f}k")
    for idx, total in enumerate(private + grants):
        ax.text(total + 0.35, idx, f"R{total:.1f}k", va="center", fontsize=8)
    ax.set_yticks(y, names)
    ax.invert_yaxis()
    ax.set_xlabel("Monthly retirement cash income (R thousand)")
    style_axis(ax, grid_axis="x")
    ax.legend(frameon=False, fontsize=8, loc="lower right")
    return save_figure(fig, "retirement-income-ladder.png")


def build_catchup_figure(catchup: dict[str, list[float]]) -> Path:
    entry_ages = np.array(catchup["entry_ages"])
    fig, ax = plt.subplots(figsize=(8.1, 4.0))
    fig.subplots_adjust(left=0.12, right=0.965, bottom=0.18, top=0.68)
    figure_header(
        fig,
        "Catch-up test",
        "Starting later requires saving harder - sometimes implausibly harder",
        "Contribution rate needed after entry to match a 15 percent saver who worked from age 20; retirement at 60.",
    )
    series = [
        (0.01, CORAL, "-", "o", "1% real return"),
        (0.03, TRUE_BLACK, "--", "s", "3% real return"),
        (0.05, GREY_500, ":", "D", "5% real return"),
    ]
    for rate, color, line, marker, label in series:
        values = np.array(catchup[f"return_{rate:.2f}"]) * 100.0
        ax.plot(entry_ages, values, color=color, linestyle=line, marker=marker,
                linewidth=2.0, markersize=4.5, label=label)
    ax.axhline(30, color=GREY_300, linewidth=1.0)
    ax.text(45, 31.5, "30% of salary", color=GREY_700, fontsize=8, ha="right")
    ax.set_xlabel("Age when formal contributions begin")
    ax.set_ylabel("Required contribution rate (%)")
    ax.set_xticks(entry_ages)
    ax.set_ylim(10, 125)
    style_axis(ax)
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    return save_figure(fig, "delayed-entry-catchup.png")


def build_fiscal_wave_figure(cohorts: dict[str, dict]) -> Path:
    ages = np.array(cohorts["secure"]["ages"])
    secure = np.array(cohorts["secure"]["fiscal_flow_by_age"]) / 1e9
    excluded = np.array(cohorts["excluded"]["fiscal_flow_by_age"]) / 1e9
    fig, ax = plt.subplots(figsize=(8.1, 4.1))
    fig.subplots_adjust(left=0.12, right=0.965, bottom=0.18, top=0.68)
    figure_header(
        fig,
        "One-million-person cohort",
        "At 60, lost tax capacity returns as a shared public bill",
        "Annual taxes minus modeled grants and public healthcare, R billion in constant 2026 rand; undiscounted.",
    )
    ax.plot(ages, excluded, color=CORAL, linewidth=2.2, marker="o", markersize=4,
            markevery=10, label="Excluded cohort")
    ax.plot(ages, secure, color=TRUE_BLACK, linewidth=2.0, linestyle="--",
            marker="s", markersize=3.8, markevery=10, label="Secure cohort")
    ax.axvline(60, color=GREY_500, linewidth=1.0)
    ax.axhline(0, color=BLACK, linewidth=1.0)
    ax.text(60.7, ax.get_ylim()[0] * 0.90, "retirement", color=GREY_700, fontsize=8)
    ax.set_xlabel("Age")
    ax.set_ylabel("Annual net public flow (R billion)")
    style_axis(ax)
    ax.legend(frameon=False, fontsize=8, loc="upper right")
    return save_figure(fig, "cohort-fiscal-wave.png")


def build_lifetime_fiscal_figure(cohorts: dict[str, dict]) -> Path:
    labels = ["Secure cohort", "Excluded cohort"]
    keys = ["secure", "excluded"]
    taxes = np.array([cohorts[k]["lifetime_taxes"] for k in keys]) / 1e12
    grants = np.array([cohorts[k]["lifetime_grants"] for k in keys]) / 1e12
    health = np.array([cohorts[k]["lifetime_health"] for k in keys]) / 1e12
    net = taxes - grants - health
    x = np.arange(2)
    fig, ax = plt.subplots(figsize=(8.1, 4.1))
    fig.subplots_adjust(left=0.12, right=0.965, bottom=0.18, top=0.68)
    figure_header(
        fig,
        "Lifetime fiscal contribution",
        "The pension crisis is also a missing-revenue crisis",
        "Cumulative public flows for one million people from age 20 to 100, R trillion in constant 2026 rand; undiscounted.",
    )
    width = 0.48
    ax.bar(x, taxes, width=width, color=TRUE_BLACK, label="Taxes paid")
    ax.bar(x, -health, width=width, color=GREY_500, label="Public healthcare")
    ax.bar(x, -grants, width=width, bottom=-health, color=CORAL, label="Old-age grants")
    ax.scatter(x, net, marker="D", s=42, color=WHITE, edgecolor=TRUE_BLACK,
               linewidth=1.2, zorder=4, label="Net lifetime balance")
    for idx, value in enumerate(net):
        ax.text(idx + 0.08, value, f"{value:+.1f}", va="center", fontsize=8.5,
                fontweight="bold", color=WHITE)
    ax.axhline(0, color=BLACK, linewidth=1.0)
    ax.set_xticks(x, labels)
    ax.set_ylabel("Cumulative public flow (R trillion)")
    style_axis(ax)
    ax.legend(frameon=False, fontsize=8, loc="upper center",
              bbox_to_anchor=(0.5, 1.08), ncol=4)
    return save_figure(fig, "lifetime-fiscal-balance.png")


def run() -> None:
    set_plot_style()
    WORK_DIR.mkdir(parents=True, exist_ok=True)
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    results = [simulate_profile(profile) for profile in PROFILES]
    results_by_key = {result["profile"]["key"]: result for result in results}
    catchup = catchup_rates()
    cohorts = {
        key: cohort_summary(results_by_key, mix)
        for key, mix in COHORT_MIXES.items()
    }

    figures = {
        "wealth_paths": str(build_wealth_paths_figure(results)),
        "income_ladder": str(build_income_ladder_figure(results)),
        "catchup": str(build_catchup_figure(catchup)),
        "fiscal_wave": str(build_fiscal_wave_figure(cohorts)),
        "lifetime_fiscal": str(build_lifetime_fiscal_figure(cohorts)),
    }
    output = {
        "model_label": "Stylized cohort model, constant 2026 rand",
        "assumptions": {
            "ages": [AGE_START, FINAL_AGE],
            "retirement_age": RETIREMENT_AGE,
            "monthly_wage_at_25": MONTHLY_WAGE_AT_25,
            "real_wage_growth": REAL_WAGE_GROWTH,
            "real_return": REAL_RETURN,
            "maximum_monthly_grant": MAX_GRANT_MONTHLY,
            "grant_full_below_private_pension": GRANT_FULL_BELOW,
            "grant_zero_above_private_pension": GRANT_ZERO_ABOVE,
            "cohort_size": 1_000_000,
            "cohort_mixes": COHORT_MIXES,
        },
        "profiles": results,
        "catchup_rates": catchup,
        "cohorts": cohorts,
        "figures": figures,
    }
    RESULTS_PATH.write_text(json.dumps(output, indent=2), encoding="utf-8")
    print(json.dumps({
        "results": str(RESULTS_PATH),
        "profiles": [
            {
                "name": r["profile"]["name"],
                "employment_years": r["employment_years"],
                "wealth_at_60": round(r["wealth_at_60"]),
                "private_monthly_pension": round(r["private_monthly_pension"]),
                "monthly_grant": round(r["monthly_grant"]),
                "lifetime_taxes": round(r["lifetime_taxes"]),
                "net_fiscal": round(r["lifetime_net_fiscal"]),
            }
            for r in results
        ],
        "catchup": catchup,
        "cohorts": {
            key: {
                "average_monthly_grant": round(value["average_monthly_grant"]),
                "grant_reliant_share": value["grant_reliant_share"],
                "lifetime_taxes_trillion": round(value["lifetime_taxes"] / 1e12, 2),
                "lifetime_net_trillion": round(value["lifetime_net_fiscal"] / 1e12, 2),
            }
            for key, value in cohorts.items()
        },
        "figures": figures,
    }, indent=2))


if __name__ == "__main__":
    run()
