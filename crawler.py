import requests
from bs4 import BeautifulSoup
import time


base_url   =  'http://www.bbc.co.uk'
search_url =  'http://www.bbc.co.uk/food/recipes/search'

query_params = {
  "page"      :"1",
  "keywords"  :"",
  "x"         :"17",
  "y"         :"15",
  "diets[0]"  :"vegetarian",
  "sortBy"    :"lastModified",
}

cookie = 'BBC-UID=1557a39a2f77f15cadde8197d113d75c3c7da8fed31896233b6b54639ea804440Mozilla/5.0%20(Windows%20NT%2010.0%3b%20WOW64)%20AppleWebKit/537.36%20(KHTML%2c%20like%20Gecko)%20Chrome/50.0.2661.94%20Safari/5; ckns_policy=111; ckns_policy_exp=1495018131230; s1=220.181.573AF71D0006CB00B052C72985; _cb_ls=1; _chartbeat2=CLVHREBFMBlYBCcyNy.1463482132006.1463482146992.1; ecos.dt=1463482147068; _chartbeat5=879,294,%2Ffood%2Frecipes%2Fsearch,http%3A%2F%2Fwww.bbc.co.uk%2Ffood%2Frecipes%2Fsearch%3Fpage%3D2%26keywords%3D%26x%3D18%26y%3D9%26diets%255B0%255D%3Dvegetarian%26sortBy%3DlastModified,D44zN8B61JnUBQdBOoCzint3nBBUi,*%5B%40id%3D\'column%2D1\'%5D%2Fdiv%5B2%5D%2Fol%5B1%5D%2Fli%5B7%5D%2Fa%5B1%5D,c,kh7jnufzSOFCY8GMrJn4Dy6vUo'
headers = {
  'Origin'                    : 'http://www.bbc.co.uk',
  'Accept-Encoding'           : 'gzip, deflate',
  'Accept-Language'           : 'en-GB,en-US;q=0.8,en;q=0.6',
  'Upgrade-Insecure-Requests' : '1',
  'User-Agent'                : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36',
  'Content-Type'              : 'application/x-www-form-urlencoded',
  'Accept'                    : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
  'Cache-Control'             : 'max-age=0',
  'Referer'                   : 'http://www.bbc.co.uk/food/recipes/search',
  'Connection'                : 'keep-alive',
  'DNT'                       : '1',
}

def crawl(i,j):
  search_range = range(i,j)

  for page in search_range:
    query_params['page'] = str(page)

    while True:
      try:
        r = requests.post(search_url, data=query_params, headers=headers)
        soup = BeautifulSoup(r.text)
        recipes = soup.find(id="article-list").contents[0].contents
        break
      except AttributeError:
        print ("Page " + str(page) + " didn't load correctly with error code: " + str(r.status_code) + ", trying again")

    for recipe in recipes:
      a = recipe.find("a")
      name = a.text
      link = a.get('href')
      with open("links.txt",'a') as f:
        f.write(str((name,link,page))+"\n")

    print ("Recipes on page " + str(page) + " saved")
    time.sleep(2)

# Loads the list of links from the text file and turns them into Python
# readable tuples
def load_links(file_location):
  with open(file_location,'r') as f:
    raw_links = f.readlines()

  links = []
  for rl in raw_links:
    trimmed = rl[:-1]
    links.append(eval(trimmed))

  return links

# Retrieves the recipe from the URL and soupify it
def get_recipe(url):
  r = requests.get(base_url + url)
  while r.status_code != 200:
    print ("Page " + url + " didn't load correctly with error code: " + str(r.status_code) + ", trying again")
    r = requests.get(base_url + url)
  return BeautifulSoup(r.text)

