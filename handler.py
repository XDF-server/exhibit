# *-* coding:utf-8 *-*

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

class TestHandler(web.RequestHandler):
        def get(self): self.write("Hello, world")

class Transcode(web.RequestHandler):

	@web.asynchronous
	@gen.engine
	def post(self):

		for i in range(1):
		
			LOG.info('- %s - API IN' % (self.__class__.__name__))
			LOG.info('- %s - PARA IN' % self.request.arguments)
			
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

		LOG.info('- %s - PARA OUT' % ret)
		LOG.info('- %s - API OUT' % (self.__class__.__name__))


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
		LOG.info('- %s - API OUT' % (self.__class__.__name__))


class UploadSubject(web.ResquestHandler):

	def post(self):
		
		for i in range(1):

			LOG.info('- %s - API IN' % (self.__class__.__name__))
			LOG.info('- %s - PARA OUT' % ret)
			
			ret = {'code':'','message':'','id':''}

			subject_json = ''.join(self.request.arguments['json'])
			subject_html = ''.join(self.request.arguments['html'])
			subject_theme = ''.join(self.request.arguments['theme'])
			subject_special = ''.join(self.request.arguments['special'])
			subject_level = ''.join(self.request.arguments['level'])
			timestamp = ''.join(self.request.arguments['timestamp'])
			secret = ''.join(self.request.arguments['secret'])

			key = subject_json + subject_html + subject_theme + subject_special + subject_level + timestamp
			secret_key = sha1(key).hexdigest()

			if secret == secret_key:

				qiniu = QiniuWrap()
				file_key = 'tmp' + secret_key + '.json'
				qiniu.upload_data("temp",file_key,subject_json)

				db = Mysql()
				db.connect_master()

				#更新主题link表
				#更新专题link表
				#更新题表
				upload_sql = "insert into neworiental_v2.entity_question (question_docx,question_body,question_answer,question_analysis,question_options,question_type,difficulty,
			
				
			
					

		

		LOG.info('- %s - PARA OUT' % ret)
		LOG.info('- %s - API OUT' % (self.__class__.__name__))

