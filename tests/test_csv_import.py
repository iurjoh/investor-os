"""Local normalized CSV regressions. All inputs are invented, never broker exports."""
import copy
import csv
import io
import unittest

from investor_os.sample_portfolio import FIELDS, SAMPLE_CSV, load_trades, summarize

HEADER = SAMPLE_CSV.splitlines()[0]
ROWS = list(csv.DictReader(io.StringIO(SAMPLE_CSV)))


def encode(rows, fields=None):
    out = io.StringIO()
    writer = csv.DictWriter(out, fieldnames=fields or HEADER.split(','))
    writer.writeheader()
    writer.writerows(rows)
    return out.getvalue()


class CsvImportTests(unittest.TestCase):
    def test_duplicate_header_never_overwrites_original_amount(self):
        for field in sorted(FIELDS | {'sequence'}):
            fields = HEADER.split(',')
            if field == 'sequence':
                fields.append(field)
            text = ','.join(fields + [field]) + '\n'
            values = [ROWS[0].get(f, '1') for f in fields]
            text += ','.join(values + ['999']) + '\n'
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, 'column names must be unique'):
                summarize(text)

    def test_quote_junk_after_closing_quote_is_rejected(self):
        text = HEADER + '\n' + SAMPLE_CSV.splitlines()[1].replace(
            'Fictional Aurora Workshop', '"Fictional Aurora"junk') + '\n'
        with self.assertRaisesRegex(ValueError, 'malformed CSV quoting or structure'):
            summarize(text)

    def test_unterminated_quote_is_rejected(self):
        text = HEADER + '\n' + SAMPLE_CSV.splitlines()[1].replace(
            'Fictional Aurora Workshop', '"Fictional Aurora Workshop') + '\n'
        with self.assertRaisesRegex(ValueError, 'malformed CSV quoting or structure'):
            summarize(text)

    def test_valid_quoted_comma_newline_and_escaped_quote_are_preserved(self):
        rows = copy.deepcopy(ROWS[:1])
        rows[0]['name'] = 'Fictional, "Workshop"\nNorth'
        result = summarize(encode(rows))
        self.assertEqual(result['holdings'][0]['name'], rows[0]['name'])
        self.assertEqual(result['total_cost_basis_sek'], '1010')

    def test_missing_each_required_column_is_rejected(self):
        for missing in sorted(FIELDS):
            fields = [f for f in HEADER.split(',') if f != missing]
            row = {k: v for k, v in ROWS[0].items() if k != missing}
            with self.subTest(field=missing), self.assertRaises(ValueError):
                summarize(encode([row], fields))

    def test_empty_each_required_value_is_rejected(self):
        for field in sorted(FIELDS):
            row = dict(ROWS[0], **{field: ''})
            with self.subTest(field=field), self.assertRaises(ValueError):
                summarize(encode([row]))

    def test_short_row_is_rejected(self):
        with self.assertRaises(ValueError):
            summarize(HEADER + '\n' + SAMPLE_CSV.splitlines()[1].rsplit(',', 1)[0])

    def test_extra_cell_and_unknown_column_are_rejected(self):
        for text in (HEADER + '\n' + SAMPLE_CSV.splitlines()[1] + ',extra',
                     HEADER + ',unknown\n' + SAMPLE_CSV.splitlines()[1] + ',extra'):
            with self.subTest(text=text), self.assertRaises(ValueError):
                summarize(text)

    def test_invalid_numeric_and_date_values_are_rejected(self):
        cases = [('date', '2026-02-30'), ('date', ''), ('quantity', 'NaN'),
                 ('gross_amount', 'Infinity'), ('fees', '-1'), ('tax', 'bad'),
                 ('fx_rate', '0'), ('quantity', '0'), ('gross_amount', '1,23')]
        for field, value in cases:
            with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                summarize(encode([dict(ROWS[0], **{field: value})]))

    def test_invalid_late_row_returns_no_partial_result(self):
        baseline = summarize(SAMPLE_CSV)
        retained = copy.deepcopy(baseline)
        for field, value in [('quantity', ''), ('transaction_id', ROWS[0]['transaction_id'])]:
            rows = copy.deepcopy(ROWS)
            rows[-1][field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                load_trades(encode(rows))
            self.assertEqual(baseline, retained)
            self.assertEqual(summarize(SAMPLE_CSV), retained)

    def test_same_batch_twice_in_one_input_is_rejected(self):
        with self.assertRaises(ValueError):
            summarize(encode(ROWS + ROWS))

    def test_same_id_changed_amount_is_rejected_not_updated(self):
        changed = dict(ROWS[0], gross_amount='9999')
        with self.assertRaises(ValueError):
            summarize(encode(ROWS + [changed]))

    def test_repeat_calls_are_equal_and_return_independent_results(self):
        first = summarize(SAMPLE_CSV)
        second = summarize(SAMPLE_CSV)
        self.assertEqual(first, second)
        self.assertEqual(first['transaction_count'], 7)
        first['holdings'][0]['quantity'] = '9999'
        self.assertEqual(summarize(SAMPLE_CSV), second)

    def test_reordered_columns_and_crlf_preserve_values(self):
        self.assertEqual(summarize(encode(ROWS, list(reversed(HEADER.split(','))))),
                         summarize(SAMPLE_CSV))
        self.assertEqual(summarize(SAMPLE_CSV.replace('\n', '\r\n')), summarize(SAMPLE_CSV))

    def test_optional_empty_sequence_on_distinct_dates_preserves_values(self):
        fields = HEADER.split(',') + ['sequence']
        self.assertEqual(summarize(encode(ROWS, fields)), summarize(SAMPLE_CSV))

    def test_blank_lines_are_ignored_but_empty_file_is_not_a_portfolio(self):
        self.assertEqual(summarize(SAMPLE_CSV.replace('\n', '\n\n')), summarize(SAMPLE_CSV))
        for text in ('', '\n\n'):
            with self.subTest(text=text), self.assertRaises(ValueError):
                summarize(text)
        self.assertEqual(summarize(HEADER)['transaction_count'], 0)


if __name__ == '__main__':
    unittest.main()
