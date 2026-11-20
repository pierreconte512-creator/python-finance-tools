"""Rates are decimal fractions; results are unrounded floats.

Only finite real inputs are accepted. Booleans are rejected even though Python
models them as integers. Monetary values must use one consistent currency.
"""

import math
from numbers import Real
from typing import Iterable


def _finite(name: str, value: float) -> float:
    if isinstance(value, bool) or not isinstance(value, Real):
        raise TypeError(f"{name} must be a real number")
    value = float(value)
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")
    return value


def _positive_integer(name: str, value: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an integer")
    if value <= 0:
        raise ValueError(f"{name} must be positive")
    return value


def compound_interest(principal: float, annual_rate: float, years: float,
                      compounds_per_year: int = 12) -> float:
    """Return future balance P * (1 + r/n)**(n*t), without contributions.

    Principal and years must be nonnegative; the periodic rate must exceed -1.
    """
    principal = _finite("principal", principal)
    annual_rate = _finite("annual_rate", annual_rate)
    years = _finite("years", years)
    n = _positive_integer("compounds_per_year", compounds_per_year)
    if principal < 0 or years < 0 or annual_rate / n <= -1:
        raise ValueError("principal/years must be nonnegative and periodic rate > -1")
    return principal * math.exp(n * years * math.log1p(annual_rate / n))


def effective_annual_rate(nominal_rate: float, compounds_per_year: int = 12) -> float:
    """Convert a nominal annual rate into an effective annual rate."""
    rate = _finite("nominal_rate", nominal_rate)
    n = _positive_integer("compounds_per_year", compounds_per_year)
    if rate / n <= -1:
        raise ValueError("periodic rate must exceed -1")
    return math.expm1(n * math.log1p(rate / n))


def loan_payment(principal: float, annual_rate: float, payments: int,
                 payments_per_year: int = 12) -> float:
    """Return a fixed end-of-period payment on a fully amortizing loan.

    annual_rate is nominal, divided by payments_per_year. Fees, taxes, and
    lender-specific rounding are excluded. Negative loan rates are unsupported.
    """
    principal = _finite("principal", principal)
    annual_rate = _finite("annual_rate", annual_rate)
    count = _positive_integer("payments", payments)
    frequency = _positive_integer("payments_per_year", payments_per_year)
    if principal < 0 or annual_rate < 0:
        raise ValueError("principal and annual_rate must be nonnegative")
    rate = annual_rate / frequency
    if rate == 0:
        return principal / count
    return principal * rate / -math.expm1(-count * math.log1p(rate))


def net_present_value(rate: float, cash_flows: Iterable[float]) -> float:
    """Return sum(C_t / (1+r)**t), starting with the cash flow at time zero.

    Cash flows are equally spaced; rate applies to that same interval. The
    iterable must contain at least one value and is consumed exactly once.
    """
    rate = _finite("rate", rate)
    if rate <= -1:
        raise ValueError("rate must exceed -1")
    flows = [_finite("cash_flow", flow) for flow in cash_flows]
    if not flows:
        raise ValueError("cash_flows must not be empty")
    # Backward evaluation avoids explicitly raising the discount factor to t.
    result = flows[-1]
    for flow in reversed(flows[:-1]):
        result = flow + result / (1 + rate)
    return result


def return_on_investment(initial_value: float, final_value: float) -> float:
    """Return simple ROI (final-initial)/initial, excluding external cash flows."""
    initial = _finite("initial_value", initial_value)
    final = _finite("final_value", final_value)
    if initial <= 0 or final < 0:
        raise ValueError("initial_value must be positive; final_value nonnegative")
    return (final - initial) / initial


def compound_annual_growth_rate(initial_value: float, final_value: float,
                                years: float) -> float:
    """Return annualized growth (final/initial)**(1/years)-1.

    Assumes no intervening deposits or withdrawals. A total loss returns -1.
    """
    initial = _finite("initial_value", initial_value)
    final = _finite("final_value", final_value)
    years = _finite("years", years)
    if initial <= 0 or final < 0 or years <= 0:
        raise ValueError("initial_value/years must be positive; final_value nonnegative")
    if final == 0:
        return -1.0
    return math.expm1((math.log(final) - math.log(initial)) / years)
