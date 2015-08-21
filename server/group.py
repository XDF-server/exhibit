# *-* coidng:utf-8 *-*

from hashlib import sha1
import json
from tornado import web,httpclient,gen

from base import Base
from business import Business
from exception import DBException,CKException
from gl import LOG
from http import Http
from mysql import Mysql

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

			#if secret == secret_key:

			if Business.group_exist(group_name):
				
				ret['code'] = 6
				ret['message'] = 'key exsit'
				#break
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
		'''
		else:
			ret['code'] = 4
			ret['message'] = 'secure key error'
			LOG.error('ERR[secure key error]') 
			break
		'''
		LOG.info('PARAMETER OUT[%s]' % ret)
		LOG.info('API OUT[%s]' % (self.__class__.__name__))
		self.write(json.dumps(ret))


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
				
				#token = self.headers.get('teacher_id')
			
				#if token is None:

				#	break

				#Business.get_group_list()
				pass
	

