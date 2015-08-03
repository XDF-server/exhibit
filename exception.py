# *-* coding:utf-8 *-*

class DBException(object):

	def __init__(self,msg):

		self.err_msg = msg

	def get_msg(self):

		return self.err_msg

		
