(function(root){
'use strict';const S=100000000n;function d(v){if(typeof v!=='string'||!/^\d{1,15}(\.\d{1,8})?$/.test(v))throw Error('Invalid decimal');const [a,b='']=v.split('.');return BigInt(a)*S+BigInt(b.padEnd(8,'0'));}function t(v){return (v/S)+'.'+(v%S).toString().padStart(8,'0');}function mul(a,b){return (a*b+S/2n)/S;}
function rateValue(v){return v.startsWith('-')?-d(v.slice(1)):d(v);}
function project(x){
 const initial=d(x.initial),annual=d(x.annual),yieldRate=d(x.yield),withholding=d(x.withholding),inflation=d(x.inflation),target=d(x.target),contributionGoal=d(x.contributionGoal),contributed=d(x.contributed);
 if(yieldRate>S||withholding>S||inflation>S||target===0n||contributionGoal===0n||!Number.isInteger(x.years)||x.years<1||x.years>50)throw Error('Invalid limits');
 if(!(rateValue(x.low)<=rateValue(x.base)&&rateValue(x.base)<=rateValue(x.high)))throw Error('Scenarios must be ordered');
 const scenarios=[];
 for(const [name,rate] of [['Conservador',x.low],['Base',x.base],['Otimista',x.high]]){
  const r=rateValue(rate);if(r>S||r< -S)throw Error('Return outside -100 to 100%');let capital=initial,deflator=S;const rows=[];
  for(let year=1;year<=x.years;year++){
   // Contribution at year end; return already includes reinvested dividends.
   capital=mul(capital,S+r)+annual;deflator=mul(deflator,S+inflation);
   const income=mul(mul(capital,yieldRate),S-withholding)/12n;
   rows.push({year,capital:t(capital),monthly_income:t(income),capital_today:t(capital*S/deflator)});
  }
  scenarios.push({name,rows,estimated_target_year:rows.find(row=>d(row.monthly_income)>=target)?.year||null});
 }
 const annualProgress=Number(contributed*10000n/contributionGoal)/100;
 const currentIncome=mul(mul(initial,yieldRate),S-withholding)/12n;
 const incomeProgress=Number(currentIncome*10000n/target)/100;
 return {scenarios,current_monthly_income:t(currentIncome),annual_progress:annualProgress,income_progress:incomeProgress,annual_display:Math.min(100,annualProgress),income_display:Math.min(100,incomeProgress)};
}
root.InvestorScenarios={project};if(typeof module!=='undefined')module.exports={project};
})(globalThis);
