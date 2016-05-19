# bbc-food
A recipe crawler for the BBC Food website in case it is taken down.

## How it works

`crawler.py` is a script which has functions related to crawling search results on the BBC Food website.


`recipe_parser.py` contains one function `parse(recipe)` that parses the BeautifullySoupified recipes and saves them as JSON objects


`links.txt` currently contains the results of the crawler's efforts at picking out all the vegetarian recipes. These are saved as a tuple of the format `(name, url, page_number)` to allow me to easily keep track of where the crawler has got up to.


Why the veggie recipes? BBC Food doesn't allow you to do a search with no criteria specified, and the vegetarian checkbox is currently the broadest criterion I could find, covering 4902 of the 11,000 recipes on the site. On a side note, I was quite surprised by the proportion of vegetarian recipes on the site, it's approaching 50%!

`recipes.txt` currently contains all the recipes listed in `links.txt` stored in line separated JSON objects with the following specification

    recipe = {
      "title":String,
      "description": String,
      "metadata": {[Header:String]}
      "image_url": URL         (optional)
      "chef":{                 (optional)
        "name":String,
        "link":URL
      }
      "show":{                 (optional)
        "name":String,
        "link":URL
      }
      "ingredients":{
        "main":[ingredient],
        ["other": [ingredient]]
      }
      "method":[String]
    }
    
    ingredient = {
      "description":String,
      "tags" : [{
        "name":String,
        "link": URL
      }]
    }
                             

`metadata` contains things like preparation time, serving size, dietary information. `ingredients` is split into `main` and `other` since some recipes have sections like "For the dressing" or "For the roux" underneath the ingredients header. Each `ingredient` comprises a description and then a list of tags found in the ingredient line. 
For example, "3 button [mushrooms](http://bbc.co.uk/food/mushrooms)" would be parsed as 

    {
      "description":"3 button mushrooms",
      "tags":[{
        "name": "mushrooms",
        "link": "/food/mushrooms"
      }]
    }
    
Some of the data is optional, as not all recipes include them.
