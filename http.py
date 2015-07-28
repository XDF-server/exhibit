# *-* coding:utf-8 *-*

import urllib
import urllib2

class Http(object):

	@staticmethod
	def post(url,data):
		
		encode_data = urllib.urlencode(data)

		req = urllib2.Request(url = url,data = encode_data)
		
		res = urllib2.urlopen(req)

		return res.read()
		
			
