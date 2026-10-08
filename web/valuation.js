/* Fixed-point decimal arithmetic for manual synthetic valuation. 8 decimal places. */
(function(root){
'use strict';const SCALE=100000000n;
function dec(v){if(typeof v!=='string'||!/^\d{1,15}(\.\d{1,8})?$/.test(v))throw Error('Use non-negative decimals, up to 8 places');const [a,b='']=v.split('.');return BigInt(a)*SCALE+BigInt(b.padEnd(8,'0'));}
function text(v){return (v/SCALE).toString()+'.'+(v%SCALE).toString().padStart(8,'0');}
function signed(v){return v<0n?'-'+text(-v):text(v);}
function mul(a,b){return (a*b+SCALE/2n)/SCALE;}
function value(holdings,inputs,asOf){
 if(!/^\d{4}-\d{2}-\d{2}$/.test(asOf)||new Date(asOf).toISOString().slice(0,10)!==asOf)throw Error('Invalid valuation date');
 const rows=[];let total=0n,cost=0n,complete=true;const sectors={},currencies={};
 for(const h of holdings){const x=inputs[h.ticker+'|'+h.mic];let mv=null,reason='Missing price/FX';
  const q=dec(h.quantity),c=dec(h.cost_basis_sek);
  if(x&&x.price!==''&&x.fx!==''){
   if(!x.source||!x.currency||!x.sector||!/^\d{4}-\d{2}-\d{2}$/.test(x.date)||new Date(x.date).toISOString().slice(0,10)!==x.date||x.date>asOf)throw Error('Missing/invalid source, currency, sector or date');
   const fx=dec(x.fx);if(fx===0n)throw Error('FX must be positive');
   if(x.currency==='SEK'&&fx!==SCALE)throw Error('SEK FX must equal 1');
   mv=mul(mul(q,dec(x.price)),fx);reason=x.date<asOf?'Dated input, not live':'Manual snapshot';total+=mv;cost+=c;
   sectors[x.sector]=(sectors[x.sector]||0n)+mv;currencies[x.currency]=(currencies[x.currency]||0n)+mv;
  }else complete=false;
  rows.push({ticker:h.ticker,mic:h.mic,name:h.name,market_value:mv===null?null:text(mv),cost:text(c),unrealized:mv===null?null:signed(mv-c),date:x?.date||null,source:x?.source||null,reason});
 }
 const group=o=>Object.entries(o).map(([name,n])=>({name,value:text(n),weight:total?Number((n*10000n)/total)/100:null}));
 return {as_of:asOf,complete,known_total:text(total),total:complete?text(total):null,unrealized:complete?signed(total-cost):null,rows,sectors:group(sectors),currencies:group(currencies)};
}
root.InvestorValuation={value};if(typeof module!=='undefined')module.exports={value};
})(globalThis);
