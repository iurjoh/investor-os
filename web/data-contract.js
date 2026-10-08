/* Validate the public synthetic fixture before rendering. Not a real-data importer. */
(function(root){
'use strict';
const LABEL='SYNTHETIC TEST DATA - NOT A REAL PORTFOLIO';
const numeric=(v)=>typeof v==='string' && /^\d+(\.\d+)?$/.test(v) && Number.isFinite(Number(v));
const day=(v)=>typeof v==='string' && /^\d{4}-\d{2}-\d{2}$/.test(v) && !isNaN(Date.parse(v)) && new Date(v).toISOString().slice(0,10)===v;
// Exact rational replay: no binary-float cost arithmetic or early quantization.
function gcd(a,b){while(b){const n=a%b;a=b;b=n;}return a;}
function rat(n,k=1n){const g=gcd(n<0n?-n:n,k);return [n/g,k/g];}
function decimal(v){const [a,b='']=v.split('.');return rat(BigInt(a+b),10n**BigInt(b.length));}
const add=(a,b)=>rat(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);
const neg=a=>[-a[0],a[1]],sub=(a,b)=>add(a,neg(b));
const mul=(a,b)=>rat(a[0]*b[0],a[1]*b[1]);
const div=(a,b)=>rat(a[0]*b[1],a[1]*b[0]);
const zero=()=>[0n,1n];
const near=(a,b)=>{const v=sub(a,b);return (v[0]<0n?-v[0]:v[0])*1000000n<=v[1];};
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
 // Reconcile holdings with the economic ledger, not just each other.
 const ledger=new Map();
 for(const t of d.trades){
  if(t.sequence!==undefined&&t.sequence!==null&&(!Number.isSafeInteger(t.sequence)||t.sequence<0))fail();
  if(t.currency==='SEK'&&Number(t.fx_rate)!==1)fail();
  const key=t.ticker+'|'+t.mic;if(!ledger.has(key))ledger.set(key,[]);ledger.get(key).push(t);
 }
 for(const h of d.holdings){
  const ts=ledger.get(h.ticker+'|'+h.mic)||[];const days=new Map();
  for(const t of ts){if(!days.has(t.date))days.set(t.date,[]);days.get(t.date).push(t);}
  for(const group of days.values())if(group.length>1&&(group.some(t=>t.sequence==null)||new Set(group.map(t=>t.sequence)).size!==group.length))fail();
  ts.sort((a,b)=>a.date.localeCompare(b.date)||(a.sequence??0)-(b.sequence??0));
  let q=zero(),c=zero();
  for(const t of ts){const n=decimal(t.quantity);
   if(t.kind==='buy'){q=add(q,n);c=add(c,mul(add(add(decimal(t.gross_amount),decimal(t.fees)),decimal(t.tax)),decimal(t.fx_rate)));}
   else{if(sub(q,n)[0]<0n)fail();c=sub(c,mul(div(c,q),n));q=sub(q,n);if(q[0]===0n)c=zero();}
  }
  if(sub(q,decimal(h.quantity))[0]!==0n||!near(c,decimal(h.cost_basis_sek)))fail();
 }
 if(d.income!==undefined){
  const inc=d.income;if(!inc||!day(inc.as_of)||!Array.isArray(inc.events)||!inc.totals||!Number.isInteger(inc.incomplete_expected)||inc.incomplete_expected<0) fail();
  if(!['gross_paid','withheld_paid','net_paid','kf_refund','expected_gross','expected_net'].every(k=>numeric(inc.totals[k]))) fail();
  if(!inc.periods||!inc.periods.monthly||!inc.periods.annual)fail();
  for(const mode of ['monthly','annual'])for(const [period,v] of Object.entries(inc.periods[mode]))if(!(mode==='monthly'?/^\d{4}-\d{2}$/:/^\d{4}$/).test(period)||!['net_paid','kf_refund','expected_net'].every(k=>numeric(v[k])))fail();
  const buckets={monthly:{},annual:{}};
  const eventIds=new Set();const computed={gross_paid:0,withheld_paid:0,net_paid:0,kf_refund:0,expected_gross:0,expected_net:0};let incomplete=0;
  for(const e of inc.events){
   if(!e||typeof e.id!=='string'||!e.id||eventIds.has(e.id)||typeof e.ticker!=='string'||!e.ticker||!['received','announced','estimated','pending'].includes(e.status)||!['dividend','kf_refund'].includes(e.kind)||!['SEK','USD','CAD','GBP'].includes(e.currency)||!day(e.observed_at)||e.observed_at>inc.as_of||typeof e.source!=='string'||!e.source||typeof e.reconciled!=='boolean') fail();
   eventIds.add(e.id);
   for(const key of ['payment_date','ex_date'])if(e[key]!==null&&!day(e[key]))fail();
   for(const key of ['gross','withheld','fx','gross_sek','net_sek'])if(e[key]!==null&&!numeric(e[key]))fail();
   if((e.fx!==null&&Number(e.fx)<=0)||(e.currency==='SEK'&&e.fx!==null&&Number(e.fx)!==1)||(e.gross!==null&&e.withheld!==null&&Number(e.withheld)>Number(e.gross)))fail();
   const g=e.gross===null||e.fx===null?null:Number(e.gross)*Number(e.fx);const net=e.gross===null||e.withheld===null||e.fx===null?null:(Number(e.gross)-Number(e.withheld))*Number(e.fx);
   if((g===null)!==(e.gross_sek===null)||(net===null)!==(e.net_sek===null)||(g!==null&&Math.abs(g-Number(e.gross_sek))>0.000001)||(net!==null&&Math.abs(net-Number(e.net_sek))>0.000001))fail();
   if(e.kind==='kf_refund'&&(e.status!=='received'||e.currency!=='SEK'||Number(e.fx)!==1||Number(e.withheld)!==0))fail();
   if(e.status==='received'){if(e.kind==='kf_refund')computed.kf_refund+=g;else{computed.gross_paid+=g;computed.withheld_paid+=Number(e.withheld)*Number(e.fx);computed.net_paid+=net;}}else{if(g!==null)computed.expected_gross+=g;if(net!==null)computed.expected_net+=net;else incomplete++;}
   if(e.payment_date!==null){
    for(const [mode,key] of [['monthly',e.payment_date.slice(0,7)],['annual',e.payment_date.slice(0,4)]]){
     const b=buckets[mode][key]??=( {net_paid:0,kf_refund:0,expected_net:0} );
     if(e.status==='received')b[e.kind==='kf_refund'?'kf_refund':'net_paid']+=net;
     else if(net!==null)b.expected_net+=net;
    }
   }
   if(e.status==='received'&&(!e.reconciled||e.payment_date===null||e.payment_date>inc.as_of||['gross','withheld','fx','gross_sek','net_sek'].some(k=>e[k]===null)))fail();
  }
  for(const mode of ['monthly','annual']){
   if(Object.keys(buckets[mode]).length!==Object.keys(inc.periods[mode]).length)fail();
   for(const [key,b] of Object.entries(buckets[mode])){
    if(!inc.periods[mode][key]||Object.keys(b).some(k=>Math.abs(b[k]-Number(inc.periods[mode][key][k]))>0.000001))fail();
   }
  }
  if(incomplete!==inc.incomplete_expected||Object.keys(computed).some(k=>Math.abs(computed[k]-Number(inc.totals[k]))>0.000001))fail();
 }
 return d;
}
const api={validate};root.InvestorData=api;if(typeof module!=='undefined')module.exports=api;
})(typeof globalThis!=='undefined'?globalThis:this);
