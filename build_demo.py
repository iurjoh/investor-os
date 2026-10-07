"""Generate only the embedded fictional portfolio for the public static demo."""
import csv, io, json, pathlib, sys
sys.path.insert(0, 'src')
from investor_os.sample_portfolio import SAMPLE_CSV, summarize
result = summarize(SAMPLE_CSV)
result['trades'] = list(csv.DictReader(io.StringIO(SAMPLE_CSV)))
pathlib.Path('web/portfolio.json').write_text(json.dumps(result, indent=2) + '\n')
