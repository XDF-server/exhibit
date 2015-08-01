# *-* coding:utf-8 *-*

import MySQLdb 
from gl import LOG
from base import Base

class Mysql(object):

	def __init__(self):
	
		self.conn = None
		self.cur = None
	
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

		except MySQLdb.Warning,w:
			print "Warning:%s" % str(w)

		except MySQLdb.Error,e:
			print "Error:%s" % str(e) 

	def query(self,sql):
		
		try:
			self.conn = MySQLdb.connect(
					host = '172.18.4.181',
					port = 3306,
					user = 'admintest',
					passwd = 'dsjw2015',
					db = 'neworiental_v2',
					charset = 'utf8')
			

			self.cur.execute(sql)	
		
		except MySQLdb.Warning,w:
			LOG.warn('Warning:%s' % str(w))

		except MySQLdb.Error,e:
			LOG.warn('Error:%s' % str(e))

		return self.cur.fetchone()

	def __def__(self):

		self.conn.close()
		
