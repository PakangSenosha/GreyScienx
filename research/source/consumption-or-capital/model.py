from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap, Normalize


WORK = Path(__file__).resolve().parent
ASSETS = WORK / "assets"
ASSETS.mkdir(parents=True, exist_ok=True)

STYLE_DIR = Path(r"C:\Users\Deriv\Desktop\GreyScienx\skills\greyscienx-editorial-pdf\scripts")
sys.path.insert(0, str(STYLE_DIR))
from greyscienx_style import add_figure_header, configure_matplotlib, save_figure, style_axis  # noqa: E402


TOKENS = configure_matplotlib(Path(r"C:\Users\Deriv\Desktop\GreyScienx\app\globals.css"))
CORAL = TOKENS["coral"]
BLACK = TOKENS["black"]
WHITE = TOKENS["white"]
G100 = TOKENS["grey-100"]
G300 = TOKENS["grey-300"]
G500 = TOKENS["grey-500"]
G700 = TOKENS["grey-700"]

CONTRIBUTION_YEARS = np.arange(2020, 2027)
SRD_REAL = np.array([26.04390814, 40.78286871, 35.84598481, 37.59619016, 37.64226332, 38.73464578, 36.8893])
YEARS = np.arange(2020, 2101)
MAIN_END = 2075

TRANSFER = {
    "Conservative": {"total": 237.26, "colour": G500, "linestyle": ":", "marker": "D"},
    "Central": {"total": 426.89, "colour": BLACK, "linestyle": "--", "marker": "s"},
    "Severe": {"total": 742.78, "colour": CORAL, "linestyle": "-", "marker": "o"},
}

INDUSTRY = {
    "Best": {
        "lag": 2,
        "survival": 0.92,
        "asset_growth": 0.05,
        "public_cash_yield": 0.05,
        "social_spillover_yield": 0.04,
        "colour": CORAL,
        "linestyle": "-",
        "marker": "o",
    },
    "Average": {
        "lag": 4,
        "survival": 0.68,
        "asset_growth": 0.025,
        "public_cash_yield": 0.03,
        "social_spillover_yield": 0.025,
        "colour": BLACK,
        "linestyle": "--",
        "marker": "s",
    },
    "Worst": {
        "lag": 6,
        "survival": 0.35,
        "asset_growth": -0.01,
        "public_cash_yield": 0.01,
        "social_spillover_yield": 0.005,
        "colour": G500,
        "linestyle": ":",
        "marker": "D",
    },
}

DISCOUNT_RATES = [0.035, 0.06, 0.10]


def header(fig, title, subtitle):
    add_figure_header(fig, title, subtitle, field="GREYSCIENCX / PAPER 3", tokens=TOKENS)


def finish(fig, filename, *, left=0.09, right=0.97, top=0.77, bottom=0.13):
    fig.subplots_adjust(left=left, right=right, top=top, bottom=bottom)
    save_figure(fig, ASSETS / filename, dpi=260)
    plt.close(fig)


def simulate_industry(params):
    asset = 0.0
    pipeline = []
    rows = []
    contributions = dict(zip(CONTRIBUTION_YEARS, SRD_REAL))
    for year in YEARS:
        asset *= 1 + params["asset_growth"]
        public_cash = asset * params["public_cash_yield"]
        spillover = asset * params["social_spillover_yield"]

        if year in contributions:
            pipeline.append((year + params["lag"], float(contributions[year])))

        matured = [(deploy_year, amount) for deploy_year, amount in pipeline if deploy_year <= year]
        pipeline = [(deploy_year, amount) for deploy_year, amount in pipeline if deploy_year > year]
        asset += sum(amount * params["survival"] for _, amount in matured)

        rows.append({
            "year": int(year),
            "asset": asset,
            "pipeline": sum(amount for _, amount in pipeline),
            "public_cash": public_cash,
            "spillover": spillover,
            "operating_benefit": public_cash + spillover,
        })
    return rows


INDUSTRY_PATHS = {name: simulate_industry(params) for name, params in INDUSTRY.items()}


def transfer_flows(name):
    factor = TRANSFER[name]["total"] / SRD_REAL.sum()
    contributions = dict(zip(CONTRIBUTION_YEARS, SRD_REAL * factor))
    return np.array([contributions.get(int(year), 0.0) for year in YEARS])


def pv_factor(year, discount):
    return 1 / ((1 + discount) ** (year - 2020))


def cumulative_transfer_pv(name, discount):
    flows = transfer_flows(name)
    return np.cumsum([flow * pv_factor(int(year), discount) for flow, year in zip(flows, YEARS)])


def industry_values(name, discount):
    rows = INDUSTRY_PATHS[name]
    discounted_flows = np.array([
        row["operating_benefit"] * pv_factor(row["year"], discount) for row in rows
    ])
    cumulative_flow = np.cumsum(discounted_flows)
    terminal = np.array([
        (row["asset"] + row["pipeline"]) * pv_factor(row["year"], discount) for row in rows
    ])
    return cumulative_flow, cumulative_flow + terminal


def first_crossing(industry_name, transfer_name, discount, include_asset=True):
    flow, inclusive = industry_values(industry_name, discount)
    industrial = inclusive if include_asset else flow
    transfer = cumulative_transfer_pv(transfer_name, discount)
    eligible = np.where((YEARS >= 2027) & (industrial >= transfer))[0]
    return int(YEARS[eligible[0]]) if eligible.size else None


def at_year(series, year):
    return float(series[np.where(YEARS == year)[0][0]])


def make_timing_gap():
    fig, ax = plt.subplots(figsize=(9.5, 5.6))
    header(fig, "Cash delivers first; capital has to survive the pipeline", "Undiscounted annual value flows in the central transfer and average industrial scenarios")
    transfer = transfer_flows("Central")
    industry = np.array([r["operating_benefit"] for r in INDUSTRY_PATHS["Average"]])
    mask = YEARS <= 2050
    ax.bar(YEARS[mask], transfer[mask], color=CORAL, width=0.82, label="Transfer welfare delivered")
    ax.plot(YEARS[mask], industry[mask], color=BLACK, linestyle="--", marker="s", markevery=4, linewidth=2.0, markersize=4, label="Industrial operating benefit")
    ax.axvspan(2020, 2026.7, color=G100, zorder=-1)
    ax.text(2023.3, 67, "GRANT YEARS", ha="center", fontsize=7.2, color=G700, fontweight="bold")
    ax.text(2038, 18, "Benefits arrive only after\ndeployment and commissioning", ha="center", fontsize=7.4, color=G700)
    ax.set_xlim(2019.3, 2050.7)
    ax.set_ylim(0, 74)
    ax.set_ylabel("Annual social value, R billion (2026 rand)")
    ax.set_xlabel("Year")
    ax.legend(frameon=False, fontsize=7.2, loc="upper right")
    style_axis(ax, TOKENS, grid_axis="y")
    finish(fig, "timing-gap.png")


def make_break_even_paths():
    fig, ax = plt.subplots(figsize=(9.5, 5.6))
    header(fig, "Under central assumptions, only the best industrial path breaks even", "Cumulative 2020 present value at a 6% real discount rate; residual public asset included")
    transfer = cumulative_transfer_pv("Central", 0.06)
    mask = YEARS <= MAIN_END
    ax.plot(YEARS[mask], transfer[mask], color=BLACK, linewidth=2.4, label="Cash transfer welfare")
    for name in ["Best", "Average", "Worst"]:
        _, inclusive = industry_values(name, 0.06)
        p = INDUSTRY[name]
        ax.plot(YEARS[mask], inclusive[mask], color=p["colour"], linestyle=p["linestyle"], marker=p["marker"], markevery=8, linewidth=2.0, markersize=4, label=f"{name} industry")
    cross = first_crossing("Best", "Central", 0.06, include_asset=True)
    if cross:
        val = at_year(transfer, cross)
        ax.scatter([cross], [val], s=45, facecolor=WHITE, edgecolor=BLACK, linewidth=1.2, zorder=5)
        ax.annotate(f"Best case crosses in {cross}", xy=(cross, val), xytext=(cross + 5, val + 70), fontsize=7.5, fontweight="bold", arrowprops={"arrowstyle": "->", "color": BLACK, "lw": 0.9})
    ax.set_xlim(2019.5, MAIN_END + 0.5)
    ax.set_ylabel("Cumulative present value, R billion")
    ax.set_xlabel("Valuation horizon")
    ax.legend(frameon=False, fontsize=7.0, loc="upper left", ncol=2)
    style_axis(ax, TOKENS, grid_axis="y")
    finish(fig, "break-even-paths.png")


def make_flow_only():
    fig, ax = plt.subplots(figsize=(9.5, 5.6))
    header(fig, "The break-even date moves when the factory itself is not counted", "Operating benefits only versus central transfer welfare; cumulative 2020 PV at 6% real")
    transfer = cumulative_transfer_pv("Central", 0.06)
    mask = YEARS <= 2100
    ax.plot(YEARS[mask], transfer[mask], color=BLACK, linewidth=2.4, label="Cash transfer welfare")
    for name in ["Best", "Average", "Worst"]:
        flow, _ = industry_values(name, 0.06)
        p = INDUSTRY[name]
        ax.plot(YEARS[mask], flow[mask], color=p["colour"], linestyle=p["linestyle"], marker=p["marker"], markevery=10, linewidth=2.0, markersize=4, label=f"{name} industry flows")
    cross = first_crossing("Best", "Central", 0.06, include_asset=False)
    if cross:
        val = at_year(transfer, cross)
        ax.scatter([cross], [val], s=45, facecolor=WHITE, edgecolor=BLACK, zorder=5)
        ax.annotate(f"Best case cash-flows cross in {cross}", xy=(cross, val), xytext=(cross + 5, val + 90), fontsize=7.5, fontweight="bold", arrowprops={"arrowstyle": "->", "lw": 0.9, "color": BLACK})
    ax.set_xlim(2019.5, 2100.5)
    ax.set_ylabel("Cumulative present value, R billion")
    ax.set_xlabel("Valuation horizon")
    ax.legend(frameon=False, fontsize=7.0, loc="upper left", ncol=2)
    style_axis(ax, TOKENS, grid_axis="y")
    finish(fig, "flow-only-break-even.png")


def make_discount_sensitivity():
    transfer_names = ["Conservative", "Central", "Severe"]
    industry_names = ["Worst", "Average", "Best"]
    fig, axes = plt.subplots(1, 3, figsize=(10.2, 5.6), sharey=True)
    header(fig, "Discounting can decide whether tomorrow ever beats today", "Asset-inclusive break-even year by transfer valuation, industrial outcome and real discount rate")
    colours = [G500, BLACK, CORAL]
    for ax, d, colour in zip(axes, DISCOUNT_RATES, colours):
        matrix = []
        for tname in transfer_names:
            row = []
            for iname in industry_names:
                cross = first_crossing(iname, tname, d, include_asset=True)
                row.append(2105 if cross is None else cross)
            matrix.append(row)
        matrix = np.array(matrix)
        cmap = LinearSegmentedColormap.from_list("early_late", [CORAL, G100, G700])
        norm = Normalize(vmin=2027, vmax=2105)
        ax.imshow(matrix, cmap=cmap, norm=norm, aspect="auto")
        for r in range(3):
            for c in range(3):
                value = matrix[r, c]
                label = "Never" if value > 2100 else str(int(value))
                text_colour = WHITE if value > 2088 else BLACK
                ax.text(c, r, label, ha="center", va="center", fontsize=8.5, fontweight="bold", color=text_colour)
        ax.set_title(f"{d*100:.1f}% real", fontsize=10, fontweight="bold")
        ax.set_xticks(range(3), industry_names, rotation=25, ha="right")
        ax.tick_params(length=0)
        for spine in ax.spines.values():
            spine.set_visible(False)
    axes[0].set_yticks(range(3), [f"{n} transfer value" for n in transfer_names])
    axes[1].tick_params(labelleft=False)
    axes[2].tick_params(labelleft=False)
    fig.text(0.51, 0.055, "Industrial outcome", ha="center", fontsize=9)
    finish(fig, "discount-sensitivity.png", left=0.17, right=0.98, bottom=0.16)


def make_value_matrix():
    transfer_names = ["Conservative", "Central", "Severe"]
    industry_names = ["Worst", "Average", "Best"]
    matrix = np.zeros((3, 3))
    for r, tname in enumerate(transfer_names):
        transfer = cumulative_transfer_pv(tname, 0.06)
        for c, iname in enumerate(industry_names):
            _, inclusive = industry_values(iname, 0.06)
            matrix[r, c] = at_year(inclusive, 2050) - at_year(transfer, 2050)
    fig, ax = plt.subplots(figsize=(9.5, 5.6))
    header(fig, "By 2050, the industrial choice wins in only two of nine pairings", "Industrial value less transfer welfare; 2020 PV at 6% real, residual public asset included")
    cmap = LinearSegmentedColormap.from_list("net", [G700, G100, CORAL])
    norm = Normalize(vmin=-550, vmax=550)
    ax.imshow(matrix, cmap=cmap, norm=norm, aspect="auto")
    for r in range(3):
        for c in range(3):
            value = matrix[r, c]
            colour = WHITE if abs(value) > 250 else BLACK
            ax.text(c, r, f"{value:+.0f}bn", ha="center", va="center", fontsize=9, fontweight="bold", color=colour)
    ax.set_xticks(range(3), [f"{n} industry" for n in industry_names])
    ax.set_yticks(range(3), [f"{n} transfer value" for n in transfer_names])
    ax.set_xlabel("Industrial outcome")
    ax.set_ylabel("Value of consumption today")
    ax.tick_params(length=0)
    for spine in ax.spines.values():
        spine.set_visible(False)
    finish(fig, "value-matrix-2050.png", left=0.18)


def make_benefit_timing():
    bins = [(2020, 2029, "2020s"), (2030, 2039, "2030s"), (2040, 2049, "2040s"), (2050, 2075, "2050-75")]
    discount = 0.06
    series = {}
    tf = transfer_flows("Central")
    transfer_pv = np.array([v * pv_factor(int(y), discount) for v, y in zip(tf, YEARS)])
    series["Cash transfer"] = transfer_pv
    for name in ["Best industry", "Average industry"]:
        base = name.split()[0]
        series[name] = np.array([r["operating_benefit"] * pv_factor(r["year"], discount) for r in INDUSTRY_PATHS[base]])
    shares = {}
    for name, values in series.items():
        bucket = []
        for start, end, _ in bins:
            mask = (YEARS >= start) & (YEARS <= end)
            bucket.append(values[mask].sum())
        total = sum(bucket)
        shares[name] = np.array(bucket) / total * 100 if total else np.zeros(len(bucket))
    fig, ax = plt.subplots(figsize=(9.5, 5.6))
    header(fig, "The two policies pay different generations", "Share of discounted operating benefit arriving in each period through 2075; residual asset excluded")
    names = list(shares)
    x = np.arange(len(names))
    bottoms = np.zeros(len(names))
    colours = [CORAL, G300, G500, BLACK]
    for i, (_, _, label) in enumerate(bins):
        vals = np.array([shares[n][i] for n in names])
        bars = ax.bar(x, vals, bottom=bottoms, color=colours[i], width=0.58, label=label)
        for j, bar in enumerate(bars):
            if vals[j] >= 7:
                text_colour = WHITE if i in (0, 3) else BLACK
                ax.text(j, bottoms[j] + vals[j] / 2, f"{vals[j]:.0f}%", ha="center", va="center", fontsize=7.3, color=text_colour, fontweight="bold")
        bottoms += vals
    ax.set_xticks(x, names)
    ax.set_ylabel("Share of discounted benefit")
    ax.set_ylim(0, 100)
    ax.legend(frameon=False, fontsize=7.2, loc="upper left", ncol=2)
    style_axis(ax, TOKENS, grid_axis="y")
    finish(fig, "benefit-timing.png")


def make_hybrid_frontier():
    shares = np.linspace(0, 1, 21)
    discount = 0.06
    transfer = cumulative_transfer_pv("Central", discount)
    transfer_2050 = at_year(transfer, 2050)
    values = {}
    for name in ["Best", "Average", "Worst"]:
        _, inclusive = industry_values(name, discount)
        industry_2050 = at_year(inclusive, 2050)
        values[name] = (1 - shares) * transfer_2050 + shares * industry_2050
    fig, ax = plt.subplots(figsize=(9.5, 5.6))
    header(fig, "A hybrid buys insurance, not a free lunch", "2050 present value under central transfer valuation; 0% industry means the full grant is retained")
    ax.fill_between(shares * 100, values["Worst"], values["Best"], color=G100, label="Outcome range")
    for name in ["Best", "Average", "Worst"]:
        p = INDUSTRY[name]
        ax.plot(shares * 100, values[name], color=p["colour"], linestyle=p["linestyle"], marker=p["marker"], markevery=5, linewidth=2.0, markersize=4, label=name)
    ax.axvline(50, color=G300, linewidth=1.0)
    ax.text(50, max(values["Best"]) * 0.96, "50 / 50", ha="center", fontsize=7.4, color=G700)
    ax.set_xlabel("Share of the envelope allocated to industry")
    ax.set_ylabel("Total social value in 2050 PV, R billion")
    ax.set_xlim(0, 100)
    ax.legend(frameon=False, fontsize=7.2, loc="upper left", ncol=2)
    style_axis(ax, TOKENS, grid_axis="y")
    finish(fig, "hybrid-frontier.png")


def make_reinvestment_sensitivity():
    growths = [0.0, 0.025, 0.05]
    labels = ["No real growth", "Average renewal", "Strong reinvestment"]
    colours = [G500, BLACK, CORAL]
    fig, ax = plt.subplots(figsize=(9.5, 5.6))
    header(fig, "Compounding is earned through maintenance and reinvestment", "Average-case lag and survival with alternative real asset-growth paths")
    for g, label, colour, ls, marker in zip(growths, labels, colours, [":", "--", "-"], ["D", "s", "o"]):
        params = dict(INDUSTRY["Average"])
        params["asset_growth"] = g
        rows = simulate_industry(params)
        vals = np.array([r["asset"] for r in rows])
        mask = YEARS <= 2075
        ax.plot(YEARS[mask], vals[mask], color=colour, linestyle=ls, marker=marker, markevery=8, linewidth=2.0, markersize=4, label=label)
        ax.text(2076, vals[np.where(YEARS == 2075)[0][0]], f"R{vals[np.where(YEARS == 2075)[0][0]]:.0f}bn", va="center", fontsize=7.3, color=colour, fontweight="bold")
    ax.set_xlim(2019.5, 2082)
    ax.set_ylabel("Productive asset value, R billion (2026 rand)")
    ax.set_xlabel("Year")
    ax.legend(frameon=False, fontsize=7.2, loc="upper left")
    style_axis(ax, TOKENS, grid_axis="y")
    finish(fig, "reinvestment-sensitivity.png")


def make_r1_choice():
    fig, ax = plt.subplots(figsize=(9.6, 5.6))
    header(fig, "R1 can relieve a constraint now or build a claim on the future", "The alternatives differ in timing, risk, ownership and who receives the benefit")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis("off")
    ax.add_patch(plt.Rectangle((0.5, 2.35), 1.5, 1.0, facecolor=BLACK, edgecolor=BLACK))
    ax.text(1.25, 2.85, "R1 PUBLIC\nRESOURCE", ha="center", va="center", color=WHITE, fontsize=8.2, fontweight="bold")
    ax.annotate("", xy=(3.05, 4.25), xytext=(2.05, 3.15), arrowprops={"arrowstyle": "-|>", "lw": 1.2, "color": BLACK})
    ax.annotate("", xy=(3.05, 1.45), xytext=(2.05, 2.55), arrowprops={"arrowstyle": "-|>", "lw": 1.2, "color": BLACK})
    boxes = [
        (3.1, 3.55, CORAL, "CONSUMPTION TODAY", "Food, power, transport, search", "Immediate • targeted • low delay"),
        (3.1, 0.75, G300, "PRODUCTIVE CAPITAL", "Pipeline, plant, skills, infrastructure", "Delayed • risky • potentially compounding"),
    ]
    for x, y, colour, title, body, note in boxes:
        ax.add_patch(plt.Rectangle((x, y), 3.0, 1.25, facecolor=colour, edgecolor=BLACK, linewidth=0.9))
        tcol = WHITE if colour == CORAL else BLACK
        ax.text(x + 0.15, y + 0.88, title, fontsize=7.6, fontweight="bold", color=tcol)
        ax.text(x + 0.15, y + 0.55, body, fontsize=6.9, color=tcol)
        ax.text(x + 0.15, y + 0.20, note, fontsize=6.5, color=tcol)
    ax.annotate("", xy=(7.1, 4.18), xytext=(6.15, 4.18), arrowprops={"arrowstyle": "-|>", "lw": 1.2, "color": BLACK})
    ax.annotate("", xy=(7.1, 1.38), xytext=(6.15, 1.38), arrowprops={"arrowstyle": "-|>", "lw": 1.2, "color": BLACK})
    ax.add_patch(plt.Rectangle((7.15, 3.55), 2.3, 1.25, facecolor=G100, edgecolor=BLACK, linewidth=0.9))
    ax.add_patch(plt.Rectangle((7.15, 0.75), 2.3, 1.25, facecolor=G700, edgecolor=BLACK, linewidth=0.9))
    ax.text(7.3, 4.43, "VALUE REALISED", fontsize=7.4, fontweight="bold")
    ax.text(7.3, 4.03, "Mostly by current\nlow-income households", fontsize=6.8)
    ax.text(7.3, 1.63, "VALUE CONDITIONAL", fontsize=7.4, fontweight="bold", color=WHITE)
    ax.text(7.3, 1.23, "On execution, survival,\naccess and time", fontsize=6.8, color=WHITE)
    ax.text(5.0, 0.2, "The economic question is not which box looks more productive; it is which complete benefit stream is worth more to society.", ha="center", fontsize=7.2, color=G700)
    finish(fig, "r1-choice.png")


def write_results():
    break_even = {}
    for d in DISCOUNT_RATES:
        key = f"{d:.3f}"
        break_even[key] = {}
        for tname in TRANSFER:
            break_even[key][tname] = {}
            for iname in INDUSTRY:
                break_even[key][tname][iname] = {
                    "asset_inclusive": first_crossing(iname, tname, d, True),
                    "operating_flows_only": first_crossing(iname, tname, d, False),
                }
    values_2050 = {}
    for d in DISCOUNT_RATES:
        key = f"{d:.3f}"
        values_2050[key] = {
            "transfer": {name: round(at_year(cumulative_transfer_pv(name, d), 2050), 2) for name in TRANSFER},
            "industry_asset_inclusive": {name: round(at_year(industry_values(name, d)[1], 2050), 2) for name in INDUSTRY},
            "industry_flows_only": {name: round(at_year(industry_values(name, d)[0], 2050), 2) for name in INDUSTRY},
        }
    payload = {
        "valuation_basis": "constant 2026 rand, discounted to 2020 where stated",
        "real_grant_envelope_r_billion": round(float(SRD_REAL.sum()), 2),
        "transfer_welfare_totals_undiscounted": {k: v["total"] for k, v in TRANSFER.items()},
        "industry_assumptions": {k: {kk: vv for kk, vv in v.items() if kk not in {"colour", "linestyle", "marker"}} for k, v in INDUSTRY.items()},
        "break_even_years": break_even,
        "values_at_2050": values_2050,
        "interpretation": {
            "asset_inclusive": "discounted operating benefits plus residual public asset and undeployed pipeline cash at the valuation horizon",
            "flows_only": "discounted public cash and net wage, supplier and consumer spillovers; residual asset excluded",
            "never": "no crossing by 2100",
        },
    }
    (WORK / "model_results.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")


def main():
    make_timing_gap()
    make_break_even_paths()
    make_flow_only()
    make_discount_sensitivity()
    make_value_matrix()
    make_benefit_timing()
    make_hybrid_frontier()
    make_reinvestment_sensitivity()
    make_r1_choice()
    write_results()
    print(WORK / "model_results.json")


if __name__ == "__main__":
    main()
