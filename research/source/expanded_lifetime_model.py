from dataclasses import dataclass
from typing import Optional


@dataclass
class Scenario:
    name: str
    separate_expense: float
    separate_rent: float
    cohabit_expense: float
    cohabit_rent: float
    income_growth: float
    expense_growth: float
    gross_investment_return: float
    investment_fee_drag: float
    investment_tax_drag: float
    debt_rate: float
    moving_cost: float
    pension_rate: float
    child_monthly_cost: float
    family_remittance: float
    care_reduction: float
    care_start_age: int
    care_end_age: int
    property_price_40: float
    deposit_rate: float
    purchase_cost_rate: float
    mortgage_real_rate: float
    home_real_growth: float
    owner_cost_rate: float
    inheritance_age: Optional[int]
    inheritance_amount: float
    retirement_expense_factor: float
    income_shocks: tuple
    emergencies: tuple
    death_age: Optional[int]
    funeral_cost: float

    @property
    def net_investment_return(self):
        return self.gross_investment_return - self.investment_fee_drag - self.investment_tax_drag


SCENARIOS = (
    Scenario(
        name="Best case",
        separate_expense=44_800,
        separate_rent=19_000,
        cohabit_expense=34_800,
        cohabit_rent=12_000,
        income_growth=0.015,
        expense_growth=0.010,
        gross_investment_return=0.055,
        investment_fee_drag=0.005,
        investment_tax_drag=0.000,
        debt_rate=0.070,
        moving_cost=20_000,
        pension_rate=0.10,
        child_monthly_cost=3_500,
        family_remittance=500,
        care_reduction=0.00,
        care_start_age=36,
        care_end_age=36,
        property_price_40=1_800_000,
        deposit_rate=0.20,
        purchase_cost_rate=0.05,
        mortgage_real_rate=0.035,
        home_real_growth=0.015,
        owner_cost_rate=0.015,
        inheritance_age=55,
        inheritance_amount=500_000,
        retirement_expense_factor=0.70,
        income_shocks=(),
        emergencies=(),
        death_age=None,
        funeral_cost=0,
    ),
    Scenario(
        name="Average case",
        separate_expense=44_800,
        separate_rent=19_000,
        cohabit_expense=36_300,
        cohabit_rent=13_000,
        income_growth=0.0075,
        expense_growth=0.0075,
        gross_investment_return=0.045,
        investment_fee_drag=0.0075,
        investment_tax_drag=0.0075,
        debt_rate=0.080,
        moving_cost=30_000,
        pension_rate=0.08,
        child_monthly_cost=5_000,
        family_remittance=1_500,
        care_reduction=0.20,
        care_start_age=36,
        care_end_age=42,
        property_price_40=1_900_000,
        deposit_rate=0.20,
        purchase_cost_rate=0.06,
        mortgage_real_rate=0.045,
        home_real_growth=0.000,
        owner_cost_rate=0.018,
        inheritance_age=55,
        inheritance_amount=200_000,
        retirement_expense_factor=0.80,
        income_shocks=((30, 1, 6, 1.00), (50, 0, 12, 0.50)),
        emergencies=((50, 100_000),),
        death_age=None,
        funeral_cost=0,
    ),
    Scenario(
        name="Worst case",
        separate_expense=47_000,
        separate_rent=20_000,
        cohabit_expense=42_500,
        cohabit_rent=14_500,
        income_growth=0.000,
        expense_growth=0.005,
        gross_investment_return=0.025,
        investment_fee_drag=0.010,
        investment_tax_drag=0.005,
        debt_rate=0.030,
        moving_cost=50_000,
        pension_rate=0.04,
        child_monthly_cost=6_500,
        family_remittance=2_500,
        care_reduction=0.40,
        care_start_age=36,
        care_end_age=45,
        property_price_40=2_100_000,
        deposit_rate=0.20,
        purchase_cost_rate=0.08,
        mortgage_real_rate=0.065,
        home_real_growth=-0.010,
        owner_cost_rate=0.022,
        inheritance_age=None,
        inheritance_amount=0,
        retirement_expense_factor=0.90,
        income_shocks=((28, 1, 12, 1.00), (43, 0, 9, 1.00), (58, 1, 60, 0.50)),
        emergencies=((58, 250_000),),
        death_age=63,
        funeral_cost=100_000,
    ),
)


def monthly_rate(annual):
    return (1 + annual) ** (1 / 12) - 1


def mortgage_payment(principal, annual_real_rate, months):
    rate = monthly_rate(annual_real_rate)
    if rate == 0:
        return principal / months
    return principal * rate / (1 - (1 + rate) ** -months)


def simulate(scenario, move_age):
    liquid = 0.0
    pension = 0.0
    home_value = 0.0
    mortgage_balance = 0.0
    mortgage_payment_monthly = 0.0
    mortgage_months_left = 0
    homeowner = False
    purchase_age = None
    move_month = (move_age - 25) * 12
    net_investment_monthly = monthly_rate(scenario.net_investment_return)
    debt_monthly = monthly_rate(scenario.debt_rate)
    home_growth_monthly = monthly_rate(scenario.home_real_growth)
    mortgage_rate_monthly = monthly_rate(scenario.mortgage_real_rate)
    milestones = {25: 0.0}
    series = [(25.0, 0.0)]
    cumulative_living_expense = 0.0
    cumulative_child_cost = 0.0
    cumulative_remittance = 0.0
    cumulative_income_lost = 0.0
    cumulative_care_income_lost = 0.0
    cumulative_pension_contributions = 0.0
    cumulative_investment_drag = 0.0
    death_month = None if scenario.death_age is None else (scenario.death_age - 25) * 12

    for month in range(50 * 12):
        age = 25 + month / 12
        years = month / 12
        expense_growth_factor = (1 + scenario.expense_growth) ** years
        salary_growth_factor = (1 + scenario.income_growth) ** years
        salaries = [30_000 * salary_growth_factor, 20_000 * salary_growth_factor]

        if scenario.death_age is not None and age >= scenario.death_age:
            salaries[0] = 0.0
        if age >= 65:
            salaries = [0.0, 0.0]

        if scenario.care_start_age <= age < scenario.care_end_age:
            reduction = salaries[1] * scenario.care_reduction
            salaries[1] -= reduction
            cumulative_care_income_lost += reduction

        shock_loss = 0.0
        for shock_age, person, duration, loss_fraction in scenario.income_shocks:
            start = (shock_age - 25) * 12
            if start <= month < start + duration:
                loss = salaries[person] * loss_fraction
                salaries[person] -= loss
                shock_loss += loss
        cumulative_income_lost += shock_loss

        cash_income = sum(salaries)

        # Retirement contributions are modelled outside the stated disposable salary.
        pension_contribution = scenario.pension_rate * cash_income if age < 65 else 0.0
        pension = pension * (1 + net_investment_monthly) + pension_contribution
        cumulative_pension_contributions += pension_contribution

        # At retirement the accumulated pension becomes available to fund consumption.
        if month == (65 - 25) * 12:
            liquid += pension
            pension = 0.0

        liquid_growth_rate = net_investment_monthly if liquid >= 0 else debt_monthly
        before_growth = liquid
        liquid *= 1 + liquid_growth_rate
        # Difference between gross and net return is an approximate fee/tax opportunity cost.
        if liquid > 0 and before_growth > 0:
            gross_m = monthly_rate(scenario.gross_investment_return)
            cumulative_investment_drag += max(0.0, before_growth * (gross_m - net_investment_monthly))

        if homeowner:
            home_value *= 1 + home_growth_monthly
            if mortgage_months_left > 0:
                interest = mortgage_balance * mortgage_rate_monthly
                principal_paid = min(mortgage_balance, mortgage_payment_monthly - interest)
                mortgage_balance -= principal_paid
                mortgage_months_left -= 1

        # Attempt to buy annually from age 40 through age 50 if a six-month cash buffer remains.
        if (not homeowner and 40 <= age <= 50 and month % 12 == 0):
            candidate_price = scenario.property_price_40 * (1 + scenario.home_real_growth) ** (age - 40)
            upfront = candidate_price * (scenario.deposit_rate + scenario.purchase_cost_rate)
            required_buffer = 6 * scenario.cohabit_expense * expense_growth_factor
            if liquid >= upfront + required_buffer:
                homeowner = True
                purchase_age = int(age)
                home_value = candidate_price
                mortgage_balance = candidate_price * (1 - scenario.deposit_rate)
                mortgage_months_left = 20 * 12
                mortgage_payment_monthly = mortgage_payment(
                    mortgage_balance, scenario.mortgage_real_rate, mortgage_months_left
                )
                liquid -= upfront

        # Housing and non-housing living costs are kept separate after a purchase or death.
        if age < move_age:
            rent = scenario.separate_rent * expense_growth_factor
            nonhousing = (scenario.separate_expense - scenario.separate_rent) * expense_growth_factor
        else:
            rent = scenario.cohabit_rent * expense_growth_factor
            nonhousing = (scenario.cohabit_expense - scenario.cohabit_rent) * expense_growth_factor

        if age >= 65:
            nonhousing *= scenario.retirement_expense_factor
        if scenario.death_age is not None and age >= scenario.death_age:
            nonhousing *= 0.65

        if homeowner:
            housing = (mortgage_payment_monthly if mortgage_months_left > 0 else 0.0)
            housing += home_value * scenario.owner_cost_rate / 12
        else:
            housing = rent

        child_cost = 0.0
        for birth_age in (36, 39):
            child_age = age - birth_age
            if 0 <= child_age < 18:
                child_cost += scenario.child_monthly_cost * expense_growth_factor
            elif 18 <= child_age < 22:
                child_cost += 0.50 * scenario.child_monthly_cost * expense_growth_factor

        remittance = 0.0
        if 30 <= age < 65:
            remittance = scenario.family_remittance * expense_growth_factor

        expense = housing + nonhousing + child_cost + remittance
        cumulative_living_expense += housing + nonhousing
        cumulative_child_cost += child_cost
        cumulative_remittance += remittance

        one_off = 0.0
        if month == move_month:
            one_off += scenario.moving_cost
        if scenario.inheritance_age is not None and month == (scenario.inheritance_age - 25) * 12:
            liquid += scenario.inheritance_amount
        for event_age, amount in scenario.emergencies:
            if month == (event_age - 25) * 12:
                one_off += amount
        if death_month is not None and month == death_month:
            one_off += scenario.funeral_cost

        liquid += cash_income - expense - one_off

        net_home_equity = 0.95 * home_value - mortgage_balance if homeowner else 0.0
        net_worth = liquid + pension + net_home_equity
        end_age = 25 + (month + 1) / 12
        series.append((end_age, net_worth))
        if end_age in (35, 45, 55, 65, 75):
            milestones[int(end_age)] = net_worth

    return {
        "move_age": move_age,
        "net_worth": series[-1][1],
        "milestones": milestones,
        "series": series,
        "purchase_age": purchase_age,
        "home_value": home_value,
        "mortgage_balance": mortgage_balance,
        "liquid": liquid,
        "pension": pension,
        "living_expense": cumulative_living_expense,
        "child_cost": cumulative_child_cost,
        "remittance": cumulative_remittance,
        "income_lost": cumulative_income_lost,
        "care_income_lost": cumulative_care_income_lost,
        "pension_contributions": cumulative_pension_contributions,
        "investment_drag": cumulative_investment_drag,
    }


def money(value):
    sign = "-" if value < 0 else ""
    return f"{sign}R{abs(value):,.0f}"


if __name__ == "__main__":
    for scenario in SCENARIOS:
        early = simulate(scenario, 25)
        late = simulate(scenario, 35)
        print(f"\n{scenario.name}")
        print("age,early,late,gap")
        for age in (25, 35, 45, 55, 65, 75):
            e = early["milestones"][age]
            l = late["milestones"][age]
            print(f"{age},{money(e)},{money(l)},{money(e-l)}")
        print(f"purchase_age_early={early['purchase_age']}")
        print(f"purchase_age_late={late['purchase_age']}")
        print(f"living_cost_saved={money(late['living_expense']-early['living_expense'])}")
        print(f"child_cost={money(early['child_cost'])}")
        print(f"remittance={money(early['remittance'])}")
        print(f"income_lost_shocks={money(early['income_lost'])}")
        print(f"income_lost_care={money(early['care_income_lost'])}")
        print(f"pension_contributions={money(early['pension_contributions'])}")
        print(f"investment_drag_early={money(early['investment_drag'])}")
