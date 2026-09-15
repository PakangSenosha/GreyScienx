"""Render the report's scientific figures in the GreyScienx print style."""

from pathlib import Path
import sys

import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle

WORK = Path(__file__).resolve().parent
ASSETS = WORK / "pdf" / "assets"
ASSETS.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(WORK))

from expanded_lifetime_model import SCENARIOS, simulate  # noqa: E402
from greyscienx_theme import (  # noqa: E402
    BLACK,
    CORAL,
    EARLY,
    GRID,
    GREY_100,
    GREY_300,
    GREY_500,
    GREY_700,
    LATER,
    MUTED,
    WHITE,
)


FONT_PATHS = [
    Path("C:/Windows/Fonts/segoeui.ttf"),
    Path("C:/Windows/Fonts/segoeuib.ttf"),
    Path("C:/Windows/Fonts/seguisb.ttf"),
]
for font_path in FONT_PATHS:
    if font_path.exists():
        font_manager.fontManager.addfont(str(font_path))

plt.rcParams.update(
    {
        "font.family": "Segoe UI",
        "font.size": 9.2,
        "axes.titlesize": 12.0,
        "axes.titleweight": "bold",
        "axes.labelsize": 9.0,
        "axes.edgecolor": BLACK,
        "axes.labelcolor": BLACK,
        "xtick.color": GREY_700,
        "ytick.color": GREY_700,
        "text.color": BLACK,
        "figure.facecolor": WHITE,
        "axes.facecolor": WHITE,
        "savefig.facecolor": WHITE,
    }
)


def add_brand_header(fig, title, subtitle=None):
    fig.add_artist(
        Rectangle(
            (0.0, 0.978), 1.0, 0.022, transform=fig.transFigure,
            facecolor=CORAL, edgecolor="none", clip_on=False,
        )
    )
    fig.text(0.055, 0.945, "GREYSCIENX / ECONOMICS", color=CORAL,
             fontsize=7.5, fontweight="bold", va="top")
    fig.text(0.055, 0.894, title, color=BLACK, fontsize=17.2,
             fontweight="bold", va="top")
    if subtitle:
        fig.text(0.055, 0.846, subtitle, color=MUTED, fontsize=8.4, va="top")


def finish_axis(ax):
    ax.grid(axis="y", color=GRID, linewidth=0.65, zorder=0)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_linewidth(1.05)
    ax.spines["bottom"].set_linewidth(1.05)
    ax.tick_params(length=3, width=0.8)


results = {
    scenario.name: {
        "scenario": scenario,
        "early": simulate(scenario, 25),
        "late": simulate(scenario, 35),
    }
    for scenario in SCENARIOS
}


# Figure 1: small multiples preserve the very different vertical scales.
fig, axes = plt.subplots(3, 1, figsize=(8.0, 8.6), sharex=True)
fig.subplots_adjust(left=0.13, right=0.955, bottom=0.075, top=0.745, hspace=0.43)
add_brand_header(
    fig,
    "Lifetime household net worth",
    "Moving into one home at 25 versus 35 | constant 2026 rand",
)

for ax, (name, bundle) in zip(axes, results.items()):
    for label, key, color, linestyle, marker in (
        ("Move in at 25", "early", EARLY, "-", "o"),
        ("Move in at 35", "late", LATER, (0, (5, 3)), "s"),
    ):
        ages = [row[0] for row in bundle[key]["series"]]
        values = [row[1] / 1_000_000 for row in bundle[key]["series"]]
        ax.plot(
            ages,
            values,
            color=color,
            linewidth=2.15,
            linestyle=linestyle,
            marker=marker,
            markevery=120,
            markersize=3.8,
            markerfacecolor=WHITE,
            markeredgewidth=1.1,
            zorder=3,
            label=label,
        )
    ax.axhline(0, color=GREY_500, linewidth=0.85, zorder=1)
    ax.axvline(35, color=GREY_500, linewidth=0.85, linestyle=(0, (2, 3)))
    annotation_y = 0.72 if name == "Worst case" else 0.90
    ax.text(
        35.45,
        annotation_y,
        "Later couple moves in",
        transform=ax.get_xaxis_transform(),
        color=MUTED,
        fontsize=7.5,
        ha="left",
        va="top",
    )
    purchase_age = bundle["early"]["purchase_age"]
    if purchase_age is not None:
        ax.axvline(purchase_age, color=GREY_300, linewidth=0.85, linestyle=(0, (1, 2)))
        purchase_label_y = 0.18 if name == "Best case" else 0.36
        ax.text(
            purchase_age + 0.45,
            purchase_label_y,
            f"Both buy at {purchase_age}",
            transform=ax.get_xaxis_transform(),
            color=MUTED,
            fontsize=7.3,
            va="bottom",
        )
    ax.set_title(name.upper(), loc="left", color=BLACK, pad=8, fontsize=10.2)
    ax.set_ylabel("Net worth (R millions)")
    finish_axis(ax)

axes[-1].set_xlabel("Age")
axes[-1].set_xlim(25, 75)
axes[-1].set_xticks([25, 35, 45, 55, 65, 75])
legend_handles = [
    Line2D([0], [0], color=EARLY, lw=2.15, marker="o", markerfacecolor=WHITE,
           markeredgecolor=EARLY, label="Move in at 25"),
    Line2D([0], [0], color=LATER, lw=2.15, linestyle=(0, (5, 3)), marker="s",
           markerfacecolor=WHITE, markeredgecolor=LATER, label="Move in at 35"),
]
fig.legend(
    handles=legend_handles,
    frameon=False,
    ncol=2,
    loc="upper left",
    bbox_to_anchor=(0.05, 0.805),
    handlelength=3.0,
    columnspacing=2.2,
)
fig.savefig(ASSETS / "figure-1-lifetime-trajectories.png", dpi=240)
plt.close(fig)


# Figure 2: the value of the timing head start.
fig, ax = plt.subplots(figsize=(8.0, 4.8))
fig.subplots_adjust(left=0.13, right=0.945, bottom=0.17, top=0.72)
add_brand_header(
    fig,
    "The ten-year head start persists",
    "Early couple's financial lead through age 75 | constant 2026 rand",
)

scenario_styles = (
    (CORAL, "-", "o"),
    (BLACK, (0, (5, 3)), "s"),
    (GREY_500, (0, (1, 2)), "D"),
)
for (name, bundle), (color, linestyle, marker) in zip(results.items(), scenario_styles):
    ages = [row[0] for row in bundle["early"]["series"]]
    gaps = [
        (early[1] - late[1]) / 1_000_000
        for early, late in zip(bundle["early"]["series"], bundle["late"]["series"])
    ]
    ax.plot(
        ages,
        gaps,
        color=color,
        linewidth=2.25,
        linestyle=linestyle,
        marker=marker,
        markevery=120,
        markersize=4.0,
        markerfacecolor=WHITE,
        markeredgewidth=1.1,
        label=name,
        zorder=3,
    )
    ax.scatter([75], [gaps[-1]], color=color, s=30, zorder=4, marker=marker)
    ax.annotate(
        f"R{gaps[-1]:.1f}m",
        (75, gaps[-1]),
        xytext=(-8, 6),
        textcoords="offset points",
        ha="right",
        va="bottom",
        color=BLACK,
        fontsize=7.8,
        fontweight="bold",
    )

ax.axvline(35, color=GREY_500, linewidth=0.85, linestyle=(0, (2, 3)))
ax.text(
    35.5,
    0.94,
    "Both couples share a home from here",
    transform=ax.get_xaxis_transform(),
    color=MUTED,
    fontsize=7.5,
    ha="left",
    va="top",
)
ax.set_xlabel("Age")
ax.set_ylabel("Early couple's lead (R millions)")
ax.set_xlim(25, 77)
ax.set_xticks([25, 35, 45, 55, 65, 75])
finish_axis(ax)
ax.legend(frameon=False, ncol=3, loc="upper left", bbox_to_anchor=(0.0, 1.17),
          handlelength=2.8, columnspacing=1.8)
fig.savefig(ASSETS / "figure-2-ten-year-head-start.png", dpi=240)
plt.close(fig)


# Figure 3: cumulative costs and foregone income included in the expanded model.
categories = [
    ("Children", "child_cost"),
    ("Family support", "remittance"),
    ("Job/disability\nincome lost", "income_lost"),
    ("Care-related\nincome lost", "care_income_lost"),
    ("Fees and tax drag", "investment_drag"),
]

fig, axes = plt.subplots(1, 3, figsize=(8.0, 4.9), sharex=True, sharey=True)
fig.subplots_adjust(left=0.20, right=0.96, bottom=0.16, top=0.70, wspace=0.16)
add_brand_header(
    fig,
    "Lifetime pressures inside the model",
    "Cumulative values for the Early couple | R millions, constant 2026 rand",
)

for index, (ax, (name, bundle)) in enumerate(zip(axes, results.items())):
    values = [bundle["early"][key] / 1_000_000 for _, key in categories]
    labels = [label for label, _ in categories]
    y_positions = list(range(len(labels)))
    bars = ax.barh(y_positions, values, color=CORAL if index == 0 else BLACK,
                   alpha=1.0 if index < 2 else 0.55, height=0.58, zorder=3)
    ax.set_title(name.upper(), loc="left", fontsize=8.6, pad=10)
    ax.set_xlabel("R millions", fontsize=8.0)
    ax.set_yticks(y_positions, labels)
    ax.invert_yaxis()
    ax.grid(axis="x", color=GRID, linewidth=0.65, zorder=0)
    ax.grid(axis="y", visible=False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_linewidth(1.0)
    ax.tick_params(axis="y", length=0, labelsize=7.4)
    ax.tick_params(axis="x", labelsize=7.4)
    for bar, value in zip(bars, values):
        if value >= 0.02:
            label = "<R0.1m" if value < 0.1 else f"R{value:.1f}m"
            ax.text(
                value + 0.06,
                bar.get_y() + bar.get_height() / 2,
                label,
                va="center",
                ha="left",
                fontsize=7.0,
                color=BLACK,
            )
    ax.set_xlim(0, 4.75)

fig.text(
    0.20,
    0.055,
    "Fees and tax drag is an opportunity cost; other bars are cash costs or income not received.",
    color=MUTED,
    fontsize=7.4,
    ha="left",
)
fig.savefig(ASSETS / "figure-3-lifetime-pressures.png", dpi=240)
plt.close(fig)

print("Rendered GreyScienx figures:")
for output in sorted(ASSETS.glob("figure-*.png")):
    print(output)
