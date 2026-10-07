import csv
import io
import unittest
from decimal import Decimal
from investor_os.sample_portfolio import SAMPLE_CSV, SAMPLE_LABEL, summarize


def altered(field, value, row=0):
    reader = csv.DictReader(io.StringIO(SAMPLE_CSV))
    fields = reader.fieldnames
    rows = list(reader)
    rows[row][field] = value
    out = io.StringIO()
    writer = csv.DictWriter(out, fieldnames=fields)
    writer.writeheader()
    writer.writerows(rows)
    return out.getvalue()


class SamplePortfolioTests(unittest.TestCase):
    def test_fictional_portfolio_reconciles(self):
        result = summarize(SAMPLE_CSV)
        self.assertEqual(result['label'], SAMPLE_LABEL)
        self.assertEqual(result['transaction_count'], 7)
        self.assertEqual([h['quantity'] for h in result['holdings']], ['15', '8', '3'])
        self.assertEqual([Decimal(h['cost_basis_sek']) for h in result['holdings']],
                         [Decimal('2265'), Decimal('1620'), Decimal('742')])
        self.assertEqual(Decimal(result['total_cost_basis_sek']), Decimal('4627'))

    def test_empty_header_is_empty_portfolio(self):
        self.assertEqual(summarize(SAMPLE_CSV.splitlines()[0])['holdings'], [])

    def test_repeatable_and_order_independent(self):
        lines = SAMPLE_CSV.splitlines()
        self.assertEqual(summarize(SAMPLE_CSV), summarize('\n'.join([lines[0]] + lines[:0:-1])))
        self.assertEqual(summarize(SAMPLE_CSV), summarize(SAMPLE_CSV))

    def test_exchange_identity_separates_same_ticker(self):
        result = summarize(altered('mic', 'XLON', 1))
        self.assertEqual(len(result['holdings']), 4)

    def test_invalid_fields_rejected(self):
        for field, value in [('transaction_id', ''), ('mic', 'bad'), ('date', '2026-02-30'),
                             ('kind', 'dividend'), ('quantity', '0'), ('quantity', '-1'),
                             ('gross_amount', 'NaN'), ('fees', '-1'), ('tax', 'Infinity'),
                             ('fx_rate', '0'), ('fx_rate', '-2')]:
            with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                summarize(altered(field, value))

    def test_duplicate_rejected(self):
        with self.assertRaises(ValueError):
            summarize(altered('transaction_id', 'DEMO001', 1))

    def test_missing_columns_rejected(self):
        with self.assertRaises(ValueError):
            summarize('date,quantity\n2026-01-01,1\n')

    def test_oversell_rejected(self):
        with self.assertRaises(ValueError):
            summarize(altered('quantity', '99', 2))

    def test_conflicting_asset_name_rejected(self):
        with self.assertRaises(ValueError):
            summarize(altered('name', 'Different fictional name', 1))

    def test_extra_fields_rejected(self):
        lines = SAMPLE_CSV.splitlines()
        lines[1] += ',extra'
        with self.assertRaises(ValueError):
            summarize('\n'.join(lines))


if __name__ == '__main__':
    unittest.main()
