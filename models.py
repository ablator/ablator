# Ablator Models

class User():
	name = ""

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