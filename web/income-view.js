(function(root){
'use strict';let income;const el=id=>document.getElementById(id);const amount=v=>v===null?'Indisponível':new Intl.NumberFormat('pt-BR',{style:'currency',currency:'SEK'}).format(Number(v));
const labels={received:'Recebido conciliado',announced:'Anunciado, não pago',estimated:'Estimado, não anunciado',pending:'Aguarda conciliação'};
function events(){
 const dest=el('income-events');dest.replaceChildren();const field=el('income-date').value,month=el('income-month').value;
 const rows=income.events.filter(e=>(!el('income-asset').value||e.ticker===el('income-asset').value)&&(!el('income-state').value||e.status===el('income-state').value)&&(!month||(e[field]||'').startsWith(month))).sort((a,b)=>(a[field]||'9999').localeCompare(b[field]||'9999'));
 rows.forEach(e=>{const n=document.createElement('div');n.className='asset';const h=document.createElement('h3');h.textContent=e.ticker+' · '+(e.kind==='kf_refund'?'Reembolso KF':'Dividendo');const d=document.createElement('p');d.textContent=(e[field]||'Data indisponível')+' · '+labels[e.status];const v=document.createElement('p');v.textContent='Bruto: '+amount(e.gross_sek)+' · Retido origem: '+(e.withheld===null?'Indisponível':e.withheld+' '+e.currency)+' · Líquido: '+amount(e.net_sek);const source=document.createElement('p');source.className='label';source.textContent='Fonte: '+e.source+' · observado em '+e.observed_at;n.append(h,d,v,source);dest.append(n)});
 if(!rows.length){const n=document.createElement('p');n.className='empty';n.textContent='Nenhum evento fictício neste filtro.';dest.append(n)}
}
function periods(){const target=el('income-periods');target.replaceChildren();Object.entries(income.periods[el('income-period').value]).forEach(([period,v])=>{const n=document.createElement('p');n.textContent=period+': líquido pago '+amount(v.net_paid)+' · KF separado '+amount(v.kf_refund)+' · esperado conhecido '+amount(v.expected_net);target.append(n)})}
function render(d){
 if(!d||!Array.isArray(d.events)||!d.totals)throw Error('missing income');income=d;
 const totals=el('income-totals');totals.replaceChildren();
 [['Bruto recebido',d.totals.gross_paid],['Retido recebido',d.totals.withheld_paid],['Líquido recebido',d.totals.net_paid],['KF recebido (separado)',d.totals.kf_refund],['Líquido esperado conhecido, não pago',d.totals.expected_net]].forEach(([l,v])=>{const n=document.createElement('p');n.textContent=l+': '+amount(v);totals.append(n)});
 const caveat=document.createElement('p');caveat.textContent='Base fictícia: '+d.as_of+'. '+d.incomplete_expected+' evento(s) esperado(s) com valor incompleto; não incluídos no total líquido conhecido.';totals.append(caveat);
 const select=el('income-asset');select.replaceChildren(new Option('Todos',''));[...new Set(d.events.map(e=>e.ticker))].sort().forEach(t=>select.append(new Option(t,t)));
 el('income-period').onchange=periods;periods();
 ['income-asset','income-state','income-date','income-month'].forEach(id=>el(id).onchange=events);events();
}
function reset(){el('income-period').value='monthly';periods();el('income-asset').value='';el('income-state').value='';el('income-date').value='payment_date';el('income-month').value='';events();}
root.InvestorIncome={render,reset};
})(globalThis);
