"""Scenario model for GreyScienx African Convergence Paper 3.

The model is conditional, not predictive. It links African manufacturing value
added to machinery purchases, then estimates equipment sales, the installed
base, lifecycle revenue and domestic value retained by South Africa. Monetary
values are constant 2024 US dollars.
"""

from __future__ import annotations

import json
import sys
import textwrap
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch, Rectangle


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
BASE_MVA_2025 = 300.0  # US$bn, rounded from Africa's ~10% of a ~US$3tn economy
SA_GDP_2024 = 401.1  # US$bn; scale comparator only
STOCK_RETENTION = 0.92  # stylised annual survival of the serviced installed base
DIRECT_VA_PER_JOB = 0.100  # US$bn per thousand jobs = US$100,000 per job
EMPLOYMENT_MULTIPLIER = 1.70

SCENARIOS = {
    "Industrial drift": {"mva_growth": 0.030, "equipment_ratio": 0.16},
    "Manufacturing catch-up": {"mva_growth": 0.055, "equipment_ratio": 0.24},
    "Industrial surge": {"mva_growth": 0.080, "equipment_ratio": 0.30},
}

CATEGORIES = [
    "Mining and materials\nhandling",
    "Food and agricultural\nprocessing",
    "Electrical machinery\nand factory power",
    "Packaging and light\nindustrial equipment",
    "Process and chemical\nequipment",
    "Controls, automation\nand robotics",
    "Medical and laboratory\nequipment",
    "General factory\nequipment",
]
CATEGORY_SHARES = np.array([0.18, 0.18, 0.17, 0.12, 0.11, 0.10, 0.08, 0.06])
SA_CAPTURE = np.array([0.10, 0.08, 0.07, 0.06, 0.06, 0.05, 0.03, 0.03])
WEIGHTED_CAPTURE = float(np.dot(CATEGORY_SHARES, SA_CAPTURE))

BUSINESS_MODELS = {
    "Distributor": {
        "capture": 0.020,
        "equipment_dva": 0.35,
        "service_rate": 0.020,
        "service_dva": 0.55,
        "platform_rate": 0.005,
        "platform_dva": 0.65,
    },
    "Machinery supplier": {
        "capture": WEIGHTED_CAPTURE,
        "equipment_dva": 0.48,
        "service_rate": 0.045,
        "service_dva": 0.70,
        "platform_rate": 0.018,
        "platform_dva": 0.78,
    },
    "Lifecycle platform": {
        "capture": 0.110,
        "equipment_dva": 0.60,
        "service_rate": 0.060,
        "service_dva": 0.76,
        "platform_rate": 0.030,
        "platform_dva": 0.84,
    },
}


def manufacturing_path(growth: float) -> np.ndarray:
    return BASE_MVA_2025 * (1 + growth) ** (YEARS - 2025)


MVA = {name: manufacturing_path(config["mva_growth"]) for name, config in SCENARIOS.items()}
EQUIPMENT = {
    name: MVA[name] * config["equipment_ratio"]
    for name, config in SCENARIOS.items()
}
CENTRAL_EQUIPMENT = EQUIPMENT["Manufacturing catch-up"]
CENTRAL_MARKET = float(CENTRAL_EQUIPMENT.sum())


def lifecycle(config: dict, sector_specific: bool = False) -> dict[str, np.ndarray | float]:
    if sector_specific:
        equipment_sales = CENTRAL_EQUIPMENT * WEIGHTED_CAPTURE
    else:
        equipment_sales = CENTRAL_EQUIPMENT * config["capture"]
    stock = np.zeros(len(YEARS))
    service = np.zeros(len(YEARS))
    platform = np.zeros(len(YEARS))
    for i, sale in enumerate(equipment_sales):
        inherited = stock[i - 1] * STOCK_RETENTION if i else 0.0
        stock[i] = inherited + sale
        service[i] = stock[i] * config["service_rate"]
        platform[i] = stock[i] * config["platform_rate"]
    equipment_dva = equipment_sales * config["equipment_dva"]
    service_dva = service * config["service_dva"]
    platform_dva = platform * config["platform_dva"]
    total_dva = equipment_dva + service_dva + platform_dva
    return {
        "equipment_sales": equipment_sales,
        "stock": stock,
        "service": service,
        "platform": platform,
        "equipment_dva": equipment_dva,
        "service_dva": service_dva,
        "platform_dva": platform_dva,
        "total_dva": total_dva,
        "gross_revenue": float(equipment_sales.sum() + service.sum() + platform.sum()),
        "dva": float(total_dva.sum()),
        "avg_dva": float(total_dva.mean()),
        "direct_jobs_k": float(total_dva.mean() / DIRECT_VA_PER_JOB),
    }


OUTCOMES = {name: lifecycle(config) for name, config in BUSINESS_MODELS.items()}
CENTRAL = lifecycle(BUSINESS_MODELS["Machinery supplier"], sector_specific=True)
CATEGORY_MARKETS = CENTRAL_MARKET * CATEGORY_SHARES
CATEGORY_SALES = CATEGORY_MARKETS * SA_CAPTURE


def new_figure(title: str, subtitle: str, field: str, height: float = 4.75):
    fig = plt.figure(figsize=(7.2, height))
    add_figure_header(fig, title, subtitle, field=field, tokens=TOKENS)
    return fig


def save(fig, name: str):
    ASSETS.mkdir(parents=True, exist_ok=True)
    save_figure(fig, ASSETS / name, dpi=260)
    plt.close(fig)


def figure_mva_paths():
    fig = new_figure(
        "Africa's factory economy has three very different scales",
        "Manufacturing value added begins at a rounded US$300bn in 2025; growth paths are constructed scenarios.",
        "GREYSCIENX / INDUSTRIAL PREMISE",
    )
    ax = fig.add_axes([0.10, 0.17, 0.82, 0.58])
    for (name, values), enc in zip(MVA.items(), [ENC[2], ENC[1], ENC[0]]):
        ax.plot(YEARS, values, label=name, **enc)
        ax.text(2050.3, values[-1], f"${values[-1]/1000:.2f}tn", va="center", fontsize=7.8, color=enc["color"], fontweight="bold")
    style_axis(ax, TOKENS)
    ax.set_xlim(2026, 2053)
    ax.set_ylim(0, 2300)
    ax.set_xlabel("Year")
    ax.set_ylabel("African manufacturing value added (US$bn, 2024 prices)")
    ax.legend(frameon=False, loc="upper left", fontsize=7.5)
    save(fig, "manufacturing-paths.png")


def figure_equipment_demand():
    fig = new_figure(
        "Industrial growth turns into machinery demand",
        "Annual capital-goods purchases rise with factory output and the investment intensity of each scenario.",
        "GREYSCIENX / CAPITAL-GOODS MARKET",
    )
    ax = fig.add_axes([0.10, 0.17, 0.82, 0.58])
    for (name, values), enc in zip(EQUIPMENT.items(), [ENC[2], ENC[1], ENC[0]]):
        ax.plot(YEARS, values, label=f"{name}: ${values.sum()/1000:.1f}tn cumulative", **enc)
        ax.text(2050.3, values[-1], f"${values[-1]:.0f}bn", va="center", fontsize=7.8, color=enc["color"], fontweight="bold")
    style_axis(ax, TOKENS)
    ax.set_xlim(2026, 2053)
    ax.set_ylim(0, 700)
    ax.set_xlabel("Year")
    ax.set_ylabel("Annual factory-equipment demand (US$bn, 2024 prices)")
    ax.legend(frameon=False, loc="upper left", fontsize=7.3)
    save(fig, "equipment-demand.png")


def figure_category_market():
    fig = new_figure(
        "Food, mining and factory power anchor the market",
        "Central catch-up case: cumulative African equipment demand by product family, 2026-2050.",
        "GREYSCIENX / MARKET COMPOSITION",
        5.0,
    )
    ax = fig.add_axes([0.29, 0.13, 0.65, 0.63])
    order = np.arange(len(CATEGORIES))[::-1]
    vals = CATEGORY_MARKETS / 1000
    colors = [TOKENS["coral"] if i < 3 else TOKENS["grey-500"] for i in range(len(CATEGORIES))]
    ax.barh(order, vals[::-1], color=colors[::-1], height=0.63)
    ax.set_yticks(order, [c.replace("\n", " ") for c in CATEGORIES[::-1]], fontsize=7.4)
    for y, value in zip(order, vals[::-1]):
        ax.text(value + 0.012, y, f"${value:.2f}tn", va="center", fontsize=7.2, fontweight="bold")
    style_axis(ax, TOKENS)
    ax.set_xlabel("Cumulative equipment demand (US$tn, 2024 prices)")
    ax.set_xlim(0, max(vals) * 1.22)
    save(fig, "category-market.png")


def figure_capture_funnel():
    fig = new_figure(
        "A large market becomes a modest South African prize",
        "The central model removes competing suppliers and foreign inputs before counting domestic value.",
        "GREYSCIENX / CAPTURE FUNNEL",
        4.9,
    )
    ax = fig.add_axes([0.05, 0.12, 0.90, 0.65])
    ax.axis("off")
    rows = [
        ("African factory-equipment demand", CENTRAL_MARKET / 1000, 0.92, TOKENS["grey-100"]),
        ("South African equipment sales", float(CENTRAL["equipment_sales"].sum()) / 1000, 0.53, TOKENS["grey-500"]),
        ("Lifecycle revenue", float(CENTRAL["service"].sum() + CENTRAL["platform"].sum()) / 1000, 0.37, TOKENS["grey-700"]),
        ("Domestic value", CENTRAL["dva"] / 1000, 0.25, TOKENS["coral"]),
    ]
    for (label, value, width, color), y in zip(rows, [0.76, 0.54, 0.32, 0.10]):
        x = 0.5 - width / 2
        ax.add_patch(FancyBboxPatch((x, y), width, 0.14, boxstyle="round,pad=0.008,rounding_size=0.008", facecolor=color, edgecolor="none"))
        foreground = TOKENS["white"] if color in (TOKENS["grey-700"], TOKENS["coral"]) else TOKENS["black"]
        ax.text(x + 0.022, y + 0.07, label, va="center", fontsize=8, color=foreground, fontweight="bold")
        ax.text(x + width - 0.022, y + 0.07, f"US${value:.2f}tn", ha="right", va="center", fontsize=9.7, color=foreground, fontweight="bold")
    ax.text(0.5, 0.01, f"Weighted equipment share: {WEIGHTED_CAPTURE*100:.1f}% | modelled annual stock survival: {STOCK_RETENTION*100:.0f}%", ha="center", fontsize=7.8, color=TOKENS["grey-700"])
    save(fig, "capture-funnel.png")


def figure_category_capture():
    fig = new_figure(
        "Mining equipment remains the strongest beachhead",
        "Central case: sector size multiplied by a product-specific South African market share.",
        "GREYSCIENX / SOUTH AFRICAN SALES",
        5.0,
    )
    ax = fig.add_axes([0.29, 0.13, 0.65, 0.63])
    order = np.argsort(CATEGORY_SALES)
    vals = CATEGORY_SALES[order]
    labels = [CATEGORIES[i].replace("\n", " ") for i in order]
    colors = [TOKENS["coral"] if i >= len(vals) - 3 else TOKENS["grey-500"] for i in range(len(vals))]
    ax.barh(np.arange(len(vals)), vals, color=colors, height=0.62)
    ax.set_yticks(np.arange(len(vals)), labels, fontsize=7.3)
    for y, value in enumerate(vals):
        ax.text(value + 1.0, y, f"${value:.0f}bn", va="center", fontsize=7.2, fontweight="bold")
    style_axis(ax, TOKENS)
    ax.set_xlabel("Cumulative South African equipment sales (US$bn)")
    ax.set_xlim(0, max(vals) * 1.23)
    save(fig, "category-capture.png")


def figure_business_models():
    fig = new_figure(
        "The business model matters as much as market share",
        "Domestic value added rises when firms manufacture more locally and monetise the installed base.",
        "GREYSCIENX / THREE OUTCOMES",
        5.0,
    )
    ax = fig.add_axes([0.11, 0.18, 0.82, 0.56])
    names = list(OUTCOMES)
    gross = [OUTCOMES[n]["gross_revenue"] for n in names]
    dva = [OUTCOMES[n]["dva"] for n in names]
    x = np.arange(3)
    width = 0.34
    b1 = ax.bar(x - width / 2, gross, width=width, color=TOKENS["grey-500"], label="Gross equipment + lifecycle revenue")
    b2 = ax.bar(x + width / 2, dva, width=width, color=TOKENS["coral"], label="Domestic value added")
    for bars in (b1, b2):
        for bar in bars:
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 12, f"${bar.get_height():.0f}bn", ha="center", fontsize=7.4, fontweight="bold")
    style_axis(ax, TOKENS)
    ax.set_xticks(x, names)
    ax.set_ylabel("Cumulative 2026-2050 value (US$bn)")
    ax.set_ylim(0, max(gross) * 1.17)
    ax.legend(frameon=False, loc="upper left", fontsize=7.3)
    save(fig, "business-models.png")


def figure_lifecycle_stack():
    fig = new_figure(
        "The installed base becomes a second export market",
        "Central supplier case: annual machinery sales create recurring demand for spares, maintenance, software, training and finance.",
        "GREYSCIENX / LIFECYCLE ECONOMICS",
    )
    ax = fig.add_axes([0.10, 0.17, 0.82, 0.58])
    equipment = CENTRAL["equipment_sales"]
    service = CENTRAL["service"]
    platform = CENTRAL["platform"]
    ax.stackplot(YEARS, equipment, service, platform, colors=[TOKENS["grey-700"], TOKENS["coral"], TOKENS["grey-300"]], labels=["Equipment", "Spares and maintenance", "Software, training and finance"], alpha=0.95)
    style_axis(ax, TOKENS)
    ax.set_xlim(2026, 2050)
    ax.set_xlabel("Year")
    ax.set_ylabel("Annual South African-linked revenue (US$bn)")
    ax.legend(frameon=False, loc="upper left", fontsize=7.2)
    save(fig, "lifecycle-stack.png")


def figure_share_jobs():
    fig = new_figure(
        "A seven per cent share becomes a material export pillar",
        "Average annual domestic value and direct employment under the central manufacturing path.",
        "GREYSCIENX / SCALE TEST",
    )
    shares = np.linspace(0, 0.12, 61)
    avg_dva = []
    for share in shares:
        cfg = dict(BUSINESS_MODELS["Machinery supplier"])
        cfg["capture"] = share
        avg_dva.append(lifecycle(cfg)["avg_dva"])
    avg_dva = np.array(avg_dva)
    jobs = avg_dva / DIRECT_VA_PER_JOB
    ax = fig.add_axes([0.10, 0.18, 0.62, 0.56])
    ax.plot(shares * 100, jobs, color=TOKENS["coral"], linewidth=2.4)
    ax.scatter([WEIGHTED_CAPTURE * 100], [CENTRAL["direct_jobs_k"]], s=80, color=TOKENS["black"], zorder=5)
    ax.annotate(f"Central case\n{CENTRAL['direct_jobs_k']:.0f}k direct jobs", (WEIGHTED_CAPTURE * 100, CENTRAL["direct_jobs_k"]), xytext=(10, 8), textcoords="offset points", fontsize=7.8, fontweight="bold")
    style_axis(ax, TOKENS)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, max(jobs) * 1.08)
    ax.set_xlabel("South African share of African capital-goods demand (%)")
    ax.set_ylabel("Average direct jobs (thousands)")
    ax2 = ax.twinx()
    ax2.set_ylim(0, max(jobs) * 1.08 * DIRECT_VA_PER_JOB)
    ax2.set_ylabel("Average annual domestic value added (US$bn)")
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_color(TOKENS["grey-300"])
    ax2.tick_params(colors=TOKENS["grey-500"], labelsize=7)
    save(fig, "share-jobs.png")


def figure_product_map():
    fig = new_figure(
        "Compete where operating knowledge travels",
        "Illustrative product positioning: South Africa's edge is strongest where complexity and service intensity overlap.",
        "GREYSCIENX / PORTFOLIO CHOICE",
        5.0,
    )
    ax = fig.add_axes([0.12, 0.17, 0.80, 0.58])
    products = {
        "Basic packaging": (24, 28), "Commodity motors": (35, 24), "Tractors": (47, 49),
        "Pumps and valves": (60, 62), "Food processing": (57, 69), "Conveyors": (64, 67),
        "Mineral processing": (74, 79), "Factory power": (68, 72), "Lab systems": (77, 76),
        "Automation": (86, 86), "Process control": (91, 90), "Remote diagnostics": (95, 96),
    }
    ax.axvspan(0, 50, color=TOKENS["grey-100"], alpha=0.8)
    ax.axhspan(55, 100, color=TOKENS["coral"], alpha=0.06)
    for name, (x, y) in products.items():
        color = TOKENS["coral"] if x >= 60 and y >= 60 else TOKENS["grey-700"]
        ax.scatter(x, y, s=40, color=color)
        ax.annotate(name, (x, y), xytext=(4, 4), textcoords="offset points", fontsize=6.8, color=color)
    style_axis(ax, TOKENS)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_xlabel("Technical differentiation and defensibility")
    ax.set_ylabel("Lifecycle service and knowledge intensity")
    ax.text(4, 96, "PRICE COMPETITION", fontsize=7, fontweight="bold", color=TOKENS["grey-500"], va="top")
    ax.text(96, 96, "PLATFORM TERRITORY", fontsize=7, fontweight="bold", color=TOKENS["coral"], ha="right", va="top")
    save(fig, "product-map.png")


def figure_roadmap():
    fig = new_figure(
        "Move from machines to installed industrial systems",
        "The capability sequence begins with surviving niches and ends with software-rich lifecycle platforms.",
        "GREYSCIENX / 2026-2050 ROADMAP",
        4.8,
    )
    ax = fig.add_axes([0.05, 0.13, 0.90, 0.63])
    ax.axis("off")
    stages = [
        ("2026-30", "Stabilise niches", "Map capabilities, protect skills, rebuild foundries and supplier quality."),
        ("2031-36", "Finance the buyer", "Export credit, leasing, dealer stock, regional technical training."),
        ("2037-43", "Own the installed base", "Service depots, common parts, remote diagnostics and upgrades."),
        ("2044-50", "Sell performance", "Automation, software, uptime contracts and African production nodes."),
    ]
    for i, (date, title, body) in enumerate(stages):
        left = 0.005 + i * 0.248
        color = TOKENS["coral"] if i == 3 else TOKENS["black"]
        ax.add_patch(FancyBboxPatch((left, 0.15), 0.225, 0.67, boxstyle="round,pad=0.012,rounding_size=0.008", facecolor=TOKENS["white"], edgecolor=TOKENS["grey-300"], linewidth=1))
        ax.add_patch(Rectangle((left, 0.70), 0.225, 0.12, color=color))
        ax.text(left + 0.018, 0.76, date, color=TOKENS["white"], fontsize=8.2, fontweight="bold", va="center")
        ax.text(left + 0.018, 0.61, textwrap.fill(title, 18), fontsize=8.1, fontweight="bold", va="top", linespacing=1.15)
        ax.text(left + 0.018, 0.40, textwrap.fill(body, 25), fontsize=6.8, color=TOKENS["grey-700"], va="top", linespacing=1.25)
        if i < 3:
            ax.annotate("", xy=(left + 0.25, 0.49), xytext=(left + 0.232, 0.49), arrowprops=dict(arrowstyle="->", color=TOKENS["coral"], lw=1.2))
    save(fig, "roadmap.png")


def export_results():
    result = {
        "period": [int(YEARS[0]), int(YEARS[-1])],
        "base_african_mva_2025_usd_bn": BASE_MVA_2025,
        "scenario_results": {
            name: {
                "mva_growth_percent": config["mva_growth"] * 100,
                "equipment_ratio_percent": config["equipment_ratio"] * 100,
                "mva_2050_usd_bn": round(float(MVA[name][-1]), 1),
                "cumulative_equipment_demand_usd_bn": round(float(EQUIPMENT[name].sum()), 1),
            }
            for name, config in SCENARIOS.items()
        },
        "central_weighted_capture_percent": round(WEIGHTED_CAPTURE * 100, 2),
        "central_equipment_sales_usd_bn": round(float(CENTRAL["equipment_sales"].sum()), 1),
        "central_lifecycle_revenue_usd_bn": round(float(CENTRAL["service"].sum() + CENTRAL["platform"].sum()), 1),
        "central_total_revenue_usd_bn": round(CENTRAL["gross_revenue"], 1),
        "central_domestic_value_added_usd_bn": round(CENTRAL["dva"], 1),
        "central_average_annual_dva_usd_bn": round(CENTRAL["avg_dva"], 2),
        "central_average_direct_jobs_thousands": round(CENTRAL["direct_jobs_k"], 1),
        "central_average_supported_jobs_thousands": round(CENTRAL["direct_jobs_k"] * EMPLOYMENT_MULTIPLIER, 1),
        "central_average_dva_percent_2024_sa_gdp": round(CENTRAL["avg_dva"] / SA_GDP_2024 * 100, 2),
        "business_models": {
            name: {
                "equipment_capture_percent": round(config["capture"] * 100, 2),
                "gross_revenue_usd_bn": round(OUTCOMES[name]["gross_revenue"], 1),
                "domestic_value_added_usd_bn": round(OUTCOMES[name]["dva"], 1),
                "average_direct_jobs_thousands": round(OUTCOMES[name]["direct_jobs_k"], 1),
            }
            for name, config in BUSINESS_MODELS.items()
        },
        "categories": [
            {
                "category": CATEGORIES[i].replace("\n", " "),
                "market_share_percent": round(CATEGORY_SHARES[i] * 100, 1),
                "sa_capture_percent": round(SA_CAPTURE[i] * 100, 1),
                "cumulative_market_usd_bn": round(float(CATEGORY_MARKETS[i]), 1),
                "sa_equipment_sales_usd_bn": round(float(CATEGORY_SALES[i]), 1),
            }
            for i in range(len(CATEGORIES))
        ],
    }
    (ROOT / "model_results.json").write_text(json.dumps(result, indent=2), encoding="utf-8")


def main():
    figure_mva_paths()
    figure_equipment_demand()
    figure_category_market()
    figure_capture_funnel()
    figure_category_capture()
    figure_business_models()
    figure_lifecycle_stack()
    figure_share_jobs()
    figure_product_map()
    figure_roadmap()
    export_results()
    print(f"Generated 10 figures in {ASSETS}")
    print(f"Central capital-goods demand: US${CENTRAL_MARKET/1000:.2f}tn")
    print(f"Weighted South African equipment share: {WEIGHTED_CAPTURE*100:.2f}%")
    print(f"Central equipment sales: US${CENTRAL['equipment_sales'].sum():.1f}bn")
    print(f"Central lifecycle revenue: US${CENTRAL['service'].sum()+CENTRAL['platform'].sum():.1f}bn")
    print(f"Central domestic value added: US${CENTRAL['dva']:.1f}bn")
    print(f"Average direct jobs: {CENTRAL['direct_jobs_k']:.0f}k")


if __name__ == "__main__":
    main()
