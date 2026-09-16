from __future__ import annotations

import json
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
PLATINUM_USD_OZ = 1200.0
PLATINUM_USD_KG = PLATINUM_USD_OZ * 32.1507


LADDER = [
    {"stage": "Refined platinum", "gross_usd": PLATINUM_USD_KG, "local_share": 0.80},
    {"stage": "Specialty catalyst", "gross_usd": 70000, "local_share": 0.55},
    {"stage": "MEA output", "gross_usd": 320000, "local_share": 0.38},
    {"stage": "Fuel-cell stacks", "gross_usd": 1600000, "local_share": 0.30},
    {"stage": "Fuel-cell systems", "gross_usd": 3200000, "local_share": 0.38},
]
for row in LADDER:
    row["local_value_usd"] = row["gross_usd"] * row["local_share"]


MODULES = [
    {"stage": "PGM refining", "scale": "100 koz Pt-eq/y", "capex": 4.0, "sales": 2.16, "exports": 1.85, "value": 1.40, "jobs": 300, "energy": 120, "water": 0.20},
    {"stage": "Catalysts + chemicals", "scale": "4 t catalyst/y", "capex": 0.9, "sales": 1.70, "exports": 1.15, "value": 0.65, "jobs": 60, "energy": 15, "water": 0.03},
    {"stage": "MEAs", "scale": "30k vehicle-eq/y", "capex": 1.2, "sales": 3.20, "exports": 2.10, "value": 1.15, "jobs": 100, "energy": 25, "water": 0.02},
    {"stage": "Fuel-cell stacks", "scale": "500 MW/y", "capex": 3.5, "sales": 3.60, "exports": 2.20, "value": 1.10, "jobs": 350, "energy": 45, "water": 0.02},
    {"stage": "Fuel-cell systems", "scale": "300 MW/y", "capex": 2.5, "sales": 4.32, "exports": 1.80, "value": 1.65, "jobs": 500, "energy": 35, "water": 0.02},
    {"stage": "PEM components", "scale": "1 GW/y", "capex": 4.0, "sales": 4.50, "exports": 2.90, "value": 1.50, "jobs": 250, "energy": 40, "water": 0.03},
    {"stage": "PEM electrolysers", "scale": "1 GW/y", "capex": 8.0, "sales": 12.60, "exports": 7.60, "value": 3.80, "jobs": 500, "energy": 80, "water": 0.05},
    {"stage": "Green H2 production", "scale": "100 MW at 65%", "capex": 8.0, "sales": 0.75, "exports": 0.10, "value": 0.40, "jobs": 60, "energy": 570, "water": 0.19},
    {"stage": "Mining / HD systems", "scale": "100 systems/y", "capex": 2.0, "sales": 2.80, "exports": 1.10, "value": 1.00, "jobs": 300, "energy": 25, "water": 0.01},
    {"stage": "PGM recycling", "scale": "2 t recovered/y", "capex": 1.5, "sales": 1.50, "exports": 0.70, "value": 0.60, "jobs": 120, "energy": 20, "water": 0.04},
]


def header(fig, title, subtitle):
    add_figure_header(fig, title, subtitle, field="GREYSCIENCX / PAPER 6", tokens=TOKENS)


def finish(fig, filename, *, left=0.10, right=0.97, top=0.77, bottom=0.14):
    fig.subplots_adjust(left=left, right=right, top=top, bottom=bottom)
    save_figure(fig, ASSETS / filename, dpi=270)
    plt.close(fig)


def annuity_factor(rate=0.08, years=20):
    return rate / (1 - (1 + rate) ** (-years))


def hydrogen_output_kg(capacity_mw, utilisation, kwh_per_kg=54):
    return capacity_mw * 1000 * 8760 * utilisation / kwh_per_kg


def hydrogen_break_even_usd_kg(capex_bn, utilisation, electricity_r_kwh=0.75, capacity_mw=100):
    output = hydrogen_output_kg(capacity_mw, utilisation)
    annual_fixed_r = capex_bn * 1e9 * (annuity_factor() + 0.03)
    variable_r_kg = electricity_r_kwh * 54 + 8.0
    return (variable_r_kg + annual_fixed_r / output) / USDZAR


def make_endowment():
    labels = ["2025 platinum\nmine production", "Reported PGM\nreserves"]
    values = [120 / 170 * 100, 63 / 76 * 100]
    fig, ax = plt.subplots(figsize=(9.5, 5.3))
    header(fig, "South Africa dominates the metal, not the equipment", "Rounded shares from USGS 2026; production and reserves are different measures")
    y = np.arange(len(labels))
    ax.barh(y, [100, 100], color=G100, height=0.52)
    ax.barh(y, values, color=CORAL, height=0.52)
    for i, v in enumerate(values):
        ax.text(v + 1.5, i, f"{v:.0f}%", va="center", fontsize=10, fontweight="bold")
    ax.set_yticks(y, labels)
    ax.invert_yaxis()
    ax.set_xlim(0, 100)
    ax.set_xlabel("South African share of reported world total (%)")
    style_axis(ax, TOKENS, grid_axis="x")
    finish(fig, "endowment.png", left=0.22)


def make_chain_map():
    nodes = [
        ("REFINED PGM", "metal", "KEEP"),
        ("CHEMICAL", "precursor", "MAKE"),
        ("CATALYST", "powder + ink", "MAKE"),
        ("CCM / MEA", "coated membrane", "MAKE"),
        ("STACK", "cells + plates", "PARTNER"),
        ("SYSTEM", "BOP + controls", "MAKE"),
        ("RECYCLE", "closed loop", "MAKE"),
    ]
    fig, ax = plt.subplots(figsize=(10.4, 5.8))
    header(fig, "The strongest opportunity sits between metal and machine", "Localise chemistry, catalysts, MEAs and system integration; partner for scale-sensitive stack platforms")
    ax.set_xlim(0, 14.7)
    ax.set_ylim(0, 5.1)
    ax.axis("off")
    xs = np.linspace(0.25, 12.65, len(nodes))
    for i, (title, sub, mode) in enumerate(nodes):
        if i < len(nodes) - 1:
            ax.add_patch(FancyArrowPatch((xs[i] + 1.72, 2.70), (xs[i + 1] - 0.12, 2.70), arrowstyle="-|>", mutation_scale=10, lw=1.1, color=G500))
        face = CORAL if mode in {"MAKE", "KEEP"} else G300
        rect = Rectangle((xs[i], 1.72), 1.72, 1.94, facecolor=face, edgecolor=BLACK, linewidth=0.9)
        ax.add_patch(rect)
        txt = WHITE if mode in {"MAKE", "KEEP"} else BLACK
        ax.text(xs[i] + 0.86, 3.10, title, ha="center", va="center", fontsize=7.0, fontweight="bold", color=txt)
        ax.text(xs[i] + 0.86, 2.52, sub, ha="center", va="center", fontsize=6.3, color=txt)
        ax.text(xs[i] + 0.86, 2.03, mode, ha="center", va="center", fontsize=6.0, fontweight="bold", color=txt)
    ax.text(7.15, 0.80, "Demand anchors: refining · ammonia · mines · buses and trucks · stationary power · export customers", ha="center", fontsize=8.0, fontweight="bold")
    finish(fig, "chain-map.png", left=0.04, right=0.98, top=0.76, bottom=0.10)


def make_value_ladder():
    labels = [x["stage"] for x in LADDER]
    gross = np.array([x["gross_usd"] / 1000 for x in LADDER])
    local = np.array([x["local_value_usd"] / 1000 for x in LADDER])
    y = np.arange(len(labels))
    fig, ax = plt.subplots(figsize=(9.7, 5.9))
    header(fig, "One kilogram of platinum can enable millions in equipment", "Gross sales and illustrative local value at alternative endpoints; bars are not additive")
    ax.barh(y, gross, color=G300, height=0.58, label="Gross sales enabled")
    ax.barh(y, local, color=CORAL, height=0.58, label="Illustrative local value")
    for i, (g, v) in enumerate(zip(gross, local)):
        ax.text(g * 1.06, i, f"${g:,.0f}k", va="center", fontsize=7.1)
        ax.text(max(v * 0.92, 30), i, f"${v:,.0f}k", ha="right", va="center", fontsize=6.8, color=WHITE if v > 60 else BLACK, fontweight="bold")
    ax.set_xscale("log")
    ax.set_xlim(20, 5000)
    ax.set_yticks(y, labels)
    ax.invert_yaxis()
    ax.set_xlabel("USD thousand per kg platinum (log scale)")
    ax.legend(frameon=False, fontsize=7.3, loc="lower right")
    style_axis(ax, TOKENS, grid_axis="x")
    finish(fig, "value-ladder.png", left=0.20)


def make_module_frontier():
    fig, ax = plt.subplots(figsize=(9.8, 6.0))
    header(fig, "Components can outrun prestige projects", "Illustrative standalone modules; bubble area is direct employment and scales differ")
    preferred = {"Catalysts + chemicals", "MEAs", "Fuel-cell systems", "PEM components", "Mining / HD systems", "PGM recycling"}
    offsets = {
        "PGM refining": (-0.95, 0.32), "Catalysts + chemicals": (0.15, -0.28), "MEAs": (0.15, 0.15),
        "Fuel-cell stacks": (0.15, -0.38), "Fuel-cell systems": (0.15, 0.15), "PEM components": (0.22, 0.30),
        "PEM electrolysers": (-2.2, 0.25), "Green H2 production": (-2.3, 0.14),
        "Mining / HD systems": (0.15, -0.35), "PGM recycling": (0.15, -0.35),
    }
    for m in MODULES:
        color = CORAL if m["stage"] in preferred else G500
        ax.scatter(m["capex"], m["value"], s=45 + m["jobs"] * 0.35, color=color, edgecolor=BLACK, linewidth=0.5, alpha=0.9)
        dx, dy = offsets[m["stage"]]
        ax.text(m["capex"] + dx, m["value"] + dy, m["stage"], fontsize=6.5, fontweight="bold")
    ax.set_xlim(0, 9)
    ax.set_ylim(0, 4.5)
    ax.set_xlabel("Capital required (R billion)")
    ax.set_ylabel("Annual local value at model scale (R billion)")
    ax.legend(handles=[Line2D([0], [0], marker="o", color="none", markerfacecolor=CORAL, markeredgecolor=BLACK, markersize=7, label="Priority local layer"), Line2D([0], [0], marker="o", color="none", markerfacecolor=G500, markeredgecolor=BLACK, markersize=7, label="Base / partner / project")], frameon=False, fontsize=7.1, loc="upper left")
    style_axis(ax, TOKENS, grid_axis="both")
    finish(fig, "module-frontier.png", right=0.94)


def make_jobs_capital():
    labels = [m["stage"] for m in MODULES]
    vals = np.array([m["jobs"] / m["capex"] for m in MODULES])
    order = np.argsort(vals)
    labels = [labels[i] for i in order]
    vals = vals[order]
    fig, ax = plt.subplots(figsize=(9.6, 6.1))
    header(fig, "System integration is more job-dense than hydrogen production", "Illustrative direct jobs per R1 billion; construction and suppliers excluded")
    y = np.arange(len(labels))
    colors = [CORAL if s in {"Fuel-cell systems", "Mining / HD systems", "PGM recycling"} else G500 for s in labels]
    ax.barh(y, vals, color=colors, height=0.55)
    for i, v in enumerate(vals):
        ax.text(v + 3, i, f"{v:,.0f}", va="center", fontsize=7.0, fontweight="bold")
    ax.set_yticks(y, labels)
    ax.set_xlim(0, 230)
    ax.set_xlabel("Direct jobs per R1 billion capital")
    style_axis(ax, TOKENS, grid_axis="x")
    finish(fig, "jobs-capital.png", left=0.24)


def make_pgm_intensity():
    labels = ["PEM electrolysis\n2022 status", "PEM electrolysis\n2026 target", "PEM electrolysis\nultimate target", "Heavy-duty fuel cell\n2025 performance target"]
    kg_per_gw = np.array([800, 100, 30, 400])
    fig, ax = plt.subplots(figsize=(9.6, 5.7))
    header(fig, "Technology progress reduces metal per gigawatt", "PGM required at published US DOE intensity benchmarks; fuel-cell and electrolyser measures are not identical")
    y = np.arange(len(labels))
    colors = [G500, CORAL, BLACK, CORAL]
    ax.barh(y, kg_per_gw, color=colors, height=0.55)
    for i, v in enumerate(kg_per_gw):
        ax.text(v + 14, i, f"{v} kg/GW", va="center", fontsize=7.5, fontweight="bold")
    ax.set_yticks(y, labels)
    ax.invert_yaxis()
    ax.set_xlim(0, 900)
    ax.set_xlabel("PGM kilograms per GW of rated output")
    style_axis(ax, TOKENS, grid_axis="x")
    finish(fig, "pgm-intensity.png", left=0.26)


def make_hydrogen_reality():
    fig, axes = plt.subplots(1, 2, figsize=(10.4, 5.7))
    header(fig, "The hydrogen market is large; the clean market is still small", "Global totals from IEA 2026; announced projects are not equivalent to committed supply")
    left_labels = ["All hydrogen\ndemand", "Low-emissions\nsupply"]
    left_vals = [100, 1]
    axes[0].bar(left_labels, left_vals, color=[G500, CORAL], width=0.58)
    for i, v in enumerate(left_vals):
        axes[0].text(i, v + 3, f">{v} Mt" if i == 0 else "~1 Mt", ha="center", fontsize=8, fontweight="bold")
    axes[0].set_title("2025 reality", fontsize=9, fontweight="bold")
    axes[0].set_ylabel("Million tonnes per year")
    axes[0].set_ylim(0, 115)
    style_axis(axes[0], TOKENS, grid_axis="y")
    right_labels = ["Announced\npipeline", "Strong\npotential", "Committed"]
    right_vals = [27, 6, 4.3]
    axes[1].bar(right_labels, right_vals, color=[G500, CORAL, BLACK], width=0.58)
    for i, v in enumerate(right_vals):
        axes[1].text(i, v + 0.8, f"{v:g} Mt", ha="center", fontsize=8, fontweight="bold")
    axes[1].set_title("Possible 2030 low-emissions supply", fontsize=9, fontweight="bold")
    axes[1].set_ylabel("Million tonnes per year")
    axes[1].set_ylim(0, 31)
    style_axis(axes[1], TOKENS, grid_axis="y")
    finish(fig, "hydrogen-reality.png", left=0.09, right=0.98, top=0.76, bottom=0.17)


def make_electrolyser_market():
    fig, axes = plt.subplots(1, 2, figsize=(10.4, 5.7))
    header(fig, "South Africa would enter a China-led, underutilised market", "IEA global electrolysis deployment and manufacturing indicators")
    years = [2024, 2025]
    installed = [2, 4]
    axes[0].bar(years, installed, color=[G500, CORAL], width=0.55)
    for x, v in zip(years, installed):
        axes[0].text(x, v + 0.15, f">{v} GW" if x == 2025 else f"{v} GW", ha="center", fontsize=8, fontweight="bold")
    axes[0].set_xticks(years)
    axes[0].set_title("Installed electrolysis capacity", fontsize=9, fontweight="bold")
    axes[0].set_ylabel("GW")
    axes[0].set_ylim(0, 4.8)
    style_axis(axes[0], TOKENS, grid_axis="y")
    share = [75, 25]
    axes[1].barh([0], share[0], color=CORAL, height=0.45, label="China")
    axes[1].barh([0], share[1], left=share[0], color=G300, height=0.45, label="Rest of world")
    axes[1].text(37.5, 0, "China ~75%", ha="center", va="center", color=WHITE, fontsize=9, fontweight="bold")
    axes[1].text(87.5, 0, "Other ~25%", ha="center", va="center", color=BLACK, fontsize=8, fontweight="bold")
    axes[1].set_title("Share of new capacity in 2025", fontsize=9, fontweight="bold")
    axes[1].set_xlim(0, 100)
    axes[1].set_ylim(-0.8, 0.8)
    axes[1].set_yticks([])
    axes[1].set_xlabel("Share of additions (%)")
    style_axis(axes[1], TOKENS, grid_axis="x")
    finish(fig, "electrolyser-market.png", left=0.09, right=0.98, top=0.76, bottom=0.17)


def make_h2_heatmap():
    capex = np.array([5.0, 8.0, 11.0])
    util = np.array([45, 60, 75, 90])
    z = np.array([[hydrogen_break_even_usd_kg(c, u / 100) for u in util] for c in capex])
    fig, ax = plt.subplots(figsize=(9.4, 5.7))
    header(fig, "Cheap electricity is necessary but not sufficient", "Break-even green-hydrogen price for a 100 MW project at R0.75/kWh; 20 years, 8% real capital charge")
    im = ax.imshow(z, cmap="Greys", aspect="auto", vmin=3.5, vmax=15)
    ax.set_xticks(np.arange(len(util)), [f"{u}%" for u in util])
    ax.set_yticks(np.arange(len(capex)), [f"R{c:g}bn" for c in capex])
    ax.set_xlabel("Electrolyser utilisation")
    ax.set_ylabel("Integrated project capital")
    for i in range(len(capex)):
        for j in range(len(util)):
            if capex[i] == 8 and util[j] == 60:
                ax.add_patch(Rectangle((j - 0.48, i - 0.48), 0.96, 0.96, facecolor="none", edgecolor=CORAL, linewidth=2.2))
            ax.text(j, i, f"${z[i, j]:.1f}/kg", ha="center", va="center", fontsize=8, color=WHITE if z[i, j] > 9 else BLACK, fontweight="bold")
    cbar = fig.colorbar(im, ax=ax, fraction=0.035, pad=0.03)
    cbar.set_label("Break-even USD/kg H2")
    finish(fig, "hydrogen-break-even.png", left=0.14, right=0.90, top=0.77, bottom=0.16)


def make_power_cost():
    tariffs = np.array([0.40, 0.55, 0.75, 0.95, 1.20])
    energy = tariffs * 54 / USDZAR
    other_variable = np.repeat(8 / USDZAR, len(tariffs))
    fixed = np.repeat((8e9 * (annuity_factor() + 0.03) / hydrogen_output_kg(100, 0.65)) / USDZAR, len(tariffs))
    fig, ax = plt.subplots(figsize=(9.7, 5.8))
    header(fig, "Electricity cannot rescue underused capital", "Central 100 MW project at 65% utilisation; illustrative USD/kg cost decomposition")
    x = np.arange(len(tariffs))
    ax.bar(x, energy, color=CORAL, width=0.62, label="Electricity")
    ax.bar(x, other_variable, bottom=energy, color=G300, width=0.62, label="Water + variable O&M")
    ax.bar(x, fixed, bottom=energy + other_variable, color=BLACK, width=0.62, label="Capital + fixed O&M")
    totals = energy + other_variable + fixed
    for i, v in enumerate(totals):
        ax.text(i, v + 0.18, f"${v:.1f}", ha="center", fontsize=7.5, fontweight="bold")
    ax.set_xticks(x, [f"R{t:.2f}" for t in tariffs])
    ax.set_xlabel("Delivered electricity tariff (R/kWh)")
    ax.set_ylabel("Break-even hydrogen cost (USD/kg)")
    ax.set_ylim(0, max(totals) * 1.2)
    ax.legend(frameon=False, fontsize=7.2, loc="upper left")
    style_axis(ax, TOKENS, grid_axis="y")
    finish(fig, "power-cost.png")


def make_applications():
    apps = ["Existing ammonia / refining", "Mine haul + off-road", "Truck / bus corridors", "Stationary backup", "Passenger vehicles", "Hydrogen export"]
    metrics = ["Demand\nvisibility", "Technical\nfit", "PGM component\nopportunity"]
    scores = np.array([[90, 72, 58], [62, 88, 92], [52, 78, 86], [70, 68, 78], [24, 35, 70], [38, 58, 32]])
    fig, ax = plt.subplots(figsize=(9.5, 6.0))
    header(fig, "Start where demand is concentrated and operation is controlled", "Illustrative opportunity scores; judgement framework, not a market forecast")
    im = ax.imshow(scores, cmap="Greys", aspect="auto", vmin=0, vmax=100)
    ax.set_xticks(np.arange(len(metrics)), metrics)
    ax.set_yticks(np.arange(len(apps)), apps)
    for i in range(scores.shape[0]):
        for j in range(scores.shape[1]):
            ax.text(j, i, f"{scores[i, j]}", ha="center", va="center", fontsize=8, color=WHITE if scores[i, j] > 74 else BLACK, fontweight="bold")
    ax.add_patch(Rectangle((-0.48, 0.52), 2.96, 1.96, facecolor="none", edgecolor=CORAL, linewidth=2.2))
    cbar = fig.colorbar(im, ax=ax, fraction=0.035, pad=0.03)
    cbar.set_label("Opportunity score (0–100)")
    finish(fig, "application-map.png", left=0.25, right=0.90, top=0.76, bottom=0.15)


def make_strategy_portfolio():
    data = {
        "Metal-export base": {"value": 5.4, "exports": 10.5, "jobs": 2200, "risk": 0.88},
        "Components-first": {"value": 8.2, "exports": 8.5, "jobs": 3000, "risk": 0.82},
        "Systems + anchors": {"value": 9.5, "exports": 7.2, "jobs": 4200, "risk": 0.76},
        "Hydrogen-export first": {"value": 5.8, "exports": 6.5, "jobs": 1700, "risk": 0.48},
    }
    labels = list(data)
    value = np.array([data[k]["value"] * data[k]["risk"] for k in labels])
    exports = np.array([data[k]["exports"] * data[k]["risk"] for k in labels])
    jobs = np.array([data[k]["jobs"] * data[k]["risk"] for k in labels])
    fig, axes = plt.subplots(1, 3, figsize=(10.5, 5.7))
    header(fig, "Components and anchor markets beat molecule-first ambition", "Risk-adjusted outcomes from illustrative R20 billion portfolios; ranking tool, not a budget proposal")
    panels = [(value, "Annual local value", "R billion"), (exports, "Annual exports", "R billion"), (jobs, "Direct jobs", "jobs")]
    x = np.arange(len(labels))
    for ax, (vals, title, unit) in zip(axes, panels):
        colors = [CORAL if label == "Systems + anchors" else G500 for label in labels]
        ax.bar(x, vals, color=colors, width=0.62)
        for i, v in enumerate(vals):
            ax.text(i, v + max(vals) * 0.04, f"{v:,.0f}" if unit == "jobs" else f"{v:.1f}", ha="center", fontsize=7.0, fontweight="bold")
        ax.set_title(title, fontsize=8.5, fontweight="bold")
        ax.set_xticks(x, [s.replace(" ", "\n") for s in labels], fontsize=5.8)
        ax.set_ylabel(unit)
        ax.set_ylim(0, max(vals) * 1.25)
        style_axis(ax, TOKENS, grid_axis="y")
    finish(fig, "strategy-portfolios.png", left=0.08, right=0.98, top=0.76, bottom=0.22)


def main():
    makers = [make_endowment, make_chain_map, make_value_ladder, make_module_frontier, make_jobs_capital, make_pgm_intensity, make_hydrogen_reality, make_electrolyser_market, make_h2_heatmap, make_power_cost, make_applications, make_strategy_portfolio]
    for maker in makers:
        maker()
    results = {
        "units": {"currency": "constant 2026 rand unless stated", "usd_zar_model_rate": USDZAR, "platinum_price_usd_oz": PLATINUM_USD_OZ},
        "value_ladder": LADDER,
        "modules": MODULES,
        "hydrogen_project": {
            "electrolyser_mw": 100,
            "central_utilisation": 0.65,
            "central_capex_r_bn": 8,
            "electricity_r_kwh": 0.75,
            "efficiency_kwh_kg": 54,
            "annual_hydrogen_t": round(hydrogen_output_kg(100, 0.65) / 1000, 1),
            "break_even_usd_kg": round(hydrogen_break_even_usd_kg(8, 0.65, 0.75), 2),
        },
        "notes": ["Scenarios are not forecasts or investment advice.", "Value-ladder endpoints are alternatives and must not be summed.", "Module scales are independent and not mass-balanced.", "PGM intensity benchmarks use different technology definitions and are directional."],
    }
    (WORK / "model_results.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(json.dumps(results["hydrogen_project"], indent=2))
    print(f"Wrote {len(list(ASSETS.glob('*.png')))} figures to {ASSETS}")


if __name__ == "__main__":
    main()
