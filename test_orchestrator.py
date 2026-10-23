import unittest
from orchestrator import Sandbox,orchestrate
class SafetyTests(unittest.TestCase):
 def test_retry(self):
  s=Sandbox();s.seed('A');a=s.execute('A','confirm_order','k');self.assertEqual(a,s.execute('A','confirm_order','k'));self.assertEqual(s.evidence('A')['stock'],0)
 def test_pending_and_stock(self):
  s=Sandbox();s.seed('B','pending');s.seed('C','captured',0);self.assertEqual(s.execute('B','confirm_order','b')['status'],'escalate');self.assertEqual(s.execute('C','confirm_order','c')['status'],'escalate')
 def test_refund(self):
  s=Sandbox();s.seed('D');self.assertEqual(s.execute('D','initiate_refund','d')['status'],'approval_required');self.assertEqual(s.execute('D','initiate_refund','approved',True)['status'],'initiated_not_credited')
 def test_untrusted_model(self):
  s=Sandbox();s.seed('E','pending');r=orchestrate(lambda _: {'action':'confirm_order'},s,'E','paid');self.assertEqual(r['result']['status'],'escalate')
 def test_key_conflict_and_missing(self):
  s=Sandbox();s.seed('F');s.execute('F','escalate','k');self.assertRaises(ValueError,s.execute,'F','confirm_order','k');self.assertEqual(s.execute('missing','confirm_order','x')['status'],'escalate')
if __name__=='__main__':unittest.main()
