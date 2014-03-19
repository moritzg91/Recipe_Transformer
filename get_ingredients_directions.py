#import urllib2
import requests
from bs4 import BeautifulSoup
from recipe import Recipe, Ingredient

resp = requests.get('http://allrecipes.com/Recipe/Easy-Tuna-Patties/Detail.aspx?soid=carousel_0_rotd&prop24=rotd')
#soup = BeautifulSoup(urllib2.urlopen(str(sys.argv[0])).read())
soup = BeautifulSoup(resp.text.lower(),"lxml")

ingredient_tags = soup.find_all(class_="fl-ing")
ingredients = []

for ingr in ingredient_tags:
    chunks = ingr.text.lstrip('\n').rstrip('\n').split('\n')
    amt_unit= chunks[0].split()
    print amt_unit
    if len(amt_unit)>1:
        amt = amt_unit[0][0]
        unit = ""
        for i in range(1,len(amt_unit)):
            unit += amt_unit[i]
        print "amt is: " + str(amt)
        print "unit is:" + str(unit) 
    else:
        amt = amt_unit[0]
        unit = "unit"
        print "amt is: " + str(amt)
        print "unit is:" + str(unit) 
    ingredients.append(Ingredient(chunks[1],amt, unit))
	

direction_tags = soup.find_all(class_="plaincharacterwrap break")
all_directions = ""
for d in direction_tags:
	all_directions += d.text

recipe = Recipe(ingredients,all_directions)

# print recipe

# print recipe.jsonify()

choice = raw_input("What transformation do you want to do? (--help for help): ") # 
if choice == '--help':
    print "1: [to|from] vegetarian"

else:
    chunks = choice.split(' ')
    direction = chunks[0]
    dimension = chunks[1]
    print "dimension: " + dimension
    print "direction: " + direction

    recipe.transform(dimension,direction)

    print recipe
    print recipe.jsonify()

#json_output = recipe.jsonify()
#print json_output
