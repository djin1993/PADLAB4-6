import time
import json
import random

DB_ERRCODE = -1
FILE = 'C:\\Users\\pripi_000\\Documents\\SpiderOak Hive\\PAD\\D.json'

class Database(object):
	"""A Database implementation"""
	_data = []
	_ids = set()

	def generate_id(self):
		while True:
			temp_id_int = random.randrange(10000, 50000)
			temp_id = str(temp_id_int)
			if not(temp_id in self._ids):
				break

		return temp_id
			
	def populate(self, file):
		f = open(file, 'r')
		self._data = json.loads( f.read() )
		f.close()
		for entry in self._data:
			self._ids.add(entry["id"])

	def depopulate(self, file):
		with open(file, 'w') as f:
			json.dump(self._data, f, sort_keys=True, indent=4, separators=(',', ': '))


	def get_one(self, identity):
		# Check for correct identity
		# time.sleep(5)
		if not(identity in self._ids):
			return DB_ERRCODE

		for entry in self._data:
			if entry["id"] == identity:
				return entry

	def get_all(self):
		# time.sleep(5)
		return self._data

	def add_one(self, entry_info):
		# time.sleep(5)
		identity = self.generate_id()
		entry_info["id"] = identity
		
		self._data.append(entry_info)
		self._ids.add(identity)
		
		return identity

	def add_asis(self, entry_info):
		
		self._data.append(entry_info)
		self._ids.add(entry_info["id"])
		
		return entry_info["id"]

	def delete_one(self, identity):
		# Check for correct identity
		# time.sleep(5)
		if not(identity in self._ids):
			return DB_ERRCODE

		self._ids.remove(identity)
		
		for dummy_i in xrange(len(self._data)):
			if self._data[dummy_i]["id"] == identity:
				break

		self._data.pop(dummy_i)


if __name__ == '__main__':
	
	db = Database()
	db.populate(FILE)

	print db.get_one('1')

	all = db.get_all()
	print all, type(all)
	print json.dumps(all, sort_keys=True, indent=4, separators=(',', ': '))

	one = db.get_one("10001")
	print one, type(one)
	print json.dumps(one, sort_keys=True, indent=4, separators=(',', ': '))

	print db._ids, type(db._ids)

	print
	some = {        "Department": "Marketing",
		"Name": "John",
		"Salary": 3000,
		"Surname": "Smith"}

	added = db.add_one(some)
	print
	print db.get_all()

	print
	some = {        "Department": "Marketing",
		"Name": "John",
		"Salary": 3000,
		"Surname": "Smith"}

	added2 = db.add_one(some)
	print
	print db.get_all()


	some = {        "Department": "Marketing",
		"Name": "John",
		"Salary": 3000,
		"Surname": "Smith",
		"id": 100}
	
	added3 = db.add_asis(some)
	print
	print db.get_all()

	print
	print added
	print added2
	print added3

	db.delete_one(added)
	db.delete_one(added2)
	db.delete_one(added3)




	print
	print db.get_all()




	db.depopulate(FILE)
	
	
	
	

			
