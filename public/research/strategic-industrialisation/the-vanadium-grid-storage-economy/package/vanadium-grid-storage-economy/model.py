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
V2O5_USD_LB = 8.0
V_TO_V2O5 = 1.785
LITRES_PER_KWH = 50.0
V_KG_PER_LITRE = 0.087


def header(fig, title, subtitle):
    add_figure_header(fig, title, subtitle, field="GREYSCIENCX / PAPER 7", tokens=TOKENS)


def finish(fig, filename, *, left=0.10, right=0.97, top=0.77, bottom=0.14):
    fig.subplots_adjust(left=left, right=right, top=top, bottom=bottom)
    save_figure(fig, ASSETS / filename, dpi=270)
    plt.close(fig)


LADDER = [
    {"stage": "V2O5 product", "gross_usd": V_TO_V2O5 * 2204.62 * V2O5_USD_LB, "local_share": 0.70},
    {"stage": "Qualified electrolyte", "gross_usd": (1000 / V_KG_PER_LITRE) * 5.0, "local_share": 0.55},
    {"stage": "VRFB energy block", "gross_usd": (1000 / V_KG_PER_LITRE / LITRES_PER_KWH) * 220, "local_share": 0.48},
    {"stage": "Complete 10 h system", "gross_usd": (1000 / V_KG_PER_LITRE / LITRES_PER_KWH) * 446, "local_share": 0.36},
]
for row in LADDER:
    row["local_value_usd"] = row["gross_usd"] * row["local_share"]


MODULES = [
    {"stage": "Vanadium mining", "scale": "5 kt V/y", "capex": 4.0, "sales": 2.80, "exports": 2.35, "value": 1.60, "jobs": 600, "energy": 400, "water": 0.80},
    {"stage": "V2O5 refining", "scale": "8 kt/y", "capex": 3.0, "sales": 2.50, "exports": 1.90, "value": 1.30, "jobs": 300, "energy": 250, "water": 0.50},
    {"stage": "Electrolyte", "scale": "8m L/y", "capex": 0.4, "sales": 0.55, "exports": 0.35, "value": 0.30, "jobs": 59, "energy": 20, "water": 0.05},
    {"stage": "Membranes", "scale": "250 MW/y", "capex": 1.2, "sales": 1.80, "exports": 1.10, "value": 0.55, "jobs": 160, "energy": 15, "water": 0.02},
    {"stage": "VRFB stacks", "scale": "100 MW/y", "capex": 1.8, "sales": 2.50, "exports": 1.50, "value": 0.80, "jobs": 250, "energy": 25, "water": 0.02},
    {"stage": "Pumps + BOS", "scale": "100 MW/y", "capex": 1.0, "sales": 1.80, "exports": 0.85, "value": 0.70, "jobs": 300, "energy": 15, "water": 0.02},
    {"stage": "Power electronics", "scale": "250 MW/y", "capex": 1.2, "sales": 2.70, "exports": 1.30, "value": 0.90, "jobs": 280, "energy": 20, "water": 0.01},
    {"stage": "Container systems", "scale": "100 MW / 1 GWh/y", "capex": 3.5, "sales": 8.00, "exports": 3.80, "value": 2.40, "jobs": 500, "energy": 50, "water": 0.03},
    {"stage": "Project integration", "scale": "100 MW / 1 GWh/y", "capex": 0.8, "sales": 1.50, "exports": 0.45, "value": 0.85, "jobs": 350, "energy": 5, "water": 0.01},
    {"stage": "Electrolyte recovery", "scale": "8m L/y service", "capex": 0.6, "sales": 0.50, "exports": 0.20, "value": 0.30, "jobs": 80, "energy": 10, "water": 0.04},
]


def capex_usd_kwh(technology, duration):
    duration = np.asarray(duration, dtype=float)
    if technology == "LFP":
        return 300.0 + 790.0 / duration
    if technology == "VRFB":
        return 220.0 + 2260.0 / duration
    raise ValueError(technology)


def pv_factor(rate=0.08, years=25):
    return sum(1 / (1 + rate) ** year for year in range(1, years + 1))


def storage_lcos_usd_kwh(technology, duration, cycles=250, vanadium_multiplier=1.0):
    years = 25
    rate = 0.08
    duration = float(duration)
    power_kw = 100_000
    energy_kwh = power_kw * duration
    base_cost = float(capex_usd_kwh(technology, duration))
    if technology == "VRFB":
        energy_share = 0.40
        adjusted_cost = base_cost * ((1 - energy_share) + energy_share * vanadium_multiplier)
        rte = 0.72
        fom = 0.020
        replacement = 0.50 * 2260.0 * power_kw
        replacement_year = 15
    else:
        adjusted_cost = base_cost
        rte = 0.85
        fom = 0.015
        replacement = 0.65 * adjusted_cost * energy_kwh
        replacement_year = 14
    capex = adjusted_cost * energy_kwh
    discounted_cost = capex + capex * fom * pv_factor(rate, years)
    discounted_cost += replacement / (1 + rate) ** replacement_year
    annual_output = energy_kwh * cycles
    discounted_output = annual_output * pv_factor(rate, years)
    charge_price = 0.75 / USDZAR
    discounted_cost += (annual_output / rte) * charge_price * pv_factor(rate, years)
    return discounted_cost / discounted_output


def make_endowment():
    labels = ["2025 mine\nproduction", "Reported\nreserves"]
    values = [5000 / 110000 * 100, 520 / 21000 * 100]
    fig, ax = plt.subplots(figsize=(9.4, 5.3))
    header(fig, "South Africa matters, but does not dominate vanadium", "USGS 2026; production and reserve shares use different measures")
    y = np.arange(len(labels))
    ax.barh(y, [100, 100], color=G100, height=0.52)
    ax.barh(y, values, color=CORAL, height=0.52)
    for i, v in enumerate(values):
        ax.text(v + 1.2, i, f"{v:.1f}%", va="center", fontsize=10, fontweight="bold")
    ax.set_yticks(y, labels)
    ax.invert_yaxis()
    ax.set_xlim(0, 100)
    ax.set_xlabel("South African share of reported world total (%)")
    style_axis(ax, TOKENS, grid_axis="x")
    finish(fig, "endowment.png", left=0.15)


def make_chain_map():
    fig, ax = plt.subplots(figsize=(10.4, 5.0))
    header(fig, "The viable chain is selective, not compulsory", "Own electrolyte and integration; partner where qualification and volume dominate")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4)
    ax.axis("off")
    stages = [
        (0.35, "MINE +\nV2O5", "BASE", CORAL),
        (1.72, "ELECTROLYTE", "MAKE", CORAL),
        (3.09, "MEMBRANE", "PARTNER", G500),
        (4.46, "STACK", "PARTNER", G500),
        (5.83, "PUMPS + BOS", "MAKE", CORAL),
        (7.20, "CONTAINER", "MAKE", CORAL),
        (8.57, "GRID SERVICE", "OWN", CORAL),
    ]
    for i, (x, label, tag, colour) in enumerate(stages):
        ax.add_patch(Rectangle((x, 1.35), 1.08, 1.25, facecolor=colour, edgecolor=BLACK, linewidth=0.9))
        txt_colour = WHITE if colour != G100 else BLACK
        ax.text(x + 0.54, 2.05, label, ha="center", va="center", fontsize=8.5, color=txt_colour, fontweight="bold")
        ax.text(x + 0.54, 1.55, tag, ha="center", va="center", fontsize=7.5, color=txt_colour)
        if i < len(stages) - 1:
            ax.add_patch(FancyArrowPatch((x + 1.10, 1.98), (stages[i + 1][0] - 0.05, 1.98), arrowstyle="-|>", mutation_scale=11, color=BLACK, linewidth=1))
    ax.text(5.0, 0.78, "Demand anchors: long-duration tenders, mines, industrial microgrids, municipalities and renewable projects", ha="center", fontsize=9, color=G700)
    finish(fig, "chain-map.png", left=0.04, right=0.98, bottom=0.08)


def make_value_ladder():
    stages = [row["stage"] for row in LADDER]
    gross = np.array([row["gross_usd"] for row in LADDER]) / 1000
    local = np.array([row["local_value_usd"] for row in LADDER]) / 1000
    fig, ax = plt.subplots(figsize=(9.8, 5.7))
    header(fig, "A tonne of vanadium can enable a larger system invoice", "Illustrative USD thousand per tonne of contained V; endpoints are alternatives")
    y = np.arange(len(stages))
    ax.barh(y, gross, color=G300, height=0.58, label="Gross product sales")
    ax.barh(y, local, color=CORAL, height=0.58, label="Assumed local value")
    for i, (g, l) in enumerate(zip(gross, local)):
        ax.text(g + 2, i, f"${g:,.0f}k", va="center", fontsize=9, fontweight="bold")
        ax.text(max(l - 2, 1), i, f"${l:,.0f}k", va="center", ha="right", fontsize=8, color=WHITE if l > 12 else BLACK, fontweight="bold")
    ax.set_yticks(y, stages)
    ax.invert_yaxis()
    ax.set_xlabel("USD thousand per tonne of contained vanadium")
    ax.legend(frameon=False, loc="upper right")
    style_axis(ax, TOKENS, grid_axis="x")
    finish(fig, "value-ladder.png", left=0.22, right=0.93)


def make_storage_demand():
    labels = ["Installed BESS\n(IRP 2025)", "Eskom phase 1\nenergy / power", "BESIPPPP\nrounds 1-3", "IRP 2025\nstorage to 2039"]
    power = [0.2, 0.199, 1.744, 8.5]
    fig, ax = plt.subplots(figsize=(9.8, 5.5))
    header(fig, "The domestic storage market is becoming material", "GW; installed capacity, awarded/procured rounds and a planning allocation are not equivalent")
    x = np.arange(len(labels))
    colors = [BLACK, G500, CORAL, G300]
    bars = ax.bar(x, power, color=colors, width=0.62)
    for b, v in zip(bars, power):
        ax.text(b.get_x() + b.get_width()/2, v + 0.18, f"{v:.3g} GW", ha="center", fontsize=9, fontweight="bold")
    ax.text(1, 1.05, "833 MWh / 199 MW\n≈ 4.2 hours", ha="center", fontsize=8.5, color=G700)
    ax.set_xticks(x, labels)
    ax.set_ylabel("Power capacity (GW)")
    ax.set_ylim(0, 9.5)
    style_axis(ax, TOKENS, grid_axis="y")
    finish(fig, "storage-demand.png", left=0.11, right=0.96, bottom=0.20)


def make_belco_scale():
    fig, axes = plt.subplots(1, 2, figsize=(10.4, 5.2))
    header(fig, "One long-duration project can absorb several years of electrolyte output", "BELCO design capacity compared with an illustrative 100 MW / 10 h VRFB")
    vals1 = [8, 50]
    vals2 = [160, 1000]
    labels = ["BELCO annual\ndesign", "100 MW / 10 h\nproject"]
    for ax, vals, ylabel in zip(axes, [vals1, vals2], ["Electrolyte (million litres)", "Energy capacity (MWh)"]):
        bars = ax.bar([0, 1], vals, color=[CORAL, BLACK], width=0.58)
        for b, v in zip(bars, vals):
            ax.text(b.get_x() + b.get_width()/2, v * 1.03 + max(vals)*0.02, f"{v:,.0f}", ha="center", fontsize=10, fontweight="bold")
        ax.set_xticks([0, 1], labels)
        ax.set_ylabel(ylabel)
        ax.set_ylim(0, max(vals)*1.18)
        style_axis(ax, TOKENS, grid_axis="y")
    finish(fig, "belco-scale.png", left=0.09, right=0.97, bottom=0.20, top=0.73)


def make_module_frontier():
    fig, ax = plt.subplots(figsize=(10.4, 6.2))
    header(fig, "Systems create value only when projects create orders", "Illustrative standalone modules; bubble area is direct employment and scales differ")
    preferred = {"Electrolyte", "Pumps + BOS", "Power electronics", "Container systems", "Project integration", "Electrolyte recovery"}
    offsets = {
        "Vanadium mining": (0.10, 0.12), "V2O5 refining": (0.10, -0.30), "Electrolyte": (0.12, 0.12),
        "Membranes": (0.10, -0.06), "VRFB stacks": (0.10, -0.30), "Pumps + BOS": (0.10, 0.13),
        "Power electronics": (0.10, 0.28), "Container systems": (-1.25, 0.15), "Project integration": (-0.28, 0.16),
        "Electrolyte recovery": (0.10, -0.27),
    }
    for row in MODULES:
        colour = CORAL if row["stage"] in preferred else G500
        ax.scatter(row["capex"], row["value"], s=row["jobs"]*1.8, color=colour, edgecolor=BLACK, linewidth=0.8, alpha=0.9)
        dx, dy = offsets[row["stage"]]
        ax.text(row["capex"] + dx, row["value"] + dy, row["stage"], fontsize=8.5, fontweight="bold")
    ax.legend(handles=[
        Line2D([0], [0], marker="o", color="none", markerfacecolor=CORAL, markeredgecolor=BLACK, markersize=9, label="Priority local layer"),
        Line2D([0], [0], marker="o", color="none", markerfacecolor=G500, markeredgecolor=BLACK, markersize=9, label="Base / partner layer"),
    ], frameon=False, loc="upper left")
    ax.set_xlim(0, 4.5)
    ax.set_ylim(0, 2.8)
    ax.set_xlabel("Capital required (R billion)")
    ax.set_ylabel("Annual local value at model scale (R billion)")
    style_axis(ax, TOKENS, grid_axis="both")
    finish(fig, "module-frontier.png", left=0.11, right=0.95)


def make_jobs_capital():
    rows = sorted(MODULES, key=lambda r: r["jobs"] / r["capex"], reverse=True)
    labels = [r["stage"] for r in rows]
    values = [r["jobs"] / r["capex"] for r in rows]
    fig, ax = plt.subplots(figsize=(9.8, 6.0))
    header(fig, "Integration is more job-dense than bulk materials", "Direct operating jobs per R1 billion of illustrative capital")
    y = np.arange(len(labels))
    colors = [CORAL if x in {"Project integration", "Pumps + BOS", "Power electronics"} else G500 for x in labels]
    bars = ax.barh(y, values, color=colors, height=0.58)
    for b, v in zip(bars, values):
        ax.text(v + 5, b.get_y() + b.get_height()/2, f"{v:,.0f}", va="center", fontsize=8.5, fontweight="bold")
    ax.set_yticks(y, labels)
    ax.invert_yaxis()
    ax.set_xlabel("Direct jobs per R1 billion capital")
    ax.set_xlim(0, max(values)*1.18)
    style_axis(ax, TOKENS, grid_axis="x")
    finish(fig, "jobs-capital.png", left=0.23, right=0.95)


def make_cost_duration():
    durations = np.array([2, 4, 6, 8, 10, 12, 16, 20, 24])
    fig, ax = plt.subplots(figsize=(9.8, 5.6))
    header(fig, "Flow batteries buy duration with tanks; lithium buys more cells", "Illustrative installed cost calibrated to PNNL's 100 MW / 10 h point estimates")
    ax.plot(durations, capex_usd_kwh("LFP", durations), color=CORAL, marker="o", linewidth=2.4, label="LFP")
    ax.plot(durations, capex_usd_kwh("VRFB", durations), color=BLACK, marker="s", linestyle="--", linewidth=2.2, label="Vanadium flow")
    ax.scatter([10, 10], [379, 446], color=[CORAL, BLACK], s=55, zorder=4)
    ax.text(10.4, 352, "$379/kWh", va="center", fontsize=8.5, color=CORAL, fontweight="bold")
    ax.text(10.4, 478, "$446/kWh", va="center", fontsize=8.5, color=BLACK, fontweight="bold")
    ax.set_xlabel("Storage duration (hours)")
    ax.set_ylabel("Installed cost (USD/kWh)")
    ax.set_xlim(2, 24)
    ax.set_ylim(250, 1400)
    ax.legend(frameon=False)
    style_axis(ax, TOKENS, grid_axis="both")
    finish(fig, "cost-duration.png", left=0.11, right=0.95)


def make_lcos_duration():
    durations = np.array([4, 6, 8, 10, 12, 16, 20, 24])
    lfp = np.array([storage_lcos_usd_kwh("LFP", d) for d in durations]) * USDZAR
    vrfb = np.array([storage_lcos_usd_kwh("VRFB", d) for d in durations]) * USDZAR
    fig, ax = plt.subplots(figsize=(9.8, 5.6))
    header(fig, "Vanadium reaches the contest only at long duration", "Illustrative 25-year LCOS; 250 full cycles/year, R0.75/kWh charging energy, 8% real discount rate")
    ax.plot(durations, lfp, color=CORAL, marker="o", linewidth=2.4, label="LFP")
    ax.plot(durations, vrfb, color=BLACK, marker="s", linestyle="--", linewidth=2.2, label="Vanadium flow")
    gap = np.abs(lfp-vrfb)
    cross_i = int(np.argmin(gap))
    ax.axvline(durations[cross_i], color=G300, linewidth=1.2)
    ax.text(durations[cross_i]+0.4, max(lfp[cross_i], vrfb[cross_i])+0.25, f"near-parity ≈ {durations[cross_i]} h", fontsize=8.5, fontweight="bold")
    ax.set_xlabel("Storage duration (hours)")
    ax.set_ylabel("Levelised cost of delivered storage (R/kWh)")
    ax.set_xlim(4, 24)
    ax.legend(frameon=False)
    style_axis(ax, TOKENS, grid_axis="both")
    finish(fig, "lcos-duration.png", left=0.12, right=0.95)


def make_sensitivity():
    cycles = np.array([150, 250, 350, 450])
    vm = np.array([0.6, 1.0, 1.4, 1.8])
    grid = np.array([[storage_lcos_usd_kwh("VRFB", 10, cycles=int(c), vanadium_multiplier=float(m))*USDZAR for c in cycles] for m in vm])
    fig, ax = plt.subplots(figsize=(9.4, 5.7))
    header(fig, "Vanadium price matters; utilisation matters more", "Illustrative 10-hour VRFB LCOS in R/kWh; coral outline is the central case")
    im = ax.imshow(grid, cmap="Greys", aspect="auto")
    for i in range(len(vm)):
        for j in range(len(cycles)):
            color = WHITE if grid[i, j] > np.median(grid) else BLACK
            ax.text(j, i, f"R{grid[i,j]:.2f}", ha="center", va="center", color=color, fontweight="bold", fontsize=9)
    ax.add_patch(Rectangle((0.5, 0.5), 1, 1, fill=False, edgecolor=CORAL, linewidth=3))
    ax.set_xticks(range(len(cycles)), [f"{c}" for c in cycles])
    ax.set_yticks(range(len(vm)), [f"{m:.1f}×" for m in vm])
    ax.set_xlabel("Full cycles per year")
    ax.set_ylabel("Vanadium-linked cost multiplier")
    cbar = fig.colorbar(im, ax=ax, fraction=0.036, pad=0.03)
    cbar.set_label("LCOS (R/kWh)")
    finish(fig, "sensitivity.png", left=0.14, right=0.91)


def make_leasing():
    capex_total = 446 * 1_000_000 * USDZAR / 1e9
    electrolyte = capex_total * 0.40
    non_electrolyte = capex_total - electrolyte
    lease_base_pv = electrolyte * 0.09 * pv_factor()
    lease_conc_pv = electrolyte * 0.07 * pv_factor()
    labels = ["Direct\npurchase", "Commercial\nelectrolyte lease", "Concessional\nelectrolyte lease"]
    upfront = [capex_total, non_electrolyte, non_electrolyte]
    future = [0, lease_base_pv, lease_conc_pv]
    fig, ax = plt.subplots(figsize=(9.8, 5.6))
    header(fig, "Leasing solves the upfront bill, not the underlying cost", "Illustrative 100 MW / 10 h VRFB; present value at 8% real over 25 years")
    x = np.arange(3)
    ax.bar(x, upfront, color=CORAL, width=0.58, label="Upfront project capital")
    ax.bar(x, future, bottom=upfront, color=G500, width=0.58, label="Present value of lease payments")
    for i, (u, f) in enumerate(zip(upfront, future)):
        ax.text(i, u+f+0.15, f"R{u+f:.1f}bn NPV", ha="center", fontsize=9, fontweight="bold")
        ax.text(i, u/2, f"R{u:.1f}bn\nupfront", ha="center", va="center", color=WHITE, fontsize=8.5, fontweight="bold")
    ax.set_xticks(x, labels)
    ax.set_ylabel("Financing requirement / present value (R billion)")
    ax.legend(frameon=False, loc="lower center", bbox_to_anchor=(0.5, -0.22), ncol=2)
    style_axis(ax, TOKENS, grid_axis="y")
    finish(fig, "leasing.png", left=0.11, right=0.96, bottom=0.25)


def make_application_map():
    rows = ["Fast ancillary services", "Four-hour peak shifting", "8–12 h renewable shifting", "Industrial microgrids", "Municipal resilience", "Multi-day backup"]
    matrix = np.array([[95, 35, 45], [95, 55, 55], [72, 90, 90], [65, 85, 80], [50, 78, 75], [25, 55, 60]])
    fig, ax = plt.subplots(figsize=(9.8, 6.1))
    header(fig, "Target the uses where duration, safety and cycling are valuable", "Illustrative opportunity scores; judgement framework, not a demand forecast")
    im = ax.imshow(matrix, cmap="Greys", vmin=0, vmax=100, aspect="auto")
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            ax.text(j, i, f"{matrix[i,j]}", ha="center", va="center", color=WHITE if matrix[i,j] > 75 else BLACK, fontweight="bold", fontsize=9)
    ax.add_patch(Rectangle((-0.48, 1.52), 2.96, 2.0, fill=False, edgecolor=CORAL, linewidth=3))
    ax.set_yticks(range(len(rows)), rows)
    ax.set_xticks(range(3), ["Demand\nvisibility", "Technical\nfit", "Local-industry\nopportunity"])
    cbar = fig.colorbar(im, ax=ax, fraction=0.035, pad=0.03)
    cbar.set_label("Opportunity score (0–100)")
    finish(fig, "application-map.png", left=0.23, right=0.90, bottom=0.18)


def make_portfolios():
    labels = ["Mineral-export\nbase", "Electrolyte-\nfirst", "Full VRFB\nchain", "Technology-neutral\nstorage hub"]
    nominal_value = np.array([5.4, 4.8, 6.5, 7.4])
    nominal_exports = np.array([9.0, 3.5, 4.0, 5.2])
    nominal_jobs = np.array([2200, 1800, 3000, 3600])
    delivery = np.array([0.85, 0.70, 0.60, 0.80])
    metrics = [nominal_value*delivery, nominal_exports*delivery, nominal_jobs*delivery]
    titles = ["Annual local value", "Annual exports", "Direct jobs"]
    ylabels = ["R billion", "R billion", "jobs"]
    fig, axes = plt.subplots(1, 3, figsize=(11.0, 5.5))
    header(fig, "A storage-industry platform beats a vanadium-only flagship", "Risk-adjusted outcomes from illustrative R20 billion portfolios; ranking tool, not a budget")
    for ax, values, title, ylabel in zip(axes, metrics, titles, ylabels):
        colors = [G500, G500, G500, CORAL]
        bars = ax.bar(np.arange(4), values, color=colors, width=0.62)
        ax.set_title(title, fontsize=11, fontweight="bold")
        ax.set_ylabel(ylabel)
        ax.set_xticks(np.arange(4), labels, fontsize=7.5)
        for b, v in zip(bars, values):
            label = f"{v:,.0f}" if ylabel == "jobs" else f"{v:.1f}"
            ax.text(b.get_x()+b.get_width()/2, v + max(values)*0.03, label, ha="center", fontsize=8.5, fontweight="bold")
        ax.set_ylim(0, max(values)*1.20)
        style_axis(ax, TOKENS, grid_axis="y")
    finish(fig, "strategy-portfolios.png", left=0.07, right=0.98, top=0.73, bottom=0.20)


def main():
    make_endowment()
    make_chain_map()
    make_value_ladder()
    make_storage_demand()
    make_belco_scale()
    make_module_frontier()
    make_jobs_capital()
    make_cost_duration()
    make_lcos_duration()
    make_sensitivity()
    make_leasing()
    make_application_map()
    make_portfolios()

    durations = [4, 8, 10, 12, 16, 24]
    results = {
        "units": {"currency": "constant 2026 rand unless stated", "usd_zar_model_rate": USDZAR, "analytical_v2o5_price_usd_lb": V2O5_USD_LB},
        "endowment": {"south_africa_2025_t_v": 5000, "world_2025_t_v": 110000, "south_africa_reserves_kt_v": 520, "world_reserves_kt_v": 21000},
        "value_ladder": LADDER,
        "modules": MODULES,
        "belco": {"design_litres_per_year": 8_000_000, "model_mwh_per_year": 160, "jobs": 59, "reported_investment_r_million": 400},
        "storage_costs": [{"duration_h": d, "lfp_capex_usd_kwh": float(capex_usd_kwh("LFP", d)), "vrfb_capex_usd_kwh": float(capex_usd_kwh("VRFB", d)), "lfp_lcos_r_kwh": storage_lcos_usd_kwh("LFP", d)*USDZAR, "vrfb_lcos_r_kwh": storage_lcos_usd_kwh("VRFB", d)*USDZAR} for d in durations],
        "central_project": {"power_mw": 100, "duration_h": 10, "energy_mwh": 1000, "lfp_capex_usd_m": 379, "vrfb_capex_usd_m": 446, "vrfb_capex_r_bn": 446*USDZAR/1000, "electrolyte_litres_m": 50, "belco_years_output": 6.25},
        "notes": ["Scenarios are not forecasts or investment advice.", "Value-ladder endpoints are alternatives and must not be summed.", "Module scales are independent and not mass-balanced.", "LCOS is a model result sensitive to cycling, replacement, efficiency, finance and charging-energy assumptions."],
    }
    (WORK / "model_results.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(json.dumps(results["central_project"], indent=2))
    print(f"Wrote 13 figures to {ASSETS}")


if __name__ == "__main__":
    main()
