import unittest
from orchestrator import Sandbox
from journey import Journey
class JourneyTests(unittest.TestCase):
 def setUp(self):self.s=Sandbox();self.j=Journey(self.s.db)
 def create_order(self,n):
  self.j.create_enquiry('E'+n,'Synthetic customer','Mixer');self.j.create_quote('Q'+n,'E'+n,4200);return self.j.approve_quote('Q'+n)['order_id']
 def test_end_to_end(self):
  c=self.create_order('1');self.assertEqual(self.j.approve_quote('Q1')['order_id'],c);self.assertEqual(self.s.execute(c,'confirm_order','early')['status'],'escalate');self.j.capture_payment(c);self.assertEqual(self.s.execute(c,'confirm_order','early')['status'],'confirmed');self.assertEqual(self.s.execute(c,'confirm_order','early')['replayed'],True);self.assertEqual(self.j.mark_delivered(c)['status'],'delivered');self.assertEqual(self.j.request_service('S1',c,as_of='2026-10-23')['status'],'requested');self.assertEqual(self.j.schedule('S1','Technician A','10:00')['status'],'scheduled');self.assertTrue(self.j.schedule('S1','Technician A','10:00')['replayed'])
 def test_warranty_and_conflict(self):
  c=self.create_order('1');self.assertEqual(self.j.request_service('S1',c)['status'],'escalate');self.j.capture_payment(c);self.s.execute(c,'confirm_order','k');self.j.mark_delivered(c);self.assertEqual(self.j.request_service('expired',c,as_of='2028-01-01')['status'],'escalate');self.j.request_service('S1',c,as_of='2026-10-23');self.j.request_service('S2',c,as_of='2026-10-23');self.j.schedule('S1','Technician A','10:00');self.assertEqual(self.j.schedule('S2','Technician A','10:00')['status'],'slot_unavailable');self.assertEqual(self.j.schedule('S2','Technician B','10:00')['status'],'scheduled')
 def test_invalid_quote(self):self.assertRaises(ValueError,self.j.create_quote,'Q','missing',1)
if __name__=='__main__':unittest.main()
