import requests
from bs4 import BeautifulSoup
import time


# Returns the recipe formatted as a JSON object
def parse(soup):
  recipe = {}
  main = soup.find(class_="recipe-main-info")
  #recipe['raw'] = main
  recipe['title'] = main.find(class_="content-title__text").text

  metadata = main.find(class_="recipe-metadata").find_all(class_="recipe-metadata-wrap")
  recipe['metadata'] = {}
  for m in metadata:
    heading = m.find_all("p")[0].text
    value   = m.find_all("p")[1].text
    recipe['metadata'][heading] = value

  if main.find(class_="recipe-description__text"):
    recipe['description'] = main.find(class_="recipe-description__text").text.strip("\n ")

  if main.find(class_="recipe-media__image"):
    recipe['image_url'] = main.find(class_="recipe-media__image").get("src")

  # Only add chef information if it exists
  if main.find(class_="recipe-chef"):
    chef = main.find(class_="chef__link")
    recipe['chef'] = {"name":chef.text,
                      "link":chef.get("href")}

  # Only add programme information if it exists
  if main.find(class_="chef__programme-name"):
    show = main.find(class_="chef__programme-name").find("a")
    recipe['show'] = {"name":show.text,
                      "link":show.get("href")}

  # Get the ingredients, and split it if they are listed in different sections,
  # like "For the dressing" or "For the stuffing"
  def get_ingredients(soup):
    ingredients = []
    for i in soup.find_all("li"):
      # Handle links first
      ingredient = {}
      if i.find("a"):
        tags = []
        for a in i.find_all("a"):
          tags.append({"name": a.text,
                       "link": a.get("href")})
          ingredient['tags'] = tags
      ingredient["description"] = i.text.strip(" ")
      ingredients.append(ingredient)
    return ingredients

  recipe['ingredients'] = {}
  main_ingredients  = main.find(class_="recipe-ingredients__list")
  recipe['ingredients']['main'] = get_ingredients(main_ingredients)

  for subheading in main.find_all(class_="recipe-ingredients__sub-heading"):
    recipe['ingredients'][subheading.text] = get_ingredients(subheading.next_sibling.next_sibling)

  # Get the instructions in the method
  method = []
  for li in main.find(class_="recipe-method__list").find_all("li"):
    method.append(li.p.text)

  recipe['method'] = method
  return recipe


