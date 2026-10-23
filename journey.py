"""Local synthetic sales-to-service workflow; all records are fictional."""
import sqlite3
from datetime import date
class Journey:
 def __init__(self,db):
  self.db=db
  self.db.executescript('''CREATE TABLE IF NOT EXISTS enquiries(id TEXT PRIMARY KEY,item TEXT NOT NULL,customer TEXT NOT NULL);CREATE TABLE IF NOT EXISTS quotes(id TEXT PRIMARY KEY,enquiry_id TEXT NOT NULL,amount INTEGER NOT NULL,status TEXT NOT NULL);CREATE TABLE IF NOT EXISTS service_requests(id TEXT PRIMARY KEY,case_id TEXT NOT NULL,status TEXT NOT NULL);CREATE TABLE IF NOT EXISTS journey_orders(id TEXT PRIMARY KEY,quote_id TEXT NOT NULL UNIQUE,case_id TEXT NOT NULL UNIQUE);CREATE TABLE IF NOT EXISTS warranties(case_id TEXT PRIMARY KEY,expires_on TEXT NOT NULL);CREATE TABLE IF NOT EXISTS appointments(service_id TEXT PRIMARY KEY,technician TEXT NOT NULL,slot TEXT NOT NULL,UNIQUE(technician,slot));''')
 def create_enquiry(self,id,customer,item):
  if not all(isinstance(x,str) and 0<len(x)<=100 for x in (id,customer,item)):raise ValueError('invalid enquiry')
  with self.db:self.db.execute('INSERT OR IGNORE INTO enquiries VALUES(?,?,?)',(id,item,customer))
  return self.db.execute('SELECT id,customer,item FROM enquiries WHERE id=?',(id,)).fetchone()
 def create_quote(self,id,enquiry_id,amount):
  if type(amount)!=int or not 0<amount<=1000000:raise ValueError('invalid amount')
  if not self.db.execute('SELECT 1 FROM enquiries WHERE id=?',(enquiry_id,)).fetchone():raise ValueError('enquiry missing')
  with self.db:self.db.execute('INSERT OR IGNORE INTO quotes VALUES(?,?,?,?)',(id,enquiry_id,amount,'draft'))
  return self.db.execute('SELECT * FROM quotes WHERE id=?',(id,)).fetchone()
 def approve_quote(self,id):
  case_id='order:'+id
  with self.db:
   quote=self.db.execute('SELECT * FROM quotes WHERE id=?',(id,)).fetchone()
   if not quote:raise ValueError('quote missing')
   self.db.execute("UPDATE quotes SET status='approved' WHERE id=?",(id,))
   self.db.execute('INSERT OR IGNORE INTO cases VALUES(?,?,?,?,?)',(case_id,'pending',1,'pending','none'))
   self.db.execute('INSERT OR IGNORE INTO journey_orders VALUES(?,?,?)',('order:'+id,id,case_id))
  payment=self.db.execute('SELECT payment FROM cases WHERE id=?',(case_id,)).fetchone()[0]
  return {'quote_id':id,'quote_status':'approved','order_id':case_id,'payment':payment}
 def capture_payment(self,case_id):
  with self.db:
   if not self.db.execute('SELECT 1 FROM journey_orders WHERE case_id=?',(case_id,)).fetchone():raise ValueError('order missing')
   self.db.execute("UPDATE cases SET payment='captured' WHERE id=?",(case_id,))
  return {'order_id':case_id,'payment':'captured','synthetic':True}
 def mark_delivered(self,case_id):
  with self.db:
   case=self.db.execute('SELECT order_status FROM cases WHERE id=?',(case_id,)).fetchone()
   if not case or case[0] not in ('confirmed','delivered'):return {'status':'escalate','reason':'order must be confirmed first'}
   self.db.execute("UPDATE cases SET order_status='delivered' WHERE id=?",(case_id,))
   self.db.execute('INSERT OR IGNORE INTO warranties VALUES(?,?)',(case_id,'2027-12-31'))
  return {'status':'delivered','warranty_expires':'2027-12-31','synthetic':True}
 def request_service(self,id,case_id,as_of=None):
  today=as_of or date.today().isoformat()
  row=self.db.execute('SELECT c.order_status,w.expires_on FROM cases c LEFT JOIN warranties w ON w.case_id=c.id WHERE c.id=?',(case_id,)).fetchone()
  if not row or row[0]!='delivered' or not row[1] or row[1]<today:return {'status':'escalate','reason':'delivery or warranty not eligible'}
  with self.db:self.db.execute('INSERT OR IGNORE INTO service_requests VALUES(?,?,?)',(id,case_id,'requested'))
  return {'status':'requested','case_id':case_id,'warranty_expires':row[1]}
 def schedule(self,service_id,technician,slot):
  if technician not in ('Technician A','Technician B') or slot not in ('10:00','14:00'):raise ValueError('invalid synthetic slot')
  with self.db:
   if not self.db.execute('SELECT 1 FROM service_requests WHERE id=?',(service_id,)).fetchone():raise ValueError('service request missing')
   prior=self.db.execute('SELECT technician,slot FROM appointments WHERE service_id=?',(service_id,)).fetchone()
   if prior:return {'status':'scheduled','technician':prior[0],'slot':prior[1],'replayed':True}
   try:self.db.execute('INSERT INTO appointments VALUES(?,?,?)',(service_id,technician,slot))
   except sqlite3.IntegrityError:return {'status':'slot_unavailable'}
   self.db.execute("UPDATE service_requests SET status='scheduled' WHERE id=?",(service_id,))
  return {'status':'scheduled','technician':technician,'slot':slot}
