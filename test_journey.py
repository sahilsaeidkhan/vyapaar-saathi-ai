import unittest
from orchestrator import Sandbox
from journey import Journey
class JourneyTests(unittest.TestCase):
 def test_quote_flow(self):
  s=Sandbox();j=Journey(s.db);self.assertEqual(j.create_enquiry('E','Synthetic customer','Mixer')[2],'Mixer');self.assertEqual(j.create_quote('Q','E',4200)[3],'draft');self.assertEqual(j.approve_quote('Q')[3],'approved');self.assertRaises(ValueError,j.create_quote,'bad','missing',1)
 def test_service_requires_delivered_order(self):
  s=Sandbox();s.seed('pending');s.seed('delivered',order='delivered');j=Journey(s.db);self.assertEqual(j.request_service('S1','pending')['status'],'escalate');self.assertEqual(j.request_service('S2','delivered')['status'],'requested');self.assertEqual(j.request_service('S2','delivered')['status'],'requested');self.assertEqual(s.db.execute('SELECT COUNT(*) FROM service_requests').fetchone()[0],1)
if __name__=='__main__':unittest.main()
