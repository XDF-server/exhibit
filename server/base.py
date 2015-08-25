# *-* coding:utf-8 *-*

import logging
import ConfigParser
from design_model import singleton
import hashlib

class Base(object):

	@staticmethod
	def enum(**enums):
		
		return type('Enum',(),enums)


	@staticmethod
	def check_parameter(keys,essential_keys):

		if keys == essential_keys:
			return False
		else:
			return True
	@staticmethod
	def isset(v):

		try:
			type(eval(v))

		except:
			print False
			return False
		else:
			print True
	
			return True
	@staticmethod
	def empty(s):

		return True if 0 == len(s) else False

	@staticmethod
	def md5(s):

		md = hashlib.md5()
		md.update(s)
		return md.hexdigest()

@singleton
class Configer(object):

	def __init__(self,ini_path = ''):

		self.cf = ConfigParser.ConfigParser()
                self.cf.read(ini_path)

	def get_configer(self,section,option):

		return self.cf.get(section,option)	

@singleton
class Logger(object):

	def __init__(self,path = '',info = '',format = ''):
		
		self.logger = logging.getLogger(info)
		self.logger.setLevel(logging.DEBUG)
		
		fh = logging.FileHandler(path)
		fh.setLevel(logging.DEBUG)

		#ch = logging.StreamHandler()
		#ch.setLevel(logging.DEBUG)

		formatter = logging.Formatter(format)
		fh.setFormatter(formatter)
		#ch.setFormatter(formatter)

		self.logger.addHandler(fh)
		#self.logger.addHandler(ch)
	
	def get_logger(self):

		return self.logger


if __name__ == '__main__':

	#keys = set(['a','b'])
	#enssential = set(['c'])
	#print Base.check_parameter(keys,enssential)
	#print keys < enssential

	print Base.empty('1')
