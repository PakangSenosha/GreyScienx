"""GreyScienx model for the fiscal price of an additional birth.

This is a transparent thought experiment, not a fertility forecast or a policy
costing. It follows one million prospective households for five years, separates
births caused by policy from births merely subsidised or brought forward, and
compares the programme cost with the discounted lifetime public-finance and
production value of an additional future worker. All money is constant 2026 rand.
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
WORK_DIR = ROOT / "work" / "price-of-another-child"
ASSET_DIR = WORK_DIR / "assets"
RESULTS_PATH = WORK_DIR / "model_results.json"
CSS_PATH = Path(r"C:\Users\Deriv\Desktop\GreyScienx\app\globals.css")
STYLE_HELPER = Path(
    r"C:\Users\Deriv\Desktop\GreyScienx\skills\greyscienx-editorial-pdf\scripts"
)
if str(STYLE_HELPER) not in sys.path:
    sys.path.insert(0, str(STYLE_HELPER))

try:
    from greyscienx_style import configure_matplotlib  # type: ignore
except Exception:
    configure_matplotlib = None


def load_brand_tokens() -> dict[str, str]:
    defaults = {
        "black": "#131200",
        "true-black": "#000000",
        "coral": "#f26157",
        "white": "#fbfffe",
        "grey-100": "#f0f1f2",
        "grey-300": "#cccccc",
        "grey-500": "#777777",
        "grey-700": "#3d3d3d",
    }
    if CSS_PATH.exists():
        css = CSS_PATH.read_text(encoding="utf-8")
        for key in list(defaults):
            match = re.search(rf"--{re.escape(key)}\s*:\s*(#[0-9a-fA-F]{{6}})", css)
            if match:
                defaults[key] = match.group(1)
    return defaults


TOKENS = load_brand_tokens()
BLACK = TOKENS["black"]
TRUE_BLACK = TOKENS["true-black"]
CORAL = TOKENS["coral"]
WHITE = TOKENS["white"]
GREY_100 = TOKENS["grey-100"]
GREY_300 = TOKENS["grey-300"]
GREY_500 = TOKENS["grey-500"]
GREY_700 = TOKENS["grey-700"]


def set_plot_style() -> None:
    configured = False
    if configure_matplotlib is not None:
        try:
            configure_matplotlib(CSS_PATH)
            configured = True
        except Exception:
            pass
    if not configured:
        plt.rcParams.update(
            {
                "font.family": "sans-serif",
                "font.sans-serif": ["Segoe UI", "Arial", "DejaVu Sans"],
                "font.size": 9.0,
                "axes.edgecolor": BLACK,
                "axes.labelcolor": BLACK,
                "axes.titlecolor": BLACK,
                "xtick.color": BLACK,
                "ytick.color": BLACK,
                "text.color": BLACK,
                "figure.facecolor": WHITE,
                "axes.facecolor": WHITE,
                "savefig.facecolor": WHITE,
                "axes.grid": True,
                "grid.color": GREY_300,
                "grid.linewidth": 0.6,
                "axes.spines.top": False,
                "axes.spines.right": False,
            }
        )
    plt.rcParams["axes.unicode_minus"] = False


def figure_header(fig: plt.Figure, field: str, title: str, subtitle: str) -> None:
    fig.add_artist(
        plt.Line2D(
            [0.065, 0.965], [0.955, 0.955], transform=fig.transFigure,
            color=CORAL, linewidth=4.0, solid_capstyle="butt"
        )
    )
    fig.text(0.065, 0.918, field.upper(), color=CORAL, fontsize=8.5,
             fontweight="bold", ha="left", va="top")
    fig.text(0.065, 0.878, title, color=BLACK, fontsize=17,
             fontweight="bold", ha="left", va="top")
    fig.text(0.065, 0.826, subtitle, color=GREY_700, fontsize=8.4,
             ha="left", va="top")


def style_axis(ax: plt.Axes, grid_axis: str = "y") -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(BLACK)
    ax.spines["bottom"].set_color(BLACK)
    ax.grid(axis=grid_axis, color=GREY_300, linewidth=0.6)
    ax.grid(axis="x" if grid_axis == "y" else "y", visible=False)
    ax.set_axisbelow(True)


def save_figure(fig: plt.Figure, name: str) -> Path:
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    path = ASSET_DIR / name
    fig.savefig(path, dpi=280, bbox_inches="tight", facecolor=WHITE)
    plt.close(fig)
    return path


HOUSEHOLDS = 1_000_000
BASELINE_BIRTHS = 350_000
REAL_DISCOUNT = 0.03
SIMULATIONS = 30_000
SEED = 11092026


@dataclass(frozen=True)
class Policy:
    key: str
    name: str
    cost_basis: str
    base_cost_bn: float
    gross_births: int
    permanent_share: float
    response_cv: float
    permanence_strength: float
    female_jobs: float
    male_jobs: float
    housing: float
    care: float
    time: float
    relationships: float


POLICIES = [
    Policy("cash", "Cash grant top-up", "R1,000 monthly for five years on all births", 21.0, 38_000, 0.38, 0.55, 18, 0.10, 0.10, 0.08, 0.10, 0.08, 0.08),
    Policy("childcare", "Free childcare", "Five years of subsidised care for 65% of births", 32.0, 74_000, 0.67, 0.42, 24, 0.28, 0.05, 0.05, 0.36, 0.24, 0.08),
    Policy("housing", "Family housing", "150,000 deeply subsidised family homes", 54.0, 78_000, 0.75, 0.48, 26, 0.10, 0.22, 0.46, 0.05, 0.08, 0.18),
    Policy("tax", "Parent tax exemption", "Five-year relief for 300,000 taxpaying parents", 42.0, 29_000, 0.43, 0.62, 17, 0.20, 0.18, 0.06, 0.08, 0.05, 0.05),
    Policy("debt", "Debt forgiveness", "R80,000 relief for 250,000 constrained adults", 20.0, 38_000, 0.56, 0.50, 20, 0.18, 0.22, 0.16, 0.04, 0.05, 0.10),
    Policy("flex", "Shorter, flexible work", "Flexible or four-day schedules for 400,000 workers", 36.0, 69_000, 0.72, 0.43, 25, 0.34, 0.06, 0.02, 0.24, 0.45, 0.12),
    Policy("bundle", "Targeted family bundle", "Housing, childcare, debt and work support for 250,000", 77.5, 132_000, 0.82, 0.36, 30, 0.24, 0.20, 0.32, 0.30, 0.31, 0.20),
]


LABOUR_SCENARIOS = {
    "Weak labour market": {"employment": 0.42, "output": 255_000, "growth": 0.007, "tax_share": 0.245},
    "Average labour market": {"employment": 0.70, "output": 345_000, "growth": 0.015, "tax_share": 0.310},
    "Strong labour market": {"employment": 0.86, "output": 410_000, "growth": 0.019, "tax_share": 0.330},
}


def survival(age: int) -> float:
    """Stylised probability that a live birth survives to each age."""
    knots_age = np.array([0, 1, 20, 40, 60, 65, 75, 85, 100])
    knots_survival = np.array([1.00, 0.975, 0.958, 0.925, 0.850, 0.810, 0.635, 0.330, 0.035])
    return float(np.interp(age, knots_age, knots_survival))


def lifetime_value(config: dict[str, float]) -> dict[str, float]:
    taxes = 0.0
    public_cost = 0.0
    production = 0.0
    for age in range(0, 101):
        alive = survival(age)
        discount = 1 / ((1 + REAL_DISCOUNT) ** age)
        if age <= 4:
            annual_public = 28_000
            annual_output = 0.0
        elif age <= 17:
            annual_public = 42_000
            annual_output = 0.0
        elif age <= 22:
            annual_public = 34_000
            annual_output = config["output"] * 0.28 * config["employment"]
        elif age <= 64:
            annual_public = 22_000
            annual_output = config["output"] * config["employment"] * ((1 + config["growth"]) ** (age - 23))
        elif age <= 84:
            annual_public = 67_000
            annual_output = config["output"] * 0.10 * config["employment"]
        else:
            annual_public = 82_000
            annual_output = 0.0
        annual_tax = annual_output * config["tax_share"]
        taxes += alive * annual_tax * discount
        public_cost += alive * annual_public * discount
        production += alive * annual_output * discount
    return {
        "taxes": taxes,
        "public_cost": public_cost,
        "net_fiscal": taxes - public_cost,
        "production": production,
    }


def beta_parameters(mean: float, strength: float) -> tuple[float, float]:
    return mean * strength, (1 - mean) * strength


def simulate_policies() -> list[dict[str, object]]:
    rng = np.random.default_rng(SEED)
    results: list[dict[str, object]] = []
    # Shared uncertainty: a hostile environment can weaken every instrument.
    female_jobs = rng.triangular(0.68, 1.0, 1.22, SIMULATIONS)
    male_jobs = rng.triangular(0.70, 1.0, 1.25, SIMULATIONS)
    housing = rng.triangular(0.72, 1.0, 1.24, SIMULATIONS)
    care = rng.triangular(0.76, 1.0, 1.20, SIMULATIONS)
    time = rng.triangular(0.76, 1.0, 1.18, SIMULATIONS)
    relationships = rng.triangular(0.66, 1.0, 1.20, SIMULATIONS)
    for policy in POLICIES:
        weights = np.array([
            policy.female_jobs, policy.male_jobs, policy.housing,
            policy.care, policy.time, policy.relationships,
        ])
        factors = np.vstack([female_jobs, male_jobs, housing, care, time, relationships])
        if weights.sum() > 0:
            environment = np.exp(np.average(np.log(factors), axis=0, weights=weights))
        else:
            environment = np.ones(SIMULATIONS)
        sigma = np.sqrt(np.log(1 + policy.response_cv ** 2))
        idiosyncratic = rng.lognormal(-0.5 * sigma ** 2, sigma, SIMULATIONS)
        gross = policy.gross_births * environment * idiosyncratic
        alpha, beta = beta_parameters(policy.permanent_share, policy.permanence_strength)
        permanent_share = rng.beta(alpha, beta, SIMULATIONS)
        permanent = np.maximum(gross * permanent_share, 1.0)
        brought_forward = np.maximum(gross - permanent, 0.0)
        cost = policy.base_cost_bn * 1e9 * rng.lognormal(-0.5 * 0.12 ** 2, 0.12, SIMULATIONS)
        cost_per_birth = cost / permanent
        result = {
            "key": policy.key,
            "name": policy.name,
            "cost_basis": policy.cost_basis,
            "base_cost_bn": policy.base_cost_bn,
            "median_gross_births": float(np.median(gross)),
            "median_permanent_births": float(np.median(permanent)),
            "median_brought_forward_births": float(np.median(brought_forward)),
            "cost_per_permanent_birth": {
                "p10": float(np.percentile(cost_per_birth, 10)),
                "median": float(np.median(cost_per_birth)),
                "p90": float(np.percentile(cost_per_birth, 90)),
            },
            "permanent_births": {
                "p10": float(np.percentile(permanent, 10)),
                "median": float(np.median(permanent)),
                "p90": float(np.percentile(permanent, 90)),
            },
            "raw_cost_per_birth": cost_per_birth,
        }
        results.append(result)
    return results


def scenario_response(policy: Policy, case: str) -> tuple[float, float, float]:
    multipliers = {
        "Worst case": (0.55, max(0.18, policy.permanent_share - 0.22), 1.12),
        "Average case": (1.00, policy.permanent_share, 1.00),
        "Best case": (1.38, min(0.94, policy.permanent_share + 0.10), 0.92),
    }
    response, permanence, cost = multipliers[case]
    gross = policy.gross_births * response
    permanent = gross * permanence
    return gross, permanent, policy.base_cost_bn * 1e9 * cost / max(permanent, 1)


def late_start_path(policy: Policy, start_year: int) -> dict[str, float]:
    delay = start_year - 2026
    # A smaller pool of prospective parents and adaptation to low-fertility life.
    parent_pool = np.exp(-0.010 * delay)
    institutional_response = np.exp(-0.014 * delay)
    permanence = max(0.30, policy.permanent_share - 0.0045 * delay)
    gross = policy.gross_births * parent_pool * institutional_response
    permanent = gross * permanence
    nominal_real_cost = policy.base_cost_bn * 1e9 * (1 + 0.006 * delay)
    return {
        "start_year": start_year,
        "permanent_births": permanent,
        "cost_per_birth": nominal_real_cost / max(permanent, 1),
        "response_index": 100 * parent_pool * institutional_response,
    }


def make_figures(policy_results: list[dict[str, object]], lifetime: dict[str, dict[str, float]]) -> None:
    set_plot_style()

    # Figure 1: uncertain cost per permanently additional birth.
    fig, ax = plt.subplots(figsize=(10.6, 5.7))
    figure_header(
        fig, "Figure 1", "The cheapest subsidy is the one that changes completed fertility",
        "Programme cost per permanently additional birth; dots are medians and whiskers span the 10th to 90th percentile."
    )
    ordered = sorted(policy_results, key=lambda x: x["cost_per_permanent_birth"]["median"], reverse=True)
    names = [item["name"] for item in ordered]
    med = np.array([item["cost_per_permanent_birth"]["median"] for item in ordered]) / 1e6
    lo = np.array([item["cost_per_permanent_birth"]["p10"] for item in ordered]) / 1e6
    hi = np.array([item["cost_per_permanent_birth"]["p90"] for item in ordered]) / 1e6
    y = np.arange(len(names))
    ax.hlines(y, lo, hi, color=GREY_500, linewidth=2.0)
    ax.scatter(med, y, color=CORAL, s=55, zorder=3)
    for idx, value in enumerate(med):
        ax.text(value + 0.08, idx, f"R{value:.2f}m", ha="left", va="center", fontsize=8, color=BLACK)
    strong_value = lifetime["Strong labour market"]["net_fiscal"] / 1e6
    ax.axvline(strong_value, color=BLACK, linestyle="--", linewidth=1.5)
    ax.text(strong_value + 0.05, len(names) - 0.52, "Strong-labour fiscal value: R0.96m", fontsize=8,
            color=BLACK, ha="left", va="center")
    ax.set_yticks(y, names)
    ax.set_xlabel("Cost per permanently additional birth (R million)")
    ax.set_xlim(0, max(hi) * 1.08)
    ax.set_ylim(-0.55, len(names) - 0.30)
    style_axis(ax, grid_axis="x")
    fig.subplots_adjust(left=0.25, right=0.96, bottom=0.14, top=0.75)
    save_figure(fig, "cost-per-additional-birth.png")

    # Figure 2: what the programme buys.
    fig, ax = plt.subplots(figsize=(10.6, 5.6))
    figure_header(
        fig, "Figure 2", "Most recipients are not the behavioural margin",
        "Births per one million prospective households over five years; baseline births are shown once for scale."
    )
    names = [item["name"] for item in policy_results]
    moved = np.array([item["median_brought_forward_births"] for item in policy_results]) / 1000
    permanent = np.array([item["median_permanent_births"] for item in policy_results]) / 1000
    y = np.arange(len(names))
    ax.barh(y, moved, color=GREY_300, height=0.62, label="Brought forward, not added")
    ax.barh(y, permanent, left=moved, color=CORAL, height=0.62, label="Permanently additional")
    for idx, value in enumerate(permanent):
        ax.text(moved[idx] + value + 2.0, idx, f"{value:.0f}k added", va="center", fontsize=8, color=BLACK)
    ax.axvline(BASELINE_BIRTHS / 1000, color=BLACK, linestyle="--", linewidth=1.5,
               label="350k births expected without policy")
    ax.set_yticks(y, names)
    ax.invert_yaxis()
    ax.set_xlabel("Births (thousands)")
    ax.set_xlim(0, 390)
    style_axis(ax, grid_axis="x")
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.27), ncol=3, frameon=False)
    fig.subplots_adjust(left=0.25, right=0.96, bottom=0.23, top=0.74)
    save_figure(fig, "birth-decomposition.png")

    # Figure 3: lifetime fiscal and production values.
    fig, axes = plt.subplots(1, 2, figsize=(10.6, 5.5))
    figure_header(
        fig, "Figure 3", "A child is not a fiscal asset until the labour market works",
        "Present value at birth, discounted at 3 percent; production is social output, not government revenue."
    )
    scenarios = list(lifetime)
    taxes = np.array([lifetime[x]["taxes"] for x in scenarios]) / 1e6
    costs = np.array([lifetime[x]["public_cost"] for x in scenarios]) / 1e6
    net = np.array([lifetime[x]["net_fiscal"] for x in scenarios]) / 1e6
    output = np.array([lifetime[x]["production"] for x in scenarios]) / 1e6
    x = np.arange(len(scenarios))
    width = 0.34
    axes[0].bar(x - width / 2, taxes, width, color=CORAL, label="Lifetime taxes")
    axes[0].bar(x + width / 2, costs, width, color=GREY_300, label="Lifetime public cost")
    axes[0].axhline(0, color=BLACK, linewidth=0.8)
    for idx, value in enumerate(net):
        axes[0].text(idx, max(taxes[idx], costs[idx]) + 0.07, f"Net {value:+.2f}m",
                     ha="center", fontsize=8, color=BLACK)
    axes[1].bar(x, output, width=0.54, color=BLACK)
    for idx, value in enumerate(output):
        axes[1].text(idx, value + 0.08, f"R{value:.2f}m", ha="center", fontsize=8, color=BLACK)
    axes[0].set_title("Public-finance account", fontsize=10, fontweight="bold")
    axes[1].set_title("Lifetime economic production", fontsize=10, fontweight="bold")
    for ax in axes:
        ax.set_xticks(x, [s.replace(" labour market", "") for s in scenarios])
        ax.set_ylabel("R million at birth")
        style_axis(ax)
    axes[0].legend(loc="lower center", bbox_to_anchor=(0.5, -0.26), ncol=2, frameon=False)
    fig.subplots_adjust(left=0.08, right=0.97, bottom=0.22, top=0.72, wspace=0.22)
    save_figure(fig, "lifetime-worker-value.png")

    # Figure 4: break-even response rate.
    fig, ax = plt.subplots(figsize=(10.6, 5.8))
    figure_header(
        fig, "Figure 4", "Large incentives make sense only if enough births are truly additional",
        "Each point is the average-case programme. Curves show the births needed to recoup cost at alternative fiscal values."
    )
    costs_bn = np.array([p.base_cost_bn for p in POLICIES])
    births_k = np.array([scenario_response(p, "Average case")[1] for p in POLICIES]) / 1000
    markers = ["o", "s", "^", "D", "v", "P", "X"]
    for idx, policy in enumerate(POLICIES):
        ax.scatter(costs_bn[idx], births_k[idx], color=CORAL if policy.key == "bundle" else BLACK,
                   marker=markers[idx], s=62, zorder=4)
        label_offsets = {
            "cash": (7, -1), "childcare": (7, 7), "housing": (7, -13),
            "tax": (7, 7), "debt": (7, 10), "flex": (7, -15), "bundle": (7, -13),
        }
        offset = label_offsets[policy.key]
        ax.annotate(policy.name.replace("Targeted ", ""), (costs_bn[idx], births_k[idx]),
                    xytext=offset, textcoords="offset points", fontsize=7.6, color=BLACK)
    grid = np.linspace(0, 85, 180)
    for label, color, style in [
        ("Average labour market", GREY_500, "--"),
        ("Strong labour market", CORAL, "-"),
    ]:
        value_m = lifetime[label]["net_fiscal"] / 1e6
        needed_k = grid / max(value_m, 0.01)
        ax.plot(grid, needed_k, color=color, linestyle=style, linewidth=1.8, label=f"Break-even: {label.replace(' labour market', '')}")
    ax.set_xlabel("Five-year programme cost (R billion)")
    ax.set_ylabel("Permanently additional births (thousands)")
    ax.set_xlim(0, 86)
    ax.set_ylim(0, max(155, births_k.max() * 1.18))
    style_axis(ax)
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.25), ncol=2, frameon=False)
    fig.subplots_adjust(left=0.10, right=0.96, bottom=0.22, top=0.73)
    save_figure(fig, "break-even-map.png")

    # Figure 5: delayed intervention and effective irreversibility.
    selected = [next(p for p in POLICIES if p.key == "cash"), next(p for p in POLICIES if p.key == "bundle")]
    years = [2026, 2040, 2060]
    fig, axes = plt.subplots(1, 2, figsize=(10.6, 5.3))
    figure_header(
        fig, "Figure 5", "Delay can turn a difficult reversal into an uneconomic one",
        "Illustrative adaptation: the prospective-parent pool and behavioural response shrink as low fertility persists."
    )
    colors = [GREY_500, CORAL]
    markers = ["s", "o"]
    for idx, policy in enumerate(selected):
        points = [late_start_path(policy, year) for year in years]
        axes[0].plot(years, [p["permanent_births"] / 1000 for p in points], color=colors[idx],
                     marker=markers[idx], linewidth=2.2, label=policy.name)
        axes[1].plot(years, [p["cost_per_birth"] / 1e6 for p in points], color=colors[idx],
                     marker=markers[idx], linewidth=2.2)
    axes[0].set_title("Permanently additional births", fontsize=10, fontweight="bold")
    axes[1].set_title("Cost per additional birth", fontsize=10, fontweight="bold")
    axes[0].set_ylabel("Births (thousands)")
    axes[1].set_ylabel("R million")
    for ax in axes:
        ax.set_xlabel("Policy start year")
        ax.set_xticks(years)
        style_axis(ax)
    axes[0].legend(loc="lower center", bbox_to_anchor=(1.12, -0.31), ncol=2, frameon=False)
    fig.subplots_adjust(left=0.08, right=0.97, bottom=0.23, top=0.72, wspace=0.23)
    save_figure(fig, "delay-and-irreversibility.png")


def main() -> None:
    WORK_DIR.mkdir(parents=True, exist_ok=True)
    lifetime = {name: lifetime_value(config) for name, config in LABOUR_SCENARIOS.items()}
    policy_results = simulate_policies()
    average_fiscal = lifetime["Average labour market"]["net_fiscal"]
    strong_fiscal = lifetime["Strong labour market"]["net_fiscal"]
    for item in policy_results:
        raw = item.pop("raw_cost_per_birth")
        item["fiscal_break_even_probability"] = {
            "average_labour": float(np.mean(raw <= average_fiscal)),
            "strong_labour": float(np.mean(raw <= strong_fiscal)),
        }
    case_table = []
    for policy in POLICIES:
        row = {"policy": policy.name}
        for case in ("Worst case", "Average case", "Best case"):
            gross, permanent, cost_per = scenario_response(policy, case)
            row[case] = {
                "gross_births": gross,
                "permanent_births": permanent,
                "cost_per_permanent_birth": cost_per,
            }
        case_table.append(row)
    late_start = {
        policy.name: [late_start_path(policy, year) for year in (2026, 2040, 2060)]
        for policy in POLICIES if policy.key in ("cash", "bundle")
    }
    payload = {
        "study": "The Price of Another Child",
        "prices": "constant 2026 rand",
        "households": HOUSEHOLDS,
        "baseline_births": BASELINE_BIRTHS,
        "window_years": 5,
        "simulations": SIMULATIONS,
        "random_seed": SEED,
        "real_discount_rate": REAL_DISCOUNT,
        "policies": [asdict(policy) for policy in POLICIES],
        "policy_results": policy_results,
        "case_table": case_table,
        "lifetime_value": lifetime,
        "late_start": late_start,
        "interpretation": {
            "additional_birth": "A birth that increases completed fertility, not merely one shifted into the five-year window.",
            "break_even": "Programme cost per additional birth is below the added worker's net lifetime fiscal value.",
            "production_warning": "Production is a social value and cannot be treated as budget revenue.",
        },
    }
    RESULTS_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    make_figures(policy_results, lifetime)

    display = {
        "lifetime_millions": {
            name: {k: round(v / 1e6, 3) for k, v in values.items()}
            for name, values in lifetime.items()
        },
        "policies": [
            {
                "name": item["name"],
                "added_births_median": round(item["median_permanent_births"]),
                "cost_per_birth_median_m": round(item["cost_per_permanent_birth"]["median"] / 1e6, 2),
                "range_m": [
                    round(item["cost_per_permanent_birth"]["p10"] / 1e6, 2),
                    round(item["cost_per_permanent_birth"]["p90"] / 1e6, 2),
                ],
                "break_even_average_pct": round(100 * item["fiscal_break_even_probability"]["average_labour"], 1),
                "break_even_strong_pct": round(100 * item["fiscal_break_even_probability"]["strong_labour"], 1),
            }
            for item in policy_results
        ],
    }
    print(json.dumps(display, indent=2))


if __name__ == "__main__":
    main()
