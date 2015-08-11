# *-* coding:utf-8 *-*

from mysql import Mysql
from gl import LOG
from exception import DBException,CKException

class Business(object):


	@staticmethod
	def is_topic(topic_id):
		
		mysql = Mysql()
		
		query_sql = "select 1 from entity_topic where id = %(topic_id)d;" 
		
		try:
			if mysql.query(query_sql,topic_id = int(topic_id)) is not None:
				return True
			else:
				return False

		except DBException as e:
			LOG.error('check topic error [%s]' % e)
			raise CKException('check topic error')

	@staticmethod
	def is_seriess(seriess_id):
		
		mysql = Mysql()
		
		query_sql = "select 1 from entity_seriess where id = %(seriess_id)d;"
		
		try:
			if mysql.query(query_sql,seriess_id = int(seriess_id)) is not None:
				return True
			else:
				return False

		except DBException as e:
			LOG.error('check seriess error [%s]' % e)
			raise CkException('check seriess error')
	@staticmethod
	def q_type_filter_num(type):

		mysql = Mysql()

		query_sql = "select count(*) from entity_question_new where type = '%(type)s';"	

		try:
			if mysql.query(query_sql,type = type) is not None:
				return mysql.fetchall()[0][0]

			else:
				return None

		except DBException as e:
			LOG.error('filtet type error [%s]' % e)
			raise CkException('filter type error')

	@staticmethod
	def q_type_filter(type,start,num):

		mysql = Mysql()

		query_sql = "select oldid from entity_question_new where type = '%(type)s' limit %(start)d,%(num)d;"	

		try:
			if mysql.query(query_sql,type = type,start = start,num = num) is not None:
				return mysql.fetchall()

			else:
				return None

		except DBException as e:
			LOG.error('filtet type error [%s]' % e)
			raise CkException('filter type error')

	@staticmethod
	def q_subject_filter_num(type):

		mysql = Mysql()

		query_sql = "select count(*) from entity_question_new where subject = '%(type)s';"	

		try:
			if mysql.query(query_sql,type = type) is not None:
				return mysql.fetchall()[0][0]

			else:
				return None

		except DBException as e:
			LOG.error('filtet type error [%s]' % e)
			raise CkException('filter type error')

	@staticmethod
	def q_subject_filter(type,start,num):

		mysql = Mysql()

		query_sql = "select oldid from entity_question_new where subject = '%(type)s' limit %(start)d,%(num)d;"	

		try:
			if mysql.query(query_sql,type = type,start = start,num = num) is not None:
				return mysql.fetchall()

			else:
				return None

		except DBException as e:
			LOG.error('filtet type error [%s]' % e)
			raise CkException('filter type error')


