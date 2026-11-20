import math
import unittest

from finance_tools import (
    compound_interest, effective_annual_rate, loan_payment,
    net_present_value, return_on_investment, compound_annual_growth_rate,
)


class FinanceTests(unittest.TestCase):
    def test_compound_interest_reference(self):
        self.assertAlmostEqual(compound_interest(1000, 0.05, 10), 1647.00949769028)

    def test_compounding_boundaries(self):
        self.assertEqual(compound_interest(1000, 0, 10), 1000)
        self.assertEqual(compound_interest(1000, 0.05, 0), 1000)
        self.assertEqual(compound_interest(0, 0.05, 10), 0)
        self.assertAlmostEqual(compound_interest(1000, -0.1, 1, 1), 900)
        self.assertAlmostEqual(compound_interest(1000, 0.21, 0.5, 1), 1100)

    def test_effective_rate_reference(self):
        self.assertAlmostEqual(effective_annual_rate(0.12), 0.1268250301319697)

    def test_effective_rate_identity(self):
        for rate in (-0.1, 0, 0.07):
            with self.subTest(rate=rate):
                self.assertAlmostEqual(effective_annual_rate(rate, 1), rate)

    def test_loan_reference(self):
        self.assertAlmostEqual(loan_payment(200000, 0.06, 360), 1199.10105030551)

    def test_loan_zero_rate(self):
        self.assertEqual(loan_payment(1200, 0, 12), 100)
        self.assertEqual(loan_payment(0, 0.05, 12), 0)

    def test_loan_tiny_rate(self):
        self.assertAlmostEqual(loan_payment(1200, 1e-15, 12), 100)

    def test_loan_amortizes(self):
        balance, annual_rate, count = 15000.0, 0.08, 48
        payment = loan_payment(balance, annual_rate, count)
        for _ in range(count):
            balance = balance * (1 + annual_rate / 12) - payment
        self.assertAlmostEqual(balance, 0, places=7)

    def test_npv_reference(self):
        self.assertAlmostEqual(net_present_value(0.1, [-1000, 600, 600]), 41.3223140495868)

    def test_npv_time_zero_and_generator(self):
        self.assertEqual(net_present_value(0.5, [-500]), -500)
        self.assertEqual(net_present_value(0, iter([-100, 40, 70])), 10)
        self.assertAlmostEqual(net_present_value(-0.1, [0, 90]), 100)

    def test_roi(self):
        self.assertAlmostEqual(return_on_investment(100, 125), 0.25)
        self.assertAlmostEqual(return_on_investment(100, 80), -0.2)
        self.assertEqual(return_on_investment(100, 0), -1)

    def test_cagr_reference(self):
        self.assertAlmostEqual(compound_annual_growth_rate(1000, 1210, 2), 0.1)

    def test_cagr_boundaries(self):
        self.assertEqual(compound_annual_growth_rate(100, 0, 2), -1)
        self.assertAlmostEqual(compound_annual_growth_rate(100, 81, 2), -0.1)
        self.assertAlmostEqual(compound_annual_growth_rate(100, 100, 2), 0)

    def test_growth_round_trip(self):
        for rate in (-0.2, 0, 0.05):
            with self.subTest(rate=rate):
                final = compound_interest(1000, rate, 5, 1)
                self.assertAlmostEqual(compound_annual_growth_rate(1000, final, 5), rate)

    def test_invalid_domains(self):
        cases = [
            (compound_interest, (-1, 0.1, 1)),
            (compound_interest, (1, 0.1, -1)),
            (compound_interest, (1, -12, 1)),
            (effective_annual_rate, (-12,)),
            (loan_payment, (-1, 0.1, 12)),
            (loan_payment, (1, -0.1, 12)),
            (net_present_value, (-1, [1])),
            (net_present_value, (0.1, [])),
            (return_on_investment, (0, 100)),
            (return_on_investment, (100, -1)),
            (compound_annual_growth_rate, (0, 100, 1)),
            (compound_annual_growth_rate, (100, -1, 1)),
            (compound_annual_growth_rate, (100, 120, 0)),
        ]
        for function, args in cases:
            with self.subTest(function=function.__name__, args=args):
                with self.assertRaises(ValueError):
                    function(*args)

    def test_invalid_counts(self):
        for count in (0, -1, 1.5, True):
            for function, args in (
                (compound_interest, (100, 0.1, 1, count)),
                (effective_annual_rate, (0.1, count)),
                (loan_payment, (100, 0.1, count)),
                (loan_payment, (100, 0.1, 12, count)),
            ):
                with self.subTest(function=function.__name__, count=count):
                    with self.assertRaises((TypeError, ValueError)):
                        function(*args)

    def test_invalid_real_inputs(self):
        valid_calls = [
            (compound_interest, [100, 0.1, 1], range(3)),
            (effective_annual_rate, [0.1], range(1)),
            (loan_payment, [100, 0.1, 12], range(2)),
            (net_present_value, [0.1, [100]], range(1)),
            (return_on_investment, [100, 120], range(2)),
            (compound_annual_growth_rate, [100, 120, 2], range(3)),
        ]
        for function, args, positions in valid_calls:
            for position in positions:
                for invalid in (math.nan, math.inf, -math.inf, True, '1', None):
                    values = args.copy()
                    values[position] = invalid
                    with self.subTest(function=function.__name__, position=position, value=invalid):
                        with self.assertRaises((ValueError, TypeError)):
                            function(*values)

    def test_invalid_cash_flows(self):
        for invalid in (math.nan, math.inf, True, '100', None):
            with self.subTest(value=invalid):
                with self.assertRaises((TypeError, ValueError)):
                    net_present_value(0.1, [100, invalid])


if __name__ == '__main__':
    unittest.main()
