"""Optional OpenAI-compatible chat-completions adapter. Configure via environment; no secrets stored."""
import json, os, urllib.request
class ModelAdapter:
 def __init__(self):
  self.url=os.environ['MODEL_API_URL'];self.key=os.environ['MODEL_API_KEY'];self.model=os.environ['MODEL_NAME']
  if not self.url.startswith('https://'):raise ValueError('HTTPS endpoint required')
 def __call__(self,context):
  payload={'model':self.model,'messages':[{'role':'system','content':'Return only JSON with action and rationale. Choose exactly one allowed action based only on provided evidence. Never claim customer credit without evidence. You cannot approve refunds.'},{'role':'user','content':json.dumps(context)}], 'response_format':{'type':'json_object'},'temperature':0}
  req=urllib.request.Request(self.url,data=json.dumps(payload).encode(),headers={'Authorization':'Bearer '+self.key,'Content-Type':'application/json'},method='POST')
  with urllib.request.urlopen(req,timeout=20) as res: data=json.load(res)
  return json.loads(data['choices'][0]['message']['content'])
