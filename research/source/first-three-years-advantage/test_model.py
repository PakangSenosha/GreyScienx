import math
import unittest

import model


class ModelTests(unittest.TestCase):
    def test_tax_threshold_is_zero(self):
        self.assertAlmostEqual(model.tax_annual(99000), 0.0, places=2)

    def test_tax_is_progressive(self):
        self.assertGreater(model.tax_annual(720000), model.tax_annual(420000))

    def test_loan_amortises(self):
        self.assertAlmostEqual(model.remaining_loan(207000, 0.115, 60, 60), 0.0, places=2)
        self.assertLess(model.remaining_loan(207000, 0.115, 60, 36), 207000)

    def test_central_combined_delays_are_monotonic(self):
        salary = model.ILL["salary"]["middle"]
        results = [
            model.first_three_years(strategy, salary, "Johannesburg")["terminal_capital_age25"]
            for strategy in model.STRATEGIES[:4]
        ]
        self.assertEqual(results, sorted(results))

    def test_thresholds_are_finite_and_positive(self):
        for value in model.break_even_results().values():
            self.assertTrue(math.isfinite(value))
            self.assertGreater(value, 0)

    def test_matrix_is_complete(self):
        rows = model.run_matrix()
        self.assertEqual(len(rows), 3 * 3 * 6)


if __name__ == "__main__":
    unittest.main()
