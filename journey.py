"""Synthetic merchant journey; no provider calls or real-world side effects."""
class Journey:
 def __init__(self, db):
  self.db=db
  self.db.executescript('''CREATE TABLE IF NOT EXISTS enquiries(id TEXT PRIMARY KEY, item TEXT NOT NULL, customer TEXT NOT NULL); CREATE TABLE IF NOT EXISTS quotes(id TEXT PRIMARY KEY, enquiry_id TEXT NOT NULL, amount INTEGER NOT NULL, status TEXT NOT NULL); CREATE TABLE IF NOT EXISTS service_requests(id TEXT PRIMARY KEY, case_id TEXT NOT NULL, status TEXT NOT NULL);''')
 def create_enquiry(self, id, customer, item):
  if not all(isinstance(x,str) and 0<len(x)<=100 for x in (id, customer, item)):raise ValueError('invalid enquiry')
  with self.db:self.db.execute('INSERT OR IGNORE INTO enquiries VALUES(?,?,?)',(id,item,customer))
  return self.db.execute('SELECT id,customer,item FROM enquiries WHERE id=?',(id,)).fetchone()
 def create_quote(self, id, enquiry_id, amount):
  if not isinstance(amount,int) or not 0<amount<=1000000:raise ValueError('invalid amount')
  if not self.db.execute('SELECT 1 FROM enquiries WHERE id=?',(enquiry_id,)).fetchone():raise ValueError('enquiry missing')
  with self.db:self.db.execute('INSERT OR IGNORE INTO quotes VALUES(?,?,?,?)',(id,enquiry_id,amount,'draft'))
  return self.db.execute('SELECT * FROM quotes WHERE id=?',(id,)).fetchone()
 def approve_quote(self,id):
  with self.db:
   c=self.db.execute("UPDATE quotes SET status='approved' WHERE id=?",(id,))
   if not c.rowcount:raise ValueError('quote missing')
  return self.db.execute('SELECT * FROM quotes WHERE id=?',(id,)).fetchone()
 def request_service(self,id,case_id):
  case=self.db.execute('SELECT order_status FROM cases WHERE id=?',(case_id,)).fetchone()
  if not case or case[0]!='delivered':return {'status':'escalate','reason':'delivery not verified'}
  with self.db:self.db.execute('INSERT OR IGNORE INTO service_requests VALUES(?,?,?)',(id,case_id,'requested'))
  return {'status':'requested','case_id':case_id}
