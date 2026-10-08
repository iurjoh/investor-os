(function(root){
'use strict';const S=100000000n;function d(v){if(typeof v!=='string'||!/^\d{1,15}(\.\d{1,8})?$/.test(v))throw Error('Invalid decimal');const [a,b='']=v.split('.');return BigInt(a)*S+BigInt(b.padEnd(8,'0'));}function t(v){return (v/S)+'.'+(v%S).toString().padStart(8,'0');}function mul(a,b){return (a*b+S/2n)/S;}
function date(v){if(typeof v!=='string'||!/^\d{4}-\d{2}-\d{2}$/.test(v)||new Date(v).toISOString().slice(0,10)!==v)throw Error('Invalid date');}
function snapshot(rows,base,asOf,codes){
 const allowed=new Set(codes);if(!allowed.has(base))throw Error('Unknown primary currency');date(asOf);let known=0n,complete=true;const ids=new Set();
 const values=rows.map(row=>{
  if(!row.id||ids.has(row.id)||!allowed.has(row.currency))throw Error('Invalid position currency/identity');ids.add(row.id);date(row.price_date);if(row.price_date>asOf||!row.source?.trim())throw Error('Invalid price evidence');
  const q=d(row.quantity),local=mul(q,d(row.price));if(q===0n)throw Error('Zero quantity');
  const history=row.history;if(!history||!allowed.has(history.currency)||history.currency!==row.currency)throw Error('Currency change requires a new synthetic position/history');date(history.date);if(history.date>asOf)throw Error('Future operation');const originalCost=d(history.local_cost);
  function converted(amount,x,day){
   if(row.currency===base){if(x&&x.rate!==''&&(x.from!==row.currency||x.to!==base||d(x.rate)!==S))throw Error('Identity FX must be 1');return amount;}
   if(!x||x.rate==='')return null;
   if(x.from!==row.currency||x.to!==base||!x.source?.trim())throw Error('FX pair/source mismatch');date(x.date);if(x.date!==day)throw Error('FX date mismatch');const fx=d(x.rate);if(!fx)throw Error('Zero FX');return mul(amount,fx);
  }
  const market=converted(local,row.market_fx,row.price_date);const cost=converted(originalCost,history.fx?.[base],history.date);
  if(market===null)complete=false;else known+=market;
  return {id:row.id,currency:row.currency,local_value:t(local),market_base:market===null?null:t(market),original_cost:t(originalCost),cost_currency:history.currency,cost_base:cost===null?null:t(cost),unrealized:market===null||cost===null?null:(market>=cost?t(market-cost):'-'+t(cost-market)),price_date:row.price_date,fx_date:row.market_fx?.date||null,source:row.source};
 });return {base,as_of:asOf,complete,total:complete?t(known):null,known_total:t(known),rows:values};
}
root.InvestorMulti={snapshot};if(typeof module!=='undefined')module.exports={snapshot};
})(globalThis);
