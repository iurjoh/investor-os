import unittest
from datetime import date
from decimal import Decimal as D
from investor_os.portfolio import Trade, calculate_position

class PositionTests(unittest.TestCase):
    def trade(self, day, txid, kind, qty, gross, fees="0", tax="0", fx="1"):
        return Trade(date(2026, 1, day), txid, kind, D(qty), D(gross), D(fees), D(tax), D(fx))

    def test_partial_sale_preserves_average_cost(self):
        p = calculate_position([
            self.trade(1, "a", "buy", "10", "1000"),
            self.trade(2, "b", "buy", "10", "2000"),
            self.trade(3, "c", "sell", "5", "1000"),
        ])
        self.assertEqual(p.quantity, D("15"))
        self.assertEqual(p.cost_basis_base, D("2250"))
        self.assertEqual(p.average_cost_base, D("150"))

    def test_base_currency_cost_includes_fx_fees_tax(self):
        p = calculate_position([self.trade(1, "a", "buy", "2", "200", "10", "5", "2")])
        self.assertEqual(p.cost_basis_base, D("430"))

    def test_full_sale_resets_rounding_residue(self):
        p = calculate_position([
            self.trade(1, "a", "buy", "3", "100"),
            self.trade(2, "b", "sell", "3", "120"),
        ])
        self.assertEqual(p.quantity, D("0"))
        self.assertEqual(p.cost_basis_base, D("0"))

    def test_rejects_oversell(self):
        with self.assertRaises(ValueError):
            calculate_position([
                self.trade(1, "a", "buy", "1", "10"),
                self.trade(2, "b", "sell", "2", "20"),
            ])

if __name__ == "__main__":
    unittest.main()

class InputContractTests(unittest.TestCase):
    def test_rejects_nonfinite_negative_and_zero_inputs(self):
        base = dict(transaction_date=date(2026, 1, 1), transaction_id='a', kind='buy',
                    quantity=D('1'), gross_amount=D('10'), fees=D('0'), tax=D('0'), fx_rate=D('1'))
        for key in ('quantity', 'gross_amount', 'fees', 'tax', 'fx_rate'):
            for value in ('NaN', 'Infinity', '-1'):
                with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                    calculate_position([Trade(**(base | {key: D(value)}))])
        for key in ('quantity', 'fx_rate'):
            with self.assertRaises(ValueError):
                calculate_position([Trade(**(base | {key: D('0')}))])

    def test_duplicate_id_rejected(self):
        t = Trade(date(2026,1,1), 'same', 'buy', D('1'), D('0'))
        with self.assertRaises(ValueError):
            calculate_position([t,t])

    def test_empty_and_zero_cost(self):
        self.assertEqual(calculate_position([]).quantity,D('0'))
        t = Trade(date(2026,1,1), 'free', 'buy', D('1'), D('0'))
        self.assertEqual(calculate_position([t]).average_cost_base,D('0'))
