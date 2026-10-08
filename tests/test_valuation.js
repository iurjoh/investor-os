const assert=require('node:assert/strict');const {value}=require('../web/valuation.js');const h=require('../web/portfolio.json').holdings;
const inputs={};h.forEach((r,i)=>inputs[r.ticker+'|'+r.mic]={price:['160','22','38'][i],fx:['1','10','7'][i],currency:['SEK','USD','CAD'][i],sector:'Synthetic '+i,date:'2026-01-31',source:'Invented manual snapshot'});
let count=0;function check(fn){fn();count++;}
check(()=>assert.equal(value(h,inputs,'2026-01-31').total,'4958.00000000'));
check(()=>assert.equal(value(h,inputs,'2026-01-31').unrealized,'331.00000000'));
check(()=>assert.equal(value([],{},'2026-01-31').total,'0.00000000'));
check(()=>{let d=structuredClone(inputs);d['DEMOB|XNYS'].price='';assert.equal(value(h,d,'2026-01-31').total,null)});
for(const [key,v] of [['price','-1'],['price','NaN'],['price','1.123456789'],['fx','0'],['fx','2'],['date','2026-02-30'],['date','2026-02-01'],['source','']])check(()=>{const d=structuredClone(inputs);d['DEMOA|XSTO'][key]=v;assert.throws(()=>value(h,d,'2026-01-31'))});
check(()=>{const d=structuredClone(inputs);d['DEMOA|XSTO'].price='0';assert.equal(value(h,d,'2026-01-31').rows[0].unrealized,'-2265.00000000')});
check(()=>{const d=structuredClone(inputs);d['DEMOA|XSTO'].date='2026-01-30';assert.equal(value(h,d,'2026-01-31').rows[0].reason,'Dated input, not live')});
check(()=>{const hs=[{ticker:'D',mic:'XSTO',name:'Invented',quantity:'0.1',cost_basis_sek:'0.02'}];const d={'D|XSTO':{price:'0.2',fx:'1',currency:'SEK',sector:'Demo',date:'2026-01-31',source:'Demo'}};assert.equal(value(hs,d,'2026-01-31').total,'0.02000000')});
console.log(count+' valuation checks passed');
