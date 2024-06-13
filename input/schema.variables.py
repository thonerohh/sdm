import os
import sys

import json
import re

CACHED = {}

# Variable Dictionary for Schema
BASIC = {
  "OBJECT": {},
  "SUBJECT": {},
  "GROUP": {},
  "STATUS": ''
}

# Patterns for Schema
organization = {
  "@context": "https://schema.org",
  "@type": "Organization",

  "name": "",
  "address": "",
  "email": "",
  "faxNumber": "",
  "telephone": "",
  "url": "",
  "logo": "",
  "taxID": "",
  "BankAccount": "",
  "iso6523": "",
  "type": "",
  "industry": "",
  "size": "",
  "location": "",
  "website": "",
  "description": "",
  "sameAs": ""
}
address = {
  "@type": "PostalAddress",
  "streetAddress": "",
  "addressLocality": "",
  "addressRegion": "",
  "postalCode": "",
  "addressCountry": ""
}
contact = {
  "@type": "ContactPoint",
  "contactType": "",
  "telephone": "",
  "email": ""
}
openingHours = {
  "@type": "OpeningHoursSpecification",
  "dayOfWeek": "",
  "opens": "",
  "closes": ""
}
members = {
  "@type": "Organization",
  "name": "",
  "url": "",
  "description": ""
}
employees = {
  "@type": "Person",
  "name": "",
  "jobTitle": "",
  "telephone": "",
  "email": ""
}
location = {
  "@type": "Place",
  "name": "",
  "address": "",
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": "",
    "longitude": ""
  }
}

# Text patterns for Schema
# constant variable for schema as schema = 'https://schema.org/'
SCHEMA = {"@context": "https://schema.org/"}
# constant variable for type as type = '@type'
TYPE = {"@type": ["WebSite","WebPage","Organization","PostalAddress","ContactPoint","OpeningHoursSpecification","Person","Place","GeoCoordinates","Product","Offer","BreadcrumbList", "ListItem","imageObject","Review","Article","Rating","AggregateRating","InteractionCounter","Restaurant","LocalBusiness", "Service","WarrantyPromise","QuantitativeValue"]}
SUPTYPE = {
  "WebSite": ["WebPage", "Organization", "Person"],
  "Person": ["Service", "Product", "GeoCoordinates"],
  "Product": ["Offer", "sameAs"],
  "Service": ["Offer", "sameAs", "author"],
  "Offer": ["price","priceCurrency", "priceValue","itemCondition","availability","AggregateRating", "Review", "WarrantyPromise"],
  "Organization": ["Product", "PostalAddress", "ContactPoint", "OpeningHoursSpecification", "Person", "Place", "LocalBusiness"],
  "LocalBusiness": ["Product", "Service", "PostalAddress", "GeoCoordinates"],
  "Place": ["GeoCoordinates"],
  # segments for schema
  "location": ["address", "geo"],
  "address": ["name", "address", "geo"],
  "geo": ["latitude", "longitude"],
  "GeoCoordinates": ["latitude", "longitude"],
  "PostalAddress": ["streetAddress", "addressLocality", "addressRegion", "postalCode", "addressCountry"],
  "ContactPoint": ["contactType", "telephone", "email"],
  "OpeningHoursSpecification": ["dayOfWeek", "opens", "closes"],
  "author": ["name", "jobTitle", "telephone", "email"],
  "sameAs": ["url"],
  "priceValue": "", # How long You can live with those money? ex. 6D
  "name": "",
  "description": "",
  "url": "",
  "logo": "",
  "taxID": "",
  "BankAccount": "",
  "iso6523": "",
  "type": "",

}
# optional variable for schema
OPTIONAL = {
    "WebSite": ["name","url","email","faxNumber","telephone","url","logo","taxID","bankAccount","iso6523",{"dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]},"opens","closes","contactType","location","streetAddress","addressLocality","addressRegion","postalCode","addressCountry","sameAs","description","industry","price","value","unitCode","priceCurrency","priceValue""priceValidUntil","category", "@id", "position","itemListElement","author","datePublished","dateModified", "image","height", "width","mainEntityOfPage","ratingValue","bestRating","aggregateRating","review","reviewCount",{"interactionType":["http://schema.org/CommentAction","http://schema.org/ReplyAction","http://schema.org/LikeAction","http://schema.org/DislikeAction","http://schema.org/FollowAction","http://schema.org/JoinAction","http://schema.org/LeaveAction","http://schema.org/InviteAction","http://schema.org/SubscribeAction","http://schema.org/UnRegisterAction","http://schema.org/ListenAction","http://schema.org/ViewAction","http://schema.org/ReadAction","http://schema.org/BookmarkAction","http://schema.org/ShareAction","http://schema.org/DonateAction","http://schema.org/DownloadAction","http://schema.org/ReviewAction","http://schema.org/WatchAction","https://schema.org/TradeAction"]},"interactionStatistic","userInteractionCount","openingHours","priceRange","servesCuisine","category",{"availability":["https://schema.org/InStock","https://schema.org/OutOfStock","https://schema.org/PreOrder","https://schema.org/BackOrder","https://schema.org/InStoreOnly","https://schema.org/OnlineOnly"]},"sku","paymentAccepted","currenciesAccepted","latitude","longitude"]
}
OPTIONS = {
"opens": ["00:00", "00:30", "01:00", "01:30", "02:00", "02:30", "03:00", "03:30", "04:00", "04:30", "05:00", "05:30", "06:00", "06:30", "07:00", "07:30", "08:00", "08:30", "09:00", "09:30", "10:00", "10:30", "11:00", "11:30", "12:00", "12:30", "13:00", "13:30", "14:00", "14:30", "15:00", "15:30", "16:00", "16:30", "17:00", "17:30", "18:00", "18:30", "19:00", "19:30", "20:00", "20:30", "21:00", "21:30", "22:00", "22:30", "23:00", "23:30"],
"closes": ["00:00", "00:30", "01:00", "01:30", "02:00", "02:30", "03:00", "03:30", "04:00", "04:30", "05:00", "05:30", "06:00", "06:30", "07:00", "07:30", "08:00", "08:30", "09:00", "09:30", "10:00", "10:30", "11:00", "11:30", "12:00", "12:30", "13:00", "13:30", "14:00", "14:30", "15:00", "15:30", "16:00", "16:30", "17:00", "17:30", "18:00", "18:30", "19:00", "19:30", "20:00", "20:30", "21:00", "21:30", "22:00", "22:30", "23:00", "23:30"],
"dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
"contactType": ["customer service", "technical support", "billing support", "bill payment", "sales", "reservations", "credit card support", "emergency", "baggage tracking", "roadside assistance", "package tracking", "flight information", "24/7 customer service", "24/7 technical support", "24/7 billing support", "24/7 bill payment", "24/7 sales", "24/7 reservations", "24/7 credit card support", "24/7 emergency", "24/7 baggage tracking", "24/7 roadside assistance", "24/7 package tracking", "24/7 flight information", ""],
"industry": ["", "Agriculture", "Automotive", "Construction", "Education", "Finance", "Health", "Hospitality", "IT", "Manufacturing", "Media", "Real Estate", "Retail", "Transportation", "Utilities"],
"size": ["1-10", "11-50", "51-200", "201-500", "501-1000", "1001-5000", "5001-10000", "10001+"],
}
# Questions for Schema

def insertor(data):
    # variable cache
    answered = {
      "route": ""
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