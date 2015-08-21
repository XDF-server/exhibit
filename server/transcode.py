# *-* coding:utf-8 *-*

from hashlib import sha1
from tornado import web,httpclient,gen

from base import Base
from gl import LOG

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

