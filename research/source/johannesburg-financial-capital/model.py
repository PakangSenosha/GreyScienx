"""Scenario model for GreyScienx African Convergence Paper 4.

The model is a transparent scale test, not a forecast. It separates capital
flow from financial-sector revenue and from value retained in South Africa.
All monetary values are constant 2024 US dollars unless stated otherwise.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle


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
YEARS = np.arange(2026, 2051)
BASE_AFRICA_GDP_2025 = 3.0  # US$tn; deliberately rounded scenario anchor
SA_GDP_2024 = 0.4011  # US$tn; comparator only
ASSET_RETENTION = 0.94
DIRECT_VA_PER_JOB = 0.000000180  # US$tn: US$180,000 annual DVA per direct job
EMPLOYMENT_MULTIPLIER = 1.60

SCENARIOS = {
    "Fragmented finance": {
        "gdp_growth": 0.035,
        "investment_share": 0.22,
        "addressable_share": 0.30,
        "jhb_capture": 0.03,
    },
    "Regional hub": {
        "gdp_growth": 0.050,
        "investment_share": 0.27,
        "addressable_share": 0.40,
        "jhb_capture": 0.08,
    },
    "Continental platform": {
        "gdp_growth": 0.065,
        "investment_share": 0.31,
        "addressable_share": 0.48,
        "jhb_capture": 0.14,
    },
}

REVENUE_RATES = {
    "Origination & advisory": 0.014,
    "FX, payments & trade services": 0.006,
    "Insurance, guarantees & risk": 0.010,
    "Asset servicing & custody": 0.0055,
}

DVA_SHARES = {
    "Origination & advisory": 0.75,
    "FX, payments & trade services": 0.78,
    "Insurance, guarantees & risk": 0.72,
    "Asset servicing & custody": 0.82,
}


def path(rate: float) -> np.ndarray:
    return BASE_AFRICA_GDP_2025 * (1 + rate) ** (YEARS - 2025)


def run_scenario(config: dict) -> dict:
    gdp = path(config["gdp_growth"])
    investment = gdp * config["investment_share"]
    addressable = investment * config["addressable_share"]
    captured = addressable * config["jhb_capture"]
    stock = np.zeros(len(YEARS))
    for i, flow in enumerate(captured):
        stock[i] = flow + (stock[i - 1] * ASSET_RETENTION if i else 0.0)
    revenues = {
        "Origination & advisory": captured * REVENUE_RATES["Origination & advisory"],
        "FX, payments & trade services": captured * REVENUE_RATES["FX, payments & trade services"],
        "Insurance, guarantees & risk": captured * REVENUE_RATES["Insurance, guarantees & risk"],
        "Asset servicing & custody": stock * REVENUE_RATES["Asset servicing & custody"],
    }
    dvas = {key: value * DVA_SHARES[key] for key, value in revenues.items()}
    revenue = np.sum(np.array(list(revenues.values())), axis=0)
    dva = np.sum(np.array(list(dvas.values())), axis=0)
    direct_jobs = dva / DIRECT_VA_PER_JOB
    return {
        "gdp": gdp,
        "investment": investment,
        "addressable": addressable,
        "captured": captured,
        "stock": stock,
        "revenues": revenues,
        "dvas": dvas,
        "revenue": revenue,
        "dva": dva,
        "direct_jobs": direct_jobs,
        "cum_gdp": float(gdp.sum()),
        "cum_investment": float(investment.sum()),
        "cum_addressable": float(addressable.sum()),
        "cum_captured": float(captured.sum()),
        "cum_revenue": float(revenue.sum()),
        "cum_dva": float(dva.sum()),
        "avg_dva": float(dva.mean()),
        "avg_direct_jobs": float(direct_jobs.mean()),
        "avg_supported_jobs": float(direct_jobs.mean() * EMPLOYMENT_MULTIPLIER),
    }


RESULTS = {name: run_scenario(config) for name, config in SCENARIOS.items()}
CENTRAL = RESULTS["Regional hub"]


def new_figure(title: str, subtitle: str, field: str, height: float = 4.75):
    fig = plt.figure(figsize=(7.2, height))
    add_figure_header(fig, title, subtitle, field=field, tokens=TOKENS)
    return fig


def save(fig, name: str):
    ASSETS.mkdir(parents=True, exist_ok=True)
    save_figure(fig, ASSETS / name, dpi=260)
    plt.close(fig)


def figure_gdp_paths():
    fig = new_figure(
        "Africa's scale determines the ceiling",
        "Constructed GDP paths begin at a rounded US$3.0tn in 2025; values are constant 2024 dollars.",
        "GREYSCIENX / CONTINENTAL SCALE",
    )
    ax = fig.add_axes([0.10, 0.17, 0.82, 0.58])
    for (name, result), enc in zip(RESULTS.items(), [ENC[2], ENC[1], ENC[0]]):
        ax.plot(YEARS, result["gdp"], label=name, **enc)
        ax.text(2050.3, result["gdp"][-1], f"${result['gdp'][-1]:.1f}tn", va="center", fontsize=7.8, color=enc["color"], fontweight="bold")
    style_axis(ax, TOKENS)
    ax.set_xlim(2026, 2053)
    ax.set_ylim(0, 15.5)
    ax.set_xlabel("Year")
    ax.set_ylabel("African GDP (US$tn, 2024 prices)")
    ax.legend(frameon=False, loc="upper left", fontsize=7.5)
    save(fig, "africa-gdp-paths.png")


def figure_capital_pool():
    fig = new_figure(
        "Only part of investment is a contestable financial market",
        "Annual institutionally or externally financed capital after domestic self-financing is removed.",
        "GREYSCIENX / ADDRESSABLE CAPITAL",
    )
    ax = fig.add_axes([0.10, 0.17, 0.82, 0.58])
    for (name, result), enc in zip(RESULTS.items(), [ENC[2], ENC[1], ENC[0]]):
        values = result["addressable"] * 1000
        ax.plot(YEARS, values, label=f"{name}: ${result['cum_addressable']:.1f}tn cumulative", **enc)
        ax.text(2050.3, values[-1], f"${values[-1]:.0f}bn", va="center", fontsize=7.6, color=enc["color"], fontweight="bold")
    style_axis(ax, TOKENS)
    ax.set_xlim(2026, 2053)
    ax.set_xlabel("Year")
    ax.set_ylabel("Annual addressable capital (US$bn, 2024 prices)")
    ax.legend(frameon=False, loc="upper left", fontsize=7.2)
    save(fig, "addressable-capital.png")


def figure_funnel():
    stages = [
        ("Gross capital\nformation", CENTRAL["cum_investment"]),
        ("Addressable\ninstitutional finance", CENTRAL["cum_addressable"]),
        ("Johannesburg-arranged\nor serviced flow", CENTRAL["cum_captured"]),
        ("Financial-services\nrevenue", CENTRAL["cum_revenue"]),
        ("South African\ndomestic value", CENTRAL["cum_dva"]),
    ]
    fig = new_figure(
        "Notional finance is not national income",
        "Central regional-hub case, cumulative 2026-2050. Each stage applies a different economic boundary.",
        "GREYSCIENX / VALUE-RETENTION FUNNEL",
        5.1,
    )
    ax = fig.add_axes([0.05, 0.10, 0.90, 0.68])
    ax.axis("off")
    widths = [0.90, 0.71, 0.48, 0.29, 0.22]
    ys = np.linspace(0.83, 0.08, len(stages))
    colors = [TOKENS["grey-100"], TOKENS["grey-300"], TOKENS["grey-500"], TOKENS["coral"], TOKENS["black"]]
    for i, ((label, value), width, y, color) in enumerate(zip(stages, widths, ys, colors)):
        x = 0.5 - width / 2
        rect = FancyBboxPatch((x, y), width, 0.12, boxstyle="round,pad=0.008,rounding_size=0.012", transform=ax.transAxes, facecolor=color, edgecolor="none")
        ax.add_patch(rect)
        fg = "white" if i in (2, 4) else TOKENS["black"]
        display = f"${value:.1f}tn" if value >= 1 else f"${value*1000:.0f}bn"
        ax.text(0.5, y + 0.075, display, transform=ax.transAxes, ha="center", va="center", color=fg, fontsize=13, fontweight="bold")
        ax.text(0.5, y + 0.028, label, transform=ax.transAxes, ha="center", va="center", color=fg, fontsize=7.0, fontweight="bold")
    save(fig, "value-retention-funnel.png")


def figure_revenue_stack():
    fig = new_figure(
        "Recurring servicing eventually rivals transaction fees",
        "Central case annual Johannesburg-linked revenue; asset servicing applies to the surviving financed stock.",
        "GREYSCIENX / REVENUE MIX",
    )
    ax = fig.add_axes([0.10, 0.17, 0.82, 0.58])
    labels = list(REVENUE_RATES)
    arrays = [CENTRAL["revenues"][key] * 1000 for key in labels]
    colors = [TOKENS["black"], TOKENS["grey-700"], TOKENS["coral"], TOKENS["grey-300"]]
    ax.stackplot(YEARS, arrays, labels=labels, colors=colors, alpha=0.98)
    style_axis(ax, TOKENS)
    ax.set_xlim(2026, 2050)
    ax.set_xlabel("Year")
    ax.set_ylabel("Annual financial-services revenue (US$bn)")
    ax.legend(frameon=False, loc="upper left", fontsize=7.0)
    save(fig, "revenue-stack.png")


def figure_outcomes():
    fig = new_figure(
        "Hub status changes the order of magnitude",
        "Cumulative results, 2026-2050. Flows are shown on the left; retained value on the right.",
        "GREYSCIENX / THREE OUTCOMES",
        5.0,
    )
    ax = fig.add_axes([0.10, 0.18, 0.55, 0.56])
    ax2 = ax.twinx()
    names = list(RESULTS)
    x = np.arange(3)
    captured = [RESULTS[n]["cum_captured"] for n in names]
    dva = [RESULTS[n]["cum_dva"] * 1000 for n in names]
    bars = ax.bar(x - 0.18, captured, width=0.36, color=TOKENS["grey-500"], label="Captured finance (US$tn)")
    bars2 = ax2.bar(x + 0.18, dva, width=0.36, color=TOKENS["coral"], label="Domestic value (US$bn)")
    ax.set_xticks(x, ["Fragmented\nfinance", "Regional\nhub", "Continental\nplatform"], fontsize=7.4)
    ax.set_ylabel("Captured finance (US$tn)")
    ax2.set_ylabel("South African domestic value (US$bn)")
    style_axis(ax, TOKENS)
    ax2.spines[["top", "right", "left"]].set_visible(False)
    ax2.tick_params(axis="y", labelsize=7, colors=TOKENS["grey-700"], length=0)
    for bar, value in zip(bars, captured):
        ax.text(bar.get_x() + bar.get_width()/2, value + max(captured)*0.02, f"${value:.2f}tn", ha="center", fontsize=7.3, fontweight="bold")
    for bar, value in zip(bars2, dva):
        ax2.text(bar.get_x() + bar.get_width()/2, value + max(dva)*0.02, f"${value:.0f}bn", ha="center", fontsize=7.3, fontweight="bold", color=TOKENS["coral"])
    ax.legend(handles=[bars, bars2], labels=["Captured finance", "Domestic value"], frameon=False, fontsize=7, loc="upper left")
    save(fig, "three-outcomes.png")


def scenario_at_capture(capture: float) -> dict:
    config = dict(SCENARIOS["Regional hub"])
    config["jhb_capture"] = capture
    return run_scenario(config)


def figure_capture_sensitivity():
    captures = np.arange(0.02, 0.201, 0.02)
    tests = [scenario_at_capture(value) for value in captures]
    annual_dva = np.array([item["avg_dva"] * 1000 for item in tests])
    jobs = np.array([item["avg_direct_jobs"] / 1000 for item in tests])
    fig = new_figure(
        "Every two points of capture have visible value",
        "Regional-hub economy with only Johannesburg's share varied; jobs are annual averages.",
        "GREYSCIENX / CAPTURE SENSITIVITY",
    )
    ax = fig.add_axes([0.10, 0.17, 0.67, 0.58])
    ax2 = ax.twinx()
    ax.plot(captures * 100, annual_dva, color=TOKENS["coral"], linewidth=2.3, marker="o", markersize=4, label="Domestic value")
    ax2.plot(captures * 100, jobs, color=TOKENS["black"], linewidth=1.8, marker="s", markersize=3.5, label="Direct jobs")
    ax.axvline(8, color=TOKENS["grey-300"], linestyle="--", linewidth=1.1)
    ax.text(8.3, annual_dva.max()*0.08, "central 8%", fontsize=7.2, color=TOKENS["grey-700"])
    style_axis(ax, TOKENS)
    ax2.spines[["top", "right", "left"]].set_visible(False)
    ax2.tick_params(axis="y", labelsize=7, colors=TOKENS["grey-700"], length=0)
    ax.set_xlabel("Johannesburg share of addressable African finance")
    ax.set_ylabel("Average annual domestic value (US$bn)")
    ax2.set_ylabel("Average direct employment (thousand)")
    ax.set_xticks(captures * 100)
    save(fig, "capture-sensitivity.png")


def figure_volume_value():
    deals = ["Offshore-routed\nmegadeal", "Johannesburg-led\nregional deal"]
    notional = np.array([10.0, 6.0])
    retention = np.array([0.12, 0.36])
    value = notional * retention / 100
    fig = new_figure(
        "A smaller deal can retain more value",
        "Illustrative examples: retained value combines local fees, wages, technology, insurance and profit.",
        "GREYSCIENX / VOLUME VERSUS VALUE",
        4.8,
    )
    ax = fig.add_axes([0.12, 0.18, 0.52, 0.56])
    x = np.arange(2)
    bars = ax.bar(x, notional, color=[TOKENS["grey-300"], TOKENS["black"]], width=0.55)
    ax.set_xticks(x, deals, fontsize=7.4)
    ax.set_ylabel("Deal size (US$bn)")
    style_axis(ax, TOKENS)
    for bar, n, v, rate in zip(bars, notional, value, retention):
        ax.text(bar.get_x()+bar.get_width()/2, n+0.25, f"${n:.0f}bn flow", ha="center", fontsize=7.5, fontweight="bold")
        ax.text(bar.get_x()+bar.get_width()/2, n*0.50, f"{rate:.2f}% retained\n= ${v*1000:.0f}m value", ha="center", va="center", fontsize=8, color=("black" if n == 10 else "white"), fontweight="bold")
    ax.text(1.48, 8.3, "The strategic target is\nretained financial value,\nnot league-table volume.", transform=ax.transData, fontsize=9.2, fontweight="bold", color=TOKENS["coral"], va="top")
    save(fig, "volume-versus-value.png")


def figure_capability_matrix():
    cities = ["Johannesburg", "Lagos", "Nairobi", "Cairo", "Casablanca", "Mauritius", "Dubai"]
    dimensions = ["Market\ndepth", "Banking &\nprojects", "Insurance &\npensions", "FX &\nderivatives", "Payments &\nfintech", "African\nreach", "Talent\nmobility", "Rule & tax\npredictability"]
    scores = np.array([
        [5, 5, 5, 5, 4, 4, 3, 3],
        [3, 4, 3, 2, 5, 5, 3, 2],
        [3, 3, 3, 2, 5, 4, 4, 3],
        [4, 4, 3, 3, 4, 3, 3, 3],
        [3, 4, 4, 3, 4, 4, 4, 4],
        [2, 3, 4, 2, 3, 4, 4, 5],
        [5, 5, 4, 5, 5, 5, 5, 5],
    ])
    fig = new_figure(
        "Johannesburg has depth; rivals have sharper edges",
        "Constructed strategic assessment, not an external ranking. Five indicates a strong relative position.",
        "GREYSCIENX / COMPETITIVE MAP",
        5.25,
    )
    ax = fig.add_axes([0.18, 0.16, 0.76, 0.58])
    from matplotlib.colors import LinearSegmentedColormap
    cmap = LinearSegmentedColormap.from_list("greycoral", [TOKENS["grey-100"], TOKENS["grey-300"], TOKENS["coral"]])
    ax.imshow(scores, cmap=cmap, vmin=1, vmax=5, aspect="auto")
    ax.set_xticks(np.arange(len(dimensions)), dimensions, fontsize=6.5)
    ax.set_yticks(np.arange(len(cities)), cities, fontsize=7.2)
    ax.tick_params(length=0)
    ax.spines[:].set_visible(False)
    for i in range(scores.shape[0]):
        for j in range(scores.shape[1]):
            ax.text(j, i, str(scores[i, j]), ha="center", va="center", fontsize=7.3, fontweight="bold", color=TOKENS["black"])
    save(fig, "competitive-capability-map.png")


def figure_flywheel():
    fig = new_figure(
        "A financial centre is a self-reinforcing network",
        "Policy can start the wheel, but trust, repeat use and liquidity keep it turning.",
        "GREYSCIENX / HUB FLYWHEEL",
        5.05,
    )
    ax = fig.add_axes([0.05, 0.08, 0.90, 0.70])
    ax.axis("off")
    labels = ["More African\nissuers", "Deeper pools\nof investors", "Higher trading\nand risk liquidity", "Lower all-in\ncost of capital", "More mandates,\nskills and data"]
    angles = np.linspace(np.pi/2, np.pi/2 - 2*np.pi, len(labels), endpoint=False)
    coords = np.c_[0.5 + 0.34*np.cos(angles), 0.50 + 0.33*np.sin(angles)]
    for i, ((x, y), label) in enumerate(zip(coords, labels)):
        box = FancyBboxPatch((x-0.105, y-0.055), 0.21, 0.11, transform=ax.transAxes, boxstyle="round,pad=0.012,rounding_size=0.02", facecolor=(TOKENS["coral"] if i == 0 else TOKENS["black"]), edgecolor="none")
        ax.add_patch(box)
        ax.text(x, y, label, transform=ax.transAxes, ha="center", va="center", fontsize=7.7, color=(TOKENS["black"] if i == 0 else "white"), fontweight="bold")
        nx, ny = coords[(i+1) % len(coords)]
        arr = FancyArrowPatch((x, y), (nx, ny), transform=ax.transAxes, arrowstyle="-|>", mutation_scale=12, color=TOKENS["grey-500"], linewidth=1.3, connectionstyle="arc3,rad=0.18", shrinkA=42, shrinkB=42)
        ax.add_patch(arr)
    ax.text(0.5, 0.50, "TRUSTED\nMARKET\nINFRASTRUCTURE", transform=ax.transAxes, ha="center", va="center", fontsize=10, fontweight="bold", color=TOKENS["coral"])
    save(fig, "financial-centre-flywheel.png")


def figure_roadmap():
    phases = [
        ("2026-30", "Repair trust", "Electricity, security, visas,\nFATF durability, market plumbing"),
        ("2030-35", "Connect markets", "PAPSS links, exchange access,\npassporting, local-currency tools"),
        ("2035-42", "Scale platforms", "Risk pools, project preparation,\nAfrican data and fund domiciles"),
        ("2042-50", "Export the stack", "Pan-African servicing, custody,\nsoftware, regulation and skills"),
    ]
    fig = new_figure(
        "The route to 2050 begins with domestic credibility",
        "Sequenced programme: reliability first, connectivity second, scalable African platforms third.",
        "GREYSCIENX / STRATEGIC ROADMAP",
        4.9,
    )
    ax = fig.add_axes([0.05, 0.12, 0.90, 0.63])
    ax.axis("off")
    for i, (years, title, detail) in enumerate(phases):
        x = 0.02 + i * 0.245
        color = TOKENS["coral"] if i == 0 else TOKENS["black"]
        ax.add_patch(FancyBboxPatch((x, 0.22), 0.215, 0.46, transform=ax.transAxes, boxstyle="round,pad=0.01,rounding_size=0.014", facecolor=color, edgecolor="none"))
        fg = TOKENS["black"] if i == 0 else "white"
        ax.text(x+0.018, 0.61, years, transform=ax.transAxes, fontsize=7.2, fontweight="bold", color=fg)
        ax.text(x+0.018, 0.48, title, transform=ax.transAxes, fontsize=10, fontweight="bold", color=fg)
        ax.text(x+0.018, 0.34, detail, transform=ax.transAxes, fontsize=6.7, color=fg, va="top")
        if i < 3:
            ax.add_patch(FancyArrowPatch((x+0.218, 0.45), (x+0.242, 0.45), transform=ax.transAxes, arrowstyle="-|>", mutation_scale=11, color=TOKENS["grey-500"], linewidth=1.2))
    save(fig, "roadmap-2050.png")


def build_all():
    figure_gdp_paths()
    figure_capital_pool()
    figure_funnel()
    figure_revenue_stack()
    figure_outcomes()
    figure_capture_sensitivity()
    figure_volume_value()
    figure_capability_matrix()
    figure_flywheel()
    figure_roadmap()
    output = {
        "model": "Johannesburg as Africa's Financial Capital",
        "units": "constant 2024 US dollars",
        "scenarios": {},
        "central_revenue_components_usd_bn": {
            key: round(float(value.sum() * 1000), 2)
            for key, value in CENTRAL["revenues"].items()
        },
    }
    for name, result in RESULTS.items():
        output["scenarios"][name] = {
            "cumulative_gdp_usd_tn": round(result["cum_gdp"], 3),
            "cumulative_investment_usd_tn": round(result["cum_investment"], 3),
            "cumulative_addressable_usd_tn": round(result["cum_addressable"], 3),
            "cumulative_captured_usd_tn": round(result["cum_captured"], 3),
            "cumulative_revenue_usd_bn": round(result["cum_revenue"] * 1000, 2),
            "cumulative_dva_usd_bn": round(result["cum_dva"] * 1000, 2),
            "average_annual_dva_usd_bn": round(result["avg_dva"] * 1000, 2),
            "average_direct_jobs": round(result["avg_direct_jobs"]),
            "average_supported_jobs": round(result["avg_supported_jobs"]),
            "average_dva_share_sa_gdp_2024_pct": round(result["avg_dva"] / SA_GDP_2024 * 100, 2),
        }
    (ROOT / "model_results.json").write_text(json.dumps(output, indent=2), encoding="utf-8")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    build_all()
