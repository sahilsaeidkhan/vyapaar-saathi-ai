const assert=require('node:assert/strict');const {cases,run}=require('./engine.js');
const expected=['Order confirmed','Waiting','Approval required','Existing order verified','Human decision required','Credit unconfirmed','Human investigation required','Service request created'];
for(let i=0;i<cases.length;i++)assert.equal(run(cases[i]).status,expected[i],cases[i].id);
assert.equal(run(cases[2],{approved:true}).status,'Refund initiated, credit unconfirmed');assert.equal(run(cases[2],{approved:true,credited:true}).status,'Credit confirmed (simulated)');assert.equal(run(cases[5],{credited:true}).status,'Credit confirmed (simulated)');
// Baseline always promises confirmation for any captured payment and otherwise asks for another payment.
// Hand-labelled expected decision on seven payment cases; service excluded.
const labels=['confirm','wait','approval','verify','escalate','wait-credit','escalate'];
const baseline=cases.slice(0,7).map(c=>c.payments.includes('captured')?'confirm':'retry');
const mapping={'Order confirmed':'confirm','Waiting':'wait','Approval required':'approval','Existing order verified':'verify','Human decision required':'escalate','Credit unconfirmed':'wait-credit','Human investigation required':'escalate'};
const proposed=cases.slice(0,7).map(c=>mapping[run(c).status]);
console.log(`Tests passed: 8 case decisions and 3 refund state checks. Synthetic benchmark: baseline ${baseline.filter((x,i)=>x===labels[i]).length}/7; prototype ${proposed.filter((x,i)=>x===labels[i]).length}/7. Hand-authored scenarios; not a general performance estimate.`);


