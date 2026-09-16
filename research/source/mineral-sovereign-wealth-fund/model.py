"""Transparent scenario model for GreyScienx Paper 10.

All monetary values are constant 2026 rand billions. The model is deliberately
illustrative: it tests the mechanics of a mineral-linked sovereign wealth fund,
not a forecast of mineral prices, tax receipts or investment returns.
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, Rectangle


ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
CSS = Path(r"C:\Users\Deriv\Desktop\GreyScienx\app\globals.css")
STYLE_DIR = Path(r"C:\Users\Deriv\Desktop\GreyScienx\skills\greyscienx-editorial-pdf\scripts")
sys.path.insert(0, str(STYLE_DIR))

from greyscienx_style import (  # noqa: E402
    add_figure_header,
    configure_matplotlib,
    line_encodings,
    save_figure,
    style_axis,
)


TOKENS = configure_matplotlib(CSS)
ENC = line_encodings(TOKENS)
YEARS = np.arange(2027, 2126)


def interpolate(points: list[tuple[int, float]]) -> np.ndarray:
    x, y = zip(*points)
    return np.interp(YEARS, x, y)


ROYALTY_BASE = interpolate(
    [
        (2027, 12.1),
        (2030, 13.5),
        (2040, 15.0),
        (2050, 13.0),
        (2060, 10.0),
        (2070, 6.0),
        (2080, 3.0),
        (2090, 0.5),
        (2125, 0.0),
    ]
)

DIVIDEND_BASE = interpolate(
    [
        (2027, 0.0),
        (2032, 2.0),
        (2040, 7.0),
        (2050, 9.0),
        (2060, 8.0),
        (2070, 5.0),
        (2080, 2.0),
        (2090, 0.5),
        (2125, 0.0),
    ]
)

RESOURCE_FACTOR = np.clip(ROYALTY_BASE / 12.1, 0.0, None)
WINDFALL_BASE = np.maximum(
    0.0,
    (3.2 + 2.5 * np.sin((YEARS - 2027) * 2 * np.pi / 11.0)) * RESOURCE_FACTOR,
)
ASSET_PROCEEDS = np.where(YEARS <= 2045, 0.5, 0.0)


SCENARIOS = {
    "Best": {
        "seed": 30.0,
        "royalty_share": 0.75,
        "dividend_share": 1.00,
        "windfall_share": 0.65,
        "integrity": 0.98,
        "real_return": 0.045,
        "withdraw_start": 2047,
        "withdraw_rate": 0.025,
    },
    "Central": {
        "seed": 15.0,
        "royalty_share": 0.50,
        "dividend_share": 0.80,
        "windfall_share": 0.40,
        "integrity": 0.92,
        "real_return": 0.040,
        "withdraw_start": 2042,
        "withdraw_rate": 0.030,
    },
    "Adverse": {
        "seed": 5.0,
        "royalty_share": 0.25,
        "dividend_share": 0.45,
        "windfall_share": 0.15,
        "integrity": 0.70,
        "real_return": 0.015,
        "withdraw_start": 2032,
        "withdraw_rate": 0.050,
    },
}


def simulate(config: dict[str, float]) -> dict[str, np.ndarray]:
    royalties = ROYALTY_BASE * config["royalty_share"]
    dividends = DIVIDEND_BASE * config["dividend_share"]
    windfalls = WINDFALL_BASE * config["windfall_share"]
    proceeds = ASSET_PROCEEDS.copy()
    gross = royalties + dividends + windfalls + proceeds
    inflow = gross * config["integrity"]

    balance = np.zeros_like(YEARS, dtype=float)
    withdrawal = np.zeros_like(YEARS, dtype=float)
    investment_return = np.zeros_like(YEARS, dtype=float)
    opening_history: list[float] = [config["seed"]]

    for i, year in enumerate(YEARS):
        opening = config["seed"] if i == 0 else balance[i - 1]
        investment_return[i] = opening * config["real_return"]
        if year >= config["withdraw_start"]:
            trailing = opening_history[-5:]
            target = config["withdraw_rate"] * float(np.mean(trailing))
            withdrawal[i] = min(target, opening + investment_return[i] + inflow[i])
        balance[i] = max(0.0, opening + investment_return[i] + inflow[i] - withdrawal[i])
        opening_history.append(balance[i])

    return {
        "royalties": royalties * config["integrity"],
        "dividends": dividends * config["integrity"],
        "windfalls": windfalls * config["integrity"],
        "proceeds": proceeds * config["integrity"],
        "inflow": inflow,
        "return": investment_return,
        "withdrawal": withdrawal,
        "balance": balance,
    }


RESULTS = {name: simulate(config) for name, config in SCENARIOS.items()}


def new_figure(title: str, subtitle: str, field: str, height: float = 4.55):
    fig = plt.figure(figsize=(7.2, height))
    add_figure_header(fig, title, subtitle, field=field, tokens=TOKENS)
    return fig


def save(fig, name: str):
    save_figure(fig, ASSETS / name, dpi=260)
    plt.close(fig)


def money(v: float) -> str:
    return f"R{v:,.0f}bn"


def figure_flow():
    fig = new_figure(
        "The fund needs a chain of custody, not a new pot of money",
        "Every rand passes through the budget before it becomes a protected financial asset.",
        "GREYSCIENX / FUND ARCHITECTURE",
        4.25,
    )
    ax = fig.add_axes([0.055, 0.11, 0.89, 0.64])
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 55)
    ax.axis("off")

    boxes = [
        (1, 19, 17, 18, "MINERAL\nRENTS", "royalties + dividends"),
        (22, 19, 17, 18, "NATIONAL\nREVENUE FUND", "all receipts recorded"),
        (43, 19, 17, 18, "DEPOSIT\nRULE", "formula, not discretion"),
        (64, 19, 17, 18, "INDEPENDENT\nMANAGER", "global portfolio"),
        (85, 19, 14, 18, "BUDGET\nTRANSFER", "only after the gate"),
    ]
    for i, (x, y, w, h, label, note) in enumerate(boxes):
        fill = TOKENS["coral"] if i in (0, 4) else TOKENS["true-black"]
        text_color = TOKENS["black"] if i in (0, 4) else TOKENS["white"]
        ax.add_patch(Rectangle((x, y), w, h, facecolor=fill, edgecolor="none"))
        ax.text(x + w / 2, y + 11.0, label, ha="center", va="center", color=text_color, fontsize=8.8, fontweight="bold")
        ax.text(x + w / 2, y + 3.7, note, ha="center", va="center", color=text_color, fontsize=6.8)
        if i < len(boxes) - 1:
            nx = boxes[i + 1][0]
            ax.add_patch(FancyArrowPatch((x + w, y + h / 2), (nx, y + h / 2), arrowstyle="-|>", mutation_scale=12, color=TOKENS["grey-500"], linewidth=1.2))

    ax.text(50, 7.2, "The industrial holding company remains legally separate from the savings portfolio.", ha="center", fontsize=8.2, fontweight="bold")
    ax.text(50, 3.0, "That separation prevents a failed factory from becoming an automatic claim on retirement savings.", ha="center", fontsize=7.5, color=TOKENS["grey-700"])
    save(fig, "fund-flow.png")


def figure_royalties():
    years = np.arange(2022, 2029)
    values = np.array([25.338, 15.979, 10.636, 11.805, 12.145, 12.762, 13.527])
    fig = new_figure(
        "The revenue base is small and visibly cyclical",
        "Actual to 2024/25; National Treasury estimates and forecasts thereafter.",
        "GREYSCIENX / MINERAL ROYALTIES",
    )
    ax = fig.add_axes([0.11, 0.16, 0.84, 0.59])
    colours = [TOKENS["grey-700"]] * 3 + [TOKENS["coral"]] * 4
    bars = ax.bar(years, values, color=colours, width=0.68, zorder=3)
    style_axis(ax, TOKENS)
    ax.set_ylabel("Mineral and petroleum royalties (Rbn)")
    ax.set_xlabel("Fiscal year ending")
    ax.set_xticks(years, [f"{y}/{str(y+1)[-2:]}" for y in years], rotation=25, ha="right")
    ax.set_ylim(0, 30)
    for bar, value in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, value + 0.7, f"R{value:.1f}bn", ha="center", fontsize=7.3, fontweight="bold")
    ax.text(2023.2, 27.6, "Commodity boom residue", fontsize=7.3, color=TOKENS["grey-500"])
    ax.text(2025.1, 7.2, "Budget path", fontsize=7.3, color=TOKENS["coral"], fontweight="bold")
    save(fig, "royalties.png")


def figure_deposits():
    r = RESULTS["Central"]
    fig = new_figure(
        "The deposit stream changes before it disappears",
        "Central case, constant 2026 rand; deposits are scenarios, not revenue forecasts.",
        "GREYSCIENX / CENTRAL INFLOWS",
    )
    ax = fig.add_axes([0.10, 0.16, 0.85, 0.59])
    ax.stackplot(
        YEARS,
        r["royalties"],
        r["dividends"],
        r["windfalls"],
        r["proceeds"],
        colors=[TOKENS["coral"], TOKENS["black"], TOKENS["grey-500"], TOKENS["grey-300"]],
        labels=["saved royalties", "public dividends", "windfall tax share", "asset proceeds"],
        alpha=0.96,
    )
    style_axis(ax, TOKENS)
    ax.set_xlim(2027, 2100)
    ax.set_ylabel("Annual deposit (Rbn)")
    ax.set_xlabel("Year")
    ax.legend(frameon=False, ncol=2, loc="upper right", fontsize=7.2)
    ax.axvline(2042, color=TOKENS["black"], linewidth=1, linestyle="--")
    ax.text(2043, 1.3, "withdrawals may begin", fontsize=7.2, color=TOKENS["grey-700"])
    save(fig, "deposit-stream.png")


def figure_balances():
    fig = new_figure(
        "Rules dominate the century-long result",
        "Fund value after deposits, real returns and rule-based withdrawals.",
        "GREYSCIENX / FUND PATHS",
    )
    ax = fig.add_axes([0.11, 0.16, 0.84, 0.59])
    for (name, result), style in zip(RESULTS.items(), ENC):
        ax.plot(YEARS, result["balance"], label=name, linewidth=2.0, markevery=10, markersize=3.8, **style)
    style_axis(ax, TOKENS)
    ax.set_xlim(2027, 2125)
    ax.set_ylabel("Fund value (Rbn, constant 2026 rand)")
    ax.set_xlabel("Year")
    ax.legend(frameon=False, loc="upper left", ncol=3)
    for name, result in RESULTS.items():
        ax.text(2123, result["balance"][-1], f"{name}: {money(result['balance'][-1])}", ha="right", va="center", fontsize=7.3, fontweight="bold")
    ax.margins(x=0.01)
    save(fig, "fund-paths.png")


def figure_withdrawals():
    fig = new_figure(
        "A permanent fund pays late and modestly",
        "Annual transfers in each scenario; early spending makes the adverse fund run down.",
        "GREYSCIENX / WITHDRAWAL RULE",
    )
    ax = fig.add_axes([0.11, 0.16, 0.84, 0.59])
    for (name, result), style in zip(RESULTS.items(), ENC):
        ax.plot(YEARS, result["withdrawal"], label=name, linewidth=2.0, markevery=10, markersize=3.8, **style)
    style_axis(ax, TOKENS)
    ax.set_xlim(2027, 2125)
    ax.set_ylabel("Annual budget transfer (Rbn)")
    ax.set_xlabel("Year")
    ax.legend(frameon=False, loc="upper left", ncol=3)
    save(fig, "withdrawals.png")


def figure_budget_scale():
    central = RESULTS["Central"]
    transfer_2060 = float(central["withdrawal"][np.where(YEARS == 2060)[0][0]])
    labels = ["Fund transfer\n2060", "Mineral royalties\n2026/27", "Old-age grant\n2026/27", "Economic development\n2026/27", "Debt-service costs\n2026/27"]
    values = [transfer_2060, 12.145, 121.8, 283.9, 432.4]
    fig = new_figure(
        "Even a successful fund does not replace the budget",
        "Central-case transfer compared with current expenditure and royalty scales.",
        "GREYSCIENX / FISCAL SCALE",
    )
    ax = fig.add_axes([0.24, 0.15, 0.71, 0.61])
    y = np.arange(len(labels))
    bars = ax.barh(y, values, color=[TOKENS["coral"], TOKENS["grey-500"], TOKENS["black"], TOKENS["grey-700"], TOKENS["true-black"]], height=0.62)
    style_axis(ax, TOKENS, grid_axis="x")
    ax.set_yticks(y, labels)
    ax.invert_yaxis()
    ax.set_xlabel("R billion, constant 2026 rand for modelled transfer")
    for bar, value in zip(bars, values):
        ax.text(value + 5, bar.get_y() + bar.get_height() / 2, money(value), va="center", fontsize=7.5, fontweight="bold")
    ax.set_xlim(0, 485)
    save(fig, "budget-scale.png")


def ending_balance(return_rate: float, withdrawal_rate: float) -> float:
    balance = 15.0
    history = [balance]
    for year in range(2027, 2126):
        inflow = 12.0 if year <= 2080 else 0.0
        draw = 0.0
        if year >= 2042:
            draw = withdrawal_rate * float(np.mean(history[-5:]))
        balance = max(0.0, balance * (1 + return_rate) + inflow - draw)
        history.append(balance)
    return balance


def figure_sustainability():
    returns = np.array([0.01, 0.02, 0.03, 0.04, 0.05, 0.06])
    draws = np.array([0.02, 0.03, 0.04, 0.05, 0.06])
    grid = np.array([[ending_balance(r, d) for r in returns] for d in draws])
    fig = new_figure(
        "A spending rule cannot outrun the portfolio forever",
        "Fund value in 2125 after R12bn annual deposits through 2080; constant 2026 rand.",
        "GREYSCIENX / SUSTAINABILITY MAP",
    )
    ax = fig.add_axes([0.14, 0.16, 0.77, 0.59])
    im = ax.imshow(grid, cmap="Greys", aspect="auto", origin="upper")
    ax.set_xticks(np.arange(len(returns)), [f"{r*100:.0f}%" for r in returns])
    ax.set_yticks(np.arange(len(draws)), [f"{d*100:.0f}%" for d in draws])
    ax.set_xlabel("Long-run real return")
    ax.set_ylabel("Withdrawal rate")
    for i in range(len(draws)):
        for j in range(len(returns)):
            value = grid[i, j]
            colour = TOKENS["white"] if value > np.nanmax(grid) * 0.45 else TOKENS["black"]
            label = "depleted" if value < 1 else money(value)
            ax.text(j, i, label, ha="center", va="center", fontsize=7.0, color=colour, fontweight="bold")
    ax.add_patch(Rectangle((2.5, 0.5), 1, 1, fill=False, edgecolor=TOKENS["coral"], linewidth=2.5))
    fig.colorbar(im, ax=ax, fraction=0.034, pad=0.03, label="Ending fund value (Rbn)")
    save(fig, "sustainability-map.png")


def annuity_future_value(payment: float, rate: float, years: int) -> float:
    if rate == 0:
        return payment * years
    return payment * (((1 + rate) ** years - 1) / rate)


def figure_debt_tradeoff():
    values = [
        annuity_future_value(12.0, 0.04, 15),
        annuity_future_value(12.0, 0.05, 15),
    ]
    fig = new_figure(
        "Saving while borrowing can create negative carry",
        "Fifteen annual R12bn allocations: invest at 4% real or avoid debt compounding at 5% real.",
        "GREYSCIENX / DEBT TRADE-OFF",
    )
    ax = fig.add_axes([0.19, 0.16, 0.72, 0.59])
    bars = ax.bar([0, 1], values, color=[TOKENS["coral"], TOKENS["black"]], width=0.58, zorder=3)
    style_axis(ax, TOKENS)
    ax.set_xticks([0, 1], ["Build the fund", "Reduce borrowing"])
    ax.set_ylabel("Value after 15 years (Rbn, constant 2026 rand)")
    ax.set_ylim(0, max(values) * 1.22)
    for bar, value in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, value + 5, money(value), ha="center", fontsize=8, fontweight="bold")
    gap = values[1] - values[0]
    ax.text(0.5, max(values) * 1.11, f"Debt-first advantage: {money(gap)}", ha="center", color=TOKENS["grey-700"], fontsize=8, fontweight="bold")
    save(fig, "debt-tradeoff.png")


def figure_portfolio():
    labels = ["Global equities", "Global bonds", "Inflation-linked / cash", "Domestic liquid assets"]
    shares = [55, 25, 10, 10]
    colours = [TOKENS["coral"], TOKENS["black"], TOKENS["grey-500"], TOKENS["grey-300"]]
    fig = new_figure(
        "The savings portfolio should diversify away from the mine",
        "Illustrative central allocation; domestic industrial equity sits in a separate holding company.",
        "GREYSCIENX / PORTFOLIO DESIGN",
    )
    ax = fig.add_axes([0.08, 0.10, 0.48, 0.66])
    wedges, _ = ax.pie(shares, colors=colours, startangle=90, counterclock=False, wedgeprops={"linewidth": 1.2, "edgecolor": TOKENS["white"]})
    ax.set_aspect("equal")
    ax2 = fig.add_axes([0.59, 0.18, 0.36, 0.51])
    ax2.axis("off")
    for i, (label, share, colour) in enumerate(zip(labels, shares, colours)):
        y = 0.90 - i * 0.21
        ax2.add_patch(Rectangle((0.0, y - 0.035), 0.06, 0.07, facecolor=colour, edgecolor="none", transform=ax2.transAxes))
        ax2.text(0.09, y + 0.015, f"{share}%", transform=ax2.transAxes, fontsize=10, fontweight="bold", va="center")
        ax2.text(0.09, y - 0.045, label, transform=ax2.transAxes, fontsize=7.5, color=TOKENS["grey-700"], va="center")
    save(fig, "portfolio.png")


def figure_governance():
    fig = new_figure(
        "Four locks protect the future claim",
        "Each lock answers a different political or financial failure mode.",
        "GREYSCIENX / GOVERNANCE",
        4.35,
    )
    ax = fig.add_axes([0.055, 0.10, 0.89, 0.66])
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 50)
    ax.axis("off")
    items = [
        ("01", "LEGAL LOCK", "Deposits and withdrawals\nset in primary legislation"),
        ("02", "BUDGET LOCK", "Every flow appears in the\nNational Revenue Fund"),
        ("03", "MANAGEMENT LOCK", "Independent mandate,\nbenchmark,\nannual audit"),
        ("04", "SPENDING LOCK", "Trailing-value rule, cap,\nand narrow escape clause"),
    ]
    for i, (num, title, body) in enumerate(items):
        x = 1 + i * 25
        fill = TOKENS["coral"] if i in (0, 3) else TOKENS["true-black"]
        fg = TOKENS["black"] if i in (0, 3) else TOKENS["white"]
        ax.add_patch(Rectangle((x, 12), 22, 27, facecolor=fill, edgecolor="none"))
        ax.text(x + 2.4, 35.5, num, color=fg, fontsize=15, fontweight="bold", va="top")
        ax.text(x + 2.4, 27.5, title, color=fg, fontsize=8.3, fontweight="bold", va="top")
        ax.text(x + 2.4, 20.5, body, color=fg, fontsize=7.3, va="top", linespacing=1.35)
    ax.text(50, 4.2, "An escape clause should delay or cap a transfer - never permit an undocumented raid.", ha="center", fontsize=7.6, color=TOKENS["grey-700"], fontweight="bold")
    save(fig, "governance.png")


def main():
    ASSETS.mkdir(parents=True, exist_ok=True)
    figure_flow()
    figure_royalties()
    figure_deposits()
    figure_balances()
    figure_withdrawals()
    figure_budget_scale()
    figure_sustainability()
    figure_debt_tradeoff()
    figure_portfolio()
    figure_governance()

    central = RESULTS["Central"]
    idx = {year: int(np.where(YEARS == year)[0][0]) for year in (2042, 2060, 2080, 2100, 2125)}
    summary = {
        "units": "constant 2026 rand billions",
        "central_fund_value": {str(year): round(float(central["balance"][i]), 1) for year, i in idx.items()},
        "central_transfer": {str(year): round(float(central["withdrawal"][i]), 1) for year, i in idx.items()},
        "ending_fund_values": {name: round(float(result["balance"][-1]), 1) for name, result in RESULTS.items()},
        "cumulative_central_deposits": round(float(np.sum(central["inflow"])), 1),
        "cumulative_central_transfers": round(float(np.sum(central["withdrawal"])), 1),
        "model_years": [int(YEARS[0]), int(YEARS[-1])],
    }
    (ROOT / "model_results.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    print("Wrote 10 figures")


if __name__ == "__main__":
    main()
