"""Small, dependency-free financial calculations with explicit conventions."""

from .calculations import (
    compound_interest, effective_annual_rate, loan_payment,
    net_present_value, return_on_investment, compound_annual_growth_rate,
)

__all__ = [
    "compound_interest", "effective_annual_rate", "loan_payment",
    "net_present_value", "return_on_investment", "compound_annual_growth_rate",
]
