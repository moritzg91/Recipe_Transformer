import json 
import sqlite3, re

dbname = 'transformation_db'

class Ingredient(object):
	def __init__(self,name, amt, measurement, calories = None, type_ = [], cuisine = None, parent = None):
		self.amt = amt
		self.measurement = self.expand_measurements(measurement)
		self.name,self.descriptor = self.clean_name(name)
		self.calories = calories
		self.type = type_
		self.cuisine = cuisine
		self.substitutes = []
		if parent:
			self.populate_from_db(recurse=False,parent=parent)
		else:
			self.populate_from_db()

		print self.name + ": " + str(self.substitutes)

	def clean_name(self,raw_name):
		descriptor = None
		name = raw_name
		chunks = raw_name.split(",")
		if len(chunks) > 1:
			name = chunks[0]
			descriptor = chunks[1]
		return (name,descriptor)

	def expand_measurements(self,measurement):
		replacements = {
			"tsp": "teaspoon",
			"tbsp": "tablespon",
			"g": "gram",
			"lb": "pound",
			"oz": "ounce",
			"l": "liter",
			"pt": "pint",
		}
		if measurement in replacements:
			return replacements[measurement]
		elif measurement[-1] == 's':
			return measurement[:-1]
		return measurement

	def replace(self,type_):
		if type_ == 'vegetarian':
			for sub in self.substitutes:
				if ("meat" not in sub.type) and ("fish" not in sub.type):
					return sub
		if type_ == 'nonvegetarian':
			for sub in self.substitutes:
				if ('meat' in sub.type) or ('fish' in sub.type):
					return sub
		if type_ == 'mexican':
			for sub in self.substitutes:
				if sub.type == 'mexican':
					return sub
		if type_ == 'unmexican':
			for sub in self.substitutes:
				if sub.type != 'mexican':
					return sub
		if type_ == 'healthy':
			for sub in self.substitutes:
				if ('healthy' in sub.type):
					return sub
		if type_ == 'unhealthy':
			for sub in self.substitutes:
				if ('healthy' not in sub.type):
					return sub
		return self

	def populate_from_db(self,recurse=True,parent=None):
		conn = sqlite3.connect(dbname)
		c = conn.cursor()
		c.execute("SELECT * FROM transformations WHERE name = ?", (self.name,))
		record = c.fetchone()
		if record:
			self.calories = record[1]
			self.type = record[2].split(',')
			self.cuisine = record[3]
			if recurse:
				sublist = record[4].split(',')
				for sub in sublist:
					c.execute("SELECT * FROM transformations WHERE name = ?", (sub,))
					record2 = c.fetchone()
					new_ingredient = Ingredient(name=record2[0],amt=self.convert_amounts(self.name,record2[0]), measurement=self.measurement, calories = record2[1], type_ = record2[2].split(','), cuisine = record2[3], parent = self)
					self.substitutes.append(new_ingredient)
			else:
				self.sublist = [parent]
		conn.commit()
		conn.close()

	def convert_amounts(self,name1,name2):
		return self.amt

	def __str__(self):
		return self.name + ', ' + self.type

	def __repr__(self):
		return str(self)



class Recipe(object):
	def __init__(self,ingredients,raw_directions):
		self.ingredients = ingredients #List of Ingredient object
		self.raw_directions = raw_directions #String (one long string)
		self.primary_cooking_method = self.get_pc_method(raw_directions) #String (one word)
		self.cooking_tools = self.get_c_tools(raw_directions) #List of strings

	def get_pc_method(self, raw_directions):
		methods_list = self.get_objs_from_file('methods.txt')
		for method in methods_list:
			if method in raw_directions.lower():
				return method

	def get_c_tools(self, raw_directions):
		c_tools_list = self.get_objs_from_file('tools.txt')
		tools = []		
		for tool in c_tools_list:		
			if tool in raw_directions.lower():
				tools.append(tool)
		return tools

	def get_objs_from_file(self,fname):
		arr = []
		f = open(fname)
		for line in f.readlines():
			arr.append(line.lower().rstrip('\n'))
		return arr

	def transform(self, dimension, direction):
		new_ingredients = []
		if dimension == 'vegetarian' and direction == 'to':
			print "transforming to vegetarian"
			for i in self.ingredients:
				if ('meat' in i.type) or ('fish' in i.type):
					new_ingredients.append(i.replace('vegetarian'))
				else:
					new_ingredients.append(i)

		elif dimension == 'vegetarian' and direction == 'from':
			print "transforming from vegetarian"
			for i in self.ingredients:
				if ('vegetable' in i.type):
					new_ingredients.append(i.replace('nonvegetarian'))
				else:
					new_ingredients.append(i)

		elif dimension == 'healthy' and direction == 'to':
			for i in self.ingredients:
				if ('healthy' not in i.type):
					new_ingredients.append(i.replace('healthy'))
				else:
					new_ingredients.append(i)

		elif dimension == 'healthy' and direction == 'from':
			for i in self.ingredients:
				if ('healthy' in i.type):
					new_ingredients.append(i.replace('unhealthy'))
				else:
					new_ingredients.append(i)

		elif dimension == 'mexican' and direction == 'to':
			for i in self.ingredients:
				if ('mexican' not in i.cuisine):
					new_ingredients.append(i.replace('mexican'))
				else:
					new_ingredients.append(i)

		elif dimension == 'mexican' and direction == 'from':
			for i in self.ingredients:
				if ('mexican' in i.type):
					new_ingredients.append(i.replace('unmexican'))
				else:
					new_ingredients.append(i)

		self.ingredients = new_ingredients
		return

	#does not mutate any of the field of Recipe - only returns the json output required by the automatic grader.
	def jsonify(self):

		#json_output = json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
		json_output = {	"ingredients" : [],
						"cooking method": self.primary_cooking_method,
						"cooking_tools": self.cooking_tools}
		for i in self.ingredients:
			json_output["ingredients"].append(
				{
					"name": i.name,
					"quantity": i.amt,
					"measurement": i.measurement
				}
			)

		return json.dumps(json_output)

	def __str__(self):
		s = "----- Ingredients: -----\n"
		for i in self.ingredients:
			s += i.amt + " " + i.measurement + ' of: ' + i.name + '\n'
		s += '\n----- Directions: -----\n' + self.raw_directions + '\n'
		s += '\n----- Primary Cooking Method: -----\n' + self.primary_cooking_method + '\n'
		s += '\n----- Cooking Tools: -----\n' + str(self.cooking_tools) + '\n'

		return s

