"""Auditable dividend receipts and estimates. No market-data requests."""
from datetime import date
from decimal import Decimal as D

STATUSES = {'received', 'announced', 'estimated', 'pending'}

def income_summary(events, as_of):
    """Only reconciled received cash counts as paid. KF refund is a separate flow."""
    if not isinstance(as_of, date):
        raise ValueError('as_of must be a date')
    seen = set()
    totals = {k: D('0') for k in ('gross_paid', 'withheld_paid', 'net_paid', 'kf_refund', 'expected_gross', 'expected_net')}
    calendar = []
    periods = {"monthly": {}, "annual": {}}
    for e in events:
        required = {'id','ticker','status','payment_date','ex_date','currency','gross','withheld','fx','source','observed_at','reconciled','kind'}
        if not required <= e.keys() or not e['id'] or e['id'] in seen:
            raise ValueError('missing fields or duplicate event')
        seen.add(e['id'])
        if e['status'] not in STATUSES or e['kind'] not in ('dividend','kf_refund') or not e['ticker'] or not e['source']:
            raise ValueError('invalid status, kind or provenance')
        if not isinstance(e['reconciled'], bool) or e['currency'] not in ('SEK','USD','CAD','GBP'):
            raise ValueError('invalid currency/reconciliation')
        try:
            pay=date.fromisoformat(e['payment_date']) if e['payment_date'] else None
            ex=date.fromisoformat(e['ex_date']) if e['ex_date'] else None
            observed=date.fromisoformat(e['observed_at'])
            gross,withheld,fx=(D(e[k]) if e[k] is not None else None for k in ('gross','withheld','fx'))
        except Exception as exc:
            raise ValueError('invalid date or amount') from exc
        if observed>as_of or any(v is not None and (not v.is_finite() or v<0) for v in (gross,withheld,fx)) or fx==0:
            raise ValueError('invalid date/amount')
        if e['currency']=='SEK' and fx is not None and fx!=1:
            raise ValueError('SEK FX must equal 1')
        if gross is not None and withheld is not None and withheld>gross:
            raise ValueError('withholding exceeds gross')
        received=e['status']=='received'
        if received and (not e['reconciled'] or pay is None or pay>as_of or None in (gross,withheld,fx)):
            raise ValueError('paid requires reconciled dated complete receipt')
        if e['kind']=='kf_refund' and (not received or withheld!=0 or e['currency']!='SEK' or fx!=1):
            raise ValueError('KF refund requires reconciled SEK receipt without withholding')
        # An announced payment in the past is pending, never automatically received.
        status='pending' if not received and pay and pay<as_of else e['status']
        g=gross*fx if gross is not None and fx is not None else None
        net=(gross-withheld)*fx if None not in (gross,withheld,fx) else None
        if received:
            if e['kind']=='kf_refund':totals['kf_refund']+=g
            else:
                totals['gross_paid']+=g;totals['withheld_paid']+=withheld*fx;totals['net_paid']+=net
        else:
            if g is not None:totals['expected_gross']+=g
            if net is not None:totals['expected_net']+=net
        if pay:
            for mode, key in [('monthly',pay.strftime('%Y-%m')),('annual',str(pay.year))]:
                bucket=periods[mode].setdefault(key,{k:D('0') for k in ('net_paid','kf_refund','expected_net')})
                if received:bucket['kf_refund' if e['kind']=='kf_refund' else 'net_paid']+=net
                elif net is not None:bucket['expected_net']+=net
        calendar.append({**e,'status':status,'gross_sek':str(g) if g is not None else None,'net_sek':str(net) if net is not None else None})
    return {'as_of':as_of.isoformat(),'totals':{k:str(v) for k,v in totals.items()},'events':calendar,
            'periods':{mode:{key:{k:str(v) for k,v in bucket.items()} for key,bucket in sorted(rows.items())} for mode,rows in periods.items()},
            'incomplete_expected':sum(e['status']!='received' and e['net_sek'] is None for e in calendar)}

# Entirely invented events, unrelated to any owner's statement or securities.
SAMPLE_EVENTS = [
    dict(id='DIV-DEMO-1',ticker='DEMOA',status='received',payment_date='2026-01-15',ex_date='2026-01-10',currency='SEK',gross='30',withheld='0',fx='1',source='Invented demo receipt 1',observed_at='2026-01-31',reconciled=True,kind='dividend'),
    dict(id='DIV-DEMO-2',ticker='DEMOB',status='received',payment_date='2026-01-20',ex_date=None,currency='USD',gross='4',withheld='0.6',fx='10',source='Invented demo receipt 2',observed_at='2026-01-31',reconciled=True,kind='dividend'),
    dict(id='KF-DEMO-1',ticker='DEMO',status='received',payment_date='2026-01-25',ex_date=None,currency='SEK',gross='5',withheld='0',fx='1',source='Invented KF refund receipt',observed_at='2026-01-31',reconciled=True,kind='kf_refund'),
    dict(id='DIV-DEMO-3',ticker='DEMOC',status='announced',payment_date='2026-02-15',ex_date='2026-02-01',currency='CAD',gross='3',withheld='0.45',fx='7',source='Invented announcement, estimated FX/tax',observed_at='2026-01-31',reconciled=False,kind='dividend'),
    dict(id='DIV-DEMO-4',ticker='DEMOA',status='estimated',payment_date='2026-03-15',ex_date=None,currency='SEK',gross='30',withheld='0',fx='1',source='Invented estimate, not an announcement',observed_at='2026-01-31',reconciled=False,kind='dividend'),
    dict(id='DIV-DEMO-5',ticker='DEMOB',status='announced',payment_date='2026-01-29',ex_date=None,currency='USD',gross='4',withheld=None,fx=None,source='Invented unconfirmed payment',observed_at='2026-01-31',reconciled=False,kind='dividend'),
]
