import copy,unittest
from datetime import date
from investor_os.income import income_summary,SAMPLE_EVENTS

class IncomeTests(unittest.TestCase):
    def summary(self, events=None):return income_summary(SAMPLE_EVENTS if events is None else events,date(2026,1,31))
    def test_paid_and_kf_are_separate(self):
        r=self.summary();self.assertEqual(r['totals']['net_paid'],'64.0');self.assertEqual(r['totals']['kf_refund'],'5');self.assertEqual(r['totals']['gross_paid'],'70')
    def test_past_date_does_not_make_received(self):self.assertEqual(self.summary()['events'][-1]['status'],'pending')
    def test_missing_inputs_stay_missing(self):
        r=self.summary();self.assertIsNone(r['events'][-1]['net_sek']);self.assertEqual(r['incomplete_expected'],1)
    def test_expected_does_not_change_paid(self):self.assertEqual(self.summary(SAMPLE_EVENTS[:3])['totals']['net_paid'],self.summary()['totals']['net_paid'])
    def test_monthly_and_annual(self):
        r=self.summary();self.assertEqual(r['periods']['monthly']['2026-01']['net_paid'],'64.0');self.assertEqual(r['periods']['annual']['2026']['kf_refund'],'5')
    def test_empty(self):self.assertEqual(self.summary([])['totals']['net_paid'],'0')
    def test_received_requires_reconciliation(self):
        e=copy.deepcopy(SAMPLE_EVENTS[:1]);e[0]['reconciled']=False
        with self.assertRaises(ValueError):self.summary(e)
    def test_invalid(self):
        for field,value in [('gross','NaN'),('withheld','31'),('fx','0'),('payment_date','2026-02-30'),('observed_at','2026-02-01'),('status','safe')]:
            e=copy.deepcopy(SAMPLE_EVENTS[:1]);e[0][field]=value
            with self.subTest(field=field),self.assertRaises(ValueError):self.summary(e)
    def test_duplicate(self):
        with self.assertRaises(ValueError):self.summary(SAMPLE_EVENTS[:1]*2)
    def test_kf_contract(self):
        e=copy.deepcopy(SAMPLE_EVENTS[2:3]);e[0]['withheld']='1'
        with self.assertRaises(ValueError):self.summary(e)
