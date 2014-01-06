#!flask/bin/python
import json, os

class DatabaseManipulation(object):
	def __init__(self):
		self.datasomething = 2
	
	def load_file(self, filename):
	    if not os.path.exists(filename):
	        open(filename, 'w').close() 
	    else:
	        return json.loads(open(filename).read())

	def update_file(self):
	    jsonFile = open("superheros.json", "w+")
	    jsonFile.write(json.dumps(superheroes))
	    jsonFile.close()		
		