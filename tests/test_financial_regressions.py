"""Fictional regressions for the independent financial review. No broker data."""
import csv,io,json,subprocess,unittest
from dataclasses import replace
from datetime import date
from decimal import Decimal as D
from pathlib import Path
from investor_os.portfolio import Trade,calculate_position
from investor_os.sample_portfolio import SAMPLE_CSV,summarize
from investor_os.income import SAMPLE_EVENTS,income_summary

class FinancialRegressions(unittest.TestCase):
    def ledger(self):
        day=date(2026,1,1)
        return [Trade(day,'A','buy',D(10),D(100),sequence=1),
                Trade(day,'C','sell',D(10),D(400),sequence=2),
                Trade(day,'B','buy',D(10),D(300),sequence=3)]
    def test_same_day_explicit_order_ignores_id_and_input_order(self):
        trades=self.ledger()
        for rows in (trades,trades[::-1],[trades[2],trades[0],trades[1]]):
            self.assertEqual(calculate_position(rows).cost_basis_base,D(300))
    def test_missing_duplicate_or_invalid_sequence_fails_closed(self):
        trades=self.ledger()
        for value in (None,1,-1,True,1.5,9007199254740992):
            with self.subTest(value=value),self.assertRaises(ValueError):
                calculate_position([trades[0],replace(trades[1],sequence=value)])
    def test_real_oversell_not_repaired(self):
        trades=self.ledger()
        with self.assertRaises(ValueError):
            calculate_position([replace(trades[0],sequence=2),replace(trades[1],sequence=1)])
    def test_csv_accepts_optional_sequence_and_rejects_ambiguous_legacy(self):
        rows=list(csv.DictReader(io.StringIO(SAMPLE_CSV)))[:3]
        for i,row in enumerate(rows):row['date']='2026-01-01';row['sequence']=str(i)
        out=io.StringIO();writer=csv.DictWriter(out,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
        self.assertEqual(D(summarize(out.getvalue())['holdings'][0]['cost_basis_sek']),D(2265))
        for row in rows:row.pop('sequence')
        out=io.StringIO();writer=csv.DictWriter(out,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
        with self.assertRaises(ValueError):summarize(out.getvalue())
    def test_income_identity_and_numeric_zero(self):
        for value in ('2','0','0.0','0.00000000','-1'):
            with self.subTest(value=value),self.assertRaises(ValueError):
                income_summary([dict(SAMPLE_EVENTS[0],fx=value)],date(2026,1,31))
        self.assertEqual(income_summary([dict(SAMPLE_EVENTS[0],fx='1.0')],date(2026,1,31))['totals']['net_paid'],'30.0')
    def test_python_output_contract_parity(self):
        data=json.loads(Path('web/portfolio.json').read_text())
        data.update(summarize(SAMPLE_CSV));data['income']=income_summary(SAMPLE_EVENTS,date(2026,1,31))
        js="const {validate}=require('./web/data-contract.js');let s='';process.stdin.on('data',x=>s+=x);process.stdin.on('end',()=>validate(JSON.parse(s)));"
        subprocess.run(['node','-e',js],input=json.dumps(data),text=True,check=True)
