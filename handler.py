#e*-* coding:utf-8 *-*

import time
import json
import urllib
from hashlib import sha1
from tornado import web,httpclient,gen

from db import Mysql
from http import Http
from gl import LOG
from base import Base
from qiniu_wrap import QiniuWrap
from exception import DBException

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


class UploadSubject(web.RequestHandler):

	def post(self):
		
		for i in range(1):

			LOG.info('API IN[%s]' % (self.__class__.__name__))
			LOG.info('PARAMETER IN[%s]' % self.request.arguments)
			
			ret = {'code':'','message':'','id':-9999}

			essential_keys = set(['json','html','theme','special','level','type','timestamp','secret'])

			if essential_keys > set(self.request.arguments.keys()):
				
				ret['code'] = -5
				ret['message'] = 'parameter is wrong'
				break

			subject_json = ''.join(self.request.arguments['json'])
			subject_html = ''.join(self.request.arguments['html'])
			subject_theme = ''.join(self.request.arguments['theme'])
			subject_special = ''.join(self.request.arguments['special'])
			subject_level = ''.join(self.request.arguments['level'])
			subject_type = ''.join(self.request.arguments['type'])
			timestamp = ''.join(self.request.arguments['timestamp'])
			secret = ''.join(self.request.arguments['secret'])

			key = subject_theme + subject_special + subject_level + timestamp
			secret_key = sha1(key).hexdigest()

			if secret == secret_key:

				qiniu = QiniuWrap()

				json_key = 'tmp_' + secret_key + '.json'
				if qiniu.upload_data("temp",json_key,subject_json) is not None:
					
					ret['code'] = -2
					ret['message'] = 'upload json failed'
					break
				
				html_key = 'tmp_' + secret_key + '.html'
				if qiniu.upload_data("temp",html_key,subject_json) is not None:
					
					ret['code'] = -3
					ret['message'] = 'upload html failed'
					break

				db = Mysql()
				db.connect_test()
				
				db.start_event()

				question_sql = "insert into entity_question (difficulty,question_docx,html,upload_time,question_type) values (%(level)d,'%(json)s','%(html)s',now(),%(type)d);"
				
				link_topic_sql = "insert into link_question_topic (question_id,topic_id) values (%(q_id)d,%(t_id)d);"
				link_series_sql = "insert into link_question_series (question_id,series_id) values (%(q_id)d,%(s_id)d);"

				try:
					question_res = db.exec_event(question_sql,level = int(subject_level),json = json_key,html = html_key,type = int(subject_type))
					question_sql = db.get_last_sql()
					question_id = db.get_last_id()
					LOG.info('SQL[%s] - RES[%s] - INS[%d]' % (question_sql,question_res,question_id))
				
					topic_res = db.exec_event(link_topic_sql,q_id = int(question_id),t_id = int(subject_theme))
					topic_sql = db.get_last_sql()
					topic_id = db.get_last_id()
					LOG.info('SQL[%s] - RES[%s] - INS[%d]' % (link_topic_sql,topic_res,topic_id))

					series_res = db.exec_event(link_series_sql,q_id = int(question_id),s_id = int(subject_special))
					series_sql = db.get_last_sql()
					series_id = db.get_last_id()
					LOG.info('SQL[%s] - RES[%s] - INS[%d]' % (link_series_sql,series_res,series_id))

					db.end_event()
				except DBException as e:
					ret['code'] = -4
					ret['message'] = 'db event failed'
					break

				ret['code'] = 0
				ret['message'] = 'success'
				ret['id'] = question_id

			else:
				ret['code'] = -1
				ret['message'] = 'secure key error'


		LOG.info('PARAMETER OUT[%s]' % ret)
		LOG.info('API OUT[%s]' % (self.__class__.__name__))
		self.write(json.dumps(ret))

