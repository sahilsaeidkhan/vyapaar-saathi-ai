"""Model-agnostic synthetic executor. Model adapter must return a structured action."""
import json, sqlite3
class Sandbox:
 def __init__(self,path=':memory:'):
  self.db=sqlite3.connect(path);self.db.executescript('CREATE TABLE IF NOT EXISTS cases(id TEXT PRIMARY KEY,payment TEXT,stock INTEGER,order_status TEXT,refund_status TEXT); CREATE TABLE IF NOT EXISTS actions(key TEXT PRIMARY KEY,case_id TEXT,action TEXT,result TEXT); CREATE TABLE IF NOT EXISTS events(id INTEGER PRIMARY KEY,case_id TEXT,event TEXT);')
 def seed(self,id,payment='captured',stock=1,order='pending'):
  self.db.execute('INSERT OR IGNORE INTO cases VALUES(?,?,?,?,?)',(id,payment,stock,order,'none'));self.db.commit()
 def evidence(self,id):
  row=self.db.execute('SELECT * FROM cases WHERE id=?',(id,)).fetchone()
  if not row:return None
  case=dict(zip(('id','payment','stock','order_status','refund_status'),row))
  # Synthetic fixture evidence; production must verify provider records.
  case['captured_attempts']=2 if id=='duplicate' else (1 if case['payment']=='captured' else 0)
  return case
 def execute(self,id,action,key,approved=False):
  if not key: raise ValueError('idempotency key required')
  with self.db:
   prior=self.db.execute('SELECT case_id,action,result FROM actions WHERE key=?',(key,)).fetchone()
   if prior:
    if prior[:2]!=(id,action):raise ValueError('idempotency key conflict')
    return {**json.loads(prior[2]),'replayed':True}
   c=self.evidence(id)
   if not c:r={'status':'escalate','reason':'missing case'}
   elif action=='confirm_order':
    if c['order_status']=='confirmed':r={'status':'already_confirmed'}
    elif c['payment']!='captured' or c['stock']<1:r={'status':'escalate','reason':'payment or stock unverified'}
    else:self.db.execute('UPDATE cases SET order_status=?,stock=stock-1 WHERE id=?',('confirmed',id));r={'status':'confirmed'}
   elif action=='initiate_refund':
    if not approved:return {'status':'approval_required'}
    elif c['payment']!='captured' or c['captured_attempts']<2:r={'status':'escalate','reason':'duplicate captured payments not verified'}
    elif c['refund_status']!='none':r={'status':'already_initiated'}
    else:self.db.execute('UPDATE cases SET refund_status=? WHERE id=?',('initiated',id));r={'status':'initiated_not_credited'}
   elif action=='escalate':r={'status':'escalated'}
   else:r={'status':'rejected','reason':'unknown action'}
   self.db.execute('INSERT INTO actions VALUES(?,?,?,?)',(key,id,action,json.dumps(r)));self.db.execute('INSERT INTO events(case_id,event) VALUES(?,?)',(id,json.dumps({'action':action,'result':r})));return r

def orchestrate(model,sandbox,case_id,request,approved=False):
 evidence=sandbox.evidence(case_id);proposal=model({'request':request,'evidence':evidence,'allowed_actions':['confirm_order','initiate_refund','escalate']})
 if not isinstance(proposal,dict) or proposal.get('action') not in ('confirm_order','initiate_refund','escalate'):return {'status':'rejected','reason':'invalid model output'}
 action=proposal['action'];return {'proposal':proposal,'evidence':evidence,'result':sandbox.execute(case_id,action,case_id+':'+action,approved)}


