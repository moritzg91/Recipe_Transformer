import urllib2
from bs4 import BeautifulSoup
from recipe import Recipe, Ingredient

soup = BeautifulSoup(urllib2.urlopen('http://allrecipes.com/Recipe/Easy-Tuna-Patties/Detail.aspx?soid=carousel_0_rotd&prop24=rotd').read())

ingredient_tags = soup.find_all(class_="fl-ing")
ingredients = []

for ingr in ingredient_tags:
	chunks = ingr.text.lstrip('\n').rstrip('\n').split('\n')
	ingredients.append(Ingredient(chunks[0],chunks[1]))
	

direction_tags = soup.find_all(class_="plaincharacterwrap break")
all_directions = ""
for d in direction_tags:
	all_directions += d.text

recipe = Recipe(ingredients,all_directions)

print recipe