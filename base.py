# *-* coding:utf-8 *-*

import logging
import ConfigParser

def isset(v):

	try:
		type(eval(v))

	except:
		print False
		return False
	else:
		print True
		return True	

class Base(object):

        @staticmethod
        def get_config(section,option):

                cf = ConfigParser.ConfigParser()
                cf.read('config.ini')
                return cf.get(section,option)	

	@staticmethod
	def init_log():

		logger = logging.getLogger('IDC_API')
		logger.setLevel(logging.DEBUG)
		
		log_path = Base.get_config('LOG','path')

		fh = logging.FileHandler(log_path)
		fh.setLevel(logging.DEBUG)

		ch = logging.StreamHandler()
		ch.setLevel(logging.DEBUG)

		formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(filename)s - %(funcName)s - %(message)s')
		fh.setFormatter(formatter)
		ch.setFormatter(formatter)

		logger.addHandler(fh)
		logger.addHandler(ch)

		return logger

	@staticmethod
	def enum(**enums):
		
		return type('Enum',(),enums)


	@staticmethod
	def check_parameter(keys,essential_keys):

		if keys == essential_keys:
			return False
		else:
			return keys < essential_keys

