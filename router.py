# *-* coding:utf-8 *-* 


import sys
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define,options

import loader
from gl import LOG
from handler import *

define('port',default = 9000,help='this is default port',type = int)

if __name__ == "__main__":
		
	tornado.options.parse_command_line()

	application = tornado.web.Application([
		(r"/test", TestHandler),
		(r'/transcode',Transcode),
		(r'/transcode_res',TranscodeRes),
		(r'/upload_question',UploadQuestion),
	])

	http_server = tornado.httpserver.HTTPServer(application)

        http_server.listen(options.port)

	LOG.info('idc_api is started,port is [%s]' % options.port)

        tornado.ioloop.IOLoop.instance().start()
