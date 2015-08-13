# *-* coding:utf-8 *-*

from mysql import Mysql
from gl import LOG
from exception import DBException,CKException
import collections

class Business(object):


	@staticmethod
	def is_topic(topic_id):
		
		mysql = Mysql()

		mysql.connect_master()
		
		query_sql = "select 1 from entity_topic where id = %(topic_id)d;" 
		
		try:
			if mysql.query(query_sql,topic_id = int(topic_id)):
				return True
			else:
				return False

		except DBException as e:
			LOG.error('check topic error [%s]' % e)
			raise CKException('check topic error')

	@staticmethod
	def is_seriess(seriess_id):
		
		mysql = Mysql()
		
		mysql.connect_master()

		query_sql = "select 1 from entity_seriess where id = %(seriess_id)d;"
		
		try:
			if mysql.query(query_sql,seriess_id = int(seriess_id)):
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
	def is_type(type_id):
		
		mysql = Mysql()
		
		mysql.connect_master()

		query_sql = "select 1 from entity_question_type where type_id = %(type_id)d and enable = 1;"
		
		try:
			if mysql.query(query_sql,type_id = int(type_id)):
				return True
			else:
				return False

		except DBException as e:
			LOG.error('check type error [%s]' % e)
			raise CkException('check type error')

		
	@staticmethod
	def q_type_filter_num(type):

		mysql = Mysql()

		mysql.connect_master()

		query_sql = "select count(*) from entity_question_new where type = '%(type)s';"	

		try:
			if mysql.query(query_sql,type = type):
				return mysql.fetchall()[0][0]

			else:
				return None

		except DBException as e:
			LOG.error('filtet type error [%s]' % e)
			raise CkException('filter type error')

	@staticmethod
	def q_type_filter(type,start,num):

		mysql = Mysql()

		mysql.connect_master()

		query_sql = "select oldid,subject from entity_question_new where type = '%(type)s' limit %(start)d,%(num)d;"	

		try:
			if mysql.query(query_sql,type = type,start = start,num = num):
				return mysql.fetchall()

			else:
				return None

		except DBException as e:
			LOG.error('filtet type error [%s]' % e)
			raise CkException('filter type error')

	@staticmethod
	def q_subject_filter_num(type):

		mysql = Mysql()

		mysql.connect_master()

		query_sql = "select count(*) from entity_question_new where subject = '%(type)s';"	

		try:
			if mysql.query(query_sql,type = type):
				return mysql.fetchall()[0][0]

			else:
				return None

		except DBException as e:
			LOG.error('filtet type error [%s]' % e)
			raise CkException('filter type error')

	@staticmethod
	def q_subject_filter(type,start,num):

		mysql = Mysql()

		mysql.connect_master()

		query_sql = "select oldid,subject from entity_question_new where subject = '%(type)s' limit %(start)d,%(num)d;"	

		try:
			if mysql.query(query_sql,type = type,start = start,num = num):
				return mysql.fetchall()

			else:
				return None

		except DBException as e:
			LOG.error('filtet type error [%s]' % e)
			raise CkException('filter type error')

	@staticmethod
	def q_mark_list():

		mysql = Mysql()
		
		mysql.connect_master()

		query_sql = "select id,name from link_question_mark;"	

		mark_list = []

		try:
			if mysql.query(query_sql):
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

		mysql.connect_master()

		query_sql = "insert into entity_question_mark (oldid,newid,mark,mark_time) values (%(oldid)d,%(newid)d,%(mark)d,now());"	

		try:
			if mysql.query(query_sql,oldid = oldid,newid = newid,mark = mark):
				return 'success'

			else:
				return None

		except DBException as e:
			LOG.error('mark error [%s]' % e)
			raise CkException('mark error')

	@staticmethod
	def add_mark(name):

		mysql = Mysql()

		mysql.connect_master()

		query_sql = "insert into link_question_mark (name) values ('%(name)s');"	

		try:
			if mysql.query(query_sql,name = name):
				return mysql.get_last_id()

			else:
				return None

		except DBException as e:
			LOG.error('add mark error [%s]' % e)
			raise CkException('add mark error')

	@staticmethod
	def q_type_list():

		mysql = Mysql()
		
		mysql.connect_master()

		query_sql = "select distinct type from entity_question_new where type is not null;"	

		type_list = []

		try:
			if mysql.query(query_sql):
				type_tuple =  mysql.fetchall()
				
				for type in type_tuple:
					tmp_tuple = (type[0])
					type_list.append(tmp_tuple)
					print type_list
				return type_list

			else:
				return None

		except DBException as e:
			LOG.error('get type error [%s]' % e)
			raise CkException('get type error')

	@staticmethod
	def q_subject_list():

		mysql = Mysql()
		
		mysql.connect_master()

		query_sql = "select distinct subject from entity_question_new where type is not null;"	

		subject_list = []

		try:
			if mysql.query(query_sql):
				subject_tuple =  mysql.fetchall()
				
				for type in subject_tuple:
					tmp_tuple = (type[0])
					subject_list.append(tmp_tuple)
					print subject_list
				return subject_list

			else:
				return None

		except DBException as e:
			LOG.error('get subject error [%s]' % e)
			raise CkException('get subject error')

'''
	@staticmethod
	def q_json_parse(question_json):

		try:
			encode_json = json.loads(question_json)

		except (ValueError,KeyError,TypeError):

			return None

		body_dict = collections.OrderedDict()
		options_dict = collections.OrderedDict()
		answer_dict = collections.OrderedDict()
		analysis_dict = collections.OrderedDict()

		if 'body' in encode_json.keys():
			question_body = encode_json['body']

			for body_item_dict in question_body:
				if 'text' == body_item_dict['type']:
					
					
			
			
			


		if 'options' in encode_json.keys():
			question_options = encode_json['options']

		if 'answer' in encode_json.keys():
			question_answer = encode_json['answer']

		if 'analysis' in encode_json.keys():
			question_analysis = encode_json['analysis']			
'''
