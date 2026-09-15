from dataclasses import dataclass


@dataclass
class Scenario:
    name: str
    separate_expense: float
    cohabit_expense: float
    income_growth: float
    expense_growth: float
    investment_return: float
    debt_rate: float
    moving_cost: float
    retirement_expense_factor: float
    retirement_income_factor: float
    shocks: tuple
    emergencies: tuple


SCENARIOS = (
    Scenario(
        name="Favourable",
        separate_expense=44_800,
        cohabit_expense=34_800,
        income_growth=0.015,
        expense_growth=0.010,
        investment_return=0.050,
        debt_rate=0.070,
        moving_cost=20_000,
        retirement_expense_factor=0.70,
        retirement_income_factor=0.50,
        shocks=(),
        emergencies=(),
    ),
    Scenario(
        name="Average",
        separate_expense=44_800,
        cohabit_expense=36_300,
        income_growth=0.0075,
        expense_growth=0.0075,
        investment_return=0.030,
        debt_rate=0.080,
        moving_cost=30_000,
        retirement_expense_factor=0.80,
        retirement_income_factor=0.45,
        shocks=((30, 0, 6), (50, 1, 6)),
        emergencies=((50, 100_000),),
    ),
    Scenario(
        name="Adverse",
        separate_expense=47_000,
        cohabit_expense=42_500,
        income_growth=0.000,
        expense_growth=0.005,
        investment_return=0.010,
        debt_rate=0.080,
        moving_cost=50_000,
        retirement_expense_factor=0.90,
        retirement_income_factor=0.40,
        shocks=((28, 1, 12), (43, 0, 9), (58, 1, 9)),
        emergencies=((58, 250_000),),
    ),
)


def monthly_rate(annual):
    return (1.0 + annual) ** (1.0 / 12.0) - 1.0


def salary_loss_for_month(scenario, age_month, salaries):
    loss = 0.0
    for start_age, person_index, duration_months in scenario.shocks:
        start = (start_age - 25) * 12
        if start <= age_month < start + duration_months:
            loss += salaries[person_index]
    return loss


def simulate(scenario, move_age):
    wealth = 0.0
    move_month = (move_age - 25) * 12
    milestones = {25: 0.0}
    cumulative_expense = 0.0
    cumulative_income = 0.0
    cumulative_income_lost = 0.0
    cumulative_emergencies = 0.0
    cumulative_positive_saving = 0.0
    cumulative_negative_cashflow = 0.0
    inv_m = monthly_rate(scenario.investment_return)
    debt_m = monthly_rate(scenario.debt_rate)

    for month in range(50 * 12):
        age = 25 + month / 12.0
        years = month / 12.0
        salaries = [30_000 * (1 + scenario.income_growth) ** years,
                    20_000 * (1 + scenario.income_growth) ** years]

        if age < 65:
            income_before_shock = sum(salaries)
            income_loss = salary_loss_for_month(scenario, month, salaries)
            income = income_before_shock - income_loss
        else:
            final_salary = 50_000 * (1 + scenario.income_growth) ** 40
            income = final_salary * scenario.retirement_income_factor
            income_loss = 0.0

        if age < move_age:
            base_expense = scenario.separate_expense
        else:
            base_expense = scenario.cohabit_expense

        expense = base_expense * (1 + scenario.expense_growth) ** years
        if age >= 65:
            expense *= scenario.retirement_expense_factor

        one_off = 0.0
        if month == move_month:
            one_off += scenario.moving_cost
        for emergency_age, amount in scenario.emergencies:
            if month == (emergency_age - 25) * 12:
                one_off += amount
                cumulative_emergencies += amount

        growth_rate = inv_m if wealth >= 0 else debt_m
        wealth *= 1 + growth_rate
        net_flow = income - expense - one_off
        wealth += net_flow

        cumulative_income += income
        cumulative_income_lost += income_loss
        cumulative_expense += expense
        if net_flow >= 0:
            cumulative_positive_saving += net_flow
        else:
            cumulative_negative_cashflow += -net_flow

        end_age = 25 + (month + 1) / 12.0
        if end_age in (35, 45, 55, 65, 75):
            milestones[int(end_age)] = wealth

    return {
        "move_age": move_age,
        "wealth": wealth,
        "milestones": milestones,
        "expense": cumulative_expense,
        "income": cumulative_income,
        "income_lost": cumulative_income_lost,
        "emergencies": cumulative_emergencies,
        "positive_saving": cumulative_positive_saving,
        "negative_cashflow": cumulative_negative_cashflow,
    }


def rands(value):
    sign = "-" if value < 0 else ""
    return f"{sign}R{abs(value):,.0f}"


for scenario in SCENARIOS:
    early = simulate(scenario, 25)
    late = simulate(scenario, 35)
    print(f"\n{scenario.name}")
    print("age,early,late,gap")
    for age in (25, 35, 45, 55, 65, 75):
        e = early["milestones"][age]
        l = late["milestones"][age]
        print(f"{age},{rands(e)},{rands(l)},{rands(e-l)}")
    print(f"lifetime_expense_early={rands(early['expense'])}")
    print(f"lifetime_expense_late={rands(late['expense'])}")
    print(f"expense_saved={rands(late['expense']-early['expense'])}")
    print(f"income_received={rands(early['income'])}")
    print(f"income_lost={rands(early['income_lost'])}")
    print(f"emergencies={rands(early['emergencies'])}")
