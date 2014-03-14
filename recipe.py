class Ingredient(object):
	def __init__(self,amt,name):
		self.amt = amt
		self.name = name

class Recipe(object):
	def __init__(self,ingredients,raw_directions):
		self.ingredients = ingredients
		self.raw_directions = raw_directions
		self.primary_cooking_method = self.get_pc_method(raw_directions)
		self.cooking_tools = self.get_c_tools(raw_directions)

	def get_pc_method(self, raw_directions):
		methods_list = ['fry', 'bake', 'roast']
		for method in methods_list:
			if method in raw_directions.lower():
				return method

	def get_c_tools(self, raw_directions):
		c_tools_list = ["knife", "grater", "dutch oven", "cutting board", "colander", "funnel", "pot", "pan", "rolling pin", "meat tenderiser", "scissors", "sieve", "spatula", "skillet"]
		tools = []
		for tool in c_tools_list:
			if tool in raw_directions.lower():
				tools.append(tool)
		return tools

	def __str__(self):
		s = "----- Ingredients: -----\n"
		for i in self.ingredients:
			s += i.amt + ': ' + i.name + '\n'
		s += '\n----- Directions: -----\n' + self.raw_directions + '\n'
		s += '\n----- Primary Cooking Method: -----\n' + self.primary_cooking_method + '\n'
		s += '\n----- Cooking Tools: -----\n' + str(self.cooking_tools) + '\n'
		return s