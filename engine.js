(function(root){
const cases=[
{id:'late',name:'Late payment success',customer:'Asha Mehta',item:'Mixer grinder',amount:4200,quote:'Approved Q-101',order:'awaiting payment',payments:['failed','captured'],stock:2,messages:1,service:'Warranty eligible after delivery',type:'late'},
{id:'pending',name:'Pending is not failed',customer:'Ravi Das',item:'Induction cooktop',amount:3100,quote:'Approved Q-102',order:'awaiting payment',payments:['pending'],stock:3,messages:1,service:'No service request',type:'pending'},
{id:'duplicate',name:'Two successful payments',customer:'Neha Jain',item:'Air purifier',amount:8900,quote:'Approved Q-103',order:'confirmed',payments:['captured','captured'],stock:1,messages:2,service:'No service request',type:'duplicate'},
{id:'timeout',name:'Action timed out',customer:'Imran Khan',item:'Ceiling fan',amount:2800,quote:'Approved Q-104',order:'confirmed in backend',payments:['captured'],stock:1,messages:2,service:'No service request',type:'timeout'},
{id:'race',name:'Last item sold at counter',customer:'Priya Rao',item:'Microwave',amount:11200,quote:'Approved Q-105',order:'awaiting confirmation',payments:['captured'],stock:0,messages:1,service:'No service request',type:'race'},
{id:'refund',name:'Refund initiated',customer:'Kabir Sen',item:'Electric kettle',amount:1900,quote:'Approved Q-106',order:'cancelled',payments:['captured'],stock:4,messages:1,service:'No service request',type:'refund'},
{id:'missing',name:'Missing payment record',customer:'Sana Ali',item:'Water purifier',amount:6500,quote:'Approved Q-107',order:'awaiting payment',payments:[],stock:1,messages:1,service:'No service request',type:'missing'},
{id:'service',name:'Warranty service request',customer:'Asha Mehta',item:'Mixer grinder',amount:4200,quote:'Approved Q-101',order:'delivered',payments:['captured'],stock:1,messages:1,service:'Warranty record found; booking requested',type:'service'}];
function run(c,state){state=state||{};let title,steps=[],status,approval=false,advance=false;
switch(c.type){case 'late':title='Confirm the paid order';steps=['Check latest payment record: one captured payment.','Recheck stock before confirming one order.','Send a simulated confirmation linked to the existing order.'];status='Order confirmed';break;
case 'pending':title='Wait for a final payment status';steps=['Payment is pending. Do not ask for another payment or confirm fulfilment.','Schedule a simulated recheck; escalate if unresolved.'];status='Waiting';break;
case 'duplicate':title='One order, possible extra payment';steps=['Two captured attempts belong to one order.','Keep one order. Request merchant approval for the extra payment refund.','Duplicate customer messages are grouped into one case.'];status=state.approved?'Refund initiated, credit unconfirmed':'Approval required';approval=!state.approved;advance=!!state.approved&&!state.credited;if(state.credited)status='Credit confirmed (simulated)';break;
case 'timeout':title='Verify before retrying';steps=['The order action timed out, but backend lookup shows the order already confirmed.','Reuse the existing order; do not create a second one.','Group duplicate customer messages into one case.'];status='Existing order verified';break;
case 'race':title='Escalate stock conflict';steps=['Payment captured, but the last unit was sold at the counter.','Do not confirm fulfilment. Ask the merchant to arrange stock or approve a refund.'];status='Human decision required';break;
case 'refund':title='Refund is in progress';steps=['The refund was initiated. Bank submission does not establish customer credit.','Communicate the current status and wait for evidence of credit.'];status=state.credited?'Credit confirmed (simulated)':'Credit unconfirmed';advance=!state.credited;break;
case 'missing':title='Escalate missing evidence';steps=['No payment record matches the order.','Do not confirm, refund or request another payment based on incomplete evidence.'];status='Human investigation required';break;
case 'service':title='Create simulated service booking';steps=['Check the linked delivered order and warranty record.','Create one simulated service request for merchant follow-up.'];status='Service request created';break;}
return {title,steps,status,approval,advance};}
root.VS={cases,run};if(typeof module!=='undefined')module.exports=root.VS;
})(typeof globalThis!=='undefined'?globalThis:this);
