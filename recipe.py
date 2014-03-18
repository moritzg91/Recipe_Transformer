import json 

class Ingredient(object):
	def __init__(self,name, amt, unit):
		self.amt = amt
		self.unit = unit
		self.name = name

class Recipe(object):
	def __init__(self,ingredients,raw_directions):
		self.ingredients = ingredients #List of Ingredient object
		self.raw_directions = raw_directions #String (one long string)
		self.primary_cooking_method = self.get_pc_method(raw_directions) #String (one word)
		self.cooking_tools = self.get_c_tools(raw_directions) #List of strings

	def get_pc_method(self, raw_directions):
		methods_list = ['fry', 'bake', 'roast', 'broil', 'stew','boil','steam','stew','barbeque','bast','grill','poach','sauté','microwave','rotisserie','sear','smoke','blanch', 'braise', 'coddle', 'infuse', 'pressure cook','simmer',' smother','steep','vacuum flask cook','marinate']
		for method in methods_list:
			if method in raw_directions.lower():
				return method

	def get_c_tools(self, raw_directions):
		c_tools_list = ["knife", "grater", "dutch oven", "cutting board", "colander", "peeler", "saucepan","funnel", "pot", "pan", "rolling pin", "meat tenderiser", "scissors", "sieve", "spatula", "skillet", "tongs","Strainer"]
		tools = []
		for tool in c_tools_list:
			if tool in raw_directions.lower():
				tools.append(tool)
		return tools

	def transform(dimension, direction):
		if dimension=="cuisine" and direction=="mexican":
			pass
			#Mexicanify the recipe by mutating its own fields
		if dimension=="cuisine" and direction=="italian":
			pass
			#Italinify the recipe
		if dimension=="healthiness" and direction=="healthy":
			pass
			#Replace butter with applesauce, frying with baking, etc
		if dimesnion=="healthiness" and direction=="unhealthy":
			pass
			#Fry instead of bake, etc
		#Need one more. Vegetarian to vegan and back?

	#does not mutate any of the field of Recipe - only returns the json output required by the automatic grader.
	def jsonify(self):
		#json_output = json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
		json_output = ""
		##for ingr in self.ingredients:
		##	json_output += json.dumps(ingr)
		return json_output

	def __str__(self):
		s = "----- Ingredients: -----\n"
		for i in self.ingredients:
			s += i.amt + " " + i.unit + ' of: ' + i.name + '\n'
		s += '\n----- Directions: -----\n' + self.raw_directions + '\n'
		s += '\n----- Primary Cooking Method: -----\n' + self.primary_cooking_method + '\n'
		s += '\n----- Cooking Tools: -----\n' + str(self.cooking_tools) + '\n'


		return s


