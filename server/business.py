# *-* coding:utf-8 *-*

from base import Base
from mysql import Mysql
from gl import LOG
from exception import DBException,CKException
import json
import re
import hashlib

question_dict_final = {}
question_dict_final['questions'] = []

class Business(object):

	@staticmethod
	def get_systematics(question_id):
		
		mysql = Mysql()

		mysql.connect_master()
		
		query_sql = "select D.name as module_name,C.name as unit_name,B.name as topic_name from (select topic_id from link_question_topic where question_id=%(question_id)d)A left outer join (select id,name,unit_id from entity_topic)B on (A.topic_id=B.id) left outer join (select id,name,module_id from entity_unit)C on (B.unit_id=C.id) left outer join (select id,name from entity_module)D on (C.module_id=D.id);" 
		
		try:
			if mysql.query(query_sql,question_id = int(question_id)):

				res = mysql.fetchall()
				systematics_list = []

				for line in res:
					module = line[0]
					unit = line[1]
					topic = line[2]					
					systematics_dict = {'module':module,'unit':unit,'topic':topic}
					systematics_list.append(systematics_dict)

				return systematics_list
			else:
				return False

		except DBException as e:
			LOG.error('get systematics error [%s]' % e)
			raise CKException('get systematics error')

	@staticmethod
	def get_group_list(system_id):
	
		mysql = Mysql()

		mysql.connect_master()
		
		query_sql = "select A.id,A.name,B.num from (select id,name from entity_group where system_id=%(system_id)d or id=0)A left outer join (select question_group,count(1) as num from entity_question where upload_id=%(system_id)d group by question_group)B on (A.id=B.question_group);" 
		
		try:
			if mysql.query(query_sql,system_id = system_id):

				res = mysql.fetchall()

				group_list = []

				for line in res:
					group_id = line[0]
					group_name = line[1]
					question_num = int(line[2]) if line[2] else 0					
					group_dict = {'id':int(group_id),'name':group_name,'num':int(question_num)}
					group_list.append(group_dict)
			
				return group_list
			else:
				return False

		except DBException as e:
			LOG.error('check topic error [%s]' % e)
			raise CKException('check topic error')


	@staticmethod
	def group_name_exist(group_name):
		
		mysql = Mysql()

		mysql.connect_master()
		
		query_sql = "select 1 from entity_group where name = '%(group_name)s';" 
		
		try:
			if mysql.query(query_sql,group_name = group_name):
				return True
			else:
				return False

		except DBException as e:
			LOG.error('check topic error [%s]' % e)
			raise CKException('check topic error')

	@staticmethod
	def group_id_exist(group_id):
		
		mysql = Mysql()

		mysql.connect_master()
		
		query_sql = "select 1 from entity_group where id = '%(group_id)d';" 
		
		try:
			if mysql.query(query_sql,group_id = int(group_id)):
				return True
			else:
				return False

		except DBException as e:
			LOG.error('check topic error [%s]' % e)
			raise CKException('check topic error')

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

		query_sql = "select name from entity_question_type where type_id = %(type_id)d and enable = 1;"
		
		try:
			if mysql.query(query_sql,type_id = int(type_id)):
				return mysql.fetch()[0]
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

		query_sql = "select id,name from link_question_mark where enable=1;"	

		mark_list = []

		try:
			if mysql.query(query_sql):
				mark_tuple =  mysql.fetchall()
				
				for mark in mark_tuple:
					tmp_tuple = (mark[0],mark[1])
					mark_list.append(tmp_tuple)
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

		query_sql = "insert into link_question_mark (name,mark_time) values ('%(name)s',now());"	

		try:
			if mysql.query(query_sql,name = name):
				return mysql.get_last_id()

			else:
				return None

		except DBException as e:
			LOG.error('add mark error [%s]' % e)
			raise CkException('add mark error')

	@staticmethod
	def verify(username,oldid,newid,verify):
		
		mysql = Mysql()

		mysql.connect_master()

		query_sql = "insert into entity_verify (username,oldid,newid,state) values ('%(username)s',%(oldid)d,%(newid)d,%(verify)d);"	

		try:
			if mysql.query(query_sql,username = username,oldid = int(oldid),newid = int(newid),verify = int(verify)):
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
				return subject_list

			else:
				return None

		except DBException as e:
			LOG.error('get subject error [%s]' % e)
			raise CkException('get subject error')

	
	@staticmethod
	def q_json_parse(question_type,question_json,sub = 0):
	
		global question_dict_final
		
		if 0 == sub:
			question_dict_final.clear()

		try:
			encode_json = json.loads(question_json)
			#print encode_json
			#print "|||"

		except (ValueError,KeyError,TypeError):

			return None,0

		body_list = []
		options_list = []
		answer_list = []
		analysis_list = []
		material_list = []
		sub_list = []
		subs_list = []

		question_dict = {}
		question_dict['questions'] = []
		blank_num = 0

		if 'body' in encode_json.keys():
			question_body = encode_json['body']
					
			body_list,num = Business.q_item_parse(question_body)
			question_dict['body'] = body_list
			blank_num = num
		#	print "题干"
		#	print body_list
		
		if 'options' in encode_json.keys():
			question_options = encode_json['options']

			for i,option in enumerate(question_options):
				opt_list,num = Business.q_item_parse(option)
				options_list.append(opt_list)

			question_dict['options'] = options_list

		#	print "题选项"
		#	print options_list

		if 'answer' in encode_json.keys():
			question_answer = encode_json['answer']

			if '判断题'.decode('utf-8') == question_type:
				if 0 == encode_json['answer']:
					answer_list = u'错'

				if 1 == encode_json['answer']:
					answer_list = u'对'

			elif 0 == len(options_list):
				answer_list,num = Business.q_item_parse(question_answer)
				if 0 == len(answer_list):
					answer_list= encode_json['answer']
			else:
				answer_list= encode_json['answer']

			question_dict['answer'] = answer_list

		#	print "题解答"
		#	print answer_list

		if 'analysis' in encode_json.keys():
			question_analysis = encode_json['analysis']			

			analysis_list,num = Business.q_item_parse(question_analysis)

			question_dict['analysis'] = analysis_list

		if 'material' in encode_json.keys():
			question_material = encode_json['material']			

			material_list,num = Business.q_item_parse(question_material)
	
			question_dict['material'] = material_list

		if 'translation' in encode_json.keys():
			question_translation = encode_json['translation']			

			translation_list,num = Business.q_item_parse(question_translation)
	
			question_dict['translation'] = translation_list

		if 0 == sub:
			question_dict_final = question_dict

		if 'questions' in encode_json.keys():
			questions = encode_json['questions']			

			for sub_question in questions:
				sub_type = sub_question['topic_type']['name']
				#print sub_question
				#print '----'
				sub_question_str = json.dumps(sub_question)
				sub_dict = {}
				sub_dict['sub_question'],sub_num = Business.q_json_parse(sub_type,sub_question_str,1)
				sub_dict['sub_num'] = sub_num
				#print sub_dict['sub_question']	
				question_dict_final['questions'].append(sub_dict)
		
		#	print "题分析"
		#	print analysis_list
		if 0 == sub:
			return question_dict_final,blank_num
		else:
			return question_dict,blank_num

	@staticmethod
	def q_item_parse(item_list):

		tmp_list = []
		blank_num = 0

		for item_dict in item_list:
			if 'text' == item_dict['type']:
				value = item_dict['value']
				value = value.replace(r'<','^<$')			
				value = value.replace(r'>','^>$')
				value = value.replace(r'^','<cdata>')
				value = value.replace(r'$','</cdata>')
				value = value.replace(r' ','&nbsp')

				if 2 == item_dict['style']:
					if 2 == item_dict['align']:
						item_html =  '<i style="text-align:center;">%s</i>' % (value.encode('utf8'))
					elif 3 == item_dict['align']:
						item_html = '<i style="float:right">%s</i>' % (value.encode('utf8'))
					else:
						item_html = '<i>%s</i>' % (value.encode('utf8'))

				elif 4 == item_dict['style']:
					if 2 == item_dict['align']:
						item_html =  '<u style="text-align:center;">%s</u>' % (value.encode('utf8'))
					elif 3 == item_dict['align']:
						item_html = '<u style="float:right">%s</u>' % (value.encode('utf8'))
					else:
						item_html = '<u>%s</u>' % (value.encode('utf8'))

				elif 16 == item_dict['style']:
					if 2 == item_dict['align']:
						item_html =  '<span style="border-bottom:dotted 2px;text-align:center;">%s</span>' % (value.encode('utf8'))
					elif 3 == item_dict['align']:
						item_html = '<span style="border-bottom:dotted 2px;float:right">%s</span>' % (value.encode('utf8'))
					else:
						item_html = '<span style="border-bottom:dotted 2px;">%s</span>' % (value.encode('utf8'))
				elif 64 == item_dict['style']:
					if 2 == item_dict['align']:
						item_html =  '<span style="border-bottom:dotted 2px;text-align:center;text-indent:2em;">%s</span>' % (value.encode('utf8'))
					elif 3 == item_dict['align']:
						item_html = '<span style="border-bottom:dotted 2px;float:right;text-indent:2em;">%s</span>' % (value.encode('utf8'))
					else:
						item_html = '<span style="border-bottom:dotted 2px;text-indent:2em;">%s</span>' % (value.encode('utf8'))

				else:
					if 2 == item_dict['align']:
						item_html =  '<span style="text-align:center;">%s</span>' % (value.encode('utf8'))
					elif 3 == item_dict['align']:
						item_html = '<span style="float:right;">%s</span>' % (value.encode('utf8'))
					else:
						item_html = '<span>%s</span>' % (value.encode('utf8'))
				
				tmp_list.append(item_html)

			if 'newline' == item_dict['type']:
				item_html = "<br />" 
				tmp_list.append(item_html)

			if 'image' == item_dict['type']:
				item_html = '<img src = "%s" />'  % (item_dict['value'].encode('utf8'))

				tmp_list.append(item_html)

			if 'option' == item_dict['type']:
				item_html = "<span>%s.</span>" % (item_dict['value'].encode('utf8'))

				tmp_list.append(item_html)

			if 'blank' == item_dict['type']:
				item_html = "_____________" 
				blank_num += 1
				tmp_list.append(item_html)

		return tmp_list,blank_num
	
	@staticmethod
	def add_user(username,password):

		password = Base.md5(password)
	
		mysql = Mysql()

		mysql.connect_master()

		query_sql = "insert into verify_user (username,password) values ('%(username)s','%(password)s');"	

		try:
			if mysql.query(query_sql,username = username,password = password):
				return mysql.get_last_id()

			else:
				return None

		except DBException as e:
			LOG.error('add user error [%s]' % e)
			raise CkException('add user error')

	@staticmethod
	def check_user(username,password):
		
		password = Base.md5(password)
	
		mysql = Mysql()

		mysql.connect_master()

		query_sql = "select password from verify_user where username='%(username)s';"	

		try:
			if mysql.query(query_sql,username = username):
				pwd = mysql.fetch()[0]
				if password == pwd:
					return True
			else:
				return False

		except DBException as e:
			LOG.error('check user error [%s]' % e)
			raise CkException('check user error')

	@staticmethod
	def get_json_by_id(oldid):
		
		mysql = Mysql()

		mysql.connect_master()

		query_sql = "select json from entity_question_new where oldid=%(oldid)d;"	

		try:
			if mysql.query(query_sql,oldid = int(oldid)):
				json = mysql.fetch()[0]
				return json
			else:
				return False

		except DBException as e:
			LOG.error('get json error [%s]' % e)
			raise CkException('get json error')

	@staticmethod
	def update_json_by_id(oldid,json):
		
		mysql = Mysql()

		mysql.connect_master()

		query_sql = "update entity_question_new set json='%(question_json)s' where oldid=%(oldid)d;"	

		try:
			if mysql.query(query_sql,oldid = int(oldid),question_json = json):
				return True
			else:
				return False

		except DBException as e:
			LOG.error('update json error [%s]' % e)
			raise CkException('update json error')

