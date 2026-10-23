(function(root){
 class DemoJourney{
  constructor(saved={}){this.cases=saved.cases||{};this.bookings=saved.bookings||{};this.timeline=saved.timeline||[];}
  act(id,operation,technician='Technician A',slot='10:00'){const result=this._act(id,operation,technician,slot);this.timeline.push({case:id,action:operation,status:result.status});return result;}
  _act(id,operation,technician='Technician A',slot='10:00'){
   if(!id)return {status:'blocked',reason:'Select a case.'};
   let c=this.cases[id]||(this.cases[id]={quote:'none',order:'none',payment:'pending',stock:1,warranty:false,service:'none'});
   if(operation==='requirements'){c.requirements='Home-use appliance · synthetic requirement';return {status:'requirements recorded',requirements:c.requirements};}
   if(operation==='quote'){if(!c.requirements)return {status:'blocked',reason:'Record the requirements first.'};if(c.quote==='none')c.quote='draft';return {status:c.quote,record:'Synthetic enquiry and quote'};}
   if(operation==='approve'){if(c.quote==='none')return {status:'blocked',reason:'Create the quote first.'};c.quote='approved';if(c.order==='none')c.order='pending';return {status:'approved',order:'order:'+id,payment:c.payment};}
   if(c.order==='none')return {status:'blocked',reason:'Approve the quote first.'};
   if(operation==='capture'){c.payment='captured';return {status:'captured',synthetic:true};}
   if(operation==='confirm'){if(c.order==='confirmed'||c.order==='delivered')return {status:'already confirmed',stock:c.stock};if(c.payment!=='captured'||c.stock<1)return {status:'blocked',reason:'Payment and stock must be verified.'};c.order='confirmed';c.stock--;return {status:'confirmed',stock:c.stock};}
   if(operation==='deliver'){if(c.order!=='confirmed'&&c.order!=='delivered')return {status:'blocked',reason:'Confirm the order first.'};c.order='delivered';c.warranty=true;return {status:'delivered',warranty:'valid (synthetic)'};}
   if(operation==='service'){if(c.order!=='delivered'||!c.warranty)return {status:'blocked',reason:'Delivery and valid warranty required.'};if(c.service==='none')c.service='requested';return {status:c.service,warranty:'valid (synthetic)'};}
   if(operation==='close'){if(c.service!=='scheduled'&&c.service!=='completed')return {status:'blocked',reason:'Schedule the service first.'};c.service='completed';return {status:'completed',evidence:'Synthetic technician completion recorded'};}
   if(operation==='schedule'){if(c.service==='none')return {status:'blocked',reason:'Request service first.'};if(c.booking)return {status:'scheduled',...c.booking,replayed:true};let key=technician+'|'+slot;if(this.bookings[key]&&this.bookings[key]!==id)return {status:'slot unavailable',reason:'Choose a different technician or slot.'};this.bookings[key]=id;c.booking={technician,slot};c.service='scheduled';return {status:'scheduled',...c.booking};}
   return {status:'blocked',reason:'Unknown action.'};
  }
 }
 root.DemoJourney=DemoJourney;if(typeof module!=='undefined')module.exports={DemoJourney};
})(typeof globalThis!=='undefined'?globalThis:this);
