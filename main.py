import recipe_parser as parser, crawler
import requests
from bs4 import BeautifulSoup
import json

with open("irish_stew.html",'r') as f:
  test_recipe = BeautifulSoup(f.read())


# Start downloading recipes from the given start index
def run(start):
  count = start
  links = crawler.load_links("links.txt")
  total = len(links)
  for l in links[start:]:
    url_suffix = l[1]
    recipe = crawler.get_recipe(url_suffix)
    parsed_recipe = parser.parse(recipe)
    parsed_recipe['url'] = crawler.base_url + url_suffix
    with open("recipes.txt",'a') as f:
      f.write(json.dumps(parsed_recipe) + "\n")

    try:
      print (str(count) + "/" + str(total) + " Recipe: " + parsed_recipe['title'] + " saved")
    except UnicodeEncodeError:
      print (str(count) + "/" + str(total) + " Recipe: " + "UNPRINTABLE" + " saved")
    count = count + 1

run(64)
