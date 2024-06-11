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