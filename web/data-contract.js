/* Validate the public synthetic fixture before rendering. Not a real-data importer. */
(function(root){
'use strict';
const LABEL='SYNTHETIC TEST DATA - NOT A REAL PORTFOLIO';
const numeric=(v)=>typeof v==='string' && /^\d+(\.\d+)?$/.test(v) && Number.isFinite(Number(v));
const day=(v)=>typeof v==='string' && /^\d{4}-\d{2}-\d{2}$/.test(v) && !isNaN(Date.parse(v)) && new Date(v).toISOString().slice(0,10)===v;
function validate(d){
 const fail=()=>{throw new Error('Invalid synthetic portfolio data');};
 if(!d || d.label!==LABEL || d.schema_version!==1 || d.base_currency!=='SEK' || !day(d.fixture_as_of) || typeof d.source!=='string' || !d.source || !numeric(d.total_cost_basis_sek) || !Array.isArray(d.holdings) || !Array.isArray(d.trades) || d.transaction_count!==d.trades.length) fail();
 const assets=new Set(), ids=new Set();let total=0;
 for(const h of d.holdings){
  if(!h || typeof h.ticker!=='string' || !h.ticker || typeof h.mic!=='string' || !/^[A-Z0-9]{4}$/.test(h.mic) || typeof h.name!=='string' || !h.name || !numeric(h.quantity) || !numeric(h.cost_basis_sek) || (h.average_cost_sek!==null && !numeric(h.average_cost_sek))) fail();
  const key=h.ticker+'|'+h.mic;if(assets.has(key)) fail();assets.add(key);
  if(Number(h.quantity)===0 && (Number(h.cost_basis_sek)!==0 || h.average_cost_sek!==null)) fail();
  if(Number(h.quantity)>0 && (h.average_cost_sek===null || Math.abs(Number(h.average_cost_sek)*Number(h.quantity)-Number(h.cost_basis_sek))>0.000001)) fail();
  total+=Number(h.cost_basis_sek);
 }
 if(Math.abs(total-Number(d.total_cost_basis_sek))>0.000001) fail();
 for(const t of d.trades){
  if(!t || typeof t.transaction_id!=='string' || !t.transaction_id || ids.has(t.transaction_id) || !day(t.date) || !assets.has(t.ticker+'|'+t.mic) || !['buy','sell'].includes(t.kind) || !['SEK','USD','CAD'].includes(t.currency)) fail();
  ids.add(t.transaction_id);
  if(!['quantity','gross_amount','fees','tax','fx_rate'].every(k=>numeric(t[k])) || Number(t.quantity)<=0 || Number(t.fx_rate)<=0) fail();
 }
 return d;
}
const api={validate};root.InvestorData=api;if(typeof module!=='undefined')module.exports=api;
})(typeof globalThis!=='undefined'?globalThis:this);
