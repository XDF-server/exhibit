# *-* coding:utf-8 *-*

from mysql import Mysql
from gl import LOG
from exception import DBException,CKException

class Business(object):


	@staticmethod
	def is_topic(topic_id):
		
		mysql = Mysql()

		mysql.connect_test()
		
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
		
		mysql.connect_test()

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
	def is_level(level_id):
		
		level_dict = {"1" : "简单","2" : "中等","3" : "困难","4" : "极难"}	

		if str(level_id) in level_dict.keys():
			return True

		return False
		
	@staticmethod
	def q_type_filter_num(type):

		mysql = Mysql()

		mysql.connect_test()

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

		mysql.connect_test()

		query_sql = "select oldid,subject from entity_question_new where type = '%(type)s' limit %(start)d,%(num)d;"	

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

		mysql.connect_test()

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

		mysql.connect_test()

		query_sql = "select oldid,subject from entity_question_new where subject = '%(type)s' limit %(start)d,%(num)d;"	

		try:
			if mysql.query(query_sql,type = type,start = start,num = num) is not None:
				return mysql.fetchall()

			else:
				return None

		except DBException as e:
			LOG.error('filtet type error [%s]' % e)
			raise CkException('filter type error')

	@staticmethod
	def q_mark_list():

		mysql = Mysql()
		
		mysql.connect_test()

		query_sql = "select id,name from link_question_mark;"	

		mark_list = []

		try:
			if mysql.query(query_sql) is not None:
				mark_tuple =  mysql.fetchall()
				
				for mark in mark_tuple:
					tmp_tuple = (mark[0],mark[1])
					mark_list.append(tmp_tuple)
					print mark_list
				return mark_list

			else:
				return None

		except DBException as e:
			LOG.error('get mark error [%s]' % e)
			raise CkException('get mark error')

	@staticmethod
	def q_mark(oldid,newid,mark):

		mysql = Mysql()

		mysql.connect_test()

		query_sql = "insert into entity_question_mark (oldid,newid,mark,mark_time) values (%(oldid)d,%(newid)d,%(mark)d,now());"	

		try:
			if mysql.query(query_sql,oldid = oldid,newid = newid,mark = mark) is not None:
				return 'success'

			else:
				return None

		except DBException as e:
			LOG.error('mark error [%s]' % e)
			raise CkException('mark error')

	@staticmethod
	def add_mark(name):

		mysql = Mysql()

		mysql.connect_test()

		query_sql = "insert into link_question_mark (name) values ('%(name)s');"	

		try:
			if mysql.query(query_sql,name = name) is not None:
				return mysql.get_last_id()

			else:
				return None

		except DBException as e:
			LOG.error('add mark error [%s]' % e)
			raise CkException('add mark error')

