"""
Automatic Salary Tax Calculator (configurable)

Usage:
 - Run: python tax_calculator.py
 - Or import calculate_tax() from this module.

The module exposes:
 - calculate_tax(income, brackets, deduction=0.0)
"""
from typing import List, Optional, Tuple

Bracket = Tuple[Optional[float], float]  # (upper_limit, rate)

# Example progressive brackets (illustrative only — replace with actual values)
EXAMPLE_BRACKETS_ANNUAL: List[Bracket] = [
    (10000, 0.00),   # 0% up to 10,000
    (30000, 0.10),   # 10% on income between 10,000 and 30,000
    (80000, 0.20),   # 20% on income between 30,000 and 80,000
    (None, 0.30),    # 30% on income above 80,000
]

def calculate_tax(income: float, brackets: List[Bracket], deduction: float = 0.0):
    """
    Calculate tax, returning (total_tax, net_income, breakdown_list)
    breakdown_list: list of dicts with keys: 'bracket_from', 'bracket_to', 'taxable', 'rate', 'tax'
    """
    if income < 0:
        raise ValueError("Income must be non-negative")

    taxable_income = max(0.0, income - deduction)
    remaining = taxable_income
    lower = 0.0
    total_tax = 0.0
    breakdown = []

    for upper, rate in brackets:
        if remaining <= 0:
            break

        if upper is None:
            taxable = remaining
            taxed_to = None
        else:
            bracket_amount = max(0.0, upper - lower)
            taxable = min(remaining, bracket_amount)
            taxed_to = upper

        tax = taxable * rate
        breakdown.append({
            "bracket_from": lower,
            "bracket_to": taxed_to,
            "taxable": round(taxable, 2),
            "rate": rate,
            "tax": round(tax, 2),
        })
        total_tax += tax
        remaining -= taxable
        lower = 0 if taxed_to is None else taxed_to

    net_income = income - total_tax
    return round(total_tax, 2), round(net_income, 2), breakdown

def format_currency(x: float):
    return f"{x:,.2f}"

if __name__ == "__main__":
    # Simple interactive CLI demo
    print("Automatic Salary Tax Calculator")
    mode = input("Calculate for (A)nnual or (M)onthly salary? [A/M]: ").strip().lower()
    if mode not in ("a", "m", "monthly", "annual"):
        print("Defaulting to Annual.")
        mode = "a"
    salary_input = input("Enter your gross salary (numbers only): ").strip()
    try:
        salary = float(salary_input)
    except ValueError:
        print("Invalid salary. Exiting.")
        raise SystemExit(1)

    if mode.startswith("m"):
        is_monthly = True
        annual_salary = salary * 12.0
    else:
        is_monthly = False
        annual_salary = salary

    print("Using example brackets. To customize, import calculate_tax() from this module.")
    brackets = EXAMPLE_BRACKETS_ANNUAL
    deduction = 0.0

    total_tax, net_annual, breakdown = calculate_tax(annual_salary, brackets, deduction=deduction)

    if is_monthly:
        gross_display = salary
        tax_display = total_tax / 12.0
        net_display = net_annual / 12.0
    else:
        gross_display = annual_salary
        tax_display = total_tax
        net_display = net_annual

    print("\n--- Summary ---")
    print(f"Gross {'monthly' if is_monthly else 'annual'} salary: {format_currency(gross_display)}")
    print(f"Total tax ({'monthly' if is_monthly else 'annual'}): {format_currency(tax_display)}")
    print(f"Net {'monthly' if is_monthly else 'annual'} income: {format_currency(net_display)}")