# *-* coding:utf-8 *-*

from tornado import web
from base import Base
from mysql import Mysql
from exception import DBException

class Index(web.RequestHandler):

	def get(self):

		title = '首页'
		self.render('index.html',title = title)


class Search(web.RequestHandler):

	def get(self):
		
		essential_keys = set(['data','type'])

		if Base.check_parameter(set(self.request.arguments.keys()),essential_keys):
			pass

		type = ''.join(self.request.arguments['type'])
		data = ''.join(self.request.arguments['data'])

		access = { '1' : '_qid_search',
			   '2' : '_q_type_filter',
			   '3' : '_q_subject_filter'}[type]

		getattr(self,access)(data)

	def _qid_search(self,data):

		index_dict = {'title' : '新旧题对比展示'}

		old_dict = self._old_question(data)

		combine_dict = dict(index_dict,**old_dict)
		print combine_dict
		self.render("new_old_question_show.html",**combine_dict)

	def _q_type_filter(self,data):

		pass

	def _q_subject_filter(self,data):
	
		pass

	def _old_question(self,data):

		for i in range(1):
		
			mysql = Mysql()
			
			try:
				mysql.connect_test()
				
				search_sql = "select id,question_body,question_options,question_answer,question_analysis from entity_question where id = %(question_id)d;"
				mysql.query(search_sql,question_id = int(data))	

				question_set = mysql.fetch()

			except DBException as e:
				break
			
		domain = "http://%s.okjiaoyu.cn/%s"	
		
		question_body = question_set[1]
		question_option = question_set[2]
		question_answer = question_set[3]
		question_analysis = question_set[4]

		body_bucket = question_body[0:2]
		option_bucket = question_option[0:2]
		answer_bucket = question_answer[0:2]
		analysis_bucket = question_analysis[0:2]

		body_url = domain % (body_bucket,question_body)
		option_url = domain % (option_bucket,question_option)
		answer_url = domain % (answer_bucket,question_answer)	
		analysis_url = domain % (analysis_bucket,question_analysis)
		
		return {'body_img_url' : body_url,'option_img_url' : option_url,'answer_img_url' : answer_url,'analysis_img_url' : analysis_url}

	def _new_question(self,data):
		
		pass

		

class Question(web.RequestHandler):

	def get(self):
		
		pass
			
