import json
import os
import re

OG_CACHE = {}

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
path = ''
output = './output'

# check if output folder exists
if not os.path.exists(output):
  os.makedirs(output)

filename = '/memcached2_open_graph'
location = [f'{output}{filename}']
extension = ['.json', '.jsonld', '.html']

# make a function to formualte the location and extension
def formulating(location, extension):
  locations = []
  for loc in location:
    for ext in extension:
      locations.append(loc + ext)
  return locations

# make function to trim all unexpected characters from path and capitalize the strings
def nameStandard(title):
  #  using regex remove all symbols with nothing
  title = re.sub(r'[^\w\s]', '', title)
  # capitalize all words
  # title = title.title()
  return title

def convert_to_metaTagHtml(data):
  meta_tags = ''
  for key, value in data.items():
    meta_tags += f'<meta property="{key}" content="{value}">\n'
  return meta_tags

# saving function to save data to memcached2_open_graph as
def saving(data):
  locations = formulating(location, extension)
  print (data)
  for loc in locations:
    # if extension of location is html
    if loc.endswith('.html'):
      data = convert_to_metaTagHtml(data)
      print(data)
      with open(loc, 'w', encoding='UTF-8') as file:
        file.write(data)
    else:
      with open(loc, 'w', encoding='UTF-8') as file:
        json.dump(data, file, indent=2)
  return True

# function to save and exit
def save_and_exit(data):
  status = saving(data)
  if status:
    print(f'Data saved to {location}')
    exit()
  else:
    print('Data not saved')
    exit()

# function to generate input fields in python with question-text as key from dictionary or if the value is a list then generate a dropdown
def get_input_from_dict(data, path):
    # variable cache
    answered = {
      "route": "",
      "new_data": {}
    }

    for key, value in data.items():
      # loop through data

      # if val is dict state
      if isinstance(value, dict):
        for prompt, options in value.items():
          print(f"{prompt}:")
          for i, option in enumerate(options):
            print(f"{i+1}. {option}")
          choice = int(input("Select an option (number): ")) - 1
          answered["new_data"][key] = options[choice]
          # add choice to path as str
          answered["route"] += f'{choice}.'

      # if val is str state
      else:
        answered["new_data"][key] = input(f"{value}: ")
        # add input:value to path as boolean if not empty
        if answered["new_data"][key] != '':
          answered["route"] += 'y.'
        else:
          answered["route"] += 'n.'

      # check the last value and if there are empty remove key as well
      if answered["new_data"][key] == '':
        del answered["new_data"][key]

    return answered["new_data"], answered["route"]

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
  if typeOf == int and statement != 0:
    return True

# make a class to validate certain OpenGraph lists
class OGValidation:
    def __init__(self):
        self.required_fields = ['og:image', 'og:type']

    def passing(self, value):
        return value is not None and value != ''

    def isItInserted(self, og_list):
        for key in self.required_fields:
            print(key)
            if key not in og_list or not self.passing(og_list[key]):
                print(key)
                return False
        return True

    def isItImage(self, og_list):
        return 'og:image' in og_list and self.passing(og_list['og:image'])

    def isItType(self, og_list, og_type):
        return 'og:type' in og_list and og_list['og:type'] == og_type
  
nd,a = get_input_from_dict(OG_LIST, path)

print (nd, a)

# set OG_LIST to result[0]
OG_LIST = nd
OG_CACHE.update(OG_LIST)

print ('answer:', a)
# set path to result[1]
path = nameStandard(a)
print ('answer path:', path)

og_validator = OGValidation()

if not og_validator.isItInserted(OG_LIST):
    print('Please fill out all required fields')
    exit()
else:
    print('All required fields filled out')

if not og_validator.isItImage(OG_LIST):
    print('Please insert og:image')
    exit()
else:
    print('og:image inserted')

if og_validator.isItType(OG_LIST, 'music'):
    print('og:type is music')
elif og_validator.isItType(OG_LIST, 'video'):
    print('og:type is video')
elif og_validator.isItType(OG_LIST, 'article'):
    print('og:type is article')
elif og_validator.isItType(OG_LIST, 'book'):
    print('og:type is book')
elif og_validator.isItType(OG_LIST, 'profile'):
    print('og:type is profile')
else:
    print('og:type is website')

# ask user for extended input and if is Yes than add to memcached2_open_graph
if input('Do you want to enter extended OpenGraph variables? (y/n): ') == 'y':
  path += f'y.'
  nd, a = get_input_from_dict(OG_EXTENDED_LIST, path)
  OG_CACHE.update(nd)
  path += nameStandard(a)

  # check if og:type is selected and if it is music or whatever than add OG_EXTENDED_LIST_MUSIC or whatever to memcached2_open_graph
  if og_validator.isItType(OG_LIST, 'music'):
    nd, a = get_input_from_dict(OG_EXTENDED_LIST_MUSIC, path)
  elif og_validator.isItType(OG_LIST, 'video'):
    nd, a = get_input_from_dict(OG_EXTENDED_LIST_VIDEO, path)
  elif og_validator.isItType(OG_LIST, 'article'):
    nd, a = get_input_from_dict(OG_EXTENDED_LIST_ARTICLE, path)
  elif og_validator.isItType(OG_LIST, 'book'):
    nd, a = get_input_from_dict(OG_EXTENDED_LIST_BOOK, path)
  elif og_validator.isItType(OG_LIST, 'profile'):
    nd, a = get_input_from_dict(OG_EXTENDED_LIST_PROFILE, path)

  OG_CACHE.update(nd)
  path += nameStandard(a)

  print ('path: ', path)
  print ('OG_CACHE:', OG_CACHE)
  # save and exit
  filename = '/extended__memcached2_open_graph'

  # add path to OG_CACHE as 'trace'
  OG_CACHE['trace'] = path
  save_and_exit(OG_CACHE)
else:
  path += f'n.'
  filename = '/shorten__memcached2_open_graph'
  OG_CACHE['trace'] = path
  save_and_exit(OG_CACHE)