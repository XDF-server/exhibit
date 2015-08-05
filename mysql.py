# *-* coding:utf-8 *-*

import MySQLdb 
from base import Base
from exception import DBException
from base import Base
from gl import LOG
from design_model import singleton

@singleton
class Mysql(object):

	def __init__(self):
	
		self.conn = None
		self.cur = None
		self.sql = ''
		self.status_enum = Base.enum(CONN_SUC = 0,CONN_ERR= -1,QUERY_SUC = 1,QUERY_ERR = -2,QUERY_WAR = 2,EVENT_SUC = 3,EVENT_ERR = -3,OTHER_ERR = -4)
		self.status = 0
		self.event_flag = False
	
	def connect_master(self):

		host = Base.get_config('SCHOOLIP_DB','host')
		port = Base.get_config('SCHOOLIP_DB','port')
		user = Base.get_config('SCHOOLIP_DB','user')
		passwd = Base.get_config('SCHOOLIP_DB','passwd')
		db = Base.get_config('SCHOOLIP_DB','db')
		charset = Base.get_config('SCHOOLIP_DB','charset')

		try:
			self.conn = MySQLdb.connect(
					host = host,
					port = int(port),
					user = user,
					passwd = passwd,
					db = db,
					charset = charset)
			
			self.cur = self.conn.cursor()

		except MySQLdb.Error,e:
			self.status = self.status_enum.CONN_ERR
			msg = "Error:%s" % str(e) 
			LOG.error('Error:%s' % str(e))
			raise DBException(msg)
	
	def connect_test(self):

		try:
			self.conn = MySQLdb.connect(
					host = '127.0.0.1',
					port = 3306,
					user = 'root',
					passwd = '1a2s3dqwe', 
					db = 'test',
					charset = 'utf8')
			
			self.cur = self.conn.cursor()

		except MySQLdb.Error,e:
			self.status = self.status_enum.CONN_ERR
			msg = "Error:%s" % str(e) 
			LOG.error('Error:%s' % str(e))
			raise DBException(msg)

	def start_event(self):

		self.event_flag = True

	def exec_event(self,sql,**kwds):

		if self.event_flag:

			self.query(sql,**kwds)
		else:
			self.status = self.status_enum.EVENT_ERR
			raise DBException('event failed')

	def end_event(self):

		self.commit()
		self.event_flag = False

	def get_last_id(self):

		return int(self.conn.insert_id())

	def get_status(self):
		
		return self.status
	
	def commit(self):
		
		self.conn.commit()

	def rollback(self):

		self.conn.rollback()

	def query(self,sql,**kwds):
		
		try:
			self.sql = sql % kwds
			print self.sql
			self.cur.execute(self.sql)	
		
		except MySQLdb.Warning,w:
			LOG.warn('Warning:%s' % str(w))
			self.status = self.status_enum.QUERY_WAR

		except MySQLdb.Error,e:
			self.rollback()
			self.event_flag = False
			LOG.error('Error:%s' % str(e))
			self.status = self.status_enum.QUERY_ERR
			raise DBException('query failed')
		
		except:
			self.status = self.status_enum.OTHER_ERR
			LOG.error('format failed')
			raise DBException('format failed')
		
		return self.cur.fetchone() if self.cur.fetchone() else 'sucess'

	def get_last_sql(self):
				
		return self.sql

	def __def__(self):

		self.conn.close()
	
	
