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

FUND = 253.54

STAGES = [
    "Resource",
    "Primary\nrefining",
    "Advanced\nmaterials",
    "Core\ncomponents",
    "System\nassembly",
    "Services &\nrecycling",
]
VALUE_WEIGHTS = np.array([0.12, 0.16, 0.20, 0.22, 0.22, 0.08])

LOCAL_SHARE = {
    "Current footprint": {
        "Manganese": [95, 45, 8, 4, 30, 8],
        "PGM / hydrogen": [92, 80, 45, 18, 20, 35],
        "Vanadium / VRFB": [70, 60, 55, 20, 35, 30],
    },
    "Focused integration": {
        "Manganese": [95, 65, 65, 35, 70, 45],
        "PGM / hydrogen": [95, 88, 72, 52, 58, 70],
        "Vanadium / VRFB": [80, 75, 80, 50, 70, 65],
    },
    "Frontier partnership": {
        "Manganese": [95, 80, 82, 60, 82, 70],
        "PGM / hydrogen": [98, 92, 85, 75, 80, 86],
        "Vanadium / VRFB": [90, 85, 90, 72, 85, 82],
    },
}
CHAIN_WEIGHTS = {"Manganese": 0.40, "PGM / hydrogen": 0.35, "Vanadium / VRFB": 0.25}

ITEMS = [
    ("Manganese ore", "Manganese", 91, 38, 20),
    ("Manganese alloys", "Manganese", 63, 54, 48),
    ("High-purity Mn sulphate", "Manganese", 74, 91, 43),
    ("Precursor / cathode material", "Manganese", 58, 84, 67),
    ("Battery cells", "Manganese", 30, 88, 96),
    ("Pack, BMS and integration", "Manganese", 68, 70, 44),
    ("PGM refining", "PGM / hydrogen", 86, 58, 42),
    ("Catalyst powder and inks", "PGM / hydrogen", 72, 86, 38),
    ("Membrane-electrode assemblies", "PGM / hydrogen", 58, 90, 55),
    ("Electrolyser / fuel-cell stacks", "PGM / hydrogen", 46, 82, 72),
    ("Hydrogen system integration", "PGM / hydrogen", 52, 77, 78),
    ("PGM recycling", "PGM / hydrogen", 78, 74, 34),
    ("Vanadium pentoxide", "Vanadium / VRFB", 70, 59, 45),
    ("VRFB electrolyte", "Vanadium / VRFB", 79, 79, 32),
    ("Stack materials", "Vanadium / VRFB", 50, 72, 52),
    ("VRFB stacks", "Vanadium / VRFB", 57, 82, 61),
    ("VRFB system integration", "Vanadium / VRFB", 72, 75, 55),
    ("Electrolyte leasing / recovery", "Vanadium / VRFB", 73, 77, 36),
]

CAPITAL = {
    "Power, water, rail and ports": 0.30,
    "Manganese materials hub": 0.17,
    "PGM and hydrogen components": 0.15,
    "Vanadium and VRFB chain": 0.11,
    "Shared chemicals and parks": 0.10,
    "Supplier and working capital": 0.07,
    "R&D, testing, skills and IP": 0.06,
    "Contingency and closure reserve": 0.04,
}

BOTTLENECKS = {
    "Reliable, competitively priced power": 95,
    "Bankable long-term offtake": 92,
    "Project governance and commissioning": 90,
    "Technology licensing and operating partner": 84,
    "Rail, port and specialised logistics": 80,
    "Water, reagents and effluent treatment": 75,
    "Process-engineering and production skills": 72,
    "Supplier finance and working capital": 64,
}


def header(fig, title, subtitle):
    add_figure_header(fig, title, subtitle, field="GREYSCIENCX / PAPER 4", tokens=TOKENS)


def finish(fig, filename, *, left=0.10, right=0.97, top=0.77, bottom=0.14):
    fig.subplots_adjust(left=left, right=right, top=top, bottom=bottom)
    save_figure(fig, ASSETS / filename, dpi=270)
    plt.close(fig)


def capture(chain, scenario):
    return float(np.dot(VALUE_WEIGHTS, np.array(LOCAL_SHARE[scenario][chain]) / 100))


def portfolio_capture(scenario):
    return float(sum(CHAIN_WEIGHTS[c] * capture(c, scenario) for c in CHAIN_WEIGHTS))


def make_endowment_gap():
    minerals = ["Platinum", "Manganese", "Vanadium"]
    reserve = np.array([88, 80, 32])
    production = np.array([70, 40, 7])
    y = np.arange(len(minerals))
    fig, ax = plt.subplots(figsize=(9.5, 5.5))
    header(fig, "A mineral endowment is a head start, not an industrial complex", "South African shares cited by official sources; reserve estimates and 2024 mined production are different measures")
    ax.barh(y + 0.18, reserve, height=0.34, color=CORAL, label="Reserve-share estimate cited in 2025 strategy")
    ax.barh(y - 0.18, production, height=0.34, color=BLACK, label="Share of 2024 world mined production")
    for i, (r, p) in enumerate(zip(reserve, production)):
        ax.text(r + 1.5, i + 0.18, f"{r}%", va="center", fontsize=8, fontweight="bold")
        ax.text(p + 1.5, i - 0.18, f"{p}%", va="center", fontsize=8, fontweight="bold")
    ax.set_yticks(y, minerals)
    ax.set_xlim(0, 100)
    ax.set_xlabel("Share of reported world total (%)")
    ax.legend(frameon=False, fontsize=7.2, loc="lower right")
    style_axis(ax, TOKENS, grid_axis="x")
    finish(fig, "endowment-gap.png", left=0.16)


def draw_node(ax, x, y, w, h, text, face, edge=BLACK, txt=BLACK, lw=0.8):
    rect = Rectangle((x, y), w, h, facecolor=face, edgecolor=edge, linewidth=lw)
    ax.add_patch(rect)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=6.8, color=txt, fontweight="bold")


def make_system_map():
    fig, ax = plt.subplots(figsize=(10.3, 6.1))
    header(fig, "Three mineral chains can share one industrial spine", "Coral stages are the strongest near-term localisation targets; grey stages need partnership, scale or imported technology")
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7.3)
    ax.axis("off")
    rows = {
        "MANGANESE": (5.5, ["Ore", "Purified\nMn", "HPMSM", "pCAM / CAM", "Cells", "Packs / BMS"]),
        "PGM / H2": (3.4, ["Mine", "Refine", "Catalyst\ninks", "MEA", "Stacks", "Systems"]),
        "VANADIUM": (1.3, ["Mine", "V2O5", "Electrolyte", "Stack\nmaterials", "VRFB stack", "Grid system"]),
    }
    target_indices = {"MANGANESE": {0, 1, 2, 5}, "PGM / H2": {0, 1, 2, 3}, "VANADIUM": {1, 2, 5}}
    for label, (y, nodes) in rows.items():
        ax.text(0.05, y + 0.42, label, ha="left", va="center", fontsize=8.5, fontweight="bold")
        for i, node in enumerate(nodes):
            x = 1.45 + i * 1.72
            face = CORAL if i in target_indices[label] else G100
            txt = WHITE if face == CORAL else BLACK
            draw_node(ax, x, y, 1.28, 0.82, node, face, txt=txt)
            if i < len(nodes) - 1:
                ax.add_patch(FancyArrowPatch((x + 1.29, y + 0.41), (x + 1.68, y + 0.41), arrowstyle="->", mutation_scale=8, linewidth=0.8, color=G700))
    ax.add_patch(Rectangle((1.45, 0.03), 9.88, 0.62, facecolor=BLACK, edgecolor=BLACK))
    ax.text(6.39, 0.34, "SHARED INDUSTRIAL COMMONS: POWER | WATER | ACIDS & GASES | ENGINEERING | TESTING | RAIL & PORTS | RECYCLING", ha="center", va="center", color=WHITE, fontsize=7.1, fontweight="bold")
    for x in [2.1, 5.54, 8.98]:
        ax.add_patch(FancyArrowPatch((x, 0.66), (x, 1.2), arrowstyle="->", mutation_scale=8, linewidth=0.8, color=CORAL))
    finish(fig, "integrated-system-map.png", left=0.04, right=0.98, bottom=0.07, top=0.77)


def make_readiness_heatmap():
    labels = [i[0] for i in ITEMS]
    readiness = np.array([i[2] for i in ITEMS])
    upside = np.array([i[3] for i in ITEMS])
    matrix = np.column_stack([readiness, upside])
    fig, ax = plt.subplots(figsize=(9.2, 8.3))
    header(fig, "The best targets sit between the mine and the finished system", "Armchair scores out of 100: readiness measures local feasibility; upside measures strategic value if capability is built")
    cmap = plt.matplotlib.colors.LinearSegmentedColormap.from_list("grey_coral", [G700, G100, CORAL])
    im = ax.imshow(matrix, aspect="auto", cmap=cmap, vmin=20, vmax=95)
    ax.set_xticks([0, 1], ["Local readiness", "Strategic upside"])
    ax.set_yticks(np.arange(len(labels)), labels)
    for r in range(matrix.shape[0]):
        for c in range(matrix.shape[1]):
            val = int(matrix[r, c])
            colour = WHITE if val >= 74 or val <= 35 else BLACK
            ax.text(c, r, str(val), ha="center", va="center", fontsize=7.2, fontweight="bold", color=colour)
    for boundary in [5.5, 11.5]:
        ax.axhline(boundary, color=WHITE, linewidth=3)
    ax.tick_params(axis="y", labelsize=7.0)
    ax.tick_params(axis="x", labelsize=8)
    cbar = fig.colorbar(im, ax=ax, fraction=0.028, pad=0.025)
    cbar.set_label("Score", fontsize=7.5)
    finish(fig, "readiness-heatmap.png", left=0.30, right=0.93, top=0.82, bottom=0.12)


def make_priority_frontier():
    fig, ax = plt.subplots(figsize=(9.6, 6.1))
    header(fig, "Build what is ready; partner where the prize is high", "Bubble size indicates relative capital intensity; scores are transparent scenario judgements, not forecasts")
    chain_style = {
        "Manganese": (CORAL, "o"),
        "PGM / hydrogen": (BLACK, "s"),
        "Vanadium / VRFB": (G500, "D"),
    }
    selected = [2, 3, 4, 7, 8, 9, 13, 15, 16]
    offsets = {
        "High-purity Mn sulphate": (1.1, 1.0, "left"),
        "Precursor / cathode material": (1.1, -2.0, "left"),
        "Battery cells": (1.1, 1.0, "left"),
        "Catalyst powder and inks": (1.1, -2.0, "left"),
        "Membrane-electrode assemblies": (1.1, 1.0, "left"),
        "Electrolyser / fuel-cell stacks": (-1.1, -2.2, "right"),
        "VRFB electrolyte": (1.1, -2.1, "left"),
        "VRFB stacks": (1.1, -3.1, "left"),
        "VRFB system integration": (1.1, -1.0, "left"),
    }
    for idx in selected:
        name, chain, ready, upside, capital = ITEMS[idx]
        colour, marker = chain_style[chain]
        ax.scatter(ready, upside, s=35 + capital * 3.0, color=colour, marker=marker, alpha=0.86, edgecolor=WHITE, linewidth=0.8, zorder=3)
        dx, dy, align = offsets[name]
        ax.text(ready + dx, upside + dy, name.replace(" and ", " & "), fontsize=6.2, color=BLACK, ha=align)
    ax.axvline(65, color=G300, linewidth=1)
    ax.axhline(75, color=G300, linewidth=1)
    ax.text(83, 94, "BUILD / SCALE", ha="center", fontsize=8, fontweight="bold", color=CORAL)
    ax.text(48, 94, "PARTNER / LICENSE", ha="center", fontsize=8, fontweight="bold", color=BLACK)
    ax.text(83, 61, "SELECTIVE LOCALISATION", ha="center", fontsize=7.5, fontweight="bold", color=G700)
    ax.text(48, 61, "PILOT / MONITOR", ha="center", fontsize=7.5, fontweight="bold", color=G700)
    ax.set_xlim(25, 100)
    ax.set_ylim(55, 98)
    ax.set_xlabel("Local readiness score")
    ax.set_ylabel("Strategic upside score")
    legend = [Line2D([0], [0], marker=m, color="none", markerfacecolor=c, label=k, markersize=6) for k, (c, m) in chain_style.items()]
    ax.legend(handles=legend, frameon=False, fontsize=7, loc="lower right")
    style_axis(ax, TOKENS, grid_axis="both")
    finish(fig, "priority-frontier.png", left=0.10, right=0.98, top=0.78, bottom=0.12)


def make_capture_ladder():
    scenarios = list(LOCAL_SHARE)
    chains = list(CHAIN_WEIGHTS)
    x = np.arange(len(chains))
    width = 0.23
    colours = [G500, BLACK, CORAL]
    hatches = ["..", "//", ""]
    fig, ax = plt.subplots(figsize=(9.5, 5.7))
    header(fig, "A focused strategy could localise two-thirds of the modelled value", "Illustrative share of value added retained locally; stage weights are held constant across three capability scenarios")
    for i, scenario in enumerate(scenarios):
        vals = [capture(c, scenario) * 100 for c in chains]
        bars = ax.bar(x + (i - 1) * width, vals, width=width, color=colours[i], hatch=hatches[i], label=scenario)
        for b, v in zip(bars, vals):
            ax.text(b.get_x() + b.get_width() / 2, v + 1.2, f"{v:.0f}%", ha="center", fontsize=7, fontweight="bold")
    ax.set_xticks(x, chains)
    ax.set_ylim(0, 100)
    ax.set_ylabel("Local share of modelled value added (%)")
    ax.legend(frameon=False, fontsize=7.2, ncol=3, loc="upper left")
    style_axis(ax, TOKENS, grid_axis="y")
    finish(fig, "capture-ladder.png")


def make_stage_capture():
    scenario = "Focused integration"
    weighted = np.zeros(len(STAGES))
    for chain, weight in CHAIN_WEIGHTS.items():
        weighted += weight * np.array(LOCAL_SHARE[scenario][chain])
    retained = VALUE_WEIGHTS * weighted
    uncaptured = VALUE_WEIGHTS * (100 - weighted)
    x = np.arange(len(STAGES))
    fig, ax = plt.subplots(figsize=(9.6, 5.7))
    header(fig, "The deepest leakage remains in components and advanced manufacturing", "Focused-integration scenario; each bar is that stage's share of the total value pool")
    ax.bar(x, retained, color=CORAL, label="Retained locally")
    ax.bar(x, uncaptured, bottom=retained, color=G300, label="Imported or captured abroad")
    for i, (r, u) in enumerate(zip(retained, uncaptured)):
        ax.text(i, r / 2, f"{r:.1f}", ha="center", va="center", fontsize=7, fontweight="bold", color=WHITE if r > 7 else BLACK)
    ax.set_xticks(x, STAGES)
    ax.set_ylabel("Share of total chain value pool (percentage points)")
    ax.legend(frameon=False, fontsize=7.2, loc="upper right")
    style_axis(ax, TOKENS, grid_axis="y")
    finish(fig, "stage-capture.png", bottom=0.17)


def make_capital_portfolio():
    labels = list(CAPITAL)
    values = np.array([CAPITAL[k] * FUND for k in labels])
    y = np.arange(len(labels))[::-1]
    fig, ax = plt.subplots(figsize=(9.6, 4.7))
    header(fig, "The inherited R253.5 billion cannot be spent only on factories", "Illustrative portfolio in constant 2026 rand; 40% is reserved for shared infrastructure, industrial commons and closure risk")
    colours = [CORAL if i < 4 else BLACK if i < 6 else G500 for i in range(len(labels))]
    ax.barh(y, values, color=colours)
    for yy, val in zip(y, values):
        ax.text(val + 1.2, yy, f"R{val:.1f}bn", va="center", fontsize=7.5, fontweight="bold")
    ax.set_yticks(y, labels)
    ax.set_xlim(0, 86)
    ax.set_xlabel("Capital allocation, R billion (2026 rand)")
    style_axis(ax, TOKENS, grid_axis="x")
    finish(fig, "capital-portfolio.png", left=0.31, right=0.95)


def make_bottleneck_bar():
    labels = list(BOTTLENECKS)
    values = np.array(list(BOTTLENECKS.values()))
    y = np.arange(len(labels))[::-1]
    fig, ax = plt.subplots(figsize=(9.6, 5.8))
    header(fig, "The binding constraints are institutional before they are geological", "Indicative criticality score: how strongly failure of one condition can strand otherwise viable downstream investment")
    bars = ax.barh(y, values, color=[CORAL if v >= 90 else BLACK if v >= 80 else G500 for v in values])
    for bar, val in zip(bars, values):
        ax.text(val + 1, bar.get_y() + bar.get_height() / 2, str(val), va="center", fontsize=7.5, fontweight="bold")
    ax.set_yticks(y, labels)
    ax.set_xlim(0, 103)
    ax.set_xlabel("Constraint criticality score (0-100)")
    style_axis(ax, TOKENS, grid_axis="x")
    finish(fig, "bottlenecks.png", left=0.34, right=0.95)


def make_policy_choice():
    labels = ["Current footprint", "Focused integration", "Frontier partnership", "Forced autarky"]
    nominal = [portfolio_capture("Current footprint") * 100, portfolio_capture("Focused integration") * 100, portfolio_capture("Frontier partnership") * 100, 78]
    viable = [nominal[0] * 0.88, nominal[1] * 0.93, nominal[2] * 0.90, nominal[3] * 0.67]
    x = np.arange(len(labels))
    fig, ax = plt.subplots(figsize=(9.5, 5.7))
    header(fig, "Local content is not the same as viable local value", "The autarky case loses utilisation and market access; partnership retains less nominal control but more realised value")
    ax.bar(x, nominal, color=G300, label="Nominal local-content ambition")
    ax.bar(x, viable, color=[G500, BLACK, CORAL, G700], width=0.58, label="Realised local value after viability factor")
    for i, v in enumerate(viable):
        ax.text(i, v + 1.5, f"{v:.0f}%", ha="center", fontsize=8, fontweight="bold")
    ax.set_xticks(x, ["Current\nfootprint", "Focused\nintegration", "Frontier\npartnership", "Forced\nautarky"])
    ax.set_ylim(0, 100)
    ax.set_ylabel("Share of modelled value pool (%)")
    ax.legend(frameon=False, fontsize=7.2, loc="upper left")
    style_axis(ax, TOKENS, grid_axis="y")
    finish(fig, "policy-choice.png", bottom=0.17)


def make_sequence():
    lanes = [
        ("Utilities, corridors and offtake", 2026, 2032, CORAL),
        ("HPMSM, electrolyte and catalysts", 2027, 2033, CORAL),
        ("Packs, balance-of-plant and systems", 2028, 2036, BLACK),
        ("Cathodes, MEAs and stack materials", 2030, 2039, BLACK),
        ("Selective cells and complete stacks", 2034, 2044, G500),
        ("Recycling and second-life networks", 2030, 2045, G500),
    ]
    fig, ax = plt.subplots(figsize=(9.6, 5.7))
    header(fig, "Sequencing beats simultaneous localisation", "The plan earns the right to move downstream by first proving inputs, demand, quality and plant utilisation")
    y = np.arange(len(lanes))[::-1]
    for yy, (name, start, end, colour) in zip(y, lanes):
        ax.barh(yy, end - start, left=start, height=0.52, color=colour)
        ax.text(start + 0.25, yy, name, va="center", ha="left", fontsize=7.1, color=WHITE, fontweight="bold")
        ax.text(end + 0.18, yy, str(end), va="center", fontsize=7, color=BLACK)
    for year in [2030, 2035, 2040]:
        ax.axvline(year, color=G300, linewidth=0.8, zorder=-1)
    ax.set_yticks([])
    ax.set_xlim(2025.5, 2046.5)
    ax.set_xlabel("Illustrative capability-building window")
    style_axis(ax, TOKENS, grid_axis="x")
    finish(fig, "sequence.png", left=0.08, right=0.96)


def make_value_chain_table_figure():
    rows = [
        ("Manganese", "HPMSM", "pCAM / CAM with partner", "Cells", "Packs, BMS, recycling"),
        ("PGM / hydrogen", "Refining and catalyst inks", "MEA with licence", "Commodity electrolyser factories", "Systems, recycling, industrial use"),
        ("Vanadium / VRFB", "V2O5 and electrolyte", "Stack materials and stacks", "Membranes at small scale", "Integration, leasing, recovery"),
    ]
    fig, ax = plt.subplots(figsize=(10.2, 4.8))
    header(fig, "The practical strategy is make, partner, import and learn", "A mineral-by-mineral decision rule avoids treating every downstream stage as equally localisable")
    ax.axis("off")
    columns = ["CHAIN", "MAKE / SCALE", "PARTNER / LICENSE", "IMPORT FOR NOW", "CLOSE THE LOOP"]
    table = ax.table(cellText=rows, colLabels=columns, loc="center", cellLoc="left", colLoc="left", colWidths=[0.15, 0.22, 0.23, 0.20, 0.23])
    table.auto_set_font_size(False)
    table.set_fontsize(7.0)
    table.scale(1, 2.0)
    for (r, c), cell in table.get_celld().items():
        cell.set_linewidth(0.4)
        cell.set_edgecolor(WHITE)
        if r == 0:
            cell.set_facecolor(BLACK)
            cell.get_text().set_color(WHITE)
            cell.get_text().set_fontweight("bold")
        else:
            cell.set_facecolor(G100 if r % 2 == 0 else WHITE)
            if c == 1:
                cell.get_text().set_color(CORAL)
                cell.get_text().set_fontweight("bold")
    finish(fig, "make-partner-import.png", left=0.03, right=0.97, top=0.70, bottom=0.10)


def write_results():
    results = {
        "resource_envelope_r_bn_2026": FUND,
        "stage_value_weights": dict(zip(STAGES, [round(float(v), 2) for v in VALUE_WEIGHTS])),
        "portfolio_local_value_share": {s: round(portfolio_capture(s), 4) for s in LOCAL_SHARE},
        "chain_local_value_share": {
            s: {c: round(capture(c, s), 4) for c in CHAIN_WEIGHTS} for s in LOCAL_SHARE
        },
        "capital_allocation_r_bn": {k: round(v * FUND, 2) for k, v in CAPITAL.items()},
        "bottleneck_scores": BOTTLENECKS,
        "readiness_items": [
            {"item": n, "chain": c, "readiness": r, "strategic_upside": u, "capital_intensity": cap}
            for n, c, r, u, cap in ITEMS
        ],
        "interpretation": {
            "focused_capture_percent": round(portfolio_capture("Focused integration") * 100, 1),
            "frontier_capture_percent": round(portfolio_capture("Frontier partnership") * 100, 1),
            "current_capture_percent": round(portfolio_capture("Current footprint") * 100, 1),
            "note": "All localisation shares, stage weights, readiness scores and capital allocations are transparent scenarios, not forecasts or investment advice.",
        },
    }
    (WORK / "model_results.json").write_text(json.dumps(results, indent=2), encoding="utf-8")


def main():
    make_endowment_gap()
    make_system_map()
    make_readiness_heatmap()
    make_priority_frontier()
    make_capture_ladder()
    make_stage_capture()
    make_capital_portfolio()
    make_bottleneck_bar()
    make_policy_choice()
    make_sequence()
    make_value_chain_table_figure()
    write_results()
    print(WORK / "model_results.json")


if __name__ == "__main__":
    main()
