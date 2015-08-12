# *-* coding:utf-8 *-*

from tornado import web
from base import Base
from mysql import Mysql
from exception import DBException
from business import Business
import urllib

class Index(web.RequestHandler):

	def get(self):

		title = '首页'
		
		subject_list = Business.q_subject_list()
		type_list = Business.q_type_list()

		self.render('index.html',title = title,type_list = type_list,subject_list = subject_list)


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

		filted_data = data
		#{'1' : "选择题","2" : "填空题","3" : "判断题","4" : "简答题"}[data]

		if 'page' not in self.request.arguments.keys():
			pid = 0
		else:
			pid = int(''.join(self.request.arguments['page']))

		num = Business.q_type_filter_num(filted_data)

		if 0 == num:
			self.write("没有此类型题")
			return

		#pid = self.get_secure_cookie("pid")

		print "当前PID %s" % pid
		'''
		if pid is None:
			#self.set_secure_cookie("pid","0",expires_days = None)
			pid = 0 
		else:
			pid = int(pid)
		'''
		#self.set_secure_cookie("data",filted_data,expires_days = None)
		#self.set_secure_cookie("type","2",expires_days = None)

		filted_set = Business.q_type_filter(filted_data,pid,1)

		#self.set_secure_cookie("pid",str(pid),expires_days = None)

		qid = filted_set[0][0]
		subject = filted_set[0][1]

		index_dict = {'title' : '新旧题对比展示','subject' : subject}

		old_dict = self._old_question(qid)

		combine_dict = dict(index_dict,**old_dict)
		
		mark_list = Business.q_mark_list()
		
		mark_dict = {'mark_list' : mark_list}

		combine_dict = dict(combine_dict,**mark_dict)

		front_url = r'href = /page?type=2&data=%s&page=%d' % (filted_data,pid-1)
		next_url = r'href = /page?type=2&data=%s&page=%d' % (filted_data,pid+1)

		page_dict = {"front_is_able" : "","next_is_able" : "","front" : front_url,"next" : next_url}

		if pid >= num - 1:
			#self.set_secure_cookie("pid","0")
			page_dict["next_is_able"] = "disabled"
			page_dict["next"] = ""

		if 0 >= pid:
			page_dict["front_is_able"] =  "disabled"
			page_dict["front"] = ""

		combine_dict = dict(combine_dict,**page_dict)

		print combine_dict

		self.render("new_old_question_show.html",**combine_dict)

	def _q_subject_filter(self,data):

		filted_data = data
		#{'1' : "数学" ,"2" : "语文","3" : "英语","4" : "历史"}[data]

		if 'page' not in self.request.arguments.keys():
			pid = 0
		else:
			pid = int(''.join(self.request.arguments['page']))

		num = Business.q_subject_filter_num(filted_data)

		if 0 == num:
			self.write("没有此类型题")
			return

		#pid = self.get_secure_cookie("pid")

		print "当前PID %s" % pid
		'''
		if pid is None:
			#self.set_secure_cookie("pid","0",expires_days = None)
			pid = 0 
		else:
			pid = int(pid)
		'''

		#self.set_secure_cookie("data",filted_data,expires_days = None)
		#self.set_secure_cookie("type","3",expires_days = None)

		filted_set = Business.q_subject_filter(filted_data,pid,1)

		#self.set_secure_cookie("pid",str(pid),expires_days = None)

		qid = filted_set[0][0]
		subject = filted_set[0][1]

		index_dict = {'title' : '新旧题对比展示','subject' : subject}

		old_dict = self._old_question(qid)

		combine_dict = dict(index_dict,**old_dict)
		
		mark_list = Business.q_mark_list()
		
		mark_dict = {'mark_list' : mark_list}

		combine_dict = dict(combine_dict,**mark_dict)

		front_url = r'href = /page?type=3&data=%s&page=%d' % (filted_data,pid-1)
		next_url = r'href = /page?type=3&data=%s&page=%d' % (filted_data,pid+1)

		page_dict = {"front_is_able" : "","next_is_able" : "","front" : front_url,"next" : next_url}

		if pid >= num - 1:
			#self.set_secure_cookie("pid","0")
			page_dict["next_is_able"] = "disabled"
			page_dict["next"] = ""

		if 0 >= pid:
			page_dict["front_is_able"] =  "disabled"
			page_dict["front"] = ""

		combine_dict = dict(combine_dict,**page_dict)

		self.render("new_old_question_show.html",**combine_dict)

		pass

	@staticmethod
	def _old_question(data):

		for i in range(1):
		
			mysql = Mysql()
			
			try:
				mysql.connect_test()
				
				search_sql = "select id,question_body,question_options,question_answer,question_analysis,question_type,difficulty from entity_question_old where id = %(question_id)d;"
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

		url_list = []

		body_url = ''
		option_url = ''
		answer_url = ''
		analysis_url = ''

		if question_body is not None: 
			body_bucket = question_body[0:2]
			body_url = domain % (body_bucket,question_body)
			url_list.append(body_url)

		if question_option is not None: 
			option_bucket = question_option[0:2]
			option_url = domain % (option_bucket,question_option)
			url_list.append(option_url)

		if question_answer is not None:
			answer_bucket = question_answer[0:2]
			answer_url = domain % (answer_bucket,question_answer)	
			url_list.append(answer_url)

		if question_analysis is not None:
			analysis_bucket = question_analysis[0:2]
			analysis_url = domain % (analysis_bucket,question_analysis)
			url_list.append(analysis_url)
	
		return {'url_list' : url_list,'type' : question_type,'level' : question_level,'q_old_id' : data}

	def _new_question(self,data):
		
		pass

class Page(web.RequestHandler):

	def get(self):

		if 'page' not in self.request.arguments.keys():
			pid = 0
		else:
			pid = int(''.join(self.request.arguments['page']))
	
		if 'type' not in self.request.arguments.keys():
			filted_type = '1'
		else:
			filted_type = ''.join(self.request.arguments['type'])

		if 'data' not in self.request.arguments.keys():
			filted_data = '1'
		else:
			filted_data = urllib.unquote(''.join(self.request.arguments['data']))

		access = {'2' : 'q_type_filter','3' : 'q_subject_filter'}[filted_type]

		filted_set = getattr(Business,access)(filted_data,pid,1)

                qid = filted_set[0][0]
		subject	= filted_set[0][1]

                index_dict = {'title' : '新旧题对比展示','subject' : subject}

                old_dict = Search._old_question(qid)

                combine_dict = dict(index_dict,**old_dict)
                 
		num_access = {'2' : 'q_type_filter_num','3' : 'q_subject_filter_num'}[filted_type]
       
                num = getattr(Business,num_access)(filted_data)
		
		mark_list = Business.q_mark_list()
		
		mark_dict = {'mark_list' : mark_list}

		combine_dict = dict(combine_dict,**mark_dict)

		front_url = r'href = /page?type=%s&data=%s&page=%d' % (filted_type,filted_data,pid-1)
		next_url = r'href = /page?type=%s&data=%s&page=%d' % (filted_type,filted_data,pid+1)

		page_dict = {"front_is_able" : "","next_is_able" : "","front" : front_url,"next" : next_url}

		#self.set_secure_cookie("pid",str(pid),expires_days = None)

                if pid >= num-1:
                        #self.set_secure_cookie("pid","0")
                        page_dict["next_is_able"] = "disabled"
			page_dict["next"] = ""

                if 0 >= pid:
                        page_dict["front_is_able"] =  "disabled"
			page_dict["front"] = ""

                combine_dict = dict(combine_dict,**page_dict)

                self.render("new_old_question_show.html",**combine_dict)

class Mark(web.RequestHandler):
	
	def post(self):

		if 'mark' not in self.request.arguments.keys():
			self.write('no')
			return
                else:
                        mark = int(''.join(self.request.arguments['mark']))
        
                if 'oldid' not in self.request.arguments.keys():
                        self.write('no')
			return
                else:
			oldid= int(''.join(self.request.arguments['oldid']))

		try:
			if Business.q_mark(oldid,0,mark) is not None:
				self.write('ok')

		except DBException as e:
			self.write('no')
			return

class AddMark(web.RequestHandler):
	
	def post(self):

                if 'name' not in self.request.arguments.keys():
                        self.write('no')
			return
                else:
                        name = ''.join(self.request.arguments['name'])

		if 'oldid' not in self.request.arguments.keys():
                        self.write('no')
			return
                else:
			oldid= int(''.join(self.request.arguments['oldid']))

		try:
			mark = Business.add_mark(name)

			if mark is not None:
				if Business.q_mark(oldid,0,mark) is not None:
					self.write('ok')
			else:
				self.write('no')
                        	return

		except DBException as e:
			self.write('no')
			return
	
