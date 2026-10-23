import io,json,os,unittest
from unittest.mock import patch
from model_adapter import ModelAdapter
class Response(io.BytesIO):
 def __enter__(self):return self
 def __exit__(self,*a):self.close()
class AdapterTests(unittest.TestCase):
 def setUp(self):self.env=patch.dict(os.environ,{'MODEL_API_URL':'https://openrouter.ai/api/v1/chat/completions','MODEL_NAME':'openrouter/free','MODEL_API_KEY':'test-key'});self.env.start()
 def tearDown(self):self.env.stop()
 def test_valid(self):
  result={'choices':[{'message':{'tool_calls':[{'function':{'name':'propose_action','arguments':json.dumps({'action':'escalate','rationale':'pending'})}}]}}]}
  with patch('urllib.request.urlopen',return_value=Response(json.dumps(result).encode())) as request:
   self.assertEqual(ModelAdapter()({'evidence':{}})['action'],'escalate');body=json.loads(request.call_args.args[0].data);self.assertEqual(body['model'],'openrouter/free');self.assertEqual(body['tools'][0]['function']['name'],'propose_action')
 def test_invalid(self):
  result={'choices':[{'message':{'tool_calls':[{'function':{'name':'propose_action','arguments':'{"action":"send_money","rationale":"x"}'}}]}}]}
  with patch('urllib.request.urlopen',return_value=Response(json.dumps(result).encode())):self.assertRaises(ValueError,ModelAdapter(),{})
if __name__=='__main__':unittest.main()
