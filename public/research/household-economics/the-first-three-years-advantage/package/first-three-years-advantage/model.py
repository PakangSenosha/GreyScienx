"""Reproducible lifetime counterfactual for The First Three Years Advantage.

All monetary results are constant 2026 rand. The model is deliberately deterministic:
it isolates the effect of the first 36 months rather than pretending to forecast a life.
Run from the paper directory with `python model.py`.
"""

from __future__ import annotations

import csv
import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "figures"
RESULTS = ROOT / "results"
INPUTS = json.loads((ROOT / "inputs.json").read_text(encoding="utf-8"))

import sys

SKILL_SCRIPTS = Path(r"C:\Users\Deriv\Documents\ChatGPT\GreySciencx\.agents\skills\greyscienx-editorial-pdf\scripts")
sys.path.insert(0, str(SKILL_SCRIPTS))
from greyscienx_style import (  # noqa: E402
    add_figure_header,
    configure_matplotlib,
    load_tokens,
    save_figure,
    style_axis,
)

CSS_PATH = ROOT.parents[2] / "app" / "globals.css"
TOKENS = configure_matplotlib(CSS_PATH)

ILL = INPUTS["illustrative_scenarios"]
SRC = INPUTS["sourced_inputs"]
START_AGE = INPUTS["metadata"]["start_age"]
TRANSITION_AGE = INPUTS["metadata"]["transition_age"]
TARGET_AGES = (30, 40, 60)


@dataclass(frozen=True)
class Strategy:
    name: str
    move_year: int
    car_year: int


STRATEGIES = (
    Strategy("Immediate independence", 0, 0),
    Strategy("One-year delay", 1, 1),
    Strategy("Two-year delay", 2, 2),
    Strategy("Three-year delay", 3, 3),
    Strategy("Home plus earlier car", 3, 1),
    Strategy("Home plus delayed car", 3, 3),
)


def tax_annual(gross: float) -> float:
    tax = SRC["tax_2026_27"]
    brackets = tax["brackets"]
    bases = tax["base_tax"]
    rates = tax["rates"]
    if gross <= brackets[0]:
        raw = gross * rates[0]
    else:
        raw = 0.0
        lower = 0.0
        limits = brackets + [float("inf")]
        for i, upper in enumerate(limits):
            if gross <= upper:
                raw = bases[i] + (gross - lower) * rates[i]
                break
            lower = upper
    return max(0.0, raw - tax["primary_rebate"])


def monthly_takehome(annual_salary: float) -> float:
    uif = min(annual_salary / 12 * ILL["uif_rate"], ILL["uif_monthly_cap"])
    return annual_salary / 12 - tax_annual(annual_salary) / 12 - uif


def annuity_payment(principal: float, annual_rate: float, months: int) -> float:
    r = annual_rate / 12
    return principal * r / (1 - (1 + r) ** -months)


def remaining_loan(principal: float, annual_rate: float, months: int, paid: int) -> float:
    if paid <= 0:
        return principal
    if paid >= months:
        return 0.0
    r = annual_rate / 12
    payment = annuity_payment(principal, annual_rate, months)
    return principal * (1 + r) ** paid - payment * ((1 + r) ** paid - 1) / r


def vehicle_value(price: float, age_months: int) -> float:
    years = age_months / 12
    if years <= 1:
        return price * (1 - ILL["transport"]["depreciation_first_year"] * years)
    return price * (1 - ILL["transport"]["depreciation_first_year"]) * (
        1 - ILL["transport"]["depreciation_later"]
    ) ** (years - 1)


def monthly_transport_km(extra_km: float = 0.0, office_days: float | None = None) -> float:
    t = ILL["transport"]
    days = t["office_days_monthly"] if office_days is None else office_days
    return 2 * t["commute_one_way_km"] * days + t["personal_km_monthly"] + extra_km


def hybrid_monthly_cost(km: float, ridehail_rate: float | None = None) -> float:
    t = ILL["transport"]
    rate = t["ridehail_per_km"] if ridehail_rate is None else ridehail_rate
    return (
        t["public_pass_monthly"]
        + km * t["ridehail_share_of_km"] * rate
        + t["family_vehicle_contribution"]
    )


def car_monthly_cost(km: float) -> float:
    t = ILL["transport"]
    principal = t["vehicle_price"] * (1 - t["deposit_share"])
    return (
        annuity_payment(principal, t["finance_nominal_rate"], t["finance_term_months"])
        + t["insurance_monthly"]
        + t["parking_and_licence_monthly"]
        + km * (t["fuel_per_km"] + t["maintenance_per_km"])
    )


def family_contribution(takehome: float, override: float | None = None) -> float:
    if override is not None:
        return override
    h = ILL["home"]
    return min(h["maximum_household_contribution"], max(h["minimum_household_contribution"], takehome * h["share_of_take_home"]))


def first_three_years(
    strategy: Strategy,
    annual_salary: float,
    city_name: str,
    *,
    family_contribution_override: float | None = None,
    extra_home_commute_km: float = 0.0,
    independence_income_uplift: float = 0.0,
    real_return: float | None = None,
) -> dict[str, Any]:
    city = ILL["city"][city_name]
    t = ILL["transport"]
    move_month = strategy.move_year * 12
    car_month = strategy.car_year * 12
    return_rate = ILL["real_investment_return"] if real_return is None else real_return
    positive_rate_m = (1 + return_rate) ** (1 / 12) - 1
    debt_rate_m = (1 + ILL["real_debt_rate"]) ** (1 / 12) - 1
    financial = 0.0
    rental_deposit = 0.0
    vehicle_purchase_month: int | None = None
    total_income = 0.0
    total_living = 0.0
    total_transport = 0.0
    total_transition = 0.0
    monthly_rows: list[dict[str, float]] = []

    for month in range(37):
        if month == move_month:
            rental_deposit = city["rent"] * ILL["moving"]["rental_deposit_months"]
            outlay = rental_deposit + ILL["moving"]["setup_furniture_and_move"]
            financial -= outlay
            total_transition += outlay
        if month == car_month:
            vehicle_purchase_month = month
            outlay = t["vehicle_price"] * t["deposit_share"] + t["initiation_fee"]
            financial -= outlay
            total_transition += outlay
        if month == 36:
            break

        salary = annual_salary * (1 + ILL["salary_real_growth_first_8_years"]) ** (month / 12)
        if month >= move_month:
            salary *= 1 + independence_income_uplift
        takehome = monthly_takehome(salary)
        total_income += takehome
        personal = ILL["personal_base_monthly"] + takehome * ILL["personal_takehome_share"]

        at_home = month < move_month
        if at_home:
            living = family_contribution(takehome, family_contribution_override) + ILL["home"]["personal_food_and_services"] + personal
        else:
            living = city["rent"] + city["utilities"] + city["groceries"] + city["household_goods"] + personal
        total_living += living

        owns_car = month >= car_month
        km = monthly_transport_km(extra_home_commute_km if at_home else 0.0)
        transport = car_monthly_cost(km) if owns_car else hybrid_monthly_cost(km)
        total_transport += transport
        net = takehome - living - transport
        financial = financial * (1 + (positive_rate_m if financial >= 0 else debt_rate_m)) + net
        monthly_rows.append({
            "month": month,
            "age": START_AGE + month / 12,
            "salary_annual": salary,
            "takehome": takehome,
            "living": living,
            "transport": transport,
            "net": net,
            "financial_balance": financial,
        })

    vehicle_equity = 0.0
    vehicle_value_now = 0.0
    vehicle_loan = 0.0
    if vehicle_purchase_month is not None:
        age_months = 36 - vehicle_purchase_month
        principal = t["vehicle_price"] * (1 - t["deposit_share"])
        vehicle_value_now = vehicle_value(t["vehicle_price"], age_months)
        vehicle_loan = remaining_loan(principal, t["finance_nominal_rate"], t["finance_term_months"], age_months)
        vehicle_equity = vehicle_value_now - vehicle_loan

    terminal_capital = financial + rental_deposit + vehicle_equity
    return {
        "strategy": strategy.name,
        "move_year": strategy.move_year,
        "car_year": strategy.car_year,
        "salary": annual_salary,
        "city": city_name,
        "terminal_capital_age25": terminal_capital,
        "financial_balance_age25": financial,
        "rental_deposit_age25": rental_deposit,
        "vehicle_equity_age25": vehicle_equity,
        "vehicle_value_age25": vehicle_value_now,
        "vehicle_loan_age25": vehicle_loan,
        "total_takehome_3y": total_income,
        "total_living_3y": total_living,
        "total_transport_3y": total_transport,
        "total_transition_outlays": total_transition,
        "monthly": monthly_rows,
    }


def future_value(balance: float, annual_contribution: float, years: int, real_return: float) -> float:
    if years == 0:
        return balance
    factor = (1 + real_return) ** years
    annuity = annual_contribution * ((factor - 1) / real_return) if real_return else annual_contribution * years
    return balance * factor + annuity


def lifetime_wealth(terminal_capital: float, annual_salary: float, target_age: int, real_return: float | None = None) -> float:
    rr = ILL["real_investment_return"] if real_return is None else real_return
    years = target_age - TRANSITION_AGE
    salary_25 = annual_salary * (1 + ILL["salary_real_growth_first_8_years"]) ** 3
    balance = terminal_capital
    for year in range(years):
        salary = salary_25 * (1 + ILL["salary_real_growth_later"]) ** year
        balance = balance * (1 + rr) + salary * ILL["retirement_saving_rate_from_25"]
    return balance


def run_matrix() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for salary_name, salary in ILL["salary"].items():
        for city in ILL["city"]:
            for strategy in STRATEGIES:
                result = first_three_years(strategy, salary, city)
                row = {k: v for k, v in result.items() if k != "monthly"}
                row["salary_scenario"] = salary_name
                for age in TARGET_AGES:
                    row[f"wealth_age_{age}"] = lifetime_wealth(result["terminal_capital_age25"], salary, age)
                rows.append(row)
    return rows


def threshold_bisect(function, lo: float, hi: float, target: float = 0.0, iterations: int = 80) -> float:
    flo = function(lo) - target
    fhi = function(hi) - target
    if flo == 0:
        return lo
    if fhi == 0:
        return hi
    if flo * fhi > 0:
        return float("nan")
    for _ in range(iterations):
        mid = (lo + hi) / 2
        fm = function(mid) - target
        if flo * fm <= 0:
            hi, fhi = mid, fm
        else:
            lo, flo = mid, fm
    return (lo + hi) / 2


def break_even_results() -> dict[str, float]:
    salary = ILL["salary"]["middle"]
    city = "Johannesburg"
    immediate = STRATEGIES[0]
    home_only = Strategy("Home three years, car now", 3, 0)
    car_later = Strategy("Independent, car in year three", 0, 3)
    base_immediate = first_three_years(immediate, salary, city)["terminal_capital_age25"]

    contrib = threshold_bisect(
        lambda x: first_three_years(home_only, salary, city, family_contribution_override=x)["terminal_capital_age25"],
        0,
        25000,
        base_immediate,
    )
    income_uplift = threshold_bisect(
        lambda x: first_three_years(immediate, salary, city, independence_income_uplift=x)["terminal_capital_age25"],
        0,
        1.0,
        first_three_years(home_only, salary, city)["terminal_capital_age25"],
    )
    extra_commute = threshold_bisect(
        lambda x: first_three_years(home_only, salary, city, extra_home_commute_km=x)["terminal_capital_age25"],
        0,
        15000,
        base_immediate,
    )

    t = ILL["transport"]
    fixed_car = car_monthly_cost(0)
    car_variable = t["fuel_per_km"] + t["maintenance_per_km"]
    hybrid_fixed = t["public_pass_monthly"] + t["family_vehicle_contribution"]
    hybrid_variable = t["ridehail_share_of_km"] * t["ridehail_per_km"]
    km_break_even = (fixed_car - hybrid_fixed) / (hybrid_variable - car_variable)
    hybrid_variable_surge = t["ridehail_share_of_km"] * t["ridehail_per_km"] * 1.25
    km_break_even_surge = (fixed_car - hybrid_fixed) / (hybrid_variable_surge - car_variable)

    home_capital = first_three_years(home_only, salary, city)["terminal_capital_age25"]
    immediate_capital = base_immediate
    independence_value_monthly = (home_capital - immediate_capital) / 36

    # Salary at which the age-60 difference is only 5% of immediate-case wealth.
    def relative_penalty(gross: float) -> float:
        early = first_three_years(home_only, gross, city)["terminal_capital_age25"]
        now = first_three_years(immediate, gross, city)["terminal_capital_age25"]
        w_early = lifetime_wealth(early, gross, 60)
        w_now = lifetime_wealth(now, gross, 60)
        return (w_early - w_now) / max(abs(w_now), 1)

    salary_5pct = threshold_bisect(relative_penalty, 240000, 3000000, 0.05)
    delayed_car_capital = first_three_years(car_later, salary, city)["terminal_capital_age25"]

    return {
        "household_contribution_monthly_break_even": contrib,
        "independence_income_uplift_break_even_share": income_uplift,
        "extra_home_transport_km_monthly_break_even": extra_commute,
        "transport_km_monthly_break_even": km_break_even,
        "transport_km_monthly_break_even_25pct_surge": km_break_even_surge,
        "independence_privacy_welfare_value_monthly_break_even": independence_value_monthly,
        "salary_where_three_year_home_advantage_is_5pct_of_age60_wealth": salary_5pct,
        "home_only_capital_advantage_age25": home_capital - immediate_capital,
        "car_delay_capital_advantage_age25": delayed_car_capital - immediate_capital,
    }


def property_use_value(capital: float, city_name: str) -> float:
    """Age-60 net worth from using early capital for a home at age 25.

    The renter comparator's rent is netted against ownership cash costs, so this
    captures both home equity and the changed housing cash flow. It is still an
    illustrative path: transaction costs are 5%, the deposit is 10%, real property
    growth is 1.5%, and maintenance/levies are 1% of value plus R1,800 a month.
    """
    city = ILL["city"][city_name]
    price = city["property_price"]
    deposit = 0.10 * price
    transaction_cost = 0.05 * price
    if capital < deposit + transaction_cost:
        return capital * (1 + ILL["real_investment_return"]) ** (60 - TRANSITION_AGE)
    inflation = SRC["macro"]["inflation_target"]
    mortgage_nominal = SRC["macro"]["sarb_policy_rate_july_2026"] + SRC["macro"]["prime_spread"]
    mortgage_real = (1 + mortgage_nominal) / (1 + inflation) - 1
    principal = price - deposit
    payment = annuity_payment(principal, mortgage_real, 240)
    loan = principal
    investment = capital - deposit - transaction_cost
    property_value = price
    invest_m = (1 + ILL["real_investment_return"]) ** (1 / 12) - 1
    debt_m = (1 + ILL["real_debt_rate"]) ** (1 / 12) - 1
    property_m = (1.015) ** (1 / 12) - 1
    mortgage_m = mortgage_real / 12
    for month in range((60 - TRANSITION_AGE) * 12):
        property_value *= 1 + property_m
        maintenance_and_levies = property_value * 0.01 / 12 + 1800
        if month < 240:
            interest = loan * mortgage_m
            principal_paid = max(0.0, payment - interest)
            loan = max(0.0, loan - principal_paid)
            owner_cost = payment + maintenance_and_levies
        else:
            owner_cost = maintenance_and_levies
        investment = investment * (1 + (invest_m if investment >= 0 else debt_m)) + city["rent"] - owner_cost
    return investment + property_value - loan


def alternative_uses(capital_advantage: float, annual_salary: float, city_name: str = "Johannesburg") -> list[dict[str, float | str]]:
    rr = ILL["real_investment_return"]
    years = 60 - TRANSITION_AGE
    invest_value = capital_advantage * (1 + rr) ** years

    # Debt is repaid first; avoided real interest over five years is then invested.
    debt = min(capital_advantage, ILL["debt_and_liquidity"]["debt_balance"])
    debt_benefit_age30 = debt * (1 + ILL["real_debt_rate"]) ** 5
    debt_remainder = max(0.0, capital_advantage - debt)
    debt_value = (debt_benefit_age30 + debt_remainder * (1 + rr) ** 5) * (1 + rr) ** 30

    reserve = min(capital_advantage, ILL["debt_and_liquidity"]["emergency_reserve"])
    liquidity_value = reserve * (1 + ILL["real_cash_return"]) ** years + max(0.0, capital_advantage - reserve) * (1 + rr) ** years

    training = ILL["training"]
    training_spend = min(capital_advantage, training["cost"])
    salary_25 = annual_salary * (1 + ILL["salary_real_growth_first_8_years"]) ** 3
    premium_flows = sum(
        salary_25
        * (1 + ILL["salary_real_growth_later"]) ** y
        * training["salary_premium"]
        * training["net_share_of_gross_premium"]
        * (1 + rr) ** (training["premium_years"] - 1 - y)
        for y in range(training["premium_years"])
    )
    training_value = (
        premium_flows + max(0.0, capital_advantage - training_spend) * (1 + rr) ** training["premium_years"]
    ) * (1 + rr) ** (years - training["premium_years"])

    t = ILL["transport"]
    cash_vehicle = min(capital_advantage, t["vehicle_price"])
    loan_rate_real = (1 + t["finance_nominal_rate"]) / (1 + SRC["macro"]["inflation_target"]) - 1
    finance_avoided_age30 = cash_vehicle * (1 + loan_rate_real) ** 5
    vehicle_value = finance_avoided_age30 * (1 + rr) ** 30 + max(0.0, capital_advantage - cash_vehicle) * (1 + rr) ** years

    housing_value = property_use_value(capital_advantage, city_name)

    return [
        {"use": "Diversified investment", "value_age60": invest_value, "capital_used": capital_advantage},
        {"use": "Debt repayment first", "value_age60": debt_value, "capital_used": capital_advantage},
        {"use": "Emergency liquidity first", "value_age60": liquidity_value, "capital_used": capital_advantage},
        {"use": "Illustrative training", "value_age60": training_value, "capital_used": capital_advantage},
        {"use": "Cash vehicle / finance avoided", "value_age60": vehicle_value, "capital_used": capital_advantage},
        {"use": "Housing deposit and home equity", "value_age60": housing_value, "capital_used": capital_advantage},
    ]


def stress_tests() -> list[dict[str, Any]]:
    salary = ILL["salary"]["middle"]
    city = "Johannesburg"
    immediate = STRATEGIES[0]
    delayed = STRATEGIES[3]
    rows: list[dict[str, Any]] = []

    def add(group: str, case: str, value: float, unit: str, advantage: float) -> None:
        rows.append({"group": group, "case": case, "input_value": value, "unit": unit, "age25_advantage": advantage, "age60_advantage": advantage * (1 + ILL["real_investment_return"]) ** 35})

    for multiplier, label in ((0.70, "Shared / cheaper rent"), (1.00, "Central rent"), (1.30, "High rent")):
        original = ILL["city"][city]["rent"]
        ILL["city"][city]["rent"] = original * multiplier
        try:
            a = first_three_years(immediate, salary, city)["terminal_capital_age25"]
            d = first_three_years(delayed, salary, city)["terminal_capital_age25"]
            add("Rent", label, ILL["city"][city]["rent"], "R/month", d - a)
        finally:
            ILL["city"][city]["rent"] = original

    for contribution in (2500, 4500, 7500, 12000, 16000):
        home_only = Strategy("Home three years, car now", 3, 0)
        a = first_three_years(immediate, salary, city)["terminal_capital_age25"]
        h = first_three_years(home_only, salary, city, family_contribution_override=contribution)["terminal_capital_age25"]
        add("Household contribution", f"R{contribution:,.0f}", contribution, "R/month", h - a)

    for office_days in (8, 13, 20, 26):
        original = ILL["transport"]["office_days_monthly"]
        ILL["transport"]["office_days_monthly"] = office_days
        try:
            a = first_three_years(immediate, salary, city)["terminal_capital_age25"]
            d = first_three_years(delayed, salary, city)["terminal_capital_age25"]
            add("Office frequency", f"{office_days} office days", office_days, "days/month", d - a)
        finally:
            ILL["transport"]["office_days_monthly"] = original

    for price in (160000, 230000, 350000):
        original = ILL["transport"]["vehicle_price"]
        ILL["transport"]["vehicle_price"] = price
        try:
            a = first_three_years(immediate, salary, city)["terminal_capital_age25"]
            d = first_three_years(delayed, salary, city)["terminal_capital_age25"]
            add("Vehicle price", f"R{price/1000:.0f}k vehicle", price, "R", d - a)
        finally:
            ILL["transport"]["vehicle_price"] = original

    central_a = first_three_years(immediate, salary, city)["terminal_capital_age25"]
    central_d = first_three_years(delayed, salary, city)["terminal_capital_age25"]
    capital = central_d - central_a
    for price in (1000000, 1400000, 1800000):
        original = ILL["city"][city]["property_price"]
        ILL["city"][city]["property_price"] = price
        try:
            value = property_use_value(capital, city)
            rows.append({"group": "Property price", "case": f"R{price/1e6:.1f}m home", "input_value": price, "unit": "R", "age25_advantage": capital, "age60_advantage": value})
        finally:
            ILL["city"][city]["property_price"] = original
    return rows


def save_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    keys = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=keys)
        writer.writeheader()
        writer.writerows(rows)


def new_figure(title: str, subtitle: str, field: str, height: float = 4.8):
    fig = plt.figure(figsize=(7.2, height))
    add_figure_header(fig, title, subtitle, field=field, tokens=TOKENS)
    return fig


def fig_strategy_wealth(matrix: list[dict[str, Any]]) -> None:
    rows = [r for r in matrix if r["salary_scenario"] == "middle" and r["city"] == "Johannesburg"]
    fig = new_figure(
        "Three years creates a gap that compounding preserves",
        "Middle-salary Johannesburg scenario; total modeled financial wealth in constant 2026 rand.",
        "GREYSCIENX / CENTRAL SCENARIO",
        5.2,
    )
    ax = fig.add_axes([0.12, 0.18, 0.82, 0.56])
    selected = [rows[0], rows[1], rows[2], rows[3]]
    enc = [
        (TOKENS["black"], "--", "s"),
        (TOKENS["grey-500"], ":", "D"),
        (TOKENS["black"], "-.", "^"),
        (TOKENS["coral"], "-", "o"),
    ]
    for row, (colour, line, marker) in zip(selected, enc):
        y = [row[f"wealth_age_{age}"] / 1e6 for age in TARGET_AGES]
        ax.plot(TARGET_AGES, y, label=row["strategy"], color=colour, linestyle=line, marker=marker, linewidth=2)
        ax.text(60.5, y[-1], f"R{y[-1]:.1f}m", color=colour, fontsize=7.5, va="center", fontweight="bold")
    style_axis(ax, TOKENS)
    ax.set_xlabel("Age")
    ax.set_ylabel("Modeled financial wealth (R million, 2026 prices)")
    ax.set_xlim(29, 64)
    ax.legend(loc="upper left", frameon=False, fontsize=7.3)
    save_figure(fig, ASSETS / "strategy-wealth.png", dpi=260)
    plt.close(fig)


def fig_age25_capital(matrix: list[dict[str, Any]]) -> None:
    rows = [r for r in matrix if r["salary_scenario"] == "middle" and r["city"] == "Johannesburg"]
    fig = new_figure(
        "Housing delay dominates the central case",
        "Net strategy-created capital at age 25, after moving and vehicle purchase transitions.",
        "GREYSCIENX / FIRST 36 MONTHS",
        5.0,
    )
    ax = fig.add_axes([0.32, 0.16, 0.62, 0.59])
    labels = [r["strategy"] for r in rows]
    values = [r["terminal_capital_age25"] / 1000 for r in rows]
    order = np.arange(len(rows))[::-1]
    colours = [TOKENS["coral"] if "Three" in label or "delayed" in label else TOKENS["grey-500"] for label in labels]
    ax.barh(order, values[::-1], color=colours[::-1], height=0.62)
    ax.set_yticks(order, labels[::-1], fontsize=7.3)
    for y, value in zip(order, values[::-1]):
        if value >= 0:
            ax.text(value + 5, y, f"R{value:,.0f}k", ha="left", va="center", fontsize=7.3, fontweight="bold")
        else:
            ax.text(value / 2, y, f"-R{abs(value):,.0f}k", ha="center", va="center", fontsize=7.0, fontweight="bold", color=TOKENS["white"])
    style_axis(ax, TOKENS)
    ax.axvline(0, color=TOKENS["black"], linewidth=0.8)
    ax.set_xlabel("Net capital at age 25 (R000, 2026 prices)")
    save_figure(fig, ASSETS / "age25-capital.png", dpi=260)
    plt.close(fig)


def fig_city_salary_heatmap(matrix: list[dict[str, Any]]) -> None:
    immediate = {(r["salary_scenario"], r["city"]): r for r in matrix if r["strategy"] == "Immediate independence"}
    delayed = {(r["salary_scenario"], r["city"]): r for r in matrix if r["strategy"] == "Three-year delay"}
    salaries = ["lower", "middle", "higher"]
    cities = ["Johannesburg", "Cape Town", "Durban"]
    data = np.array([
        [(delayed[(s, c)]["wealth_age_60"] - immediate[(s, c)]["wealth_age_60"]) / 1e6 for c in cities]
        for s in salaries
    ])
    fig = new_figure(
        "The advantage survives every salary-city combination tested",
        "Age-60 wealth difference: three-year combined delay minus immediate independence.",
        "GREYSCIENX / SENSITIVITY GRID",
        4.8,
    )
    ax = fig.add_axes([0.18, 0.18, 0.72, 0.54])
    im = ax.imshow(data, cmap="Greys", aspect="auto")
    ax.set_xticks(range(len(cities)), cities, fontsize=8)
    ax.set_yticks(range(len(salaries)), [s.title() + " salary" for s in salaries], fontsize=8)
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            ax.text(j, i, f"R{data[i, j]:.2f}m", ha="center", va="center", fontsize=9, fontweight="bold", color=TOKENS["coral"] if data[i, j] > np.median(data) else TOKENS["black"])
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(length=0)
    fig.colorbar(im, ax=ax, fraction=0.035, pad=0.04, label="R million")
    save_figure(fig, ASSETS / "city-salary-sensitivity.png", dpi=260)
    plt.close(fig)


def fig_transport_thresholds(thresholds: dict[str, float]) -> None:
    t = ILL["transport"]
    kms = np.linspace(0, 1800, 181)
    car = np.array([car_monthly_cost(k) for k in kms])
    hybrid = np.array([hybrid_monthly_cost(k) for k in kms])
    surge = np.array([hybrid_monthly_cost(k, t["ridehail_per_km"] * 1.25) for k in kms])
    fig = new_figure(
        "Distance determines whether car-later still works",
        "Monthly private cost; hybrid means a public-transport pass plus ride-hailing for 35% of kilometres.",
        "GREYSCIENX / TRANSPORT BREAK-EVEN",
        5.0,
    )
    ax = fig.add_axes([0.12, 0.17, 0.82, 0.58])
    ax.plot(kms, car / 1000, color=TOKENS["black"], linestyle="--", marker="s", markevery=30, label="Financed used car")
    ax.plot(kms, hybrid / 1000, color=TOKENS["coral"], linestyle="-", marker="o", markevery=30, label="Hybrid transport")
    ax.plot(kms, surge / 1000, color=TOKENS["grey-500"], linestyle=":", marker="D", markevery=30, label="Hybrid, 25% ride-hail surge")
    ax.axvline(thresholds["transport_km_monthly_break_even"], color=TOKENS["coral"], linewidth=1, alpha=0.7)
    ax.text(thresholds["transport_km_monthly_break_even"] + 20, 5.0, f"base break-even\n{thresholds['transport_km_monthly_break_even']:,.0f} km/month", fontsize=7.2, color=TOKENS["coral"])
    style_axis(ax, TOKENS)
    ax.set_xlabel("Total travel (km per month)")
    ax.set_ylabel("Private monthly transport cost (R000)")
    ax.set_xlim(0, 1800)
    ax.legend(loc="upper left", frameon=False, fontsize=7.3)
    save_figure(fig, ASSETS / "transport-break-even.png", dpi=260)
    plt.close(fig)


def fig_return_sensitivity(matrix: list[dict[str, Any]]) -> None:
    salary = ILL["salary"]["middle"]
    city = "Johannesburg"
    immediate = first_three_years(STRATEGIES[0], salary, city)["terminal_capital_age25"]
    delayed = first_three_years(STRATEGIES[3], salary, city)["terminal_capital_age25"]
    returns = np.linspace(0.01, 0.08, 15)
    diffs = [(lifetime_wealth(delayed, salary, 60, r) - lifetime_wealth(immediate, salary, 60, r)) / 1e6 for r in returns]
    fig = new_figure(
        "Returns amplify the gap; they do not create it",
        "Age-60 advantage of three-year combined delay, middle-salary Johannesburg scenario.",
        "GREYSCIENX / REAL-RETURN SENSITIVITY",
        4.8,
    )
    ax = fig.add_axes([0.12, 0.18, 0.82, 0.55])
    ax.plot(returns * 100, diffs, color=TOKENS["coral"], linestyle="-", marker="o", linewidth=2.2)
    for r in (0.03, 0.05, 0.07):
        value = np.interp(r, returns, diffs)
        ax.scatter([r * 100], [value], color=TOKENS["black"], marker="s", zorder=3)
        ax.text(r * 100 + 0.08, value, f"R{value:.2f}m", fontsize=7.2, va="bottom")
    style_axis(ax, TOKENS)
    ax.set_xlabel("Real annual investment return (%)")
    ax.set_ylabel("Age-60 wealth advantage (R million, 2026 prices)")
    save_figure(fig, ASSETS / "return-sensitivity.png", dpi=260)
    plt.close(fig)


def main() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    RESULTS.mkdir(parents=True, exist_ok=True)
    matrix = run_matrix()
    thresholds = break_even_results()
    central = [r for r in matrix if r["salary_scenario"] == "middle" and r["city"] == "Johannesburg"]
    immediate = next(r for r in central if r["strategy"] == "Immediate independence")
    delayed = next(r for r in central if r["strategy"] == "Three-year delay")
    advantage = delayed["terminal_capital_age25"] - immediate["terminal_capital_age25"]
    alternatives = alternative_uses(advantage, ILL["salary"]["middle"], "Johannesburg")
    stresses = stress_tests()

    save_csv(RESULTS / "scenario_matrix.csv", matrix)
    save_csv(RESULTS / "alternative_uses.csv", alternatives)
    save_csv(RESULTS / "stress_tests.csv", stresses)
    (RESULTS / "break_even_thresholds.json").write_text(json.dumps(thresholds, indent=2), encoding="utf-8")
    summary = {
        "central_scenario": central,
        "central_age25_advantage_three_year_delay": advantage,
        "break_even_thresholds": thresholds,
        "alternative_uses": alternatives,
        "stress_tests": stresses,
        "method": {
            "price_basis": "constant 2026 rand",
            "early_window_months": 36,
            "common_post_25_retirement_saving_rate": ILL["retirement_saving_rate_from_25"],
            "central_real_return": ILL["real_investment_return"],
            "interpretation": "deterministic counterfactual, not forecast or financial advice"
        },
    }
    (RESULTS / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    fig_strategy_wealth(matrix)
    fig_age25_capital(matrix)
    fig_city_salary_heatmap(matrix)
    fig_transport_thresholds(thresholds)
    fig_return_sensitivity(matrix)

    print(json.dumps({
        "central_age25_advantage": advantage,
        "central_age60_advantage": delayed["wealth_age_60"] - immediate["wealth_age_60"],
        "thresholds": thresholds,
        "rows": len(matrix),
    }, indent=2))


if __name__ == "__main__":
    main()
