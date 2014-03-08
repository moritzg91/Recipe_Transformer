import urllib2
from bs4 import BeautifulSoup

soup = BeautifulSoup(urllib2.urlopen('http://allrecipes.com/Recipe/Easy-Tuna-Patties/Detail.aspx?soid=carousel_0_rotd&prop24=rotd').read())

print "Ingredients \n"
print (soup.find_all(class_="fl-ing"))
print "Direction \n"
print (soup.find_all(class_="plaincharacterwrap break"))
