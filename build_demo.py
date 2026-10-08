"""Generate only the embedded fictional portfolio for the public static demo."""
import csv, io, json, pathlib, sys
sys.path.insert(0, 'src')
from investor_os.sample_portfolio import SAMPLE_CSV, summarize
result = summarize(SAMPLE_CSV)
result['schema_version'] = 1
result['fixture_as_of'] = '2026-01-08'
result['calculation_method'] = 'weighted-average Decimal; acquisition includes fees and tax'
result['source'] = 'Embedded wholly invented SAMPLE_CSV, not a broker export'
result['trades'] = list(csv.DictReader(io.StringIO(SAMPLE_CSV)))
currencies = {'XSTO': 'SEK', 'XNYS': 'USD', 'XTSE': 'CAD'}
for trade in result['trades']:
    trade['currency'] = currencies[trade['mic']]
from datetime import date
from investor_os.income import income_summary, SAMPLE_EVENTS
result['income'] = income_summary(SAMPLE_EVENTS, date(2026, 1, 31))
pathlib.Path('web/portfolio.json').write_text(json.dumps(result, indent=2) + '\n')
