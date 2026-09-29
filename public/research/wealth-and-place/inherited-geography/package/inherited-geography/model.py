"""Inherited Geography: distributional property-inheritance model.

This is a transparent scenario model, not a forecast and not a race-to-wealth
imputation engine. It has three deliberately separate layers:

1. observed evidence anchors (probate, NIDS, Census and deeds summaries);
2. matched-descendant property-condition simulations; and
3. a synthetic population-group intake layer used only to show how observed
   differences in formal-estate incidence and location could map into a broad
   distribution of inherited property.

All monetary values are constant 2024 rand. Population-group labels reproduce
historically produced South African statistical categories; they are not
individual characteristics and must never be used to infer an individual's
wealth.
"""

from __future__ import annotations

import csv
import json
import math
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parent
FIGURES = ROOT / "figures"
WORKSPACE = ROOT.parents[2]
STYLE_DIR = WORKSPACE / ".agents" / "skills" / "greyscienx-editorial-pdf" / "scripts"
sys.path.insert(0, str(STYLE_DIR))

from greyscienx_style import (  # noqa: E402
    add_figure_header,
    configure_matplotlib,
    line_encodings,
    save_figure,
    style_axis,
)


SEED = 20260920
N = 100_000
YEARS = np.array([20, 40, 60])
BASE_SALARY = 420_000.0
BASE_SAVING_RATE = 0.08
BASE_LIQUID_WEALTH = 50_000.0
FIN_RETURN = 0.035

TOKENS = configure_matplotlib(WORKSPACE / "app" / "globals.css")
ENC = line_encodings(TOKENS)


@dataclass(frozen=True)
class PropertyProfile:
    label: str
    short: str
    median_value: float
    value_sigma: float
    real_appreciation: tuple[float, float, float]
    marketability: tuple[float, float, float]
    housing_yield: tuple[float, float, float]
    maintenance: tuple[float, float, float]
    rent_probability: float
    rental_net_share: tuple[float, float, float]
    collateral_ltv: tuple[float, float, float]
    opportunity_probability: float
    debt_ratio: tuple[float, float, float]
    heir_probs: tuple[float, ...]


PROFILES = {
    "none": PropertyProfile(
        "No inherited property", "None", 0, 0, (0, 0, 0), (0, 0, 0),
        (0, 0, 0), (0, 0, 0), 0, (0, 0, 0), (0, 0, 0), 0,
        (0, 0, 0), (1.0,),
    ),
    "communal": PropertyProfile(
        "Rural or communal family residence", "Communal", 350_000, 0.45,
        (-0.005, 0.004, 0.015), (0.05, 0.14, 0.30), (0.025, 0.045, 0.065),
        (0.008, 0.014, 0.025), 0.05, (0.35, 0.55, 0.75), (0.00, 0.00, 0.05),
        0.04, (0.00, 0.00, 0.03), (0.12, 0.24, 0.25, 0.18, 0.12, 0.09),
    ),
    "township": PropertyProfile(
        "Titled township home", "Township", 560_000, 0.38,
        (-0.005, 0.008, 0.025), (0.55, 0.78, 0.93), (0.035, 0.055, 0.075),
        (0.010, 0.018, 0.030), 0.18, (0.40, 0.60, 0.80), (0.12, 0.30, 0.50),
        0.10, (0.00, 0.03, 0.12), (0.22, 0.34, 0.25, 0.13, 0.06),
    ),
    "middle_suburb": PropertyProfile(
        "Middle-value suburban home", "Middle suburb", 1_500_000, 0.42,
        (0.000, 0.015, 0.032), (0.78, 0.91, 0.98), (0.030, 0.046, 0.062),
        (0.010, 0.018, 0.030), 0.22, (0.45, 0.65, 0.82), (0.28, 0.45, 0.62),
        0.16, (0.00, 0.06, 0.18), (0.35, 0.40, 0.18, 0.07),
    ),
    "high_property": PropertyProfile(
        "High-value property or small portfolio", "High property", 4_500_000, 0.65,
        (0.000, 0.018, 0.036), (0.84, 0.94, 0.99), (0.028, 0.043, 0.060),
        (0.009, 0.017, 0.028), 0.52, (0.50, 0.70, 0.88), (0.35, 0.53, 0.70),
        0.24, (0.00, 0.08, 0.22), (0.40, 0.38, 0.16, 0.06),
    ),
    "farm": PropertyProfile(
        "Productive agricultural property", "Productive farm", 3_500_000, 0.70,
        (-0.010, 0.012, 0.035), (0.42, 0.72, 0.94), (0.000, 0.000, 0.000),
        (0.010, 0.025, 0.045), 0.00, (0.00, 0.00, 0.00), (0.18, 0.38, 0.58),
        0.22, (0.00, 0.08, 0.25), (0.28, 0.36, 0.22, 0.10, 0.04),
    ),
}


# Evidence-constrained synthetic intake profiles. The any-property rate is a
# scenario bracket around estate-to-death ratios, not a measured probability
# that an individual descendant receives property. Location/type weights are
# deliberately broad and are never used to classify a real person.
GROUP_PROFILES = {
    "Black African": {
        "p_any": (0.12, 0.20, 0.30),
        "p_large_observed": 0.03,
        "claim_divisor_probs": (0.15, 0.35, 0.30, 0.20),
        "weights": {"communal": 0.30, "township": 0.38, "middle_suburb": 0.20, "high_property": 0.04, "farm": 0.08},
    },
    "Coloured": {
        "p_any": (0.20, 0.30, 0.42),
        "p_large_observed": 0.09,
        "claim_divisor_probs": (0.25, 0.40, 0.25, 0.10),
        "weights": {"communal": 0.05, "township": 0.35, "middle_suburb": 0.40, "high_property": 0.12, "farm": 0.08},
    },
    "Indian or Asian": {
        "p_any": (0.30, 0.42, 0.55),
        "p_large_observed": 0.23,
        "claim_divisor_probs": (0.45, 0.35, 0.15, 0.05),
        "weights": {"communal": 0.02, "township": 0.18, "middle_suburb": 0.52, "high_property": 0.22, "farm": 0.06},
    },
    "White": {
        "p_any": (0.50, 0.68, 0.82),
        "p_large_observed": 0.45,
        "claim_divisor_probs": (0.55, 0.30, 0.12, 0.03),
        "weights": {"communal": 0.01, "township": 0.03, "middle_suburb": 0.48, "high_property": 0.32, "farm": 0.16},
    },
}


OBSERVED_LARGE_WEALTH = {
    "Black African": {"probate": 0.03, "nids_all": 0.08, "nids_ex_possessions": 0.05},
    "Coloured": {"probate": 0.09, "nids_all": 0.15, "nids_ex_possessions": 0.09},
    "Indian or Asian": {"probate": 0.23, "nids_all": 0.25, "nids_ex_possessions": 0.26},
    "White": {"probate": 0.45, "nids_all": 0.47, "nids_ex_possessions": 0.42},
}


AGRI_PROFILES = {
    "Communal / rain-fed": {
        "title_factor": (0.05, 0.15, 0.30), "appreciation": (-0.01, 0.002, 0.015),
        "income_yield": (-0.005, 0.010, 0.028), "collateral_ltv": (0.0, 0.0, 0.03),
    },
    "Communal / water + capital": {
        "title_factor": (0.08, 0.20, 0.35), "appreciation": (-0.005, 0.008, 0.022),
        "income_yield": (0.010, 0.035, 0.070), "collateral_ltv": (0.0, 0.02, 0.08),
    },
    "Freehold / rain-fed": {
        "title_factor": (0.70, 0.86, 0.96), "appreciation": (-0.005, 0.010, 0.028),
        "income_yield": (0.000, 0.020, 0.045), "collateral_ltv": (0.20, 0.35, 0.50),
    },
    "Freehold / water + capital": {
        "title_factor": (0.82, 0.93, 0.99), "appreciation": (0.000, 0.018, 0.038),
        "income_yield": (0.020, 0.055, 0.095), "collateral_ltv": (0.30, 0.48, 0.65),
    },
}


def triangular(rng: np.random.Generator, bounds: tuple[float, float, float], size: int) -> np.ndarray:
    low, mode, high = bounds
    if low == mode == high:
        return np.full(size, low, dtype=float)
    return rng.triangular(low, mode, high, size)


def lognormal_from_median(rng: np.random.Generator, median: float, sigma: float, size: int) -> np.ndarray:
    if median == 0:
        return np.zeros(size)
    return rng.lognormal(mean=math.log(median), sigma=sigma, size=size)


def annuity_future_value(payment: np.ndarray, rate: np.ndarray, years: int) -> np.ndarray:
    return payment * (((1 + rate) ** years - 1) / np.maximum(rate, 1e-9))


def baseline_wealth(years: int) -> float:
    annual_saving = BASE_SALARY * BASE_SAVING_RATE
    return BASE_LIQUID_WEALTH * (1 + FIN_RETURN) ** years + annual_saving * (((1 + FIN_RETURN) ** years - 1) / FIN_RETURN)


def simulate_property(profile_key: str, seed_offset: int = 0, opportunity: bool = False) -> dict[str, np.ndarray]:
    p = PROFILES[profile_key]
    rng = np.random.default_rng(SEED + seed_offset)
    size = N
    gross = lognormal_from_median(rng, p.median_value, p.value_sigma, size)
    heirs = rng.choice(np.arange(1, len(p.heir_probs) + 1), size=size, p=np.asarray(p.heir_probs) / np.sum(p.heir_probs))
    debt_ratio = triangular(rng, p.debt_ratio, size)
    administration_haircut = rng.triangular(0.0, 0.025 if profile_key != "communal" else 0.04, 0.12 if profile_key != "communal" else 0.20, size)
    inherited_equity = gross * (1 - debt_ratio) * (1 - administration_haircut) / heirs
    appreciation = triangular(rng, p.real_appreciation, size)
    marketability = triangular(rng, p.marketability, size)
    gross_housing_yield = triangular(rng, p.housing_yield, size)
    maintenance = triangular(rng, p.maintenance, size)
    net_housing_yield = np.maximum(0.0, gross_housing_yield - maintenance)
    rental_net_share = triangular(rng, p.rental_net_share, size)
    rented = rng.random(size) < p.rent_probability
    collateral_ltv = triangular(rng, p.collateral_ltv, size)
    financial_return = rng.triangular(0.02, FIN_RETURN, 0.055, size)

    # Agricultural property earns productive income rather than housing services.
    if profile_key == "farm":
        productive_yield = rng.triangular(-0.01, 0.025, 0.075, size)
        use_share = rng.triangular(0.25, 0.50, 0.75, size)
        housing_payment = np.zeros(size)
        rental_payment = np.zeros(size)
        productive_payment = np.maximum(0.0, inherited_equity * productive_yield) * use_share
    else:
        use_share = 1 / np.sqrt(heirs) if profile_key == "communal" else np.ones(size)
        housing_payment = inherited_equity * net_housing_yield * use_share * (~rented) * rng.triangular(0.35, 0.55, 0.75, size)
        rental_payment = inherited_equity * net_housing_yield * rented * rental_net_share
        productive_payment = np.zeros(size)

    out: dict[str, np.ndarray] = {
        "gross_initial": gross,
        "inherited_equity": inherited_equity,
        "heirs": heirs.astype(float),
        "marketability": marketability,
        "collateral_ltv": collateral_ltv,
    }
    for year in YEARS:
        property_value = inherited_equity * (1 + appreciation) ** year
        marketable_equity = property_value * marketability
        housing_fv = annuity_future_value(housing_payment, financial_return, int(year))
        rental_fv = annuity_future_value(rental_payment, financial_return, int(year))
        productive_fv = annuity_future_value(productive_payment, financial_return, int(year))
        opp_gain = np.zeros(size)
        if opportunity and profile_key != "none":
            eligible = rng.random(size) < p.opportunity_probability
            capacity_year5 = inherited_equity * (1 + appreciation) ** 5 * marketability * collateral_ltv
            capital_used = np.minimum(capacity_year5, rng.lognormal(math.log(180_000), 0.65, size))
            # Net gain after financing costs. Losses remain possible.
            net_multiple = rng.triangular(-0.45, 0.22, 1.25, size)
            opp_gain = eligible * capital_used * net_multiple * (1 + financial_return) ** max(0, int(year) - 5)
        baseline = np.full(size, baseline_wealth(int(year)))
        total = baseline + marketable_equity + housing_fv + rental_fv + productive_fv + opp_gain
        broader = baseline + property_value + housing_fv + rental_fv + productive_fv + opp_gain
        out[f"property_value_{year}"] = property_value
        out[f"marketable_equity_{year}"] = marketable_equity
        out[f"housing_{year}"] = housing_fv
        out[f"rental_{year}"] = rental_fv
        out[f"productive_{year}"] = productive_fv
        out[f"opportunity_{year}"] = opp_gain
        out[f"baseline_{year}"] = baseline
        out[f"total_{year}"] = total
        out[f"broader_{year}"] = broader
    return out


def percentile_summary(values: np.ndarray) -> dict[str, float]:
    return {
        "p10": float(np.percentile(values, 10)),
        "p25": float(np.percentile(values, 25)),
        "median": float(np.percentile(values, 50)),
        "p75": float(np.percentile(values, 75)),
        "p90": float(np.percentile(values, 90)),
        "mean": float(np.mean(values)),
    }


def matched_results() -> tuple[dict, dict[str, dict[str, np.ndarray]], dict[str, dict[str, np.ndarray]]]:
    direct = {}
    extended = {}
    results: dict[str, dict] = {}
    for i, key in enumerate(PROFILES):
        direct[key] = simulate_property(key, i * 100, opportunity=False)
        extended[key] = simulate_property(key, i * 100, opportunity=True)
        initial_liquid = direct[key]["inherited_equity"] * direct[key]["marketability"]
        results[key] = {
            "label": PROFILES[key].label,
            "initial_inherited_equity": percentile_summary(direct[key]["inherited_equity"]),
            "initial_liquid_equivalent": percentile_summary(initial_liquid),
            "horizons": {},
        }
        for year in YEARS:
            vals = direct[key][f"total_{year}"]
            broader = direct[key][f"broader_{year}"]
            results[key]["horizons"][str(year)] = {
                "marketable_net_worth": percentile_summary(vals),
                "broader_resource_value": percentile_summary(broader),
                "probability_over_1m": float(np.mean(vals >= 1_000_000)),
                "probability_over_3m": float(np.mean(vals >= 3_000_000)),
                "probability_over_10m": float(np.mean(vals >= 10_000_000)),
            }
        year = 40
        baseline_40 = baseline_wealth(year)
        initial_median = float(np.median(initial_liquid))
        increment_40 = float(np.median(direct[key][f"total_{year}"]) - baseline_40)
        results[key]["property_momentum_40"] = {
            "median_increment_over_no_property": increment_40,
            "increment_per_rand_initial_liquid_equivalent": (increment_40 / initial_median) if initial_median > 0 else 0.0,
        }
        opp = extended[key][f"opportunity_{year}"]
        results[key]["decomposition_40_means"] = {
            "same_earnings_and_saving": float(np.mean(direct[key][f"baseline_{year}"])),
            "marketable_property_equity": float(np.mean(direct[key][f"marketable_equity_{year}"])),
            "reinvested_housing_savings": float(np.mean(direct[key][f"housing_{year}"])),
            "reinvested_rental_income": float(np.mean(direct[key][f"rental_{year}"])),
            "reinvested_farm_income": float(np.mean(direct[key][f"productive_{year}"])),
            "opportunity_channel_extended_case_mean": float(np.mean(opp)),
            "opportunity_channel_use_probability": float(np.mean(opp != 0)),
            "opportunity_channel_conditional_median": float(np.median(opp[opp != 0])) if np.any(opp != 0) else 0.0,
        }
    return results, direct, extended


def group_intake_results() -> tuple[dict, dict[str, np.ndarray]]:
    results = {}
    raw = {}
    type_keys = ["communal", "township", "middle_suburb", "high_property", "farm"]
    for i, (group, cfg) in enumerate(GROUP_PROFILES.items()):
        rng = np.random.default_rng(SEED + 10_000 + i)
        p_any = triangular(rng, cfg["p_any"], N)
        receives = rng.random(N) < p_any
        keys = np.array(type_keys, dtype=object)
        probs = np.array([cfg["weights"][k] for k in type_keys])
        chosen = rng.choice(keys, size=N, p=probs)
        claim_divisor = rng.choice(
            np.arange(1, len(cfg["claim_divisor_probs"]) + 1),
            size=N,
            p=np.asarray(cfg["claim_divisor_probs"]) / np.sum(cfg["claim_divisor_probs"]),
        )
        inherited = np.zeros(N)
        liquid_equivalent = np.zeros(N)
        for j, key in enumerate(type_keys):
            mask = receives & (chosen == key)
            if not np.any(mask):
                continue
            p = PROFILES[key]
            count = int(mask.sum())
            gross = lognormal_from_median(rng, p.median_value, p.value_sigma, count)
            heirs = rng.choice(np.arange(1, len(p.heir_probs) + 1), size=count, p=np.asarray(p.heir_probs) / np.sum(p.heir_probs))
            debt = triangular(rng, p.debt_ratio, count)
            admin = rng.triangular(0.0, 0.035, 0.15 if key != "communal" else 0.22, count)
            share = gross * (1 - debt) * (1 - admin) / (heirs * claim_divisor[mask])
            marketability = triangular(rng, p.marketability, count)
            inherited[mask] = share
            liquid_equivalent[mask] = share * marketability
        raw[group] = liquid_equivalent
        receiver_vals = liquid_equivalent[receives]
        results[group] = {
            "modeled_any_property_probability": float(receives.mean()),
            "observed_large_formal_wealth_probability": cfg["p_large_observed"],
            "all_descendants_liquid_equivalent": percentile_summary(liquid_equivalent),
            "receivers_only_liquid_equivalent": percentile_summary(receiver_vals),
            "probability_liquid_equivalent_over_250k": float(np.mean(liquid_equivalent >= 250_000)),
            "property_type_weights_conditional_on_receipt": cfg["weights"],
        }
    return results, raw


def agricultural_results() -> tuple[dict, dict[str, dict[str, np.ndarray]]]:
    results = {}
    raw = {}
    initial_land_value = 2_500_000.0
    horizon = 20
    for i, (label, cfg) in enumerate(AGRI_PROFILES.items()):
        rng = np.random.default_rng(SEED + 20_000 + i)
        title_factor = triangular(rng, cfg["title_factor"], N)
        appreciation = triangular(rng, cfg["appreciation"], N)
        income_yield = triangular(rng, cfg["income_yield"], N)
        ltv = triangular(rng, cfg["collateral_ltv"], N)
        fin_r = rng.triangular(0.02, 0.035, 0.055, N)
        terminal_land = initial_land_value * (1 + appreciation) ** horizon
        marketable = terminal_land * title_factor
        income_fv = annuity_future_value(np.maximum(0, initial_land_value * income_yield) * 0.55, fin_r, horizon)
        collateral_capacity = initial_land_value * title_factor * ltv
        resource_value = terminal_land + income_fv
        marketable_value = marketable + income_fv
        raw[label] = {
            "marketable": marketable_value,
            "resource": resource_value,
            "collateral": collateral_capacity,
            "income_fv": income_fv,
        }
        results[label] = {
            "same_initial_land_value": initial_land_value,
            "marketable_value_20": percentile_summary(marketable_value),
            "broader_resource_value_20": percentile_summary(resource_value),
            "collateral_capacity_initial": percentile_summary(collateral_capacity),
            "reinvested_productive_income_20": percentile_summary(income_fv),
        }
    return results, raw


def new_figure(title: str, subtitle: str, field: str, height: float = 5.0):
    fig = plt.figure(figsize=(7.2, height))
    add_figure_header(fig, title, subtitle, field=field, tokens=TOKENS)
    return fig


def save(fig, name: str):
    FIGURES.mkdir(parents=True, exist_ok=True)
    save_figure(fig, FIGURES / name, dpi=270)
    plt.close(fig)


def fmt_millions(v: float) -> str:
    return f"R{v / 1_000_000:.1f}m"


def figure_evidence_threshold():
    fig = new_figure(
        "Formal wealth is uneven - and the sources disagree in patterned ways",
        "Adults with wealth above R250,000: probate estimate (2009-2019 pooled) and NIDS Wave 4 (2014/15).",
        "GREYSCIENX / OBSERVED EVIDENCE",
        5.0,
    )
    ax = fig.add_axes([0.12, 0.19, 0.82, 0.56])
    groups = list(OBSERVED_LARGE_WEALTH)
    x = np.arange(len(groups))
    width = 0.24
    series = [
        ("Probate", "probate", TOKENS["coral"]),
        ("NIDS: all wealth", "nids_all", TOKENS["black"]),
        ("NIDS: excl. possessions", "nids_ex_possessions", TOKENS["grey-500"]),
    ]
    for j, (label, key, color) in enumerate(series):
        vals = [OBSERVED_LARGE_WEALTH[g][key] * 100 for g in groups]
        bars = ax.bar(x + (j - 1) * width, vals, width=width, color=color, label=label)
        for bar, value in zip(bars, vals):
            ax.text(bar.get_x() + bar.get_width() / 2, value + 1.0, f"{value:.0f}%", ha="center", va="bottom", fontsize=7.0, fontweight="bold", color=color)
    ax.set_xticks(x, ["Black\nAfrican", "Coloured", "Indian or\nAsian", "White"])
    ax.set_ylabel("Share of adults aged 20+ (%)")
    ax.set_ylim(0, 55)
    style_axis(ax, TOKENS)
    ax.legend(frameon=False, ncol=3, fontsize=7.2, loc="upper left")
    save(fig, "observed-formal-wealth-threshold.png")


def figure_property_bundle():
    labels = ["Resale", "Housing use", "Rent", "Collateral", "Liquidity", "Appreciation"]
    data = np.array([
        [0.15, 0.75, 0.20, 0.05, 0.15, 0.30],
        [0.72, 0.80, 0.55, 0.45, 0.62, 0.50],
        [0.92, 0.82, 0.62, 0.78, 0.90, 0.72],
        [0.96, 0.75, 0.78, 0.88, 0.94, 0.82],
        [0.70, 0.25, 0.25, 0.62, 0.58, 0.60],
    ])
    rows = ["Communal residence", "Titled township", "Middle suburb", "High property", "Productive farm"]
    fig = new_figure(
        "'Property' is not one economic instrument",
        "Illustrative institutional capacity scores from the model assumptions; not measured group averages.",
        "GREYSCIENX / PROPERTY BUNDLE",
        5.1,
    )
    ax = fig.add_axes([0.22, 0.16, 0.72, 0.60])
    cmap = plt.matplotlib.colors.LinearSegmentedColormap.from_list("greycoral", [TOKENS["grey-100"], TOKENS["coral"], TOKENS["black"]])
    im = ax.imshow(data, cmap=cmap, vmin=0, vmax=1, aspect="auto")
    ax.set_xticks(np.arange(len(labels)), labels, rotation=28, ha="right")
    ax.set_yticks(np.arange(len(rows)), rows)
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            ax.text(j, i, f"{data[i, j]:.2f}", ha="center", va="center", fontsize=7.2, color="white" if data[i, j] > 0.55 else TOKENS["black"], fontweight="bold")
    ax.tick_params(length=0)
    ax.spines[:].set_visible(False)
    cax = fig.add_axes([0.22, 0.08, 0.50, 0.025])
    cb = fig.colorbar(im, cax=cax, orientation="horizontal")
    cb.set_label("Relative channel capacity in scenario design", fontsize=7.2)
    cb.ax.tick_params(labelsize=6.8, length=0)
    save(fig, "property-bundle-heatmap.png")


def figure_matched_fans(direct: dict[str, dict[str, np.ndarray]]):
    fig = new_figure(
        "The same descendant can finish with very different wealth",
        "Matched earnings, education, household size and saving. Marketable net worth in constant 2024 rand.",
        "GREYSCIENX / MATCHED DESCENDANTS",
        5.4,
    )
    ax = fig.add_axes([0.11, 0.18, 0.83, 0.58])
    styles = [
        ("none", TOKENS["grey-500"], ":", "o"),
        ("communal", TOKENS["grey-700"], "--", "s"),
        ("township", TOKENS["coral"], "-", "o"),
        ("middle_suburb", TOKENS["black"], "-", "s"),
        ("high_property", TOKENS["black"], "--", "D"),
        ("farm", TOKENS["coral"], ":", "D"),
    ]
    for key, color, ls, marker in styles:
        meds = np.array([np.median(direct[key][f"total_{y}"]) for y in YEARS]) / 1e6
        lo = np.array([np.percentile(direct[key][f"total_{y}"], 25) for y in YEARS]) / 1e6
        hi = np.array([np.percentile(direct[key][f"total_{y}"], 75) for y in YEARS]) / 1e6
        ax.plot(YEARS, meds, color=color, ls=ls, marker=marker, lw=1.7, ms=4.5, label=PROFILES[key].short)
        ax.fill_between(YEARS, lo, hi, color=color, alpha=0.08)
    style_axis(ax, TOKENS)
    ax.set_xlabel("Years since inheritance")
    ax.set_ylabel("Marketable net worth (R million, 2024 prices)")
    ax.set_xlim(18, 62)
    ax.legend(frameon=False, ncol=2, fontsize=7.2, loc="upper left")
    save(fig, "matched-descendant-trajectories.png")


def figure_overlap(direct: dict[str, dict[str, np.ndarray]]):
    fig = new_figure(
        "The distributions overlap; property type does not determine destiny",
        "Forty-year marketable net worth. Violin width shows density; white dot is the median.",
        "GREYSCIENX / WITHIN-SCENARIO HETEROGENEITY",
        5.2,
    )
    ax = fig.add_axes([0.12, 0.19, 0.82, 0.56])
    keys = list(PROFILES)
    vals = [np.clip(direct[k]["total_40"] / 1e6, 0, 30) for k in keys]
    parts = ax.violinplot(vals, showmeans=False, showmedians=False, showextrema=False, widths=0.78)
    for i, body in enumerate(parts["bodies"]):
        body.set_facecolor(TOKENS["coral"] if i in (2, 5) else TOKENS["black"])
        body.set_edgecolor("none")
        body.set_alpha(0.72 if i != 0 else 0.40)
    meds = [np.median(v) for v in vals]
    q25 = [np.percentile(v, 25) for v in vals]
    q75 = [np.percentile(v, 75) for v in vals]
    x = np.arange(1, len(keys) + 1)
    ax.vlines(x, q25, q75, color="white", lw=3)
    ax.scatter(x, meds, color="white", edgecolor=TOKENS["black"], s=22, zorder=3)
    ax.set_xticks(x, [PROFILES[k].short.replace(" ", "\n") for k in keys])
    ax.set_ylabel("Marketable net worth after 40 years (R million)")
    style_axis(ax, TOKENS)
    save(fig, "distribution-overlap-40-years.png")


def figure_decomposition(results: dict):
    keys = ["communal", "township", "middle_suburb", "high_property", "farm"]
    components = [
        ("Marketable property equity", "marketable_property_equity", TOKENS["black"]),
        ("Housing savings", "reinvested_housing_savings", TOKENS["coral"]),
        ("Rental income", "reinvested_rental_income", TOKENS["grey-500"]),
        ("Farm income", "reinvested_farm_income", TOKENS["grey-300"]),
    ]
    fig = new_figure(
        "Market value is only one part of the inheritance dividend",
        "Mean incremental value at 40 years; same earnings-and-saving baseline removed.",
        "GREYSCIENX / CHANNEL DECOMPOSITION",
        5.2,
    )
    ax = fig.add_axes([0.12, 0.19, 0.82, 0.56])
    x = np.arange(len(keys))
    bottom = np.zeros(len(keys))
    for label, field, color in components:
        values = np.array([results[k]["decomposition_40_means"][field] for k in keys]) / 1e6
        ax.bar(x, values, bottom=bottom, color=color, label=label)
        bottom += values
    ax.set_xticks(x, [PROFILES[k].short.replace(" ", "\n") for k in keys])
    ax.set_ylabel("Median incremental wealth (R million, 2024 prices)")
    style_axis(ax, TOKENS)
    ax.legend(frameon=False, fontsize=7.0, ncol=2, loc="upper left")
    save(fig, "channel-decomposition-40-years.png")


def figure_group_intake(raw: dict[str, np.ndarray]):
    fig = new_figure(
        "Group-conditioned scenarios still contain wide overlap",
        "Synthetic liquid-equivalent inheritance distributions; zeros included. These are not observed group means.",
        "GREYSCIENX / EVIDENCE-CONSTRAINED SCENARIO",
        5.2,
    )
    ax = fig.add_axes([0.12, 0.19, 0.82, 0.56])
    groups = list(raw)
    xs = np.linspace(0, 4.0, 220)
    bins = np.linspace(0, 4.0, 180)
    for i, group in enumerate(groups):
        positive = raw[group][raw[group] > 0] / 1e6
        positive = positive[positive < 4.0]
        hist, edges = np.histogram(positive, bins=bins, density=True)
        centres = (edges[:-1] + edges[1:]) / 2
        kernel = np.ones(7) / 7
        smooth = np.convolve(hist, kernel, mode="same")
        color = [TOKENS["coral"], TOKENS["grey-500"], TOKENS["grey-700"], TOKENS["black"]][i]
        ls = ["-", "--", ":", "-"][i]
        ax.plot(centres, smooth, color=color, ls=ls, lw=1.8, label=group)
    style_axis(ax, TOKENS)
    ax.set_xlabel("Liquid-equivalent inheritance among modeled receivers (R million)")
    ax.set_ylabel("Density")
    ax.set_xlim(0, 4)
    ax.legend(frameon=False, fontsize=7.2)
    save(fig, "synthetic-group-intake-overlap.png")


def figure_agriculture(raw: dict[str, dict[str, np.ndarray]]):
    fig = new_figure(
        "The same hectares can transfer different economic capacity",
        "Identical R2.5m starting land value; twenty-year medians and interquartile ranges, constant 2024 rand.",
        "GREYSCIENX / AGRICULTURAL PROPERTY MODULE",
        5.3,
    )
    ax = fig.add_axes([0.13, 0.22, 0.80, 0.54])
    labels = list(raw)
    x = np.arange(len(labels))
    for offset, field, name, color in [(-0.16, "marketable", "Marketable value + reinvested income", TOKENS["coral"]), (0.16, "resource", "Broader resource value + reinvested income", TOKENS["black"])]:
        meds = np.array([np.median(raw[k][field]) for k in labels]) / 1e6
        q25 = np.array([np.percentile(raw[k][field], 25) for k in labels]) / 1e6
        q75 = np.array([np.percentile(raw[k][field], 75) for k in labels]) / 1e6
        ax.bar(x + offset, meds, width=0.30, color=color, label=name)
        ax.errorbar(x + offset, meds, yerr=[meds - q25, q75 - meds], fmt="none", ecolor=TOKENS["grey-700"], lw=1.0, capsize=2)
    ax.set_xticks(x, [s.replace(" / ", "\n") for s in labels])
    ax.set_ylabel("Value after 20 years (R million)")
    style_axis(ax, TOKENS)
    ax.legend(frameon=False, fontsize=7.0, loc="upper left")
    save(fig, "agricultural-module.png")


def figure_sensitivity():
    # One-at-a-time central effects for a R1.5m inherited home after 40 years.
    base = 1_500_000 * (1.015 ** 40)
    factors = [
        ("Real appreciation", 1_500_000 * (1.032 ** 40) - base, 1_500_000 * (1.000 ** 40) - base),
        ("Marketability", base * (0.98 - 0.91), base * (0.78 - 0.91)),
        ("Number of heirs", base / 1 - base / 2, base / 4 - base / 2),
        ("Net housing yield", annuity_future_value(np.array([1_500_000 * 0.04]), np.array([FIN_RETURN]), 40)[0] - annuity_future_value(np.array([1_500_000 * 0.028]), np.array([FIN_RETURN]), 40)[0], annuity_future_value(np.array([1_500_000 * 0.012]), np.array([FIN_RETURN]), 40)[0] - annuity_future_value(np.array([1_500_000 * 0.028]), np.array([FIN_RETURN]), 40)[0]),
        ("Administration haircut", base * (1.0 - 0.975), base * (0.88 - 0.975)),
    ]
    labels = [x[0] for x in factors][::-1]
    high = np.array([x[1] for x in factors][::-1]) / 1e6
    low = np.array([x[2] for x in factors][::-1]) / 1e6
    y = np.arange(len(labels))
    fig = new_figure(
        "Appreciation and heir division drive the widest sensitivity",
        "One-at-a-time change from a middle-suburb central case at 40 years; illustrative, not a forecast interval.",
        "GREYSCIENX / SENSITIVITY",
        5.0,
    )
    ax = fig.add_axes([0.23, 0.18, 0.69, 0.56])
    ax.barh(y, high, color=TOKENS["coral"], label="Favourable bound")
    ax.barh(y, low, color=TOKENS["grey-500"], label="Adverse bound")
    ax.axvline(0, color=TOKENS["black"], lw=0.8)
    ax.set_yticks(y, labels)
    ax.set_xlabel("Change in 40-year value (R million)")
    style_axis(ax, TOKENS)
    ax.legend(frameon=False, fontsize=7.2, loc="lower right")
    save(fig, "sensitivity-tornado.png")


def write_parameters():
    rows = []
    for key, p in PROFILES.items():
        d = asdict(p)
        for field, value in d.items():
            if field in {"label", "short"}:
                continue
            rows.append({"module": "matched_descendant", "profile": key, "parameter": field, "value": json.dumps(value), "status": "scenario range"})
    for group, cfg in GROUP_PROFILES.items():
        rows.append({"module": "group_intake", "profile": group, "parameter": "p_any", "value": json.dumps(cfg["p_any"]), "status": "scenario bracket around probate evidence"})
        rows.append({"module": "group_intake", "profile": group, "parameter": "type_weights", "value": json.dumps(cfg["weights"]), "status": "synthetic location/type mixture"})
    with (ROOT / "parameters.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["module", "profile", "parameter", "value", "status"])
        writer.writeheader()
        writer.writerows(rows)


def main():
    FIGURES.mkdir(parents=True, exist_ok=True)
    matched, direct, extended = matched_results()
    group_results, group_raw = group_intake_results()
    agri_results, agri_raw = agricultural_results()
    results = {
        "model_identity": {
            "seed": SEED,
            "draws_per_scenario": N,
            "currency": "constant 2024 South African rand",
            "horizons_years": YEARS.tolist(),
            "matched_salary": BASE_SALARY,
            "matched_saving_rate": BASE_SAVING_RATE,
            "financial_return_real": FIN_RETURN,
            "interpretation": "scenario model, not forecast or causal estimate",
        },
        "matched_descendants": matched,
        "synthetic_group_intake": group_results,
        "agricultural_module": agri_results,
    }
    (ROOT / "model_results.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    write_parameters()
    figure_evidence_threshold()
    figure_property_bundle()
    figure_matched_fans(direct)
    figure_overlap(direct)
    figure_decomposition(matched)
    figure_group_intake(group_raw)
    figure_agriculture(agri_raw)
    figure_sensitivity()
    print(json.dumps({
        "matched_40y_medians": {k: round(v["horizons"]["40"]["marketable_net_worth"]["median"]) for k, v in matched.items()},
        "group_modeled_any": {k: round(v["modeled_any_property_probability"], 3) for k, v in group_results.items()},
        "agri_20y_market_medians": {k: round(v["marketable_value_20"]["median"]) for k, v in agri_results.items()},
    }, indent=2))


if __name__ == "__main__":
    main()
