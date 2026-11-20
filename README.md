# Python Finance Tools

[![Tests](https://github.com/pierreconte512-creator/python-finance-tools/actions/workflows/tests.yml/badge.svg)](https://github.com/pierreconte512-creator/python-finance-tools/actions/workflows/tests.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

A lightweight Python library for common financial calculations. It offers a
small, documented API, explicit timing conventions, input validation, and an
automated test suite. No runtime dependencies, API keys, or network access are
required.

## Features

| Function | Calculation | Convention |
| --- | --- | --- |
| `compound_interest` | Future balance with compound interest | Nominal annual rate; no contributions |
| `effective_annual_rate` | Effective annual rate | Discrete compounding |
| `loan_payment` | Fixed loan payment | Payments at period end; fully amortizing |
| `net_present_value` | Discounted cash-flow value | First cash flow occurs at time zero |
| `return_on_investment` | Simple holding-period return | No external cash flows |
| `compound_annual_growth_rate` | Annualized growth | No external cash flows |

## Installation

Requires Python 3.9 or newer. Clone and install from source:

```bash
git clone https://github.com/pierreconte512-creator/python-finance-tools.git
cd python-finance-tools
python -m pip install .
```

For development, use `python -m pip install -e .`. The project is not currently
published to PyPI.

## Quick start

```python
from finance_tools import (
    compound_interest,
    effective_annual_rate,
    loan_payment,
    net_present_value,
    return_on_investment,
    compound_annual_growth_rate,
)

print(f"{compound_interest(1000, 0.05, 10):.2f}")  # 1647.01
print(f"{effective_annual_rate(0.12):.4%}")        # 12.6825%
print(f"{loan_payment(200000, 0.06, 360):.2f}")    # 1199.10
print(f"{net_present_value(0.1, [-1000, 600, 600]):.2f}")  # 41.32
print(f"{return_on_investment(100, 125):.0%}")     # 25%
print(f"{compound_annual_growth_rate(1000, 1210, 2):.0%}")  # 10%
```

All examples use synthetic, illustrative amounts.

## API and assumptions

Rates are decimal fractions: `0.05` means 5%. Use one consistent currency.
Functions return unrounded `float` values; round for display only. These are
analytical tools, not a currency ledger: binary floating-point arithmetic does
not implement cent-by-cent accounting or lender-specific rounding.

- `compound_interest(principal, annual_rate, years, compounds_per_year=12)`:
  computes `P * (1 + r/n) ** (n*t)`. Principal and years must be nonnegative;
  the periodic rate must exceed -1. Fractional years are supported by the
  formula; actual banking accrual conventions may differ.
- `effective_annual_rate(nominal_rate, compounds_per_year=12)`:
  computes `(1 + r/n) ** n - 1`; the periodic rate must exceed -1.
- `loan_payment(principal, annual_rate, payments, payments_per_year=12)`:
  accepts a nonnegative principal and nominal annual rate, a positive integer
  payment count, and a positive integer frequency. At zero interest the
  payment is `principal / payments`. Taxes, fees, and insurance are excluded.
- `net_present_value(rate, cash_flows)`: accepts a nonempty iterable of equally
  spaced cash flows, including the initial outlay at index zero. The discount
  rate applies to each cash-flow interval and must exceed -1.
- `return_on_investment(initial_value, final_value)`: computes
  `(final - initial) / initial`. Initial value must be positive and final value
  nonnegative. Include proceeds consistently; external deposits and withdrawals
  require a different return measure.
- `compound_annual_growth_rate(initial_value, final_value, years)`: computes
  `(final / initial) ** (1 / years) - 1`. Initial value and years must be
  positive; final value may be zero (a total loss returns -1).

Nonfinite values and invalid domains raise `ValueError`; unsupported numeric
types and noninteger counts raise `TypeError`. Boolean values are rejected.
Inputs should be ordinary finite Python real numbers; `Decimal` inputs are not
supported. Extreme magnitudes may exceed floating-point range and raise
`OverflowError` or yield nonfinite results.

## Tests

Run the suite using only the Python standard library:

```bash
python -m unittest discover -s tests -v
```

The tests cover independently calculated examples, zero and negative rates
where supported, loan amortization, growth round trips, invalid domains,
nonfinite inputs, and iterators. GitHub Actions runs the suite on Python
3.9–3.14 for pushes to `main` and pull requests, and verifies the installed
package can be imported outside the source directory.

## Contributing

Bug reports and focused pull requests are welcome. Please include a minimal
reproducible example, document any changed financial convention, and add a
regression test. Run the test suite before submitting a change. Do not include
credentials, account details, or private financial data in issues or examples.

## Scope

This library provides deterministic arithmetic for education and analysis.
It does not fetch market data, connect to brokers, execute trades, or predict
investment performance.

## License

Released under the [MIT License](LICENSE).
