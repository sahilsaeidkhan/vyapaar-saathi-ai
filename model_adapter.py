"""OpenRouter-compatible tool proposal adapter; credentials supplied through environment."""
import json,os,urllib.request
class ModelAdapter:
 def __init__(self):
  self.url=os.environ['MODEL_API_URL'];self.key=os.environ['MODEL_API_KEY'];self.model=os.environ['MODEL_NAME']
  if self.url!='https://openrouter.ai/api/v1/chat/completions' or self.model!='openrouter/free':raise ValueError('Only the approved free route is supported')
 def __call__(self,context):
  schema={'type':'object','properties':{'action':{'type':'string','enum':['confirm_order','initiate_refund','escalate']},'rationale':{'type':'string'}},'required':['action','rationale'],'additionalProperties':False}
  payload={'model':self.model,'messages':[{'role':'system','content':'Propose one safe next action using only supplied synthetic evidence. Pending or missing payment requires escalation. The executor independently enforces approval. Never claim refund credit without evidence.'},{'role':'user','content':json.dumps(context)}], 'tools':[{'type':'function','function':{'name':'propose_action','description':'Propose a single action for independent policy validation','parameters':schema}}], 'tool_choice':{'type':'function','function':{'name':'propose_action'}},'temperature':0}
  req=urllib.request.Request(self.url,data=json.dumps(payload).encode(),headers={'Authorization':'Bearer '+self.key,'Content-Type':'application/json'},method='POST')
  with urllib.request.urlopen(req,timeout=45) as res:data=json.load(res)
  calls=data['choices'][0]['message'].get('tool_calls',[])
  if len(calls)!=1 or calls[0]['function']['name']!='propose_action':raise ValueError('No valid tool proposal')
  result=json.loads(calls[0]['function']['arguments'])
  if not isinstance(result,dict) or set(result)!={'action','rationale'} or result['action'] not in ('confirm_order','initiate_refund','escalate') or not isinstance(result['rationale'],str):raise ValueError('Invalid proposal')
  return result
