OG_LIST = {
    'determiner': 'the' | 'a' | 'an',
    'title': 'Enter title',
    'description': 'Enter description',
    'url': 'Enter URL',
    'locale': 'ru_RU' | 'en_US' | 'en_GB',
    'image': 'Enter image URL',
}

OG_EXTENDED_LIST = {
  'image:width': 'Enter image width',
  'image:height': 'Enter image height',
  'image:alt': 'Enter image alt',
  'locale:alternate': 'Enter alternate locale',
  'site_name': 'Enter site name',
  'type': 'website' | 'music' | 'video' | 'article' | 'book' | 'profile'
}

OG_EXTENDED_LIST_MUSIC = {
  'music:song': 'Enter song URL',
  'music:song:disc': 'Enter song disc',
  'music:song:track': 'Enter song track',
  'music:musician': 'Enter musician URL',
  'music:release_date': 'Enter release date',
  'music:duration': 'Enter duration',
  'music:album': 'Enter album URL',
  'music:album:disc': 'Enter album disc',
  'music:album:track': 'Enter album track',
  'music:creator': 'Enter creator URL',
}

OG_EXTENDED_LIST_VIDEO = {
  'video:actor': 'Enter actor URL',
  'video:actor:role': 'Enter actor role',
  'video:director': 'Enter director URL',
  'video:writer': 'Enter writer URL',
  'video:duration': 'Enter duration',
  'video:release_date': 'Enter release date',
  'video:tag': 'Enter tag',
  'video:series': 'Enter series URL',
}

OG_EXTENDED_LIST_ARTICLE = {
  'article:published_time': 'Enter published time',
  'article:modified_time': 'Enter modified time',
  'article:expiration_time': 'Enter expiration time',
  'article:author': 'Enter author URL',
  'article:section': 'Enter section',
  'article:tag': 'Enter tag'
}

OG_EXTENDED_LIST_BOOK = {
  'book:author': 'Enter author URL',
  'book:isbn': 'Enter ISBN',
  'book:release_date': 'Enter release date',
  'book:tag': 'Enter tag'
}

OG_EXTENDED_LIST_PROFILE = {
  'profile:first_name': 'Enter first name',
  'profile:last_name': 'Enter last name',
  'profile:username': 'Enter username',
  'profile:gender': 'Enter gender'
}