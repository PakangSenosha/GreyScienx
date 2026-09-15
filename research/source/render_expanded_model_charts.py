from pathlib import Path
import sys

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

sys.path.insert(0, str(Path(__file__).parent))
from expanded_lifetime_model import SCENARIOS, simulate


OUTPUTS = Path(__file__).parents[1] / "outputs"
EARLY = "#0072B2"
LATE = "#D55E00"
SCENARIO_COLORS = ["#009E73", "#0072B2", "#CC79A7"]
GRID = "#D8DEE6"
TEXT = "#1F2937"


def millions(x, _):
    if abs(x) < 1e-9:
        return "R0"
    return f"R{x:,.0f}m"


results = {}
for scenario in SCENARIOS:
    results[scenario.name] = {
        "scenario": scenario,
        "early": simulate(scenario, 25),
        "late": simulate(scenario, 35),
    }


plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 10,
    "axes.titlesize": 13,
    "axes.labelsize": 10,
    "axes.edgecolor": "#9CA3AF",
    "axes.labelcolor": TEXT,
    "xtick.color": TEXT,
    "ytick.color": TEXT,
    "text.color": TEXT,
})


# Figure 1: one trajectory panel per scenario.
fig, axes = plt.subplots(3, 1, figsize=(11, 12), sharex=True)
fig.patch.set_facecolor("white")
fig.suptitle("Lifetime household net worth: moving in at 25 versus 35", fontsize=17, fontweight="bold", y=0.99)

for ax, (name, bundle) in zip(axes, results.items()):
    ax.set_facecolor("white")
    for label, key, color in (("Move in at 25", "early", EARLY), ("Move in at 35", "late", LATE)):
        ages = [row[0] for row in bundle[key]["series"]]
        values = [row[1] / 1_000_000 for row in bundle[key]["series"]]
        ax.plot(ages, values, color=color, linewidth=2.4, label=label)
    ax.axhline(0, color="#6B7280", linewidth=1)
    ax.axvline(35, color="#6B7280", linewidth=1, linestyle="--")
    ax.text(35.3, 0.88, "Later couple consolidates", transform=ax.get_xaxis_transform(),
            va="top", ha="left", fontsize=9, color="#4B5563")
    purchase_early = bundle["early"]["purchase_age"]
    if purchase_early is not None:
        ax.axvline(purchase_early, color="#9CA3AF", linewidth=0.9, linestyle=":")
        ax.text(purchase_early + 0.3, 0.08, f"Both buy at {purchase_early}",
                transform=ax.get_xaxis_transform(), va="bottom", fontsize=9, color="#4B5563")
    ax.set_title(name, loc="left", fontweight="bold")
    ax.set_ylabel("Net worth (R millions, 2026 purchasing power)")
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    ax.spines[["top", "right"]].set_visible(False)

axes[-1].set_xlabel("Age")
axes[-1].set_xlim(25, 75)
axes[-1].set_xticks([25, 35, 45, 55, 65, 75])
handles, labels = axes[0].get_legend_handles_labels()
fig.legend(handles, labels, frameon=False, ncol=2, loc="upper center", bbox_to_anchor=(0.5, 0.967))
fig.tight_layout(rect=[0, 0, 1, 0.95])
fig.savefig(OUTPUTS / "lifetime-wealth-trajectories-v0.5.png", dpi=180, facecolor="white")
plt.close(fig)


# Figure 2: the value of the ten-year head start.
fig, ax = plt.subplots(figsize=(11, 6.3), constrained_layout=True)
fig.patch.set_facecolor("white")
ax.set_facecolor("white")
for color, (name, bundle) in zip(SCENARIO_COLORS, results.items()):
    ages = [row[0] for row in bundle["early"]["series"]]
    gaps = [(e[1] - l[1]) / 1_000_000 for e, l in zip(bundle["early"]["series"], bundle["late"]["series"])]
    ax.plot(ages, gaps, color=color, linewidth=2.5, label=name)
    ax.scatter([75], [gaps[-1]], color=color, s=38, zorder=3)
    ax.annotate(f"R{gaps[-1]:.1f}m", (75, gaps[-1]), xytext=(-8, 7),
                textcoords="offset points", ha="right", color=TEXT, fontsize=9)

ax.axvline(35, color="#6B7280", linewidth=1, linestyle="--")
ax.text(35.4, 0.95, "Both couples share a home from here", transform=ax.get_xaxis_transform(),
        va="top", ha="left", fontsize=9, color="#4B5563")
ax.set_title("The Early couple's financial lead keeps changing after age 35", loc="left", fontsize=16, fontweight="bold")
ax.set_xlabel("Age")
ax.set_ylabel("Early couple's lead (R millions, 2026 purchasing power)")
ax.set_xlim(25, 76)
ax.set_xticks([25, 35, 45, 55, 65, 75])
ax.grid(axis="y", color=GRID, linewidth=0.8)
ax.spines[["top", "right"]].set_visible(False)
ax.legend(frameon=False, ncol=3, loc="upper left")
fig.savefig(OUTPUTS / "ten-year-head-start-v0.5.png", dpi=180, facecolor="white")
plt.close(fig)


# Figure 3: cumulative assumptions now included in each lifetime.
categories = [
    ("Children", "child_cost"),
    ("Family support", "remittance"),
    ("Job/disability income lost", "income_lost"),
    ("Care-related income lost", "care_income_lost"),
    ("Fees and tax drag", "investment_drag"),
]

fig, axes = plt.subplots(1, 3, figsize=(14, 6.2), sharey=True)
fig.patch.set_facecolor("white")
fig.suptitle("Lifetime pressures included in the expanded model", fontsize=17, fontweight="bold")

for ax, color, (name, bundle) in zip(axes, SCENARIO_COLORS, results.items()):
    values = [bundle["early"][key] / 1_000_000 for _, key in categories]
    labels = [label for label, _ in categories]
    bars = ax.barh(labels, values, color=color, alpha=0.88)
    ax.set_title(name, fontweight="bold")
    ax.set_xlabel("Cumulative R millions")
    ax.grid(axis="x", color=GRID, linewidth=0.8)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.tick_params(axis="y", length=0)
    for bar, value in zip(bars, values):
        if value > 0.02:
            value_label = "<R0.1m" if value < 0.1 else f"R{value:.1f}m"
            ax.text(value + 0.05, bar.get_y() + bar.get_height() / 2,
                    value_label, va="center", fontsize=9)
    ax.set_xlim(0, max(4.6, max(values) + 0.7))

fig.text(0.5, 0.01,
         "Fees and tax drag is an opportunity cost relative to the gross investment return; other bars are cash costs or lost income.",
         ha="center", fontsize=9, color="#4B5563")
fig.tight_layout(rect=[0, 0.075, 1, 0.93])
fig.savefig(OUTPUTS / "expanded-model-lifetime-pressures-v0.5.png", dpi=180, facecolor="white")
plt.close(fig)

print("Rendered:")
for name in (
    "lifetime-wealth-trajectories-v0.5.png",
    "ten-year-head-start-v0.5.png",
    "expanded-model-lifetime-pressures-v0.5.png",
):
    print(OUTPUTS / name)
