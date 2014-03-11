class Ingredient(object):
	def __init__(self,amt,name):
		self.amt = amt
		self.name = name

class Recipe(object):
	def __init__(self,ingredients,raw_directions):
		self.ingredients = ingredients
		self.raw_directions = raw_directions
		return
	def __str__(self):
		s = "----- Ingredients: -----\n"
		for i in self.ingredients:
			s += i.amt + ': ' + i.name + '\n'
		s += '\n----- Directions: -----' + self.raw_directions + '\n'
		return s