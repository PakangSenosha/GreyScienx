from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.patches import FancyArrowPatch, Rectangle


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

USDZAR = 18.0

# End-point products made from 1,000 tonnes of contained manganese. These are
# alternative system boundaries, not additive stages.
LADDER = [
    {"stage": "44% ore", "output_t": 2273, "price_usd_t": 200, "local_share": 0.65},
    {"stage": "HPMSM", "output_t": 3125, "price_usd_t": 1800, "local_share": 0.45},
    {"stage": "Cathode material", "output_t": 8850, "price_usd_t": 15000, "local_share": 0.28},
    {"stage": "Battery cells", "output_gwh": 4.545, "price_usd_kwh": 80, "local_share": 0.20},
    {"stage": "Pack / system", "output_gwh": 4.545, "price_usd_kwh": 120, "local_share": 0.32},
]

for row in LADDER:
    if "output_t" in row:
        row["sales_usdm"] = row["output_t"] * row["price_usd_t"] / 1e6
    else:
        row["sales_usdm"] = row["output_gwh"] * 1e6 * row["price_usd_kwh"] / 1e6
    row["local_value_usdm"] = row["sales_usdm"] * row["local_share"]


# Independently-sized, plausible first industrial modules. They are deliberately
# not mass-balanced because the comparison is about industrial project choices.
MODULES = [
    {"stage": "Ore extraction", "scale": "5 Mt ore/y", "capex": 10.0, "sales": 18.0, "exports": 15.0, "value": 9.0, "jobs": 2000, "energy": 300, "water": 2.50, "freight": 5.00},
    {"stage": "High-purity Mn", "scale": "100 kt/y", "capex": 8.0, "sales": 4.0, "exports": 3.6, "value": 1.8, "jobs": 500, "energy": 700, "water": 0.50, "freight": 0.15},
    {"stage": "HPMSM", "scale": "30 kt/y", "capex": 4.5, "sales": 0.972, "exports": 0.90, "value": 0.437, "jobs": 180, "energy": 90, "water": 0.18, "freight": 0.035},
    {"stage": "pCAM / CAM", "scale": "20 kt/y", "capex": 7.0, "sales": 5.4, "exports": 4.0, "value": 1.5, "jobs": 450, "energy": 50, "water": 0.10, "freight": 0.025},
    {"stage": "Battery cells", "scale": "5 GWh/y", "capex": 18.0, "sales": 7.2, "exports": 2.5, "value": 1.44, "jobs": 900, "energy": 200, "water": 0.10, "freight": 0.10},
    {"stage": "Packs / systems", "scale": "2 GWh/y", "capex": 3.0, "sales": 4.32, "exports": 1.0, "value": 1.51, "jobs": 500, "energy": 20, "water": 0.02, "freight": 0.05},
    {"stage": "Recycling", "scale": "10 kt feed/y", "capex": 2.0, "sales": 0.54, "exports": 0.20, "value": 0.32, "jobs": 250, "energy": 25, "water": 0.03, "freight": 0.01},
]


def header(fig, title, subtitle):
    add_figure_header(fig, title, subtitle, field="GREYSCIENCX / PAPER 5", tokens=TOKENS)


def finish(fig, filename, *, left=0.10, right=0.97, top=0.77, bottom=0.14):
    fig.subplots_adjust(left=left, right=right, top=top, bottom=bottom)
    save_figure(fig, ASSETS / filename, dpi=270)
    plt.close(fig)


def annuity_factor(rate: float, years: int) -> float:
    return rate / (1 - (1 + rate) ** (-years))


def hpmsm_break_even(capex_bn: float, utilization: float, capacity_t: float = 30000, opex_usd_t: float = 1100) -> float:
    annualised_capital_r = capex_bn * 1e9 * annuity_factor(0.08, 20)
    sustaining_r = capex_bn * 1e9 * 0.02
    output = capacity_t * utilization
    return opex_usd_t + (annualised_capital_r + sustaining_r) / USDZAR / output


def make_endowment():
    metrics = ["World mined output\n(2025, contained Mn)", "World resources\n(official estimate)", "Global exports\n(2025 estimate)"]
    shares = [38, 70, 40]
    fig, ax = plt.subplots(figsize=(9.5, 5.4))
    header(fig, "South Africa starts with scale, not downstream dominance", "Shares are rounded from USGS and Statistics South Africa; the measures are not directly comparable")
    y = np.arange(len(metrics))
    ax.barh(y, [100] * len(y), color=G100, height=0.52)
    ax.barh(y, shares, color=CORAL, height=0.52)
    for i, v in enumerate(shares):
        ax.text(v + 1.8, i, f"{v}%", va="center", fontsize=10, fontweight="bold")
    ax.set_yticks(y, metrics)
    ax.set_xlim(0, 100)
    ax.set_xlabel("South African share of reported global total (%)")
    ax.invert_yaxis()
    style_axis(ax, TOKENS, grid_axis="x")
    finish(fig, "endowment.png", left=0.24)


def make_chain_map():
    stages = [
        ("ORE", "mine + concentrate", "MAKE"),
        ("REFINED Mn", "metal / oxide", "MAKE"),
        ("HPMSM", "battery chemical", "MAKE"),
        ("pCAM / CAM", "active material", "PARTNER"),
        ("CELLS", "electrochemical unit", "OPTION"),
        ("PACKS", "BMS + integration", "MAKE"),
        ("RECYCLE", "recover + recirculate", "MAKE"),
    ]
    fig, ax = plt.subplots(figsize=(10.4, 5.8))
    header(fig, "The chain is a sequence of qualification gates", "South Africa should deepen capability selectively; each arrow requires chemistry, customers and reliable operation")
    ax.set_xlim(0, 14.7)
    ax.set_ylim(0, 5.1)
    ax.axis("off")
    xs = np.linspace(0.25, 12.65, len(stages))
    for i, (title, sub, mode) in enumerate(stages):
        if i < len(stages) - 1:
            ax.add_patch(FancyArrowPatch((xs[i] + 1.72, 2.70), (xs[i + 1] - 0.12, 2.70), arrowstyle="-|>", mutation_scale=10, lw=1.1, color=G500))
        face = CORAL if mode == "MAKE" else (G300 if mode == "PARTNER" else WHITE)
        edge = CORAL if mode == "MAKE" else BLACK
        rect = Rectangle((xs[i], 1.72), 1.72, 1.94, facecolor=face, edgecolor=edge, linewidth=1.0)
        ax.add_patch(rect)
        txt = WHITE if mode == "MAKE" else BLACK
        ax.text(xs[i] + 0.86, 3.11, title, ha="center", va="center", fontsize=7.6, fontweight="bold", color=txt)
        ax.text(xs[i] + 0.86, 2.52, sub, ha="center", va="center", fontsize=6.5, color=txt)
        ax.text(xs[i] + 0.86, 2.03, mode, ha="center", va="center", fontsize=6.0, fontweight="bold", color=txt)
    ax.text(6.6, 0.78, "Shared spine: power · water · reagents · laboratories · logistics · standards · project execution · offtake", ha="center", fontsize=8.2, fontweight="bold")
    finish(fig, "chain-map.png", left=0.04, right=0.98, top=0.76, bottom=0.10)


def make_value_ladder():
    labels = [r["stage"] for r in LADDER]
    sales = np.array([r["sales_usdm"] for r in LADDER])
    local = np.array([r["local_value_usdm"] for r in LADDER])
    y = np.arange(len(labels))
    fig, ax = plt.subplots(figsize=(9.8, 6.0))
    header(fig, "Downstream sales grow faster than manganese-created value", "Gross annual sales enabled by 1,000 tonnes of contained manganese; end points are alternatives, not additive")
    ax.barh(y, sales, color=G300, height=0.58, label="Gross sales of end product")
    ax.barh(y, local, color=CORAL, height=0.58, label="Illustrative value retained locally")
    for i, (s, v) in enumerate(zip(sales, local)):
        gross_label = f"${s:,.1f}m" if s < 10 else f"${s:,.0f}m"
        ax.text(s + 8, i, gross_label, va="center", fontsize=7.4, color=G700)
        if v > 18:
            ax.text(v - 5, i, f"${v:,.0f}m", ha="right", va="center", fontsize=7.0, color=WHITE, fontweight="bold")
        else:
            ax.text(v + 2, i - 0.18, f"${v:,.1f}m local", va="center", fontsize=6.8, color=BLACK)
    ax.set_yticks(y, labels)
    ax.set_xlabel("USD million per 1,000 tonnes contained Mn")
    ax.set_xlim(0, 600)
    ax.invert_yaxis()
    ax.legend(frameon=False, fontsize=7.5, loc="upper right")
    style_axis(ax, TOKENS, grid_axis="x")
    finish(fig, "value-ladder.png", left=0.19)


def make_module_frontier():
    fig, ax = plt.subplots(figsize=(9.8, 6.0))
    header(fig, "Factory visibility is not project quality", "Illustrative standalone modules; bubble area represents direct employment and scales differ by stage")
    for m in MODULES:
        x = m["capex"]
        y = m["value"]
        size = 45 + m["jobs"] * 0.16
        color = CORAL if m["stage"] in {"HPMSM", "pCAM / CAM", "Packs / systems", "Recycling"} else G500
        ax.scatter(x, y, s=size, color=color, alpha=0.88, edgecolor=BLACK, linewidth=0.5)
        dx, dy = 0.28, 0.15
        if m["stage"] == "Ore extraction":
            dx, dy = 0.25, -0.55
        if m["stage"] == "Battery cells":
            dx, dy = -4.0, 0.25
        if m["stage"] == "pCAM / CAM":
            dx, dy = -0.2, -0.55
        if m["stage"] == "High-purity Mn":
            dx, dy = 0.3, 0.15
        ax.text(x + dx, y + dy, m["stage"], fontsize=7.0, fontweight="bold")
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 10)
    ax.set_xlabel("Capital required (R billion)")
    ax.set_ylabel("Annual local value added at model scale (R billion)")
    ax.legend(handles=[Line2D([0], [0], marker="o", color="none", markerfacecolor=CORAL, markeredgecolor=BLACK, markersize=7, label="Priority / partner-led stage"), Line2D([0], [0], marker="o", color="none", markerfacecolor=G500, markeredgecolor=BLACK, markersize=7, label="Existing base / later option")], frameon=False, fontsize=7.2, loc="upper right")
    style_axis(ax, TOKENS, grid_axis="both")
    finish(fig, "module-frontier.png", right=0.93)


def make_jobs_capital():
    labels = [m["stage"] for m in MODULES]
    values = np.array([m["jobs"] / m["capex"] for m in MODULES])
    order = np.argsort(values)
    labels = [labels[i] for i in order]
    values = values[order]
    fig, ax = plt.subplots(figsize=(9.6, 5.8))
    header(fig, "Assembly and recycling add job-dense layers", "Illustrative direct jobs per R1 billion of capital; supplier and construction jobs are excluded")
    y = np.arange(len(labels))
    ax.barh(y, values, color=[CORAL if x in {"Packs / systems", "Recycling"} else G500 for x in labels], height=0.55)
    for i, v in enumerate(values):
        ax.text(v + 4, i, f"{v:,.0f}", va="center", fontsize=7.6, fontweight="bold")
    ax.set_yticks(y, labels)
    ax.set_xlim(0, 230)
    ax.set_xlabel("Direct jobs per R1 billion capital")
    style_axis(ax, TOKENS, grid_axis="x")
    finish(fig, "jobs-capital.png", left=0.22)


def make_resources():
    labels = [m["stage"] for m in MODULES]
    energy = np.array([m["energy"] / m["sales"] for m in MODULES])
    water = np.array([m["water"] / m["sales"] for m in MODULES])
    y = np.arange(len(labels))
    fig, axes = plt.subplots(1, 2, figsize=(10.4, 6.0), sharey=True)
    header(fig, "Resource exposure changes sharply along the chain", "Annual energy and water per R1 billion of module sales; engineering assumptions, not plant quotations")
    axes[0].barh(y, energy, color=CORAL, height=0.56)
    axes[1].barh(y, water, color=G500, height=0.56)
    for ax, vals, xlabel in [(axes[0], energy, "GWh per R1bn sales"), (axes[1], water, "Million m³ per R1bn sales")]:
        for i, v in enumerate(vals):
            ax.text(v + max(vals) * 0.02, i, f"{v:.2f}" if max(vals) < 1 else f"{v:.0f}", va="center", fontsize=6.8)
        ax.set_xlabel(xlabel)
        style_axis(ax, TOKENS, grid_axis="x")
    axes[0].set_yticks(y, labels)
    axes[0].invert_yaxis()
    finish(fig, "resource-intensity.png", left=0.20, right=0.97, top=0.77, bottom=0.15)


def make_freight_density():
    labels = [m["stage"] for m in MODULES]
    vals = np.array([m["freight"] * 1000 / m["sales"] for m in MODULES])
    order = np.argsort(vals)
    labels = [labels[i] for i in order]
    vals = vals[order]
    fig, ax = plt.subplots(figsize=(9.6, 5.8))
    header(fig, "Processing trades bulk freight for specification risk", "Outbound tonnes per R1 million of sales; log scale reveals the change in value density")
    y = np.arange(len(labels))
    ax.barh(y, vals, color=[CORAL if x in {"HPMSM", "pCAM / CAM", "Packs / systems", "Recycling"} else G500 for x in labels], height=0.55)
    for i, v in enumerate(vals):
        ax.text(v * 1.10, i, f"{v:.1f}", va="center", fontsize=7.0, fontweight="bold")
    ax.set_xscale("log")
    ax.set_xlim(1, 500)
    ax.set_yticks(y, labels)
    ax.set_xlabel("Outbound tonnes per R1 million of sales (log scale)")
    style_axis(ax, TOKENS, grid_axis="x")
    finish(fig, "freight-density.png", left=0.22)


def make_hpmsm_heatmap():
    capex = np.array([1.5, 3.0, 4.5, 6.0])
    util = np.array([55, 65, 75, 85, 95])
    z = np.array([[hpmsm_break_even(c, u / 100) for u in util] for c in capex])
    fig, ax = plt.subplots(figsize=(9.4, 5.8))
    header(fig, "HPMSM economics depend on utilisation as much as chemistry", "Break-even real product price for a 30,000 t/y plant; includes operating cost, annualised capital and sustaining capital")
    im = ax.imshow(z, cmap="Greys", aspect="auto", vmin=1200, vmax=4200)
    ax.set_xticks(np.arange(len(util)), [f"{u}%" for u in util])
    ax.set_yticks(np.arange(len(capex)), [f"R{c:g}bn" for c in capex])
    ax.set_xlabel("Achieved utilisation")
    ax.set_ylabel("Initial capital requirement")
    for i in range(len(capex)):
        for j in range(len(util)):
            face = CORAL if (capex[i] == 4.5 and util[j] == 75) else None
            if face:
                ax.add_patch(Rectangle((j - 0.48, i - 0.48), 0.96, 0.96, facecolor="none", edgecolor=CORAL, linewidth=2.2))
            ax.text(j, i, f"${z[i, j]:,.0f}", ha="center", va="center", fontsize=8, color=WHITE if z[i, j] > 2700 else BLACK, fontweight="bold")
    cbar = fig.colorbar(im, ax=ax, fraction=0.035, pad=0.03)
    cbar.set_label("Break-even price (USD/t)")
    finish(fig, "hpmsm-break-even.png", left=0.13, right=0.90, top=0.77, bottom=0.16)


def make_price_ranges():
    util = np.arange(55, 96, 5)
    be = np.array([hpmsm_break_even(4.5, u / 100) for u in util])
    fig, ax = plt.subplots(figsize=(9.7, 5.8))
    header(fig, "A qualified plant still needs a viable price corridor", "Central 30,000 t/y HPMSM module; external project prices are sponsor assumptions, not market forecasts")
    ax.plot(util, be, color=BLACK, linewidth=2.2, marker="o", markersize=4, label="Model break-even, R4.5bn capex")
    refs = [(1419, "Low sponsor case  $1,419/t", G500), (1800, "Paper central sales case  $1,800/t", CORAL), (3220, "High sponsor case  $3,220/t", G700)]
    for val, label, color in refs:
        ax.axhline(val, color=color, linewidth=1.3, linestyle="--")
        ax.text(95.5, val, label, ha="right", va="bottom", fontsize=6.8, color=color)
    ax.set_xlim(53, 97)
    ax.set_ylim(1000, 3800)
    ax.set_xlabel("Achieved utilisation (%)")
    ax.set_ylabel("USD per tonne HPMSM")
    style_axis(ax, TOKENS, grid_axis="both")
    finish(fig, "price-corridor.png")


def make_africa_demand():
    years = np.array([2030, 2040, 2050])
    cases = {"Low": [5, 15, 30], "Central": [12, 45, 90], "High": [25, 90, 180]}
    styles = {"Low": (G500, "--"), "Central": (CORAL, "-"), "High": (BLACK, "-")}
    fig, ax = plt.subplots(figsize=(9.7, 5.8))
    header(fig, "Africa could anchor a first market", "Illustrative annual addressable battery demand; scenarios are stress tests, not forecasts")
    for name, vals in cases.items():
        color, ls = styles[name]
        ax.plot(years, vals, color=color, linewidth=2.2, marker="o", linestyle=ls, label=name)
        ax.text(2050.6, vals[-1], f"{vals[-1]} GWh", va="center", fontsize=7.3, fontweight="bold", color=color)
    ax.scatter([2030], [3.6], color=WHITE, edgecolor=BLACK, zorder=4, s=55)
    ax.text(2031, 3.6, "World Bank mini-grid benchmark: 3.6 GWh", va="center", fontsize=6.8)
    ax.set_xlim(2028, 2057)
    ax.set_ylim(0, 200)
    ax.set_xticks(years)
    ax.set_xlabel("Year")
    ax.set_ylabel("Annual addressable demand (GWh)")
    ax.legend(frameon=False, fontsize=7.5, loc="upper left")
    style_axis(ax, TOKENS, grid_axis="both")
    finish(fig, "africa-demand.png")


def make_strategy_portfolio():
    # Normalised R50bn portfolios; the score reflects modelled annual local value
    # discounted for utilisation, market access and execution risk.
    strategies = {
        "Ore-heavy": {"value": 11.6, "exports": 19.8, "jobs": 7600, "risk": 0.82},
        "Chemicals-first": {"value": 8.9, "exports": 13.7, "jobs": 5200, "risk": 0.78},
        "Partnered midstream": {"value": 13.5, "exports": 15.4, "jobs": 8000, "risk": 0.76},
        "Cell-first": {"value": 5.4, "exports": 6.9, "jobs": 3900, "risk": 0.52},
    }
    labels = list(strategies)
    realised = np.array([strategies[k]["value"] * strategies[k]["risk"] for k in labels])
    exports = np.array([strategies[k]["exports"] * strategies[k]["risk"] for k in labels])
    jobs = np.array([strategies[k]["jobs"] * strategies[k]["risk"] for k in labels])
    x = np.arange(len(labels))
    fig, axes = plt.subplots(1, 3, figsize=(10.5, 5.7))
    header(fig, "Partnership buys value; ore still buys volume", "Risk-adjusted outcomes from illustrative R50 billion portfolios; this ranks strategies rather than forecasting returns")
    panels = [(realised, "Annual local value", "R billion"), (exports, "Annual exports", "R billion"), (jobs, "Direct jobs", "jobs")]
    for ax, (vals, title, unit) in zip(axes, panels):
        colors = [CORAL if label == "Partnered midstream" else G500 for label in labels]
        ax.bar(x, vals, color=colors, width=0.62)
        for i, v in enumerate(vals):
            lab = f"{v:,.0f}" if unit == "jobs" else f"{v:.1f}"
            ax.text(i, v + max(vals) * 0.035, lab, ha="center", fontsize=7.2, fontweight="bold")
        ax.set_title(title, fontsize=8.5, fontweight="bold")
        ax.set_xticks(x, [s.replace(" ", "\n") for s in labels], fontsize=6.3)
        ax.set_ylabel(unit)
        ax.set_ylim(0, max(vals) * 1.25)
        style_axis(ax, TOKENS, grid_axis="y")
    finish(fig, "strategy-portfolios.png", left=0.08, right=0.98, top=0.76, bottom=0.19)


def make_sequence():
    rows = [
        ("HPMSM qualification + offtake", 2026, 2030, "MAKE"),
        ("Pack, BMS + storage integration", 2026, 2034, "MAKE"),
        ("Recycling + traceability", 2027, 2036, "MAKE"),
        ("pCAM / CAM joint venture", 2028, 2035, "PARTNER"),
        ("African demand aggregation", 2026, 2036, "ENABLE"),
        ("4–6 GWh cell option", 2030, 2036, "OPTION"),
    ]
    fig, ax = plt.subplots(figsize=(9.8, 5.7))
    header(fig, "The sequence should earn the right to move downstream", "Each stage opens only after technical qualification, offtake and reliable operating evidence")
    for i, (label, start, end, mode) in enumerate(rows):
        y = len(rows) - i
        color = CORAL if mode == "MAKE" else (BLACK if mode == "PARTNER" else G500)
        ax.plot([start, end], [y, y], color=color, linewidth=10, solid_capstyle="butt")
        ax.text(start + 0.12, y, label, va="center", fontsize=7.1, color=WHITE if mode in {"MAKE", "PARTNER"} else BLACK, fontweight="bold")
        ax.text(end + 0.12, y, mode, va="center", fontsize=6.5, fontweight="bold", color=color)
    for x, text in [(2028, "qualify"), (2030, "first scale gate"), (2033, "midstream gate"), (2036, "cell decision")]:
        ax.axvline(x, color=G300, linewidth=0.8)
        ax.text(x, 0.55, text, ha="center", fontsize=6.2, color=G700)
    ax.set_xlim(2025.5, 2037.5)
    ax.set_ylim(0.25, len(rows) + 0.75)
    ax.set_yticks([])
    ax.set_xlabel("Indicative decision window")
    style_axis(ax, TOKENS, grid_axis="x")
    ax.grid(False)
    finish(fig, "sequence.png", left=0.08, right=0.94, top=0.77, bottom=0.16)


def main():
    for fn in [
        make_endowment,
        make_chain_map,
        make_value_ladder,
        make_module_frontier,
        make_jobs_capital,
        make_resources,
        make_freight_density,
        make_hpmsm_heatmap,
        make_price_ranges,
        make_africa_demand,
        make_strategy_portfolio,
        make_sequence,
    ]:
        fn()

    results = {
        "units": {"currency": "constant 2026 rand unless stated", "usd_zar_model_rate": USDZAR},
        "ladder": LADDER,
        "modules": MODULES,
        "hpmsm_break_even": {
            "central_capex_r_bn": 4.5,
            "capacity_t_y": 30000,
            "opex_usd_t": 1100,
            "at_75_percent_utilisation_usd_t": round(hpmsm_break_even(4.5, 0.75), 1),
            "at_90_percent_utilisation_usd_t": round(hpmsm_break_even(4.5, 0.90), 1),
        },
        "africa_demand_scenarios_gwh": {"2030": {"low": 5, "central": 12, "high": 25}, "2040": {"low": 15, "central": 45, "high": 90}, "2050": {"low": 30, "central": 90, "high": 180}},
        "notes": [
            "Model outputs are scenarios, not forecasts or investment advice.",
            "Product ladder end points are alternative system boundaries and must not be summed.",
            "Module scales are independent; employment is direct operating employment only.",
        ],
    }
    (WORK / "model_results.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(json.dumps(results["hpmsm_break_even"], indent=2))
    print(f"Wrote {len(list(ASSETS.glob('*.png')))} figures to {ASSETS}")


if __name__ == "__main__":
    main()
