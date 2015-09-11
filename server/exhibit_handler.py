# *-* coding:utf-8 *-*

from tornado import web
from base import Base
from gl import LOG
from mysql import Mysql
from exception import DBException
from business import Business
import urllib
import json

class Register(web.RequestHandler):

	def get(self):

		self.render("register.html",title = "注册")

	def post(self):

		if 'username' not in self.request.arguments.keys():
                        self.write('no')
			return
                else:
			username = ''.join(self.request.arguments['username'])

		if 'password' not in self.request.arguments.keys():
                        self.write('no')
			return
		else:
			password = ''.join(self.request.arguments['password'])

		try:
			user_id = Business.add_user(username,password)

			if user_id:
				self.set_secure_cookie('uname',username,expires_days = None)
				self.write('ok')
			
			else:
				self.write('no')
		except DBException:
			
			self.write('no')
			return 

class Login(web.RequestHandler):

	def get(self):

		self.render("login.html",title = '登陆')

	def post(self):

		if 'username' not in self.request.arguments.keys():
                        self.write('no')
			return
                else:
			username = ''.join(self.request.arguments['username'])

		if 'password' not in self.request.arguments.keys():
                        self.write('no')
			return
		else:
			password = ''.join(self.request.arguments['password'])

		try:
			if Business.check_user(username,password):
				self.set_secure_cookie('uname',username,expires_days = None)
				self.write('ok')
			
			else:
				self.write('no')
		except DBException:
			
			self.write('no')
			return 


class Index(web.RequestHandler):

	def get(self):

		title = '首页'
	
		username = self.get_secure_cookie('uname')

		subject_list = ()
		type_list = ()
		subject_list = Business.q_subject_list()
		type_list = Business.q_type_list()

		self.render('index.html',title = title,username = username,type_list = type_list,subject_list = subject_list)


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

		username = self.get_secure_cookie('uname')
		index_dict = {'username':username,'title' : '新旧题对比展示','front_is_able' : 'disabled','next_is_able' : 'disabled',"front":"","next":""}

		old_dict = self._old_question(data)
		new_dict = self._new_question(data)
		
		if old_dict is None or new_dict is None:
			self.write('搜无此题')
			return

		combine_dict = dict(index_dict,**old_dict)
		combine_dict = dict(combine_dict,**new_dict)

		mark_list = Business.q_mark_list()
		mark_dict = {'mark_list' : mark_list}
		combine_dict = dict(combine_dict,**mark_dict)

		systematics_list = Business.get_systematics(data)
		systematics_dict = {'systematics_list' : systematics_list}

		combine_dict = dict(combine_dict,**systematics_dict)

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

		username = self.get_secure_cookie('uname')

		index_dict = {'username':username,'title' : '新旧题对比展示','subject' : subject}

		old_dict = self._old_question(qid)

		combine_dict = dict(index_dict,**old_dict)
	
		new_dict = self._new_question(qid)
		
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

		combine_dict = dict(combine_dict,**new_dict)

		systematics_list = Business.get_systematics(qid)
		systematics_dict = {'systematics_list' : systematics_list}

		combine_dict = dict(combine_dict,**systematics_dict)

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

		username = self.get_secure_cookie('uname')

		index_dict = {'username':username,'title' : '新旧题对比展示','subject' : subject}

		old_dict = self._old_question(qid)

		combine_dict = dict(index_dict,**old_dict)
		
		new_dict = self._new_question(qid)

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

		combine_dict = dict(combine_dict,**new_dict)

		systematics_list = Business.get_systematics(qid)
		systematics_dict = {'systematics_list' : systematics_list}

		combine_dict = dict(combine_dict,**systematics_dict)

		self.render("new_old_question_show.html",**combine_dict)

	@staticmethod
	def _old_question(data):

		for i in range(1):
		
			mysql = Mysql()
			
			try:
				mysql.connect_master()
				
				search_sql = "select id,question_body,question_options,question_answer,question_analysis,question_type,difficulty from entity_question_old where id = %(question_id)d;"
				if 0 == mysql.query(search_sql,question_id = int(data)):	
					return None
				else:
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

	@staticmethod
	def _new_question(data):
	
		for i in range(1):
		
			mysql = Mysql()
			
			try:
				mysql.connect_master()
				
				search_sql = "select id,json,subject,type from entity_question_new where oldid = %(oldid)d;"
				if 0 == mysql.query(search_sql,oldid = int(data)):	
					return None
				else:
					question_set = mysql.fetch()

			except DBException as e:
				break

		newid = question_set[0]
		question_json = question_set[1]
		question_subject = question_set[2]
		question_type = question_set[3]

		new_question_dict = {}
		new_question_dict['q_new_id'] = newid
		new_question_dict['new_question'],new_question_dict['blank_num'] = Business.q_json_parse(question_type,question_json)
		new_question_dict['subject'] = question_subject

		return new_question_dict

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

		username = self.get_secure_cookie('uname')

                index_dict = {'username':username,'title' : '新旧题对比展示','subject' : subject}

                old_dict = Search._old_question(qid)

                combine_dict = dict(index_dict,**old_dict)

		num_access = {'2' : 'q_type_filter_num','3' : 'q_subject_filter_num'}[filted_type]
       
                num = getattr(Business,num_access)(filted_data)
		
		mark_list = Business.q_mark_list()
		
		mark_dict = {'mark_list' : mark_list}

		combine_dict = dict(combine_dict,**mark_dict)

		new_dict = Search._new_question(qid)

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

		combine_dict = dict(combine_dict,**new_dict)

		systematics_list = Business.get_systematics(qid)
		systematics_dict = {'systematics_list' : systematics_list}
		LOG.info('haha%s' % systematics_dict)
		combine_dict = dict(combine_dict,**systematics_dict)

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

		if 'newid' not in self.request.arguments.keys():
                        self.write('no')
			return
                else:
			newid= int(''.join(self.request.arguments['newid']))

		try:
			if Business.q_mark(oldid,newid,mark) is not None:
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

class Verify(web.RequestHandler):

	def post(self):

		if 'oldid' not in self.request.arguments.keys():
                        self.write('no')
			return
                else:
			oldid= int(''.join(self.request.arguments['oldid']))

		if 'newid' not in self.request.arguments.keys():
                        self.write('no')
			return
		else:
			newid= int(''.join(self.request.arguments['newid']))

		if 'verify' not in self.request.arguments.keys():
                        self.write('no')
			return
		else:
			verify= int(''.join(self.request.arguments['verify']))

		try: 
			username = self.get_secure_cookie('uname')

			if Business.verify(username,oldid,newid,verify):
				self.write('ok')
			else:
				self.write('no')	

		except DBException as e:
			self.write('no')
			return

class CheckUser(web.RequestHandler):

	def post(self):

		if 'username' not in self.request.arguments.keys():
                        self.write('no')
			return
                else:
			username = int(''.join(self.request.arguments['username']))

		if 'password' not in self.request.arguments.keys():
                        self.write('no')
			return
		else:
			password = int(''.join(self.request.arguments['password']))
	
		
class SubmitAnswer(web.RequestHandler):

	def post(self):

		if 'oldid' not in self.request.arguments.keys():
                        self.write('no')
			return
                else:
			oldid = int(''.join(self.request.arguments['oldid']))

		if 'new_answer' not in self.request.arguments.keys():
                        self.write('no')
			return
		else:
			new_answer = ''.join(self.request.arguments['new_answer'])
		
		try: 
			question_json = Business.get_json_by_id(oldid)
			
			if question_json is False:
				self.write('no')
				return 
			
			encode_json = json.loads(question_json)
			
		except DBException as e:
			self.write('no')
			return

		new_answer_dict = {}
		new_answer_list = new_answer.split('|')

		for new_answer in new_answer_list:
			if Base.empty(new_answer) is False:
				index_answer = new_answer.split(',')
				answer_index = index_answer[0]
				answer_content = index_answer[1]
				new_answer_dict[answer_index] = answer_content

		for index,answer in new_answer_dict.items():
			for item in encode_json['answer']:
				if 'text' == item['type']:
					item['value'] = answer.decode('utf8')
					item['index'] = index

		new_question_json = json.dumps(encode_json,ensure_ascii = False)

		try: 
			if Business.update_json_by_id(oldid,new_question_json):
				self.write('ok')
				return
			
		except DBException as e:
			self.write('no')
			return
