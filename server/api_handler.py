# *-* coding:utf-8 *-*

import time
import json
import urllib
from hashlib import sha1
from tornado import web,httpclient,gen

from mysql import Mysql
from http import Http
from gl import LOG
from base import Base
from qiniu_wrap import QiniuWrap
from exception import DBException,CKException
from mongo import Mongo
from business import Business

class TestHandler(web.RequestHandler):
        def get(self): self.write("Hello, world")

class Transcode(web.RequestHandler):

	@web.asynchronous
	@gen.engine
	def post(self):

		for i in range(1):
		
			LOG.info('API IN[%s]' % (self.__class__.__name__))
			LOG.info('PARA IN[%s]' % self.request.arguments)
			
			ret = {'code':'','message':''}

			schoolid = ''.join(self.request.arguments['schoolid'])
			filepath = ''.join(self.request.arguments['filepath'])
			timestamp = ''.join(self.request.arguments['timestamp'])
			secret = ''.join(self.request.arguments['secret'])

			key = schoolid + filepath + timestamp
			secret_key = sha1(key).hexdigest()

			if secret == secret_key:

				db = Mysql()
				db.connect_master()

				ip_sql  = "select ip from entity_school_info where school_id = '%s'" % (schoolid)

				schoolip = db.query(ip_sql)

				if schoolip is None:

					ret['code'] = -2 
					ret['message'] = 'schoolid is not exist'
					
					LOG.error('schoolid is not exist [%s]' % schoolid)
					break
					
				schoolip = ''.join(schoolip)

				LOG.info('remote school ip [%s]' % (schoolip))

				timestamp = str(int(time.time()))

				key = filepath + timestamp
				secret = sha1(key).hexdigest()

				post_data = {'filepath':filepath,'timestamp':timestamp,'secret':secret}

				local_port = Base.get_config('LOCAL','port')
				
				schoolip = 'http://' + schoolip +':' + local_port + '/transcode'

				client = httpclient.AsyncHTTPClient()
				response = yield gen.Task(client.fetch,schoolip,method = 'POST',body = urllib.urlencode(post_data))
				#Http.post(schoolip,post_data)

				if response.body is None:
					
					ret['code'] = -3
					ret['message'] = 'request local server failed'

					LOG.error('request local server failed [%s]' % schoolip)
					break
				
				ret['code'] = 0
				ret['message'] = 'success'

			else:
				ret['code'] = -1
				ret['message'] = 'secure key error'
				
				LOG.error('secure key error')
			
		self.write(json.dumps(ret))
		self.finish()

		LOG.info('PARA OUT[%s]' % ret)
		LOG.info('API OUT[%s]' % (self.__class__.__name__))


class TranscodeRes(web.RequestHandler):

	def post(self):

		for i in range(1):
		
			LOG.info('- %s - API IN' % (self.__class__.__name__))
			ret = {'code':'','message':''}

class UploadFile(web.RequestHandler):
	
	def get(self):
		
		self.write('''
        		<html>
            			<head><title>Upload File</title></head>
            			<body>
                			<form action='uploadfile' enctype="multipart/form-data" method='post'>
                    			<input type='file' name='audio'/><br/>
                    			<input type='submit' value='submit'/>
                			</form>
            			</body>
        		</html>
        	''')

	def post(self):

		LOG.info('- %s - API IN' % (self.__class__.__name__))
		ret = {'code':'','message':''}

		file_metas = self.request.files['audio']

		for meta in file_metas:
		
			filename = meta['filename']

			with open(filename, 'wb') as up:
				up.write(meta['body'])

		#upload_qiniu('fs-hd', filename)
		#self.write(upload_qiniu('fs-hd', filename))
		self.write(json.dumps(ret))

		LOG.info(ret)
		LOG.info('API OUT[%s]' % (self.__class__.__name__))


class UploadQuestion(web.RequestHandler):

	def post(self):
		
		for i in range(1):

			self.set_header("Access-Control-Allow-Origin", "*")

			LOG.info('API IN[%s]' % (self.__class__.__name__))
			LOG.info('PARAMETER IN[%s]' % self.request.arguments)
			
			ret = {'code':'','message':'','id':-9999}

			essential_keys = set(['json','html','topic','seriess','level','type','subject','timestamp','secret'])

			if Base.check_parameter(set(self.request.arguments.keys()),essential_keys):
				ret['code'] = 1
				ret['message'] = 'invalid parameters'
				LOG.error('ERR[in parameter invalid]') 
				break

			question_json = ''.join(self.request.arguments['json'])
			question_html = ''.join(self.request.arguments['html'])
			question_topic = ''.join(self.request.arguments['topic'])
			question_seriess = ''.join(self.request.arguments['seriess'])
			question_level = ''.join(self.request.arguments['level'])
			question_type = ''.join(self.request.arguments['type'])
			question_subject = ''.join(self.request.arguments['subject'])
			timestamp = ''.join(self.request.arguments['timestamp'])
			secret = ''.join(self.request.arguments['secret'])

			if Business.is_level(question_level) is False:
				ret['code'] = 1
				ret['message'] = 'invalid parameters'
				LOG.error('ERR[level is invalid]') 
				break

			if Base.empty(timestamp):
				ret['code'] = 1
				ret['message'] = 'invalid parameters'
				LOG.error('ERR[timestamp empty]') 
				break
			
			try:
				question_json = urllib.unquote(question_json)
				encode_json = json.loads(question_json,encoding = 'utf-8')
				question_html = urllib.unquote(question_html)
				encode_html = json.loads(question_html,encoding = 'utf-8')

				if Base.empty(question_topic) and Base.empty(question_seriess):
					ret['code'] = 1
					ret['message'] = 'invalid parameters'
					LOG.error('ERR[topic and seriess empty]') 
					break

				if Base.empty(question_topic) is False:
					topic_list = question_topic.split(',')

					for question_theme in topic_list:
						if Business.is_topic(question_theme) is False:
							ret['code'] = 1
							ret['message'] = 'invalid parameters'
							LOG.error('ERR[topic %s invalid]' % question_theme) 
							break

				if Base.empty(question_seriess) is False:
					seriess_list = question_seriess.split(',')

					for question_special in seriess_list:
						if Business.is_seriess(question_special) is False:
							ret['code'] = 1
							ret['message'] = 'invalid parameters'
							LOG.error('ERR[seriess %s invalid]' % question_theme) 
							break

				type_name =  Business.is_type(question_type)

				if type_name is False:
					ret['code'] = 1
					ret['message'] = 'invalid parameters'
					LOG.error('ERR[type is invalid]') 
					break

			except (ValueError,KeyError,TypeError):
				ret['code'] = 1
				ret['message'] = 'invalid parameters'
				LOG.error('ERR[json format invalid]') 
				break
			
			except CKException: 
				ret['code'] = 3
				ret['message'] = 'server error'
				LOG.error('ERR[mysql exception]') 
				break

			key = question_topic + question_seriess + question_level + question_type + subject + timestamp
			secret_key = sha1(key).hexdigest()
				
			if secret == secret_key:
				
				qiniu = QiniuWrap()

				json_key = 'tmp_' + secret_key + '.json'
				if qiniu.upload_data("temp",json_key,question_json) is not None:
					ret['code'] = 4
					ret['message'] = 'qiniu error'
					LOG.error('ERR[json upload  qiniu exception]') 
					break
				
				html_key = 'tmp_' + secret_key + '.html'
				if qiniu.upload_data("temp",html_key,question_html) is not None:
					ret['code'] = 4
					ret['message'] = 'qiniu error'
					LOG.error('ERR[html upload  qiniu exception]') 
					break

				db = Mysql()

				question_sql = "insert into entity_question (difficulty,question_docx,html,upload_time,question_type,subject_id,newFormat) values (%(level)d,'%(json)s','%(html)s',now(),'%(type)s',%(subject_id)d,1);"
				
				link_topic_sql = "insert into link_question_topic (question_id,topic_id) values (%(q_id)d,%(t_id)d);"
				link_series_sql = "insert into link_question_series (question_id,series_id) values (%(q_id)d,%(s_id)d);"

				try:
					db.connect_master()
					db.start_event()
					question_res = db.exec_event(question_sql,level = int(question_level),json = json_key,html = html_key,type = type_name,subject_id = int(question_subject))
					question_sql = db.get_last_sql()
					question_id = db.get_last_id()
					LOG.info('SQL[%s] - RES[%s] - INS[%d]' % (question_sql,question_res,question_id))
			
					if Base.empty(question_topic) is False:
						topic_list = question_topic.split(',')
						for question_theme in topic_list:
							topic_res = db.exec_event(link_topic_sql,q_id = int(question_id),t_id = int(question_theme))
							topic_sql = db.get_last_sql()
							topic_id = db.get_last_id()
							LOG.info('SQL[%s] - RES[%s] - INS[%d]' % (link_topic_sql,topic_res,topic_id))
					if Base.empty(question_seriess) is False:
						seriess_list = question_seriess.split(',')

						for question_special in seriess_list:
							series_res = db.exec_event(link_series_sql,q_id = int(question_id),s_id = int(question_special))
							series_sql = db.get_last_sql()
							series_id = db.get_last_id()
							LOG.info('SQL[%s] - RES[%s] - INS[%d]' % (link_series_sql,series_res,series_id))

				except DBException as e:
					ret['code'] = 3
					ret['message'] = 'server error'
					break
				
				encode_json['question_id'] = question_id
				encode_html['question_id'] = question_id

				mongo = Mongo()

				try:
					mongo.connect('resource')
					mongo.select_collection('mongo_question_json')
					json_id = mongo.insert_one(encode_json)
					LOG.info('MONGO[insert json] - DATA[%s] - INS[%s]' % (question_json,json_id))

					mongo.select_collection('mongo_question_html')
					html_id = mongo.insert_one(encode_html)
					LOG.info('MONGO[insert html] - DATA[%s] - INS[%s]' % (question_html,html_id))

				except DBException as e:
					ret['code'] = 3 
					ret['message'] = 'server error'
					LOG.error('ERR[mongo exception]') 
					break

				db.end_event()

				ret['code'] = 0
				ret['message'] = 'success'
				ret['id'] = question_id

			else:
				ret['code'] = 5 
				ret['message'] = 'secure key error'
				LOG.error('ERR[secure key error]') 
				break

		LOG.info('PARAMETER OUT[%s]' % ret)
		LOG.info('API OUT[%s]' % (self.__class__.__name__))
		self.write(json.dumps(ret))

class CreateGroup(web.RequestHandler):

	def post(self):
		
		for i in range(1):

			LOG.info('API IN[%s]' % (self.__class__.__name__))
                        LOG.info('PARAMETER IN[%s]' % self.request.arguments)

                        ret = {'code':'','message':''}

                        essential_keys = set(['name','timestamp','secret'])

                        if Base.check_parameter(set(self.request.arguments.keys()),essential_keys):

                                ret['code'] = 1
                                ret['message'] = 'invalid parameter'
                                break
			
			group_name = ''.join(self.request.arguments['name'])
			timestamp = ''.join(self.request.arguments['timestamp'])
			secret = ''.join(self.request.arguments['secret'])

			
			if Base.empty(group_name) or Base.empty(timestamp) or Base.empty(secret):
				
				ret['code'] = 1
				ret['message'] = 'invalid parameter'
				break

			key = group_name + timestamp;
			secret_key = sha1(key).hexdigest()

			if secret == secret_key:

				if Business.group_exist(group_name):
					
					ret['code'] = 6
					ret['message'] = 'key exsit'
			
				#token = self.headers.get('teacher_id')
			
				#if token is None:

				#	break
				token = '7a9c0ee95ce14406866914839a1469e8'
				user_info_url = "http://10.60.0.159:7001/data_subscription/getUserInfo"
				post_data = {'tonken' : token}
				user_info = Http.post(user_info_url,post_data)
				
				print user_info
	
				db = Mysql()
		
				group_sql = "insert into entity_group (name) values ('%(group_name)s');"

				try:
					db.connect_master()
					group_res = db.query(group_sql,group_name = group_name)

					group_sql = db.get_last_sql()
					group_id = db.get_last_id()
					LOG.info('SQL[%s] - RES[%s] - INS[%d]' % (group_sql,group_res,group_id))
				
				except DBException as e:
					ret['code'] = 3
					ret['message'] = 'server error'
					break
				
				ret['code'] = 0
				ret['message'] = 'success'

			else:
				ret['code'] = 4
				ret['message'] = 'secure key error'
				LOG.error('ERR[secure key error]') 
				break

		LOG.info('PARAMETER OUT[%s]' % ret)
		LOG.info('API OUT[%s]' % (self.__class__.__name__))
		self.write(json.dumps(ret))

'''
class GetGroupList(web.RequestHandler):

	def post(self):

		for i in range(1):
			
			LOG.info('API IN[%s]' % (self.__class__.__name__))
                        LOG.info('PARAMETER IN[%s]' % self.request.arguments)

                        ret = {'code':'','message':'','group_list' : []}

                        essential_keys = set(['timestamp','secret'])

                        if Base.check_parameter(set(self.request.arguments.keys()),essential_keys):

                                ret['code'] = 1
                                ret['message'] = 'invalid parameter'
                                break
			
			timestamp = ''.join(self.request.arguments['timestamp'])
			secret = ''.join(self.request.arguments['secret'])

			key = timestamp;
			secret_key = sha1(key).hexdigest()

			if secret == secret_key:
				
				#Business.get_group_list()
		
'''	

class Uptoken(web.RequestHandler):

	def post(self):

		for i in range(1):
	
			LOG.info('API IN[%s]' % (self.__class__.__name__))
                        LOG.info('PARAMETER IN[%s]' % self.request.arguments)

                        ret = {'code':'','message':'','uptoken':-9999}

                        essential_keys = set(['bucket','key','timestamp','secret'])

                        if Base.check_parameter(set(self.request.arguments.keys()),essential_keys):

                                ret['code'] = -5
                                ret['message'] = 'parameter is wrong'
                                break

                        bucket_name = ''.join(self.request.arguments['bucket'])
                        key = ''.join(self.request.arguments['key'])
                        timestamp = ''.join(self.request.arguments['timestamp'])
                        secret = ''.join(self.request.arguments['secret'])

                        key = bucket_name + key + timestamp
                        secret_key = sha1(key).hexdigest()

			#if secret == secret_key:
			
			qiniu = QiniuWrap()

			uptoken = qiniu.get_uptoken(bucket_name,key)

			ret['code'] = 0
			ret['message'] = 'success'
			ret['uptoken'] = uptoken
			'''
			else:
				ret['code'] = -1
                                ret['message'] = 'secure key error'
			'''
		LOG.info('PARAMETER OUT[%s]' % ret)
                LOG.info('API OUT[%s]' % (self.__class__.__name__))
                self.write(json.dumps(ret))


