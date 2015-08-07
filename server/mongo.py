# *-* conding:utf-8 *-*

from design_model import singleton
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from gl import LOG

@singleton
class Mongo(object):

	def __init__(self):

		self.client = None	
		self.db = None
		self.collection = None

	def connect(self,db):
		
		try:
			self.client = MongoClient(host = 'localhost',port = 27017)
			self.db = self.client[db]
	
		except ConnectionFailure,e:
			LOG.error('mongo connect failed [%s]' % e)

	def select_collection(self,collection):

		self.collection = self.db[collection]
		
	def insert_one(self,data):
		
		return self.collection.insert_one(data).inserted_id

	def insert(self,data):
		
		return self.collection.insert_one(data)
		
	def get_collection(self):
			
		return self.collection
		
'''
db = Mongo()
db.connect('resource')
db.select_collection('mongo_subject_json')
data = {'hahah':'fjlfdjfdl','fjdlfjdsf':'fjnbn','jfkjflds':'jfdjfld'}
print db.insert_one(data)
'''			









