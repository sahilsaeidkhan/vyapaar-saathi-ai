"""Local-only synthetic agent server. Never expose this development server to the internet."""
import json, os
from http.server import SimpleHTTPRequestHandler,HTTPServer
from pathlib import Path
from orchestrator import Sandbox,orchestrate
from model_adapter import ModelAdapter
from journey import Journey
ROOT=Path(__file__).parent
sandbox=Sandbox(str(Path(__file__).parent/'sandbox.db'))
for case,payment,stock,order in [('late','captured',2,'pending'),('pending','pending',3,'pending'),('duplicate','captured',1,'confirmed'),('timeout','captured',1,'confirmed'),('race','captured',0,'pending'),('refund','captured',4,'cancelled'),('missing','missing',1,'pending'),('service','captured',1,'delivered')]: sandbox.seed(case,payment,stock,order)
journey=Journey(sandbox.db)
class Handler(SimpleHTTPRequestHandler):
 def __init__(self,*a,**k):super().__init__(*a,directory=str(ROOT),**k)
 def do_GET(self):
  if self.path=='/api/health':
   body=b'{"synthetic":true}';self.send_response(200);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body);return
  super().do_GET()
 def do_POST(self):
  if self.path not in ('/api/run','/api/configure','/api/journey'):self.send_error(404);return
  if self.headers.get('Origin')!='http://127.0.0.1:8766' or self.headers.get('Content-Type')!='application/json':self.send_error(403);return
  try:
   n=int(self.headers.get('Content-Length','0'))
   if n<1 or n>5000:raise ValueError('invalid request length')
   data=json.loads(self.rfile.read(n))
   if self.path=='/api/configure':
    key=data.get('key','')
    if not isinstance(key,str) or not key.startswith('sk-or-v1-') or len(key)>300:raise ValueError('invalid key')
    os.environ['MODEL_API_KEY']=key;os.environ['MODEL_API_URL']='https://openrouter.ai/api/v1/chat/completions';os.environ['MODEL_NAME']='openrouter/free'
    body=b'{"configured":true}';self.send_response(200);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body);return
   if self.path=='/api/journey':
    op=data.get('operation');case_id=data.get('case_id')
    if case_id not in ('late','pending','duplicate','timeout','race','refund','missing','service'):raise ValueError('unknown case')
    if op=='enquiry_quote':
     enquiry=journey.create_enquiry('enquiry:'+case_id,'Synthetic customer','Synthetic appliance')
     quote=journey.create_quote('quote:'+case_id,enquiry[0],4200)
     result={'enquiry':enquiry,'quote':quote}
    elif op=='approve_quote':result=journey.approve_quote('quote:'+case_id)
    elif op=='capture':result=journey.capture_payment('order:quote:'+case_id)
    elif op=='confirm':result=sandbox.execute('order:quote:'+case_id,'confirm_order','journey-confirm:'+case_id)
    elif op=='deliver':result=journey.mark_delivered('order:quote:'+case_id)
    elif op=='journey_service':result=journey.request_service('journey-service:'+case_id,'order:quote:'+case_id)
    elif op=='schedule':result=journey.schedule('journey-service:'+case_id,data.get('technician','Technician A'),data.get('slot','10:00'))
    elif op=='service':result=journey.request_service('service:'+case_id,case_id)
    else:raise ValueError('unknown operation')
    body=json.dumps(result).encode();self.send_response(200);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body);return
   id=data.get('case_id','');request=data.get('request','')
   if id not in ('late','pending','duplicate','timeout','race','refund','missing','service'):raise ValueError('unknown case')
   if os.environ.get('MODEL_API_KEY'):
    model=ModelAdapter();mode='configured model'
   else:
    # Offline planner is deterministic and conservative. Service is excluded from executor.
    action={'late':'confirm_order','duplicate':'initiate_refund','timeout':'confirm_order'}.get(id,'escalate')
    model=lambda context:{'action':action,'rationale':'Offline demonstration policy'};mode='offline rules'
   result=orchestrate(model,sandbox,id,request,approved=(data.get('approve') is True));result['mode']=mode;result['after']=sandbox.evidence(id)
   body=json.dumps(result).encode();self.send_response(200);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body)
  except Exception:
   body=b'{"error":"Request failed. Check model configuration and retry."}';self.send_response(400);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body)
if __name__=='__main__':
 print('Synthetic demo: http://127.0.0.1:8766',flush=True);HTTPServer(('127.0.0.1',8766),Handler).serve_forever()



