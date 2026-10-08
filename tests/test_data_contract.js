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
console.log(count+' data-contract checks passed');
