"""GreyScienx Paper 1: The R350 Industrialisation Counterfactual.

This is a transparent thought experiment, not a national forecast. Fiscal-year
SRD expenditure and allocations are mapped to calendar years by their opening
year. Monetary results are constant 2026 rand unless labelled nominal.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import FancyArrowPatch, Rectangle


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "work" / "r350-industrialisation-counterfactual"
ASSETS = OUT / "assets"
ASSETS.mkdir(parents=True, exist_ok=True)

CSS = Path(r"C:\Users\Deriv\Desktop\GreyScienx\app\globals.css")
STYLE_DIR = Path(r"C:\Users\Deriv\Desktop\GreyScienx\skills\greyscienx-editorial-pdf\scripts")
sys.path.insert(0, str(STYLE_DIR))

from greyscienx_style import (  # noqa: E402
    add_figure_header,
    configure_matplotlib,
    save_figure,
    style_axis,
)


TOKENS = configure_matplotlib(CSS)
CORAL = TOKENS["coral"]
BLACK = TOKENS["black"]
TRUE_BLACK = TOKENS["true-black"]
WHITE = TOKENS["white"]
G100 = TOKENS["grey-100"]
G300 = TOKENS["grey-300"]
G500 = TOKENS["grey-500"]
G700 = TOKENS["grey-700"]

FY = ["2020/21", "2021/22", "2022/23", "2023/24", "2024/25", "2025/26", "2026/27"]
YEARS_OF_CONTRIBUTION = np.arange(2020, 2027)

# R billion. 2020/21 and 2021/22 are audited outcomes; 2022/23-2024/25 are
# audited outcomes in the 2026 ENE; 2025/26 is a revised estimate; 2026/27 is
# the current budget estimate.
SRD_NOMINAL = np.array([19.7566, 32.3307, 30.3791, 33.7429, 35.2763, 37.4625, 36.8893])

# Calendar-year CPI indices on a December 2024 = 100 basis. 2020 is derived
# from Stats SA's 2021 average and 2021 inflation; 2025-2026 use the Treasury
# estimates in Budget 2026. They are sufficient for an explicitly approximate
# constant-rand conversion.
CPI_INDEX = np.array([80.38, 84.0, 89.8, 95.1, 99.3, 102.48, 105.96])
SRD_REAL = SRD_NOMINAL * CPI_INDEX[-1] / CPI_INDEX

MODEL_YEARS = np.arange(2020, 2051)
REAL_DEBT_COST = 0.048
CURRENT_ANNUAL_GRANT = 36.8893

SCENARIO_ASSUMPTIONS = {
    "Best": {
        "lag": 2,
        "survival": 0.92,
        "asset_growth": 0.05,
        "public_cash_yield": 0.05,
        "colour": CORAL,
        "linestyle": "-",
        "marker": "o",
    },
    "Average": {
        "lag": 4,
        "survival": 0.68,
        "asset_growth": 0.025,
        "public_cash_yield": 0.03,
        "colour": BLACK,
        "linestyle": "--",
        "marker": "s",
    },
    "Worst": {
        "lag": 6,
        "survival": 0.35,
        "asset_growth": -0.01,
        "public_cash_yield": 0.01,
        "colour": G500,
        "linestyle": ":",
        "marker": "D",
    },
}


def header(fig, title, subtitle):
    add_figure_header(fig, title, subtitle, field="GREYSCIENX / PAPER 1", tokens=TOKENS)


def finish(fig, name, *, left=0.09, right=0.97, top=0.77, bottom=0.13):
    fig.subplots_adjust(left=left, right=right, top=top, bottom=bottom)
    save_figure(fig, ASSETS / name, dpi=260)
    plt.close(fig)


def simulate(lag, survival, asset_growth, public_cash_yield):
    asset = 0.0
    pipeline = []
    cumulative_cash = 0.0
    debt = 0.0
    rows = []
    contributions = dict(zip(YEARS_OF_CONTRIBUTION, SRD_REAL))

    for year in MODEL_YEARS:
        asset *= 1 + asset_growth
        debt *= 1 + REAL_DEBT_COST

        annual_cash = asset * public_cash_yield
        cumulative_cash += annual_cash

        if year in contributions:
            amount = float(contributions[year])
            pipeline.append((year + lag, amount))
            debt += amount

        matured = [(deploy_year, amount) for deploy_year, amount in pipeline if deploy_year <= year]
        pipeline = [(deploy_year, amount) for deploy_year, amount in pipeline if deploy_year > year]
        asset += sum(amount * survival for _, amount in matured)

        pipeline_cash = sum(amount for _, amount in pipeline)
        book_value = asset + pipeline_cash
        net_borrowed_position = book_value + cumulative_cash - debt
        rows.append({
            "year": int(year),
            "productive_asset": asset,
            "pipeline_cash": pipeline_cash,
            "book_value": book_value,
            "annual_public_cash": annual_cash,
            "cumulative_public_cash": cumulative_cash,
            "associated_debt": debt,
            "net_borrowed_position": net_borrowed_position,
        })
    return rows


RESULTS = {
    name: simulate(
        assumptions["lag"],
        assumptions["survival"],
        assumptions["asset_growth"],
        assumptions["public_cash_yield"],
    )
    for name, assumptions in SCENARIO_ASSUMPTIONS.items()
}


def value(name, year, key):
    return next(row[key] for row in RESULTS[name] if row["year"] == year)


def make_srd_ledger():
    fig, ax = plt.subplots(figsize=(9.6, 5.7))
    header(
        fig,
        "The counterfactual begins with a R225.8bn envelope",
        "Completed spending through 2025/26 plus the 2026/27 allocation; 2025/26 is revised and 2026/27 is budgeted",
    )
    x = np.arange(len(FY))
    w = 0.36
    ax.bar(x - w / 2, SRD_NOMINAL, width=w, color=BLACK, label="Nominal expenditure / allocation")
    ax.bar(x + w / 2, SRD_REAL, width=w, color=CORAL, label="Constant 2026 rand")
    for i, (nominal, real) in enumerate(zip(SRD_NOMINAL, SRD_REAL)):
        ax.text(i - w / 2, nominal + 0.8, f"{nominal:.1f}", ha="center", fontsize=6.8)
        ax.text(i + w / 2, real + 0.8, f"{real:.1f}", ha="center", fontsize=6.8, color=CORAL)
    ax.axvline(4.5, color=G500, linewidth=0.8, linestyle=":")
    ax.text(4.55, 47.5, "estimate / budget", color=G500, fontsize=7.2)
    ax.set_xticks(x, FY, rotation=30, ha="right")
    ax.set_ylabel("R billion")
    ax.set_ylim(0, 52)
    ax.legend(frameon=False, fontsize=7.3, ncol=2, loc="upper left")
    style_axis(ax, TOKENS, grid_axis="y")
    finish(fig, "srd-ledger.png", bottom=0.20)


def make_gross_fund_benchmark():
    fig, ax = plt.subplots(figsize=(9.4, 5.5))
    header(
        fig,
        "Compounding alone produces a R257bn-R333bn fund",
        "Mechanical 31 March 2027 value before project delays, impairments, operating costs or debt financing",
    )
    ages = 2027 - (YEARS_OF_CONTRIBUTION + 0.5)
    rates = [0.04, 0.08, 0.12]
    values = [float(np.sum(SRD_NOMINAL * (1 + rate) ** ages)) for rate in rates]
    labels = ["4% nominal return", "8% nominal return", "12% nominal return"]
    colours = [G500, BLACK, CORAL]
    bars = ax.barh(np.arange(3), values, color=colours, height=0.55)
    for bar, val in zip(bars, values):
        ax.text(val + 4, bar.get_y() + bar.get_height() / 2, f"R{val:.0f}bn", va="center", fontsize=9, fontweight="bold")
    ax.axvline(SRD_NOMINAL.sum(), color=BLACK, linewidth=1.0, linestyle=":")
    ax.text(SRD_NOMINAL.sum() + 3, 2.45, f"Contributions: R{SRD_NOMINAL.sum():.1f}bn", fontsize=7.3)
    ax.set_yticks(np.arange(3), labels)
    ax.set_xlabel("Nominal fund value, R billion")
    ax.set_xlim(0, 360)
    style_axis(ax, TOKENS, grid_axis="x")
    finish(fig, "gross-fund-benchmark.png", left=0.23)


def make_fund_anatomy():
    fig, ax = plt.subplots(figsize=(9.6, 5.6))
    header(
        fig,
        "A large fund balance is not the same as factories",
        "End-2026 model snapshot in constant 2026 rand; undeployed cash remains valuable but produces nothing",
    )
    names = list(SCENARIO_ASSUMPTIONS)
    productive = np.array([value(name, 2026, "productive_asset") for name in names])
    pipeline = np.array([value(name, 2026, "pipeline_cash") for name in names])
    x = np.arange(3)
    ax.bar(x, productive, color=[CORAL, BLACK, G500], width=0.58, label="Operating productive assets")
    ax.bar(x, pipeline, bottom=productive, color=G300, width=0.58, label="Undeployed pipeline cash")
    for i in range(3):
        if productive[i] > 25:
            ax.text(i, productive[i] / 2, f"R{productive[i]:.0f}bn\nproductive", ha="center", va="center", fontsize=8,
                    color=WHITE, fontweight="bold")
        else:
            ax.text(i, productive[i] + 4, f"R{productive[i]:.0f}bn productive", ha="center", va="bottom", fontsize=7.4,
                    color=BLACK, fontweight="bold")
        ax.text(i, productive[i] + pipeline[i] / 2, f"R{pipeline[i]:.0f}bn\nwaiting", ha="center", va="center", fontsize=8)
        ax.text(i, productive[i] + pipeline[i] + 7, f"R{productive[i] + pipeline[i]:.0f}bn book value", ha="center", fontsize=7.4)
    ax.set_xticks(x, ["Best\n2-year lag", "Average\n4-year lag", "Worst\n6-year lag"])
    ax.set_ylabel("R billion, constant 2026 rand")
    ax.set_ylim(0, 285)
    ax.legend(frameon=False, fontsize=7.3, ncol=2, loc="upper right")
    style_axis(ax, TOKENS, grid_axis="y")
    finish(fig, "fund-anatomy-2026.png")


def make_asset_paths():
    fig, ax = plt.subplots(figsize=(9.5, 5.6))
    header(
        fig,
        "By 2050, governance dominates the starting endowment",
        "Operating productive assets after deployment losses, depreciation and retained real growth",
    )
    for name, assumptions in SCENARIO_ASSUMPTIONS.items():
        series = [row["productive_asset"] for row in RESULTS[name]]
        ax.plot(MODEL_YEARS, series, linewidth=2.1, color=assumptions["colour"],
                linestyle=assumptions["linestyle"], marker=assumptions["marker"], markevery=5, markersize=3.4, label=name)
        ax.text(2050.35, series[-1], f"R{series[-1]:.0f}bn", va="center", fontsize=7.4, color=assumptions["colour"])
    ax.axvline(2027, color=G500, linewidth=0.8)
    ax.text(2027.4, 730, "No new SRD diversion after 2026/27", fontsize=7.1, color=G500)
    ax.set_xlabel("Year")
    ax.set_ylabel("R billion, constant 2026 rand")
    ax.set_xlim(2020, 2053)
    ax.set_ylim(0, 850)
    ax.legend(frameon=False, fontsize=7.4, loc="upper left")
    style_axis(ax, TOKENS)
    finish(fig, "productive-assets-to-2050.png")


def make_public_cash_paths():
    fig, ax = plt.subplots(figsize=(9.5, 5.6))
    header(
        fig,
        "Only the best case can finance one current SRD year by 2050",
        "Annual public cash yield combines modelled dividends and tax receipts; the R36.9bn line is a fixed 2026 benchmark",
    )
    for name, assumptions in SCENARIO_ASSUMPTIONS.items():
        series = [row["annual_public_cash"] for row in RESULTS[name]]
        ax.plot(MODEL_YEARS, series, linewidth=2.1, color=assumptions["colour"],
                linestyle=assumptions["linestyle"], marker=assumptions["marker"], markevery=5, markersize=3.4, label=name)
        ax.text(2050.35, series[-1], f"R{series[-1]:.1f}bn", va="center", fontsize=7.4, color=assumptions["colour"])
    ax.axhline(CURRENT_ANNUAL_GRANT, color=G500, linewidth=1.0, linestyle="-.")
    ax.text(2020.4, CURRENT_ANNUAL_GRANT + 1.2, "2026/27 SRD allocation: R36.9bn", fontsize=7.2, color=G500)
    ax.set_xlabel("Year")
    ax.set_ylabel("Annual public cash, R billion")
    ax.set_xlim(2020, 2053)
    ax.set_ylim(0, 45)
    ax.legend(frameon=False, fontsize=7.4, loc="upper left", ncol=3, columnspacing=1.4)
    style_axis(ax, TOKENS)
    finish(fig, "public-cash-to-2050.png")


def make_borrowing_test():
    fig, ax = plt.subplots(figsize=(9.5, 5.6))
    header(
        fig,
        "A borrowed industrial fund must beat its funding cost",
        "Fund book value plus cumulative public cash, less associated debt carried at 4.8% real; not a forecast of national debt",
    )
    for name, assumptions in SCENARIO_ASSUMPTIONS.items():
        series = [row["net_borrowed_position"] for row in RESULTS[name]]
        ax.plot(MODEL_YEARS, series, linewidth=2.1, color=assumptions["colour"],
                linestyle=assumptions["linestyle"], marker=assumptions["marker"], markevery=5, markersize=3.4, label=name)
        ax.text(2050.35, series[-1], f"{series[-1]:+.0f}", va="center", fontsize=7.4, color=assumptions["colour"])
    ax.axhline(0, color=BLACK, linewidth=1.0)
    ax.fill_between(MODEL_YEARS, -900, 0, color=G100, alpha=0.55)
    ax.text(2021, -760, "Below zero: debt grows faster than recoverable public value", fontsize=7.3, color=G700)
    ax.set_xlabel("Year")
    ax.set_ylabel("Net public position, R billion (2026 rand)")
    ax.set_xlim(2020, 2053)
    ax.set_ylim(-900, 560)
    ax.legend(frameon=False, fontsize=7.4, loc="upper left")
    style_axis(ax, TOKENS)
    finish(fig, "borrowed-fund-test.png")


def sensitivity_asset_2050(survival, growth, lag=4):
    rows = simulate(lag, survival, growth, 0.0)
    return next(row["productive_asset"] for row in rows if row["year"] == 2050)


def make_sensitivity_heatmap():
    survivals = np.array([0.3, 0.45, 0.6, 0.75, 0.9])
    growths = np.array([-0.02, 0.0, 0.02, 0.04, 0.06])
    matrix = np.array([[sensitivity_asset_2050(s, g) for g in growths] for s in survivals])
    cmap = LinearSegmentedColormap.from_list("grey_coral", [WHITE, G300, G700, CORAL])
    fig, ax = plt.subplots(figsize=(9.0, 6.0))
    header(
        fig,
        "Project survival and real growth multiply each other",
        "2050 productive assets under a four-year deployment lag; values are R billion in constant 2026 rand",
    )
    ax.imshow(matrix, cmap=cmap, aspect="auto")
    ax.set_xticks(range(len(growths)), [f"{g*100:+.0f}%" for g in growths])
    ax.set_yticks(range(len(survivals)), [f"{s*100:.0f}%" for s in survivals])
    ax.set_xlabel("Annual real asset growth after depreciation")
    ax.set_ylabel("Share of committed capital reaching viable operation")
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            val = matrix[i, j]
            ax.text(j, i, f"R{val:.0f}bn", ha="center", va="center", fontsize=7.5,
                    color=WHITE if val > 350 else BLACK, fontweight="bold")
    ax.set_xticks(np.arange(-0.5, len(growths), 1), minor=True)
    ax.set_yticks(np.arange(-0.5, len(survivals), 1), minor=True)
    ax.grid(which="minor", color=WHITE, linewidth=1.3)
    ax.tick_params(which="minor", bottom=False, left=False)
    for spine in ax.spines.values():
        spine.set_visible(False)
    finish(fig, "sensitivity-heatmap.png", left=0.18, bottom=0.16)


def make_r1_lifecycle():
    fig, ax = plt.subplots(figsize=(9.7, 5.7))
    header(
        fig,
        "R1 transferred and R1 invested solve different problems",
        "The comparison is financial and temporal; Paper 2 will value the welfare loss from withholding the grant",
    )
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")
    lanes = [
        (78, "TRANSFER", "R1 reaches a household", "Food, transport, data, debt or job search now", CORAL),
        (50, "FUNDED INDUSTRY", "R1 enters a ring-fenced fund", "Cash -> procurement -> plant -> output -> tax/dividend", BLACK),
        (22, "BORROWED INDUSTRY", "R1 asset is matched by R1 debt", "Value exists only if risk-adjusted return beats funding cost", G500),
    ]
    for y, label, first, second, colour in lanes:
        ax.text(2, y, label, color=colour, fontsize=8, fontweight="bold", va="center")
        ax.add_patch(Rectangle((22, y - 8), 25, 16, facecolor=WHITE, edgecolor=colour, linewidth=1.4))
        ax.text(34.5, y, first, ha="center", va="center", fontsize=8.2, fontweight="bold")
        ax.add_patch(FancyArrowPatch((48, y), (57, y), arrowstyle="-|>", mutation_scale=12, color=colour, linewidth=1.2))
        ax.add_patch(Rectangle((58, y - 8), 39, 16, facecolor=G100, edgecolor="none"))
        ax.text(77.5, y, second, ha="center", va="center", fontsize=7.7, wrap=True)
    ax.text(50, 3, "Immediate security is not a failed factory. A factory is not stored household welfare. The policy problem is allocation across time.",
            ha="center", fontsize=7.6, color=G700)
    finish(fig, "r1-lifecycle.png", left=0.07, right=0.97)


def write_results():
    completed_nominal = float(SRD_NOMINAL[:-1].sum())
    total_nominal = float(SRD_NOMINAL.sum())
    total_real = float(SRD_REAL.sum())
    gross_rates = {}
    ages = 2027 - (YEARS_OF_CONTRIBUTION + 0.5)
    for rate in (0.04, 0.08, 0.12):
        gross_rates[f"{rate:.0%}"] = round(float(np.sum(SRD_NOMINAL * (1 + rate) ** ages)), 2)

    scenarios = {}
    for name, assumptions in SCENARIO_ASSUMPTIONS.items():
        scenarios[name] = {
            "assumptions": {
                "deployment_lag_years": assumptions["lag"],
                "capital_survival_share": assumptions["survival"],
                "real_asset_growth": assumptions["asset_growth"],
                "public_cash_yield": assumptions["public_cash_yield"],
            },
            "2026": {key: round(value(name, 2026, key), 2) for key in (
                "productive_asset", "pipeline_cash", "book_value", "associated_debt", "net_borrowed_position"
            )},
            "2050": {key: round(value(name, 2050, key), 2) for key in (
                "productive_asset", "annual_public_cash", "cumulative_public_cash", "associated_debt", "net_borrowed_position"
            )},
            "productive_asset_per_real_rand_2050": round(value(name, 2050, "productive_asset") / total_real, 2),
        }

    result = {
        "valuation_basis": "constant 2026 rand unless stated",
        "completed_nominal_spending_through_2025_26_r_billion": round(completed_nominal, 2),
        "current_2026_27_allocation_r_billion": round(float(SRD_NOMINAL[-1]), 2),
        "programme_envelope_through_2026_27_nominal_r_billion": round(total_nominal, 2),
        "programme_envelope_constant_2026_r_billion": round(total_real, 2),
        "gross_mechanical_fund_at_march_2027_nominal_r_billion": gross_rates,
        "real_associated_debt_cost": REAL_DEBT_COST,
        "scenarios": scenarios,
    }
    (OUT / "model_results.json").write_text(json.dumps(result, indent=2), encoding="utf-8")


def main():
    make_srd_ledger()
    make_gross_fund_benchmark()
    make_fund_anatomy()
    make_asset_paths()
    make_public_cash_paths()
    make_borrowing_test()
    make_sensitivity_heatmap()
    make_r1_lifecycle()
    write_results()
    print(OUT / "model_results.json")


if __name__ == "__main__":
    main()
