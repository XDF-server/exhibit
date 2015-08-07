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




		
		
