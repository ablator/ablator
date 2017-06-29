import hashlib

####### Stuff that simulates an ORM and Caching in this early alpha

HASH_SALT = "omsn"

users = []
functionalities = []
availabilities = []

####### 

class User():
	"""Represents a user of the software.
	
	Users are always anonymized and only represented by a hash
	value, so privacy can be guaranteed.
	
	Hashing will use the provided object's __repr__ method, so please
	make sure that the __repr__ method outputs a value that is unique to
	the user and unchanging.
	"""
	name = ""
	
	def __repr__(self):
		return self.name
	
	@classmethod
	def user_from_object(cls, user_object):
		user_hash = cls.hash_from_object(user_object)
		existing_users = [u for u in users if u.name == user_hash]
		if len(existing_users) > 0:
			return existing_users[0]
		
		u = User()
		u.name = user_hash
		users.append(u)
		return u
		
	@classmethod
	def hash_from_object(cls, hashable_object):
		return hashlib.sha256(HASH_SALT.encode() + str(hashable_object).encode()).hexdigest()
		

class Functionality():
	"""
	behaviour, functionality, program option
	"""
	name = ""
	options = [] # list of strings
	
class Availability():
	user = User() # foreign key
	functionality = Functionality() # foreign key
	enabled_index = None # or an integer
	
print(User.user_from_object("hallo"))
print(User.user_from_object("hallo"))
