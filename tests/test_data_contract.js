'use strict';
const assert=require('node:assert/strict');
const fs=require('node:fs');
const {validate}=require('../web/data-contract.js');
const sample=JSON.parse(fs.readFileSync('web/portfolio.json','utf8'));
let count=0;
function ok(d){validate(d);count++;}
function bad(edit){const d=structuredClone(sample);edit(d);assert.throws(()=>validate(d));count++;}
ok(sample);
ok({...sample,holdings:[],trades:[],transaction_count:0,total_cost_basis_sek:'0'});
bad(d=>d.label='REAL');bad(d=>d.schema_version=2);bad(d=>d.total_cost_basis_sek='NaN');
bad(d=>d.holdings[0].quantity='-1');bad(d=>d.holdings[0].average_cost_sek=null);
bad(d=>d.total_cost_basis_sek='1');bad(d=>d.trades[0].fx_rate='0');
bad(d=>d.trades[0].currency='');bad(d=>d.trades[0].date='2026-02-30');
bad(d=>d.trades.push(d.trades[0]));bad(d=>d.holdings.push(d.holdings[0]));
bad(d=>d.trades[0].transaction_id=d.trades[1].transaction_id);
bad(d=>d.holdings[0].cost_basis_sek='Infinity');bad(d=>delete d.holdings);
bad(d=>d.income.events[0].status='promised');bad(d=>d.income.events[0].reconciled=false);bad(d=>d.income.events[0].net_sek='NaN');bad(d=>d.income.events.push(d.income.events[0]));bad(d=>d.income.totals.net_paid='NaN');
bad(d=>d.income.totals.net_paid='100');bad(d=>d.income.events[0].net_sek='100');bad(d=>d.income.incomplete_expected=0);
console.log(count+' data-contract checks passed');
// Independent financial-review regressions (entirely invented).
bad(d=>d.income.periods.monthly['2026-01'].net_paid='999999');
bad(d=>d.income.periods.annual['2026'].net_paid='1234');
bad(d=>delete d.income.periods.monthly['2026-01']);
bad(d=>d.income.periods.monthly['2026-13']={net_paid:'0',kf_refund:'0',expected_net:'0'});
bad(d=>d.income.periods.monthly['2026-02'].expected_net='0');
bad(d=>d.income.periods.annual['2026'].kf_refund='64');
bad(d=>d.trades[0].gross_amount='999999');
bad(d=>d.trades[0].quantity='11');
bad(d=>d.trades[0].fees='999');
bad(d=>d.trades[0].tax='999');
bad(d=>d.trades[3].fx_rate='99');
bad(d=>d.trades[0].fx_rate='2');
for(const fx of ['0','0.0','0.00000000','2'])bad(d=>d.income.events[0].fx=fx);
// Change derived fields/totals too: zero FX must still fail, not only checksum.
for(const fx of ['0.0','0.00000000'])bad(d=>{
 const e=d.income.events[1];e.fx=fx;e.gross_sek='0';e.net_sek='0';
 d.income.totals.gross_paid='30';d.income.totals.withheld_paid='0';d.income.totals.net_paid='30';
 d.income.periods.monthly['2026-01'].net_paid='30';d.income.periods.annual['2026'].net_paid='30';
});
const ordered=structuredClone(sample);ordered.trades=ordered.trades.slice(0,3);ordered.transaction_count=3;
ordered.holdings=ordered.holdings.slice(0,1);
for(const [i,t] of ordered.trades.entries()){t.date='2026-01-02';t.sequence=i;t.fees='0';t.tax='0';t.quantity='10';t.fx_rate='1';}
ordered.trades[0].transaction_id='A';ordered.trades[0].gross_amount='100';
ordered.trades[1].transaction_id='C';ordered.trades[1].kind='sell';ordered.trades[1].gross_amount='400';
ordered.trades[2].transaction_id='B';ordered.trades[2].kind='buy';ordered.trades[2].gross_amount='300';
Object.assign(ordered.holdings[0],{quantity:'10',cost_basis_sek:'300',average_cost_sek:'30'});ordered.total_cost_basis_sek='300';
ok(ordered);ordered.trades.reverse();ok(ordered);
for(const edit of [d=>delete d.trades[0].sequence,d=>d.trades[0].sequence=1,d=>d.trades[0].sequence=-1,d=>d.trades[0].sequence=true,d=>d.trades[0].sequence=1.5]){
 const d=structuredClone(ordered);edit(d);assert.throws(()=>validate(d));count++;
}
console.log(count+' total data-contract checks passed (including financial regressions)');
