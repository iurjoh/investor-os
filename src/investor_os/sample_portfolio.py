"""Deterministic fictional trade loader and CLI. No broker imports or network I/O."""
import argparse
import csv
import io
import json
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path

from .portfolio import Trade, calculate_position

SAMPLE_LABEL = "SYNTHETIC TEST DATA - NOT A REAL PORTFOLIO"
# Every name, quantity, amount, date and FX rate below is invented.
SAMPLE_CSV = """transaction_id,date,ticker,mic,name,kind,quantity,gross_amount,fees,tax,fx_rate
DEMO001,2026-01-02,DEMOA,XSTO,Fictional Aurora Workshop,buy,10,1000,10,0,1
DEMO002,2026-01-03,DEMOA,XSTO,Fictional Aurora Workshop,buy,10,2000,10,0,1
DEMO003,2026-01-04,DEMOA,XSTO,Fictional Aurora Workshop,sell,5,900,5,0,1
DEMO004,2026-01-05,DEMOB,XNYS,Fictional Blue Orchard,buy,8,160,2,0,10
DEMO005,2026-01-06,DEMOC,XTSE,Fictional Cedar Observatory,buy,4,120,1,0,7
DEMO006,2026-01-07,DEMOC,XTSE,Fictional Cedar Observatory,sell,4,140,1,0,7
DEMO007,2026-01-08,DEMOC,XTSE,Fictional Cedar Observatory,buy,3,105,1,0,7
"""
FIELDS = set(SAMPLE_CSV.splitlines()[0].split(','))


def load_trades(text):
    """Strict normalized CSV loader, grouped by ticker + exchange (MIC).

    gross/fees/tax are in one trade currency; FX converts each to SEK.
    Duplicate IDs and malformed values fail the whole import. No silent repair.
    """
    reader = csv.DictReader(io.StringIO(text))
    if set(reader.fieldnames or ()) not in (FIELDS, FIELDS | {'sequence'}):
        raise ValueError("CSV columns must match the documented trade format")
    seen = set()
    grouped = {}
    names = {}
    for row in reader:
        if None in row or any(v is None for v in row.values()):
            raise ValueError("CSV row has missing or extra fields")
        txid = row['transaction_id'].strip()
        ticker, mic, name = (row[k].strip() for k in ('ticker', 'mic', 'name'))
        if not txid or txid in seen:
            raise ValueError("transaction IDs must be non-empty and unique")
        if not ticker or not name or len(mic) != 4 or not mic.isascii() or not mic.isalnum() or mic != mic.upper():
            raise ValueError("asset requires ticker, name and a four-character MIC")
        seen.add(txid)
        key = (ticker, mic)
        if key in names and names[key] != name:
            raise ValueError("inconsistent asset name")
        names[key] = name
        try:
            values = {k: Decimal(row[k]) for k in ('quantity', 'gross_amount', 'fees', 'tax', 'fx_rate')}
            day = date.fromisoformat(row['date'])
            sequence_text = row.get('sequence', '').strip()
            if sequence_text and (not sequence_text.isascii() or not sequence_text.isdigit()):
                raise ValueError('invalid execution sequence')
            sequence = int(sequence_text) if sequence_text else None
        except (InvalidOperation, ValueError) as exc:
            raise ValueError("invalid decimal or ISO date") from exc
        if any(not v.is_finite() or v < 0 for v in values.values()) or values['fx_rate'] == 0:
            raise ValueError("amounts must be finite and non-negative; FX positive")
        if values['quantity'] == 0 or row['kind'] not in ('buy', 'sell'):
            raise ValueError("trade requires positive quantity and buy/sell kind")
        grouped.setdefault(key, []).append(Trade(day, txid, row['kind'], **values, sequence=sequence))
    return names, grouped


def summarize(text):
    names, grouped = load_trades(text)
    holdings = []
    total = Decimal('0')
    for (ticker, mic), trades in sorted(grouped.items()):
        position = calculate_position(trades)
        total += position.cost_basis_base
        holdings.append(dict(ticker=ticker, mic=mic, name=names[(ticker, mic)],
            quantity=str(position.quantity), cost_basis_sek=str(position.cost_basis_base),
            average_cost_sek=None if position.average_cost_base is None else str(position.average_cost_base)))
    return dict(label=SAMPLE_LABEL, base_currency='SEK', transaction_count=sum(map(len, grouped.values())),
                holdings=holdings, total_cost_basis_sek=str(total),
                limitations=['No market values, dividends, cash or investment recommendations.',
                             'Normalized trade format, not an Avanza importer.',
                             'CLI only; no dashboard, login, storage or hosted app.'])


def main():
    parser = argparse.ArgumentParser(description=SAMPLE_LABEL)
    parser.add_argument('--write-sample', type=Path, help='write invented fixture to a new local CSV (never overwrites)')
    args = parser.parse_args()
    if args.write_sample:
        with args.write_sample.open('x', encoding='utf-8', newline='') as f:
            f.write(SAMPLE_CSV)
    print(json.dumps(summarize(SAMPLE_CSV), indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
