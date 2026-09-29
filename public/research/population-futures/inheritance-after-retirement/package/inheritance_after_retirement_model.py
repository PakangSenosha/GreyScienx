"""GreyScienx armchair model for inheritance in a long-life society.

The model compares inheritances received at ages 40, 55, 70 and 85 with a
living transfer at 35. It also tests capital compounding, first-home timing,
business runway, simplified South African transfer-tax wedges, parental
retirement reserves and three-generation wealth paths. All money is constant
2026 rand. The results are scenarios, not forecasts or tax advice.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
WORK_DIR = ROOT / "work" / "inheritance-after-retirement"
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


TRANSFER = 1_000_000.0
RECEIPT_AGES = [35, 40, 55, 70, 85]
FINAL_AGE = 100
START_MONTHLY_SALARY = 30_000.0
REAL_WAGE_GROWTH = 0.012
SALARY_SAVING_RATE = 0.03
PORTFOLIO_RETURN = 0.04
HOME_PRICE = 1_800_000.0
HOME_DEPOSIT = 0.20 * HOME_PRICE
BUSINESS_CAPITAL = 250_000.0


def future_value(amount: float, years: int, rate: float) -> float:
    return amount * ((1 + rate) ** years)


def donation_tax(gift: float) -> float:
    """Simplified 2026/27 donation tax for one natural-person donor."""
    taxable = max(0.0, gift - 150_000.0)
    return 0.20 * min(taxable, 30_000_000.0) + 0.25 * max(0.0, taxable - 30_000_000.0)


def estate_duty(net_estate: float) -> float:
    """Simplified duty after only the R3.5m general abatement."""
    dutiable = max(0.0, net_estate - 3_500_000.0)
    return 0.20 * min(dutiable, 30_000_000.0) + 0.25 * max(0.0, dutiable - 30_000_000.0)


def gift_from_total_budget(budget: float) -> float:
    """Largest gift when the tax must also be paid from the donor's budget."""
    low, high = 0.0, budget
    for _ in range(100):
        mid = (low + high) / 2
        if mid + donation_tax(mid) <= budget:
            low = mid
        else:
            high = mid
    return low


def deposit_age_without_transfer() -> int:
    balance = 0.0
    for age in range(25, 101):
        salary = START_MONTHLY_SALARY * 12 * ((1 + REAL_WAGE_GROWTH) ** (age - 25))
        balance *= 1 + PORTFOLIO_RETURN
        balance += salary * SALARY_SAVING_RATE
        if balance >= HOME_DEPOSIT:
            return age
    return 101


def retirement_reserve(lifespan: int, parent_age: int = 65) -> float:
    annual_income_gap = 5_000.0 * 12
    care_buffer = 500_000.0
    years = max(0, lifespan - parent_age)
    if years == 0:
        income_reserve = 0.0
    else:
        income_reserve = annual_income_gap * (1 - (1 + 0.03) ** (-years)) / 0.03
    return income_reserve + care_buffer


def dynasty_paths() -> dict[str, float]:
    initial = 2_000_000.0
    elder_return = 0.04

    gen1_estate = future_value(initial, 35, elder_return)
    gen1_receipt = gen1_estate - estate_duty(gen1_estate)
    gen2_estate = future_value(gen1_receipt, 30, elder_return)
    late_final = gen2_estate - estate_duty(gen2_estate)

    def early_path(recipient_return: float) -> float:
        gen1_gift = gift_from_total_budget(initial)
        gen1_wealth_at_65 = future_value(gen1_gift, 30, recipient_return)
        gen2_gift = gift_from_total_budget(gen1_wealth_at_65)
        return future_value(gen2_gift, 35, recipient_return)

    return {
        "late_bequests_4pct": late_final,
        "early_gifts_4pct": early_path(0.04),
        "early_gifts_5pct": early_path(0.05),
        "no_tax_neutral_4pct": future_value(initial, 65, 0.04),
    }


def make_results() -> dict:
    timing = {
        str(age): {
            str(int(rate * 100)): future_value(TRANSFER, FINAL_AGE - age, rate)
            for rate in (0.02, 0.04, 0.06)
        }
        for age in RECEIPT_AGES
    }

    purpose_shares = {
        "35": [0.40, 0.30, 0.15, 0.10, 0.05],
        "40": [0.35, 0.30, 0.15, 0.15, 0.05],
        "55": [0.20, 0.15, 0.10, 0.40, 0.15],
        "70": [0.05, 0.05, 0.00, 0.50, 0.40],
        "85": [0.00, 0.00, 0.00, 0.30, 0.70],
    }

    baseline_home_age = deposit_age_without_transfer()
    opportunity = {}
    for age in RECEIPT_AGES:
        purchase_age = age if age <= baseline_home_age else baseline_home_age
        opportunity[str(age)] = {
            "first_home_purchase_age": purchase_age,
            "years_earlier_than_baseline": max(0, baseline_home_age - age),
            "business_runway_to_65": max(0, 65 - age),
        }

    tax_examples = {}
    for budget in (1_000_000.0, 10_000_000.0, 40_000_000.0):
        gift = gift_from_total_budget(budget)
        bequest = budget - estate_duty(budget)
        tax_examples[str(int(budget))] = {
            "donor_budget": budget,
            "living_gift_received": gift,
            "donations_tax": budget - gift,
            "bequest_received": bequest,
            "estate_duty": budget - bequest,
        }

    safe_transfers = {
        str(lifespan): {
            str(int(wealth)): max(0.0, wealth - retirement_reserve(lifespan))
            for wealth in (2_000_000.0, 5_000_000.0, 10_000_000.0)
        }
        for lifespan in (85, 100, 120)
    }

    compounding_80 = {
        str(int(rate * 100)): future_value(TRANSFER, 80, rate)
        for rate in (0.02, 0.04, 0.06)
    }

    return {
        "study": "Inheritance After Retirement",
        "prices": "constant 2026 rand",
        "core_assumptions": {
            "transfer": TRANSFER,
            "final_age": FINAL_AGE,
            "start_monthly_salary": START_MONTHLY_SALARY,
            "real_wage_growth": REAL_WAGE_GROWTH,
            "salary_saving_rate": SALARY_SAVING_RATE,
            "portfolio_return": PORTFOLIO_RETURN,
            "home_price": HOME_PRICE,
            "home_deposit": HOME_DEPOSIT,
            "business_capital": BUSINESS_CAPITAL,
        },
        "value_at_100": timing,
        "purpose_shares": purpose_shares,
        "baseline_first_home_age": baseline_home_age,
        "opportunity": opportunity,
        "tax_examples": tax_examples,
        "safe_transfers": safe_transfers,
        "dynasty_paths": dynasty_paths(),
        "compounding_80_years": compounding_80,
        "warnings": [
            "Receipt ages and uses are scenarios, not forecasts of South African households.",
            "Tax cases simplify 2026/27 rules and exclude CGT, transfer duty, spouse deductions, trusts, expenses and avoidance.",
            "The dynasty model assumes fixed real returns, 100-year lives and 30-year generation gaps.",
            "The safe-transfer test is an illustrative reserve rule, not financial advice.",
        ],
    }


def make_figures(data: dict) -> None:
    set_plot_style()

    # Figure 1: value at age 100 by transfer age and return.
    fig, ax = plt.subplots(figsize=(10.6, 5.5))
    figure_header(
        fig, "Figure 1", "Inheritance loses economic runway as it arrives later",
        "Value at age 100 of R1 million received at each age; age 35 is a living-transfer reference."
    )
    styles = [
        ("2", GREY_500, ":", "D", "2% real return"),
        ("4", BLACK, "--", "s", "4% real return"),
        ("6", CORAL, "-", "o", "6% real return"),
    ]
    for key, color, line, marker, label in styles:
        values = [data["value_at_100"][str(age)][key] / 1e6 for age in RECEIPT_AGES]
        ax.plot(RECEIPT_AGES, values, color=color, linestyle=line, marker=marker,
                linewidth=2.2, markersize=6, label=label)
    ax.axvline(65, color=GREY_300, linewidth=1.2)
    ax.text(65, ax.get_ylim()[1] * 0.93, "conventional retirement age", rotation=90,
            ha="right", va="top", color=GREY_700, fontsize=8)
    ax.set_xlabel("Age when capital arrives")
    ax.set_ylabel("Value at age 100, R million")
    ax.set_xticks(RECEIPT_AGES, ["35 gift", "40", "55", "70", "85"])
    style_axis(ax)
    ax.legend(loc="upper right", frameon=False, ncol=1)
    fig.subplots_adjust(left=0.09, right=0.92, bottom=0.14, top=0.75)
    save_figure(fig, "inheritance-timing.png")

    # Figure 2: the purpose of capital changes with receipt age.
    fig, ax = plt.subplots(figsize=(10.6, 5.5))
    figure_header(
        fig, "Figure 2", "Capital gradually changes from formation to transmission",
        "Illustrative allocation of a transfer by recipient age; shares sum to 100 percent."
    )
    categories = ["Home formation", "Business / study", "Debt reduction", "Retirement / care", "Onward transfer"]
    colors = [CORAL, BLACK, GREY_700, GREY_300, GREY_500]
    hatches = [None, None, "//", "..", "xx"]
    y_positions = np.arange(len(RECEIPT_AGES))
    left = np.zeros(len(RECEIPT_AGES))
    for idx, category in enumerate(categories):
        vals = np.array([data["purpose_shares"][str(age)][idx] * 100 for age in RECEIPT_AGES])
        bars = ax.barh(y_positions, vals, left=left, color=colors[idx], height=0.62,
                       label=category, hatch=hatches[idx], edgecolor=BLACK if hatches[idx] else colors[idx],
                       linewidth=0.6 if hatches[idx] else 0)
        for bar, value, start in zip(bars, vals, left):
            if value >= 15:
                text_color = WHITE if idx in (1, 2, 4) else BLACK
                ax.text(start + value / 2, bar.get_y() + bar.get_height() / 2,
                        f"{value:.0f}%", ha="center", va="center", color=text_color,
                        fontsize=8, fontweight="bold")
        left += vals
    ax.set_xlabel("Share of transfer")
    ax.set_ylabel("Age when capital arrives")
    ax.set_yticks(y_positions, [str(age) for age in RECEIPT_AGES])
    ax.set_xlim(0, 100)
    style_axis(ax, grid_axis="x")
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.37), ncol=3, frameon=False)
    fig.subplots_adjust(left=0.11, right=0.97, bottom=0.32, top=0.75)
    save_figure(fig, "capital-purpose.png")

    # Figure 3: capital access for home and enterprise formation.
    fig, axes = plt.subplots(1, 2, figsize=(10.6, 5.3))
    figure_header(
        fig, "Figure 3", "Late inheritance misses the first-home and enterprise windows",
        "R30,000 starting monthly salary; 3 percent salary saving; R360,000 home deposit; retirement at 65."
    )
    ages = RECEIPT_AGES
    baseline = data["baseline_first_home_age"]
    purchase = [data["opportunity"][str(age)]["first_home_purchase_age"] for age in ages]
    axes[0].bar(range(len(ages)), purchase, color=[CORAL, CORAL, GREY_500, GREY_500, GREY_500])
    axes[0].axhline(baseline, color=BLACK, linestyle="--", linewidth=1.4, label=f"No transfer: age {baseline}")
    axes[0].set_xticks(range(len(ages)), [str(age) for age in ages])
    axes[0].set_xlabel("Age when transfer arrives")
    axes[0].set_ylabel("Age of first-home purchase")
    axes[0].set_title("First-home entry")
    axes[0].set_ylim(25, 58)
    axes[0].legend(frameon=False, loc="upper left")
    for x, value in enumerate(purchase):
        axes[0].text(x, value + 0.8, str(value), ha="center", fontsize=8)
    style_axis(axes[0])

    runway = [data["opportunity"][str(age)]["business_runway_to_65"] for age in ages]
    axes[1].bar(range(len(ages)), runway, color=[CORAL, CORAL, GREY_500, GREY_300, GREY_300])
    axes[1].set_xticks(range(len(ages)), [str(age) for age in ages])
    axes[1].set_xlabel("Age when transfer arrives")
    axes[1].set_ylabel("Years before age 65")
    axes[1].set_title("Runway for a capital-funded business")
    axes[1].set_ylim(0, 34)
    for x, value in enumerate(runway):
        axes[1].text(x, value + 0.8, str(value), ha="center", fontsize=8)
    style_axis(axes[1])
    fig.subplots_adjust(left=0.08, right=0.97, bottom=0.15, top=0.70, wspace=0.25)
    save_figure(fig, "housing-business-windows.png")

    # Figure 6: three-generation paths.
    fig, ax = plt.subplots(figsize=(10.6, 5.4))
    figure_header(
        fig, "Figure 6", "Earlier ownership matters only when the heir can use it better",
        "Gen 0 starts with R2m at 65; Gen 2 is measured at 70; simplified transfer taxes included."
    )
    labels = ["Late bequests\n4% return", "Early gifts\n4% return", "Early gifts\n5% return"]
    keys = ["late_bequests_4pct", "early_gifts_4pct", "early_gifts_5pct"]
    values = [data["dynasty_paths"][key] / 1e6 for key in keys]
    bars = ax.bar(range(3), values, color=[BLACK, GREY_500, CORAL], width=0.62)
    benchmark = data["dynasty_paths"]["no_tax_neutral_4pct"] / 1e6
    ax.axhline(benchmark, color=BLACK, linestyle=":", linewidth=1.4,
               label=f"No-tax 4% benchmark: R{benchmark:.1f}m")
    for bar, value in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, value + 0.8, f"R{value:.1f}m",
                ha="center", fontsize=9, fontweight="bold")
    ax.set_xticks(range(3), labels)
    ax.set_ylabel("Gen 2 wealth at age 70, R million")
    style_axis(ax)
    ax.legend(frameon=False, loc="upper left")
    fig.subplots_adjust(left=0.10, right=0.97, bottom=0.19, top=0.72)
    save_figure(fig, "dynasty-paths.png")

    # Figure 5: eighty years of compounding.
    fig, ax = plt.subplots(figsize=(10.6, 5.3))
    figure_header(
        fig, "Figure 5", "Eighty years turns small return differences into dynasties",
        "Future value of R1m in constant 2026 rand; log scale keeps all three outcomes visible."
    )
    rates = [2, 4, 6]
    values = [data["compounding_80_years"][str(rate)] / 1e6 for rate in rates]
    bars = ax.bar(range(3), values, color=[GREY_500, BLACK, CORAL], width=0.58)
    ax.set_yscale("log")
    ax.set_xticks(range(3), [f"{rate}% real" for rate in rates])
    ax.set_xlabel("Annual return")
    ax.set_ylabel("Value after 80 years, R million (log scale)")
    for bar, value in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, value * 1.14, f"R{value:.1f}m",
                ha="center", fontsize=9, fontweight="bold")
    style_axis(ax)
    fig.subplots_adjust(left=0.11, right=0.97, bottom=0.15, top=0.72)
    save_figure(fig, "eighty-year-compounding.png")

    # Figure 4: safe transfer frontier.
    fig, ax = plt.subplots(figsize=(10.6, 5.5))
    figure_header(
        fig, "Figure 4", "A parent cannot gift wealth that may finance another 55 years",
        "Safe gift after reserving a R5,000 monthly income gap plus R500,000 care buffer at age 65."
    )
    wealths = [2, 5, 10]
    x = np.arange(len(wealths))
    width = 0.23
    cases = [(85, CORAL, "-", "Life to 85"), (100, BLACK, "//", "Life to 100"), (120, GREY_500, "..", "Life to 120")]
    for offset, (lifespan, color, hatch, label) in enumerate(cases):
        vals = [data["safe_transfers"][str(lifespan)][str(int(w * 1e6))] / 1e6 for w in wealths]
        bars = ax.bar(x + (offset - 1) * width, vals, width=width, color=color,
                      hatch=hatch, edgecolor=BLACK if hatch else color, linewidth=0.6, label=label)
        for bar, value in zip(bars, vals):
            ax.text(bar.get_x() + bar.get_width() / 2, value + 0.12, f"{value:.1f}",
                    ha="center", va="bottom", fontsize=7.4)
    ax.set_xticks(x, [f"R{w}m" for w in wealths])
    ax.set_xlabel("Parent wealth at age 65")
    ax.set_ylabel("Illustrative safe living transfer, R million")
    style_axis(ax)
    ax.legend(loc="upper left", frameon=False, ncol=3)
    fig.subplots_adjust(left=0.10, right=0.97, bottom=0.15, top=0.72)
    save_figure(fig, "safe-transfer-frontier.png")


def main() -> None:
    WORK_DIR.mkdir(parents=True, exist_ok=True)
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    data = make_results()
    RESULTS_PATH.write_text(json.dumps(data, indent=2), encoding="utf-8")
    make_figures(data)
    display = {
        "value_at_100_4pct_m": {
            age: round(values["4"] / 1e6, 2)
            for age, values in data["value_at_100"].items()
        },
        "baseline_first_home_age": data["baseline_first_home_age"],
        "dynasty_paths_m": {
            key: round(value / 1e6, 2)
            for key, value in data["dynasty_paths"].items()
        },
        "compounding_80_years_m": {
            key: round(value / 1e6, 2)
            for key, value in data["compounding_80_years"].items()
        },
        "safe_transfer_r2m": {
            life: round(values["2000000"] / 1e6, 2)
            for life, values in data["safe_transfers"].items()
        },
    }
    print(json.dumps(display, indent=2))


if __name__ == "__main__":
    main()
