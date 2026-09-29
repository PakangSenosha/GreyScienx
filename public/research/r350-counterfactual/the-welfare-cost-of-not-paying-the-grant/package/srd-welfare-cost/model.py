from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap, Normalize
from matplotlib.patches import FancyArrowPatch, Rectangle


ROOT = Path(__file__).resolve().parents[2]
WORK = Path(__file__).resolve().parent
ASSETS = WORK / "assets"
ASSETS.mkdir(parents=True, exist_ok=True)

STYLE_DIR = Path(r"C:\Users\Deriv\Desktop\GreyScienx\skills\greyscienx-editorial-pdf\scripts")
sys.path.insert(0, str(STYLE_DIR))
from greyscienx_style import (  # noqa: E402
    add_figure_header,
    configure_matplotlib,
    save_figure,
    style_axis,
)


TOKENS = configure_matplotlib(Path(r"C:\Users\Deriv\Desktop\GreyScienx\app\globals.css"))

CORAL = TOKENS["coral"]
BLACK = TOKENS["black"]
WHITE = TOKENS["white"]
G100 = TOKENS["grey-100"]
G300 = TOKENS["grey-300"]
G500 = TOKENS["grey-500"]
G700 = TOKENS["grey-700"]


FISCAL_YEARS = ["2020/21", "2021/22", "2022/23", "2023/24", "2024/25", "2025/26", "2026/27"]
REAL_ENVELOPE_BY_YEAR = np.array([26.04390814, 40.78286871, 35.84598481, 37.59619016, 37.64226332, 38.73464578, 36.8893])
TOTAL_REAL = float(REAL_ENVELOPE_BY_YEAR.sum())

SCENARIOS = {
    "Conservative": {
        "consumption_share": 0.80,
        "local_multiplier": 1.10,
        "equity_weight": 1.10,
        "replacement_credit_share": 0.10,
        "real_credit_cost": 0.15,
        "credit_years": 2,
        "scarring_share": 0.02,
        "labour_income_loss": 0.9,
        "colour": G500,
        "linestyle": ":",
        "marker": "D",
    },
    "Central": {
        "consumption_share": 0.93,
        "local_multiplier": 1.25,
        "equity_weight": 1.50,
        "replacement_credit_share": 0.20,
        "real_credit_cost": 0.25,
        "credit_years": 3,
        "scarring_share": 0.08,
        "labour_income_loss": 4.6,
        "colour": BLACK,
        "linestyle": "--",
        "marker": "s",
    },
    "Severe": {
        "consumption_share": 0.99,
        "local_multiplier": 1.45,
        "equity_weight": 2.00,
        "replacement_credit_share": 0.30,
        "real_credit_cost": 0.35,
        "credit_years": 4,
        "scarring_share": 0.20,
        "labour_income_loss": 13.5,
        "colour": CORAL,
        "linestyle": "-",
        "marker": "o",
    },
}

POVERTY_PATHS = {
    "Conservative": np.array([0.70, 0.70, 0.30, 0.25, 0.20, 0.18, 0.15]),
    "Central": np.array([1.35, 1.35, 0.90, 0.80, 0.70, 0.65, 0.60]),
    "Severe": np.array([2.00, 2.00, 1.60, 1.50, 1.40, 1.30, 1.20]),
}

INDUSTRIAL_PV = {"Best": 693.7, "Average": 233.3, "Worst": 42.2}
INDUSTRIAL_ASSET_2050 = {"Best": 788.8, "Average": 303.7, "Worst": 72.0}
CAPITAL_PER_JOB_M = {"Best": 1.0, "Average": 1.5, "Worst": 3.0}
FORMER_RECIPIENT_CAPTURE = {"Best": 0.25, "Average": 0.15, "Worst": 0.05}
RECIPIENT_BENCHMARK_M = 8.0


def compute_scenarios():
    out = {}
    for name, s in SCENARIOS.items():
        direct = TOTAL_REAL * s["consumption_share"]
        activity = direct * s["local_multiplier"]
        weighted = direct * s["equity_weight"]
        principal = TOTAL_REAL * s["replacement_credit_share"]
        credit = principal * ((1 + s["real_credit_cost"]) ** s["credit_years"] - 1)
        scar = TOTAL_REAL * s["scarring_share"]
        labour = s["labour_income_loss"]
        welfare = weighted + credit + scar + labour
        out[name] = {
            "direct_consumption_loss": direct,
            "gross_local_activity_loss": activity,
            "distribution_weighted_consumption": weighted,
            "replacement_credit_burden": credit,
            "human_capital_scarring": scar,
            "labour_income_loss": labour,
            "welfare_equivalent_cost": welfare,
            "cost_per_rand_withheld": welfare / TOTAL_REAL,
            "additional_poor_person_years_m": float(POVERTY_PATHS[name].sum()),
        }
    return out


RESULTS = compute_scenarios()


def header(fig, title, subtitle):
    add_figure_header(fig, title, subtitle, field="GREYSCIENCX / PAPER 2", tokens=TOKENS)


def finish(fig, filename, *, left=0.09, right=0.97, top=0.77, bottom=0.13):
    fig.subplots_adjust(left=left, right=right, top=top, bottom=bottom)
    save_figure(fig, ASSETS / filename, dpi=260)
    plt.close(fig)


def make_grant_adequacy():
    labels = ["Original SRD\nR350", "Current SRD\nR370", "Food poverty\nline", "Lower-bound\npoverty line", "Upper-bound\npoverty line"]
    values = np.array([350, 370, 868, 1457, 2962])
    colours = [CORAL, BLACK, G300, G500, G700]
    fig, ax = plt.subplots(figsize=(9.5, 5.6))
    header(fig, "The grant was small, but not trivial at the margin", "Monthly amounts compared with Statistics South Africa's May 2026 poverty lines")
    bars = ax.bar(np.arange(len(values)), values, color=colours, width=0.62)
    for i, (bar, val) in enumerate(zip(bars, values)):
        ax.text(bar.get_x() + bar.get_width() / 2, val + 70, f"R{val:,}", ha="center", fontsize=8, fontweight="bold")
    ax.text(0.5, 615, "R370 = 43% of the\nfood poverty line", ha="center", fontsize=8, color=CORAL, fontweight="bold")
    ax.set_xticks(np.arange(len(values)), labels)
    ax.set_ylabel("Rand per person per month")
    ax.set_ylim(0, 3300)
    style_axis(ax, TOKENS, grid_axis="y")
    finish(fig, "grant-adequacy.png")


def make_household_diffusion():
    fig, ax = plt.subplots(figsize=(9.6, 5.6))
    header(fig, "The recipient is an individual; the grant behaves like household income", "Rapid-assessment responses show extensive pooling and concentration in larger households")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis("off")
    boxes = [
        (0.4, 2.1, 2.1, 1.3, CORAL, "R350 reaches\none recipient", WHITE),
        (3.4, 3.55, 2.6, 1.15, BLACK, "53.1% usually pool\nwith household income", WHITE),
        (3.4, 2.15, 2.6, 1.15, G300, "35.0% sometimes\npool the grant", BLACK),
        (3.4, 0.75, 2.6, 1.15, G100, "11.9% report\nnever pooling", BLACK),
        (7.0, 2.1, 2.5, 1.3, G700, "70% live in households\nwith 4+ people", WHITE),
    ]
    for x, y, w, h, colour, text_value, text_colour in boxes:
        ax.add_patch(Rectangle((x, y), w, h, facecolor=colour, edgecolor=BLACK, linewidth=0.9))
        ax.text(x + w / 2, y + h / 2, text_value, ha="center", va="center", fontsize=8, color=text_colour, fontweight="bold")
    for y in [4.12, 2.72, 1.32]:
        ax.add_patch(FancyArrowPatch((2.55, 2.75), (3.25, y), arrowstyle="-|>", mutation_scale=12, linewidth=1.0, color=BLACK))
    for y in [4.12, 2.72, 1.32]:
        ax.add_patch(FancyArrowPatch((6.05, y), (6.9, 2.75), arrowstyle="-|>", mutation_scale=12, linewidth=1.0, color=G500))
    ax.text(5.0, 0.25, "Withholding one payment removes spending power from a shared household budget, not only from one adult.",
            ha="center", fontsize=7.5, color=G700)
    finish(fig, "household-diffusion.png")


def make_consumption_activity():
    names = list(SCENARIOS)
    direct = [RESULTS[n]["direct_consumption_loss"] for n in names]
    activity = [RESULTS[n]["gross_local_activity_loss"] for n in names]
    x = np.arange(3)
    fig, ax = plt.subplots(figsize=(9.5, 5.6))
    header(fig, "Without the grant, R203bn-R251bn of household spending disappears", "Gross local activity includes a deliberately modest scenario multiplier; it is not added again to welfare cost")
    w = 0.34
    b1 = ax.bar(x - w / 2, direct, width=w, color=BLACK, label="Direct household consumption")
    b2 = ax.bar(x + w / 2, activity, width=w, color=CORAL, label="Gross local activity")
    for bars in [b1, b2]:
        for bar in bars:
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 7, f"R{bar.get_height():.0f}bn", ha="center", fontsize=7.4, fontweight="bold")
    ax.set_xticks(x, names)
    ax.set_ylabel("R billion, constant 2026 rand")
    ax.set_ylim(0, 400)
    ax.legend(frameon=False, ncol=2, fontsize=7.3, loc="upper left")
    style_axis(ax, TOKENS, grid_axis="y")
    finish(fig, "consumption-and-local-activity.png")


def make_cumulative_central_cost():
    central_total = RESULTS["Central"]["welfare_equivalent_cost"]
    annual = REAL_ENVELOPE_BY_YEAR / TOTAL_REAL * central_total
    cumulative = np.cumsum(annual)
    fig, ax = plt.subplots(figsize=(9.5, 5.6))
    header(fig, "The social bill is incurred before most industrial returns arrive", "Central scenario welfare-equivalent cost allocated across the seven-year grant envelope")
    ax.fill_between(np.arange(7), cumulative, color=CORAL, alpha=0.22)
    ax.plot(np.arange(7), cumulative, color=CORAL, linewidth=2.3, marker="o", markersize=4)
    for i, val in enumerate(cumulative):
        ax.text(i, val + 13, f"R{val:.0f}bn", ha="center", fontsize=7.2, color=CORAL, fontweight="bold")
    ax.set_xticks(np.arange(7), FISCAL_YEARS, rotation=28, ha="right")
    ax.set_ylabel("Cumulative welfare-equivalent cost, R billion")
    ax.set_ylim(0, 485)
    style_axis(ax, TOKENS, grid_axis="y")
    finish(fig, "central-cost-timeline.png")


def make_welfare_ledger():
    names = list(SCENARIOS)
    components = [
        ("Distribution-weighted consumption", [RESULTS[n]["distribution_weighted_consumption"] for n in names], BLACK),
        ("Replacement-credit burden", [RESULTS[n]["replacement_credit_burden"] for n in names], G500),
        ("Health and human-capital scarring", [RESULTS[n]["human_capital_scarring"] for n in names], G300),
        ("Labour-income enablement", [RESULTS[n]["labour_income_loss"] for n in names], CORAL),
    ]
    x = np.arange(3)
    bottom = np.zeros(3)
    fig, ax = plt.subplots(figsize=(9.5, 5.6))
    header(fig, "The explicit welfare cost is R237bn-R743bn", "Scenario valuation in constant 2026 consumption-equivalent rand; not a fiscal expenditure estimate")
    for label, vals, colour in components:
        vals = np.array(vals)
        ax.bar(x, vals, bottom=bottom, color=colour, width=0.58, label=label)
        bottom += vals
    for i, total in enumerate(bottom):
        ax.text(i, total + 18, f"R{total:.0f}bn\n{total / TOTAL_REAL:.2f} per R1", ha="center", fontsize=8, fontweight="bold")
    ax.set_xticks(x, names)
    ax.set_ylabel("Welfare-equivalent cost, R billion")
    ax.set_ylim(0, 840)
    ax.legend(frameon=False, fontsize=6.9, ncol=2, loc="upper left")
    style_axis(ax, TOKENS, grid_axis="y")
    finish(fig, "welfare-ledger.png")


def make_poverty_paths():
    x = np.arange(7)
    fig, ax = plt.subplots(figsize=(9.5, 5.6))
    header(fig, "The strongest evidence is early; later poverty paths are scenarios", "Additional people below the poverty line without SRD, averaged by fiscal year")
    for name, vals in POVERTY_PATHS.items():
        s = SCENARIOS[name]
        ax.plot(x, vals, color=s["colour"], linestyle=s["linestyle"], marker=s["marker"], linewidth=2.1, markersize=4, label=name)
        ax.text(6.15, vals[-1], f"{vals.sum():.1f}m person-years", va="center", fontsize=7.2, color=s["colour"])
    ax.axvspan(-0.15, 1.15, color=G100, zorder=0)
    ax.text(0.5, 2.18, "Research-anchored\npandemic range", ha="center", fontsize=7.2, color=G700)
    ax.set_xticks(x, FISCAL_YEARS, rotation=28, ha="right")
    ax.set_ylabel("Additional people in poverty, millions")
    ax.set_ylim(0, 2.35)
    ax.set_xlim(-0.2, 7.15)
    ax.legend(frameon=False, fontsize=7.2, loc="upper right")
    style_axis(ax, TOKENS, grid_axis="y")
    finish(fig, "poverty-scenarios.png")


def make_tradeoff_matrix():
    welfare_names = list(SCENARIOS)
    industry_names = ["Worst", "Average", "Best"]
    matrix = np.array([[INDUSTRIAL_PV[i] - RESULTS[w]["welfare_equivalent_cost"] for i in industry_names] for w in welfare_names])
    fig, ax = plt.subplots(figsize=(9.5, 5.6))
    header(fig, "Only exceptional industry comfortably clears the welfare hurdle", "Industrial public value less no-grant welfare cost; 2026 present values, R billion")
    norm = Normalize(vmin=-750, vmax=750)
    cmap = LinearSegmentedColormap.from_list("grey_coral", [G700, G100, CORAL])
    ax.imshow(matrix, cmap=cmap, norm=norm, aspect="auto")
    for r in range(matrix.shape[0]):
        for c in range(matrix.shape[1]):
            val = matrix[r, c]
            colour = WHITE if abs(val) > 320 else BLACK
            ax.text(c, r, f"{val:+.0f}bn", ha="center", va="center", fontsize=9, color=colour, fontweight="bold")
    ax.set_xticks(np.arange(3), [f"{n} industry\nPV R{INDUSTRIAL_PV[n]:.0f}bn" for n in industry_names])
    ax.set_yticks(np.arange(3), [f"{n} welfare cost\nR{RESULTS[n]['welfare_equivalent_cost']:.0f}bn" for n in welfare_names])
    ax.set_xlabel("Paper 1 industrial outcome")
    ax.set_ylabel("Paper 2 no-grant hardship outcome")
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(length=0)
    finish(fig, "industrial-welfare-matrix.png", left=0.19, right=0.97)


def make_jobs_compensation():
    names = ["Best", "Average", "Worst"]
    total_jobs = np.array([INDUSTRIAL_ASSET_2050[n] * 1000 / CAPITAL_PER_JOB_M[n] for n in names])
    former_jobs = np.array([total_jobs[i] * FORMER_RECIPIENT_CAPTURE[n] for i, n in enumerate(names)])
    shares = former_jobs / (RECIPIENT_BENCHMARK_M * 1_000_000) * 100
    fig, ax = plt.subplots(figsize=(9.5, 5.6))
    header(fig, "Industrial jobs do not automatically compensate the people who lost the grant", "Illustrative 2050 job access for former recipient households; not an employment forecast")
    x = np.arange(3)
    bars = ax.bar(x, former_jobs, color=[CORAL, BLACK, G500], width=0.58)
    for i, bar in enumerate(bars):
        ax.text(i, bar.get_height() + 10000, f"{bar.get_height()/1000:.0f}k jobs\n{shares[i]:.2f}% of 8m", ha="center", fontsize=8, fontweight="bold")
    ax.set_xticks(x, ["Best\nR1.0m per lasting job\n25% captured", "Average\nR1.5m per lasting job\n15% captured", "Worst\nR3.0m per lasting job\n5% captured"])
    ax.set_ylabel("Lasting jobs reaching former recipient households")
    ax.set_ylim(0, max(former_jobs) * 1.25)
    style_axis(ax, TOKENS, grid_axis="y")
    finish(fig, "jobs-compensation.png")


def make_risk_ladder():
    fig, ax = plt.subplots(figsize=(9.6, 5.6))
    header(fig, "Social instability is a tail risk, not a line item", "Plausible escalation channels if income support is withdrawn during mass unemployment")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis("off")
    stages = [
        (0.4, 0.8, 2.0, 1.0, G100, "1 / PRIVATE COPING", "Meals cut, debt rises, assets sold"),
        (2.75, 1.65, 2.0, 1.0, G300, "2 / LOCAL STRAIN", "Informal demand falls, arrears spread"),
        (5.1, 2.5, 2.0, 1.0, G500, "3 / PUBLIC FRICTION", "Protest, crime risk, service conflict"),
        (7.25, 3.35, 2.3, 1.0, CORAL, "4 / SYSTEMIC SHOCK", "Unrest, emergency spending,\nlost capital"),
    ]
    for x, y, w, h, colour, title, body in stages:
        text_colour = WHITE if colour in [G500, CORAL] else BLACK
        ax.add_patch(Rectangle((x, y), w, h, facecolor=colour, edgecolor=BLACK, linewidth=0.9))
        ax.text(x + 0.12, y + 0.67, title, fontsize=7.1, color=text_colour, fontweight="bold")
        ax.text(x + 0.12, y + 0.28, body, fontsize=6.6, color=text_colour)
    for i in range(3):
        x1, y1, _, _, _, _, _ = stages[i]
        x2, y2, _, _, _, _, _ = stages[i + 1]
        ax.add_patch(FancyArrowPatch((x1 + 2.02, y1 + 0.5), (x2 - 0.05, y2 + 0.5), arrowstyle="-|>", mutation_scale=12, color=BLACK, linewidth=1.1))
    ax.text(5.0, 0.3, "The model leaves stage 4 unpriced because attribution is weak and the distribution is dominated by rare events.", ha="center", fontsize=7.4, color=G700)
    finish(fig, "social-risk-ladder.png")


def write_results():
    job_results = {}
    for name in ["Best", "Average", "Worst"]:
        total_jobs = INDUSTRIAL_ASSET_2050[name] * 1000 / CAPITAL_PER_JOB_M[name]
        former = total_jobs * FORMER_RECIPIENT_CAPTURE[name]
        job_results[name] = {
            "illustrative_total_lasting_jobs": round(total_jobs),
            "jobs_reaching_former_recipient_households": round(former),
            "share_of_8m_recipient_benchmark_percent": round(former / (RECIPIENT_BENCHMARK_M * 1_000_000) * 100, 3),
        }
    payload = {
        "valuation_basis": "constant 2026 consumption-equivalent rand unless stated",
        "real_grant_envelope_r_billion": round(TOTAL_REAL, 2),
        "scenarios": {name: {**{k: v for k, v in SCENARIOS[name].items() if k not in {"colour", "linestyle", "marker"}}, **{k: round(v, 2) for k, v in result.items()}} for name, result in RESULTS.items()},
        "additional_poverty_person_years_million": {n: round(float(v.sum()), 2) for n, v in POVERTY_PATHS.items()},
        "paper1_industrial_public_value_pv_2026_r_billion_at_3_5_percent": INDUSTRIAL_PV,
        "jobs_compensation": job_results,
    }
    (WORK / "model_results.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")


if __name__ == "__main__":
    make_grant_adequacy()
    make_household_diffusion()
    make_consumption_activity()
    make_cumulative_central_cost()
    make_welfare_ledger()
    make_poverty_paths()
    make_tradeoff_matrix()
    make_jobs_compensation()
    make_risk_ladder()
    write_results()
    print(WORK / "model_results.json")
