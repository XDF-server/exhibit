# *-* coding:utf-8 *-*

from hashlib import sha1
import json
from tornado import web,httpclient,gen
import urllib

from base import Base,Configer
from business import Business
from exception import DBException,CKException
from http import Http
from gl import LOG
from mysql import Mysql
from mongo import Mongo
from qiniu_wrap import QiniuWrap

class UploadQuestion(web.RequestHandler):

	@web.asynchronous
	@gen.engine
	def post(self):
		
		for i in range(1):

			self.set_header("Access-Control-Allow-Origin", "*")

			LOG.info('API IN[%s]' % (self.__class__.__name__))
			LOG.info('PARAMETER IN[%s]' % self.request.arguments)
			
			ret = {'code':'','message':'','id':-9999}

			essential_keys = set(['json','html','topic','seriess','level','type','group','timestamp','secret'])

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
			question_group = ''.join(self.request.arguments['group'])
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

				if 0 != question_group:
					if Business.group_id_exist(question_group) is False:
						ret['code'] = 8
						ret['message'] = 'key not exsit'
						LOG.error('ERROR[group not exist]')
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

			key = question_topic + question_seriess + question_level + question_type + question_group + timestamp
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

 				configer = Configer()
                                remote_host = configer.get_configer('REMOTE','host')
                                remote_port = configer.get_configer('REMOTE','port')
                                remote_uri = configer.get_configer('REMOTE','uri')

                                remote_url = "http://%s:%s/%s" % (remote_host,remote_port,remote_uri)

                                token = self.get_cookie("teacher_id")
                                LOG.info('TOKEN[%s]' % token)

                                if token is None:
                                        ret['code'] = 6
                                        ret['message'] = 'invalid token'
                                        LOG.error('ERROR[token empty]')
                                        break

                                post_data = {'token' : token}

                                client = httpclient.AsyncHTTPClient()
                                response = yield gen.Task(client.fetch,remote_url,method = 'POST',body = urllib.urlencode(post_data
))
                                #response = Http.post(remote_url,post_data)

                                encode_body = json.loads(response.body)

                                if 0 == encode_body['code'] and 2 == encode_body['code']:
                                        ret['code'] = 7
                                        ret['message'] = 'invalid token'
                                        LOG.error('ERR[token not exist]')
                                        break

                                if 1 == encode_body['code']:
                                        subject_id = encode_body['subject_id']
                                        grade_id = encode_body['grade_id']
                                        system_id = encode_body['system_id']
                                        org_type = encode_body['org_type']

					db = Mysql()

					question_sql = "insert into entity_question (difficulty,question_docx,html,upload_time,question_type,subject_id,new_format,upload_id,upload_src,question_group,grade_id) values (%(level)d,'%(json)s','%(html)s',now(),'%(type)s',%(subject_id)d,1,%(upload_id)d,%(upload_src)d,%(question_group)d,%(grade_id)d);"
					
					link_topic_sql = "insert into link_question_topic (question_id,topic_id) values (%(q_id)d,%(t_id)d);"

					link_series_sql = "insert into link_question_series (question_id,series_id) values (%(q_id)d,%(s_id)d);"

					try:
						db.connect_master()
						db.start_event()

						question_res = db.exec_event(question_sql,level = int(question_level),json = json_key,html = html_key,type = type_name,subject_id = int(subject_id),upload_id = int(system_id),upload_src = int(org_type),question_group = int(question_group),grade_id = int(grade_id))
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

                                else:
                                        ret['code'] = 3
                                        ret['message'] = 'server error'
                                        LOG.error('ERROR[remote error]')
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
		self.finish()
