import os
import sys

import json
import re

CACHED = {}

# Variable Dictionary for Schema
BASIC = {
  "GROUP": {
    "@context": {
      "sc": "https://schema.org"
    },
  },
  "SUBJECT": {
    "@type":{
      # Representation
      "ws":"WebSite", #WebSystem
      "wp":"WebPage",
      "ap":"AboutPage",
      "conp":"ContactPage",
      "qap":"QAPage",
      # Rerepresentation
      "ls":"BreadcrumbList",
      ## Confusing objects
      "ao":"AudioObject",
      "io":"ImageObject",
      "vo":"VideoObject",
      # Independent Object
      "ps":"Person",
      "pr":"Product",
      "sr":"Service",
      "or":"Organization",
      "locb":"LocalBusiness",
      "event":"Event",
      ## Subjective independent object
      "irl":"IndividualRole",
      "pgr":"ProductGroup",
      ## Specific
      "gor":"GovernmentalOrganization",
      "ngo":"NGO",
      "cor":"Corporation",
      "er":"EmployeeRole",
      "rest":"Restaurant",
      "land":"Landform",
      # Dependent Object
      "rew":"Review",
      ## Creative object
      "creow":"CreativeWork",
      "book":"Book",
      "movie":"Movie",
      "music":"MusicRecording",
      "recip":"Recipe",
      "tv":"TVSeries",
      # Object Specification
      "arai":"AggregateRating",
      "aoe":"AggregateOffer",
      "rai":"Rating",
      "wan":"WarrantyPromise",
      # Formal Action
      "conp":"ContactPoint",
      ## Action Specification
      "oe":"Offer",
      "ohs":"OpeningHoursSpecification",
      "gc":"GeoCoordinates",
      "ic":"InteractionCounter",
      # Property
      "pl":"Place",
      "pla":"PostalAddress",
    }
  },
  "OBJECT": {},
  "STATE": '' #cache
}

# Minimized type version
MTYPE = {
"Product":[

],
"Organization":{
  "@type":["Organization"],
  "name":"Enter the name of organization",
  "description":"Enter the description of organization",
  "address":{
    "@type": ["PostalAddress"],
    "addressCountry": "Enter the country name",
    "addressRegion": "Enter the region",
    "addressLocality": "Enter the city",
    "postalCode": "Enter the postal code",
    "streetAddress": "Enter full street address including postal code number",
  },
  "email": "email",
  "faxNumber": "Enter the fax",
  "telephone": "Enter the telephone",
  "url": "Enter the url of organization",
  "logo": "Enter the url of logo",
  "taxID": "Enter the tax ID",
  "BaID": "Enter the Bank ID",
  "iso6523": "Enter the iso6523 code of organization",
  "openningHours":[
    {
      "@type":["OpeningHoursSpecification"],
      "dayOfWeek":[
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
      ],
      "opens":["00:00", "00:30", "01:00", "01:30", "02:00", "02:30", "03:00", "03:30", "04:00", "04:30", "05:00", "05:30", "06:00", "06:30", "07:00", "07:30", "08:00", "08:30", "09:00", "09:30", "10:00", "10:30", "11:00", "11:30", "12:00", "12:30", "13:00", "13:30", "14:00", "14:30", "15:00", "15:30", "16:00", "16:30", "17:00", "17:30", "18:00", "18:30", "19:00", "19:30", "20:00", "20:30", "21:00", "21:30", "22:00", "22:30", "23:00", "23:30"],
      "closes":["00:00", "00:30", "01:00", "01:30", "02:00", "02:30", "03:00", "03:30", "04:00", "04:30", "05:00", "05:30", "06:00", "06:30", "07:00", "07:30", "08:00", "08:30", "09:00", "09:30", "10:00", "10:30", "11:00", "11:30", "12:00", "12:30", "13:00", "13:30", "14:00", "14:30", "15:00", "15:30", "16:00", "16:30", "17:00", "17:30", "18:00", "18:30", "19:00", "19:30", "20:00", "20:30", "21:00", "21:30", "22:00", "22:30", "23:00", "23:30"],
    }
  ],
  "member": [
    {
      "@type": ["Person"],
      "name": "Enter the name of person"
    }
  ],
  "contactPoint": [
    {
      "@type": ["ContactPoint"],
      "contactType": ["customer service", "technical support", "billing support", "bill payment", "sales", "reservations", "credit card support", "emergency", "baggage tracking", "roadside assistance", "package tracking", "flight information", "24/7 customer service", "24/7 technical support", "24/7 billing support", "24/7 bill payment", "24/7 sales", "24/7 reservations", "24/7 credit card support", "24/7 emergency", "24/7 baggage tracking", "24/7 roadside assistance", "24/7 package tracking", "24/7 flight information", ""],
      "telephone": "Enter telephone"
    },
    "sameAs":["*"]
  ],
},
"LocalBusiness":{
  "@type":["localBusiness"],
  "name":"Enter the name of local business",
  "description":"Enter the description of local business",
  "currenciesAccepted":["", "USD", "RUR"],
  "paymentAccepted":["","Cash","Credit Card","Cash and credit card"],
  "image":"Enter URL of an image",
  "url":"Enter URL of an organization",
  "address":{
    "@type": ["PostalAddress"],
    "addressCountry": "Enter the country name",
    "addressRegion": "Enter the region",
    "addressLocality": "Enter the city",
    "postalCode": "Enter the postal code",
    "streetAddress": "Enter full street address including postal code number",
  },
  "priceRange":["$","$$","$$$"],
  "sameAs":["*"]
},
"warranty":{
  "@type":["WarrantyPromise"],
  "name":"Enter the name of warranty",
  "durationOfWarranty":{
    "@type":["QuantitativeValue"],
    "unitCode":["ANN"],
    "value":"Enter the number of warrantied years from 1 to 99"
  }
},
"offers":{
  "@type": ["Offer"],
  "name":"Type name of product",
  "availability":["https://schema.org/InStock","https://schema.org/OutOfStock","https://schema.org/PreOrder","https://schema.org/BackOrder","https://schema.org/InStoreOnly","https://schema.org/OnlineOnly"],
  "price":"Enter the price",
  "priceCurrent":["", "USD", "RUR"],
  "priceValidUntil":"Enter time format Year Month Day (no validation)",
  "url":"Enter the url of the offer"
},
}
#if array it is selectable options. if array contains empty value, it is entry point "Enter Your value". If tupple have only one option it is preselected. If value in tupple is equal to asterisk, then insert as much as possible values, and if there are none to add enter nothing to end up an array
context = {"@context":"https://schema.org/"}
context_type = MTYPE
variable = MTYPE[0].key
question_context = f'''Do you have an {variable}'''

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