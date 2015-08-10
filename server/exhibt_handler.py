# *-* coding:utf-8 *-*

from tornado import web
from base import Base
from mysql import Mysql
from exception import DBException
from business import Business

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

		access = { '1' : '_qid_search',
			   '2' : '_q_type_filter',
			   '3' : '_q_subject_filter'}[type]


		if self.request.arguments.has_key('data'):
			data = ''.join(self.request.arguments['data'])
			getattr(self,access)(data)

		else:
			getattr(self,access)()

	def _qid_search(self,data):

		index_dict = {'title' : '新旧题对比展示','front_is_able' : '','next_is_able' : '',"front":"","next":""}

		old_dict = self._old_question(data)

		combine_dict = dict(index_dict,**old_dict)
		self.render("new_old_question_show.html",**combine_dict)

	def _q_type_filter(self,data):

		filted_data = {'1' : "选择题","2" : "填空题","3" : "判断题","4" : "简答题"}[data]

		pid = self.get_secure_cookie("pid")
		print pid

		if pid is None:
			self.set_secure_cookie("pid","0",expires_days = None)
			self.set_secure_cookie("data",filted_data,expires_days = None)
			self.set_secure_cookie("type","2",expires_days = None)
			pid = 0 
		else:
			pid = int(pid)


		filted_set = Business.q_type_filter(filted_data,pid,1)

		self.set_secure_cookie("pid",str(pid),expires_days = None)

		qid = filted_set[0][0]

		index_dict = {'title' : '新旧题对比展示'}

		old_dict = self._old_question(qid)

		combine_dict = dict(index_dict,**old_dict)
			
		num = Business.q_type_filter_num(filted_data)

		page_dict = {"front_is_able" : "","next_is_able" : "","front" : r'href = /front',"next" : r'href = /next'}

		if pid >= num:
			self.set_secure_cookie("pid","0")
			page_dict["next_is_able"] = "disabled"
			page_dict["next"] = ""

		if 0 >= pid:
			page_dict["front_is_able"] =  "disabled"
			page_dict["front"] = ""

		combine_dict = dict(combine_dict,**page_dict)

		self.render("new_old_question_show.html",**combine_dict)

	def _q_subject_filter(self,data):
	
		pass

	@staticmethod
	def _old_question(data):

		for i in range(1):
		
			mysql = Mysql()
			
			try:
				mysql.connect_test()
				
				search_sql = "select id,question_body,question_options,question_answer,question_analysis,question_type,difficulty from entity_question where id = %(question_id)d;"
				mysql.query(search_sql,question_id = int(data))	

				question_set = mysql.fetch()

			except DBException as e:
				break
			
		domain = "http://%s.okjiaoyu.cn/%s"	
		
		question_body = question_set[1]
		question_option = question_set[2]
		question_answer = question_set[3]
		question_analysis = question_set[4]
		question_type = question_set[5]
		question_level = question_set[6]

		body_bucket = question_body[0:2]
		option_bucket = question_option[0:2]
		answer_bucket = question_answer[0:2]
		analysis_bucket = question_analysis[0:2]

		body_url = domain % (body_bucket,question_body)
		option_url = domain % (option_bucket,question_option)
		answer_url = domain % (answer_bucket,question_answer)	
		analysis_url = domain % (analysis_bucket,question_analysis)
		
		return {'body_img_url' : body_url,'option_img_url' : option_url,'answer_img_url' : answer_url,'analysis_img_url' : analysis_url,'type' : question_type,'level' : question_level}

	def _new_question(self,data):
		
		pass

class Front(web.RequestHandler):

	def get(self):
	
		pid = self.get_secure_cookie("pid")

		if pid is None:
			self.write('不可以执行此操作')
		else:
			pid = int(pid)

		pid -= 1

		filted_type = self.get_secure_cookie("type")
		filted_data = self.get_secure_cookie("data")

		filted_set = Business.q_type_filter(filted_data,pid,1)

                qid = filted_set[0][0]

                index_dict = {'title' : '新旧题对比展示'}

                old_dict = Search._old_question(qid)

                combine_dict = dict(index_dict,**old_dict)
                        
                num = Business.q_type_filter_num(filted_data)
		
		page_dict = {"front_is_able" : "","next_is_able" : "","front" : r'href = /front',"next" : r'href = /next'}

                if pid-1 >= num:
                        self.set_secure_cookie("pid","0")
                        page_dict["next_is_able"] = "disabled"
			page_dict["next"] = ""

                if 0 >= pid:
                        page_dict["front_is_able"] =  "disabled"
			page_dict["front"] = ""

                combine_dict = dict(combine_dict,**page_dict)

		self.set_secure_cookie("pid",str(pid),expires_days = None)

                self.render("new_old_question_show.html",**combine_dict)

		
class Next(web.RequestHandler):

	def get(self):
	
		pid = self.get_secure_cookie("pid")
		
		if pid is None:
			self.write('不可以执行此操作')
		else:
			pid = int(pid)

		pid += 1
	
		filted_type = self.get_secure_cookie("type")
		filted_data = self.get_secure_cookie("data")

		filted_set = Business.q_type_filter(filted_data,pid,1)

                qid = filted_set[0][0]

                index_dict = {'title' : '新旧题对比展示'}

                old_dict = Search._old_question(qid)

                combine_dict = dict(index_dict,**old_dict)
                        
                num = Business.q_type_filter_num(filted_data)

		page_dict = {"front_is_able" : "","next_is_able" : "","front" : r'href = /front',"next" : r'href = /next'}

                if pid+1 >= num:
                        self.set_secure_cookie("pid","0")
                        page_dict["next_is_able"] = "disabled"
			page_dict["next"] = ""

                if 0 >= pid:
                        page_dict["front_is_able"] =  "disabled"
			page_dict["front"] = ""

                combine_dict = dict(combine_dict,**page_dict)

		self.set_secure_cookie("pid",str(pid),expires_days = None)

                self.render("new_old_question_show.html",**combine_dict)

		
