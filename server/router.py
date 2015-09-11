#!/usr/bin/python2.7
# *-* coding:utf-8 *-* 

import os
import sys
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define,options

from loader import Loader

define('port',default = 9000,help='this is default port',type = int)

if __name__ == "__main__":
	
	Loader.load()

	from gl import LOG
	from exhibit_handler import *
	
	tornado.options.parse_command_line()

	settings = {"cookie_secret": "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E="}

	application = tornado.web.Application([
		
		(r'/index',Index),
		(r'/search',Search),
		(r'/page',Page),
		(r'/mark',Mark),
		(r'/addmark',AddMark),
		(r'/verify',Verify),
		(r'/check_user',CheckUser),
		(r'/login',Login),
		(r'/register',Register),
		(r'/submit_answer',SubmitAnswer),
	],
	template_path = os.path.join(os.path.dirname(__file__),os.pardir,'templates'),
	static_path = os.path.join(os.path.dirname(__file__),os.pardir,'static'),
	**settings
	)

	http_server = tornado.httpserver.HTTPServer(application)

        http_server.listen(options.port)

	LOG.info('idc_api is started,port is [%s]' % options.port)

        tornado.ioloop.IOLoop.instance().start()

