import json
import os

OG_LIST = {
  'og:determiner': {
    'Select determiner': ['a', 'an', 'the', 'auto']
  },
  'og:title': 'Enter title',
  'og:description': 'Enter description',
  'og:type': {
    'Select type': ['website', 'article', 'book', 'profile', 'music', 'video']
  },
  'og:url': 'Enter URL',
  'og:locale': {
    'Select locale': ['en_US', 'en_GB', 'es_ES', 'es_LA', 'fr_FR', 'fr_CA', 'de_DE', 'it_IT', 'ja_JP', 'ko_KR', 'pt_BR', 'ru_RU', 'tr_TR', 'zh_CN']
  },
  'og:image': 'Enter image URL',
}

# works if og:image entered
OG_EXTENDED_LIST = {
  'og:image:width': 'Enter image width',
  'og:image:height': 'Enter image height',
  'og:image:alt': 'Enter image alt',
  'og:locale:alternate': 'Enter alternate locale',
  'og:site_name': 'Enter site name',
}
# works if og:type selected as music
OG_EXTENDED_LIST_MUSIC = {
  'og:music:song': 'Enter song URL',
  'og:music:song:disc': 'Enter song disc',
  'og:music:song:track': 'Enter song track',
  'og:music:musician': 'Enter musician URL',
  'og:music:release_date': 'Enter release date',
  'og:music:duration': 'Enter duration',
  'og:music:album': 'Enter album URL',
  'og:music:album:disc': 'Enter album disc',
  'og:music:album:track': 'Enter album track',
  'og:music:creator': 'Enter creator URL',
}
# works if og:type selected as video
OG_EXTENDED_LIST_VIDEO = {
  'og:video:actor': 'Enter actor URL',
  'og:video:actor:role': 'Enter actor role',
  'og:video:director': 'Enter director URL',
  'og:video:writer': 'Enter writer URL',
  'og:video:duration': 'Enter duration',
  'og:video:release_date': 'Enter release date',
  'og:video:tag': 'Enter tag',
  'og:video:series': 'Enter series URL',
}
# works if og:type selected as article
OG_EXTENDED_LIST_ARTICLE = {
  'og:article:published_time': 'Enter published time',
  'og:article:modified_time': 'Enter modified time',
  'og:article:expiration_time': 'Enter expiration time',
  'og:article:author': 'Enter author URL',
  'og:article:section': 'Enter section',
  'og:article:tag': 'Enter tag'
}
# works if og:type selected as book
OG_EXTENDED_LIST_BOOK = {
  'og:book:author': 'Enter author URL',
  'og:book:isbn': 'Enter ISBN',
  'og:book:release_date': 'Enter release date',
  'og:book:tag': 'Enter tag'
}
# works if og:type selected as profile
OG_EXTENDED_LIST_PROFILE = {
  'og:profile:first_name': 'Enter first name',
  'og:profile:last_name': 'Enter last name',
  'og:profile:username': 'Enter username',
  'og:profile:gender': 'Enter gender'
}
# cache list
memcached2_open_graph = []
path = ''
output = './output/'
filename = 'memcached2_open_graph'
location = [f'{output}/{filename}']
extension = ['.json', '.jsonld']

# make a function to formualte the location and extension
def formulating(location, extension):
  locations = []
  for loc in location:
    for ext in extension:
      locations.append(loc + ext)
  return locations

# saving function to save data to memcached2_open_graph as
def saving(data):
  locations = formulating(location, extension)
  for loc in locations:
    with open(loc, 'w', encoding='UTF-8') as file:
      json.dump(data, file, indent=2)
  return True

# function to save and exit
def save_and_exit(data):
  status = saving(data, location)
  if status:
    print('Data saved to memcached2_open_graph')
    exit()
  else:
    print('Data not saved to memcached2_open_graph')
    exit()

# function to generate input fields in python with question-text as key from dictionary or if the value is a list then generate a dropdown
def get_input_from_dict(data, path):
    answered = {
      "route": "",
      "image": False,
      "type": ""
    }
    new_data = {}
    for key, value in data.items():
      if isinstance(value, dict):
        for prompt, options in value.items():
          print(f"{prompt}:")
          for i, option in enumerate(options):
            print(f"{i+1}. {option}")
          choice = int(input("Select an option (number): ")) - 1
          new_data[prompt] = options[choice]
          # add choice to path as str
          answered["route"] += options[choice] + '/'
      else:
        new_data[key] = input(f"{value}: ")
        # add input:value to path as str
        answered["route"] += data[key] + '/'
        # add image: True if og:image was inputed
        if key == 'og:image':
          answered["image"] = True
    return new_data, answered

# function to check if statement is truthful
def passing(statement):
  typeOf = type(statement)
  # if typoOf bool and statement is True
  if typeOf == bool and statement:
    return True
  # if typeOf str and statement is not empty
  if typeOf == str and statement != '':
    return True
  # if typeof number and statement is at least 100%
  if typeOf == int and statement >= 1:
    return True

# make a class to validate certain OpenGraph lists
class OGValidation:
  def isItInserted(self, og_list):
    for key in og_list:
      if not passing(og_list[key]):
        return False
    return True
  # function to check if og:image is inserted
  def isItImage(self, og_list):
    if not passing(og_list['og:image']):
      return False
    return True
  # function to check if og:type is selected as music
  def isItMusic(self, og_list):
    if og_list['og:type'] == 'music':
      return True
    return False
  # function to check if og:type is selected as video
  def isItVideo(self, og_list):
    if og_list['og:type'] == 'video':
      return True
    return False
  # function to check if og:type is selected as article
  def isItArticle(self, og_list):
    if og_list['og:type'] == 'article':
      return True
    return False
  # function to check if og:type is selected as book
  def isItBook(self, og_list):
    if og_list['og:type'] == 'book':
      return True
    return False
  # function to check if og:type is selected as profile
  def isItProfile(self, og_list):
    if og_list['og:type'] == 'profile':
      return True
    return False
  
result = get_input_from_dict(OG_LIST, path)
# set OG_LIST to result[0]
OG_LIST = result[0]
# set path to result[1]
path = result[1]['route']

# add OG_LIST to memcached2_open_graph
memcached2_open_graph.append(OG_LIST)
if not OGValidation().isItInserted(OG_LIST):
  print('Please fill out all required fields')
  exit()
else:
  print('All required fields filled out')

if not OGValidation().isItImage(OG_LIST):
  print('Please insert og:image')
  exit()
else:
  print('og:image inserted')

if OGValidation().isItMusic(OG_LIST):
  print('og:type is music')
elif OGValidation().isItVideo(OG_LIST):
  print('og:type is video')
elif OGValidation().isItArticle(OG_LIST):
  print('og:type is article')
elif OGValidation().isItBook(OG_LIST):
  print('og:type is book')
elif OGValidation().isItProfile(OG_LIST):
  print('og:type is profile')
else:
  print('og:type is website')