# *-* conding:utf-8 *-*

from design_model import singleton
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure,ServerSelectionTimeoutError
from gl import LOG
from base import Configer
from exception import DBException

@singleton
class Mongo(object):

	def __init__(self):

		self.client = None	
		self.db = None
		self.collection = None

	def connect(self,db):
	
		configer = Configer()

		mongo_host = configer.get_configer('MONGO','host')
		mongo_port = int(configer.get_configer('MONGO','port'))
			
		try:
			self.client = MongoClient(host = mongo_host,port = mongo_port)
			self.db = self.client[db]
	
		except ConnectionFailure,e:
			LOG.error('mongo connect failed [%s]' % e)
			raise DBException('mongo connect failed')

	def select_collection(self,collection):
		
		try:
			self.collection = self.db[collection]

		except ServerSelectionTimeoutError as e:
			LOG.error('mongo select failed [%s]' % e)
			raise DBException('mongo select failed')
		
	def insert_one(self,data):
		
		return self.collection.insert_one(data).inserted_id

	def insert(self,data):
		
		return self.collection.insert_one(data)
		
	def get_collection(self):
			
		return self.collection

        def get_handle(self, index):
                return MongoClient(eval(Configer().get_configer('MONGO', 'configs'))[index])

        def remove(self, data):
            return self.collection.remove(data)

'''
db = Mongo()
db.connect('resource')
db.select_collection('mongo_subject_json')
data = {'hahah':'fjlfdjfdl','fjdlfjdsf':'fjnbn','jfkjflds':'jfdjfld'}
print db.insert_one(data)
'''			









