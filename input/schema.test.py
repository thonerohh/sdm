import json
import os
import sys

# specify current directory
current_dir = os.path.dirname(os.path.realpath(__file__))

# Define the schema.org pattern for a Person
geo_schema = {
    "@context": "https://schema.org",
    "@type": "GeoCoordinates",
    "latitude": "",
    "longitude": ""
}
review_schema = {
    "@context": "https://schema.org",
    "@type": "Review",
    "author": "",
    "datePublished": "",
    "reviewRating": "",
    "reviewBody": ""
}
aggregate_rating_schema = {
    "@context": "https://schema.org",
    "@type": "AggregateRating",
    "ratingValue": "",
    "bestRating": "",
    "worstRating": "",
    "ratingCount": ""
} 
contact_schema = {
    "@context": "https://schema.org",
    "@type": "ContactPoint",
    "contactType": ["customer service", "technical support", "billing support", "bill payment", "sales", "reservations", "credit card support", "emergency", "baggage tracking", "roadside assistance", "package tracking", "flight information", "24/7 customer service", "24/7 technical support", "24/7 billing support", "24/7 bill payment", "24/7 sales", "24/7 reservations", "24/7 credit card support", "24/7 emergency", "24/7 baggage tracking", "24/7 roadside assistance", "24/7 package tracking", "24/7 flight information", ""],
    "telephone": "",
    "email": ""
}
brand_schema = {
    "@context": "https://schema.org",
    "@type": "Brand",
    "name": "",
    "url": "",
    "logo": ""
}

warranty_schema = {
    "@context": "https://schema.org",
    "@type": "WarrantyPromise",
    "durationOfWarranty": ""
}
address_schema = {
    "@context": "https://schema.org",
    "@type": "PostalAddress",
    "streetAddress": "",
    "addressLocality": "",
    "addressRegion": "",
    "postalCode": "",
    "addressCountry": ""
}
offer_schema = {
    "@context": "https://schema.org",
    "@type": "Offer",
    "availability":["https://schema.org/InStock","https://schema.org/OutOfStock","https://schema.org/PreOrder","https://schema.org/BackOrder","https://schema.org/InStoreOnly","https://schema.org/OnlineOnly"],
    "price": "",
    "priceCurrency": "",
    "url": "",
    "warranty": [warranty_schema]
}
product_schema = {
    "@context": "https://schema.org",
    "@type": "Product",
    "name": "",
    "description": "",
    "sku": "",
    "brand": "",
    "image": "",
    "offers": [offer_schema]
}
person_schema = {
    "@context": "https://schema.org",
    "@type": "Person",
    "name": "",
    "names": [],
    "surname": "",
    "email": "",
    "telephone": "",
    "address": [address_schema],
    "endSleep": ["","00:00", "00:30", "01:00", "01:30", "02:00", "02:30", "03:00", "03:30", "04:00", "04:30", "05:00", "05:30", "06:00", "06:30", "07:00", "07:30", "08:00", "08:30", "09:00", "09:30", "10:00", "10:30", "11:00", "11:30", "12:00", "12:30", "13:00", "13:30", "14:00", "14:30", "15:00", "15:30", "16:00", "16:30", "17:00", "17:30", "18:00", "18:30", "19:00", "19:30", "20:00", "20:30", "21:00", "21:30", "22:00", "22:30", "23:00", "23:30"],
    "startSleep": ["","00:00", "00:30", "01:00", "01:30", "02:00", "02:30", "03:00", "03:30", "04:00", "04:30", "05:00", "05:30", "06:00", "06:30", "07:00", "07:30", "08:00", "08:30", "09:00", "09:30", "10:00", "10:30", "11:00", "11:30", "12:00", "12:30", "13:00", "13:30", "14:00", "14:30", "15:00", "15:30", "16:00", "16:30", "17:00", "17:30", "18:00", "18:30", "19:00", "19:30", "20:00", "20:30", "21:00", "21:30", "22:00", "22:30", "23:00", "23:30"],
    "products": [product_schema]
}
local_business_schema = {
    "@context": "https://schema.org",
    "@type": "LocalBusiness",
    "name": "",
    "description": "",
    "url": "",
    "telephone": "",
    "address": [address_schema],
    "contactPoint": [contact_schema],
    "logo": "",
    "image": "",
    "openingHours": ["", "Mo-Su 00:00-23:59"],
    "priceRange": "",
    "currenciesAccepted": ["", "USD", "RUR"],
    "paymentAccepted": ["","Cash","Credit Card","Cash and credit card"],
    "hasMap": "",
    "geo": [geo_schema],
    "review": [review_schema],
    "aggregateRating": [aggregate_rating_schema],
    "servesCuisine": "",
    "menu": "",
    "acceptsReservations": "",
}
organization_schema = {
    "@context": "https://schema.org",
    "@type": "Organization",
    "name":"",
    "description":"",
    "address": [address_schema],
    "contactPoint": [contact_schema],
    "member": [person_schema],
    "product": [product_schema],
    "localBusiness": [local_business_schema],
    "url": "",
    "logo": "",
    "openingHours": ["", "Mo-Su 00:00-23:59"],
    "sameAs":[]
}
schemas = [
    person_schema,
    local_business_schema,
    organization_schema,
    product_schema,
    offer_schema
]

def ask_questions(pattern):
    keys = list(pattern.keys())  # Make a copy of the keys
    for key in keys:
        value = pattern[key]
        if key.startswith('@'):
            continue  # Skip keys that start with '@'
        if isinstance(value, dict):
            print(f"Please provide details for {key}:")
            pattern[key] = ask_questions(value)
        elif isinstance(value, list):
            # check if the list is not empty
            if len(value) > 0:
                if isinstance(value[0], dict):
                    # ask do you want to add this item
                    add_item = input(f"Do you want to add items to {key}? (yes/no): ").strip().lower()
                    if add_item == 'y' or add_item == 'yes':
                        while True:
                            print(f"Adding items to {key}.")
                            item = ask_questions(value[0].copy())
                            pattern[key].append(item)
                            add_more = input("Do you want to add another item? (yes/no): ").strip().lower()
                            if add_more != 'y' and add_more != 'yes':
                                # remove [0] item from the list
                                pattern[key].pop(0)
                                # print the list of items
                                print(f"{key}:")
                                for i, item in enumerate(pattern[key], 1):
                                    print(f"{i}. {item}")
                                # ask is it ok to keep the list
                                keep_list = input("Do you want to keep the list? (yes/no): ").strip().lower()
                                if keep_list != 'y' and keep_list != 'yes':
                                    # remove the list
                                    pattern.pop(key)
                                break
                    else:
                        # remove this key
                        pattern.pop(key)
                    
                else:
                    # make a list of options
                    print(f"Please select a {key} from the following options:")
                    for i, option in enumerate(pattern[key], 1):
                        if option == "":
                            print(f"{i}. Enter your own value")
                        else:
                            print(f"{i}. {option}")
                    # make a choice
                    choice = int(input("Select an option (number): ")) - 1
                    # check if pattern[choice] is not empty
                    if pattern[key][choice] != "":
                        pattern[key] = value[choice]
                    else:
                        # if empty, ask for input
                        pattern[key] = input(f"Please provide {key}: ").strip()
                    
            #  if list is empty ask until no answer
            else:
                print(f"Please provide values for {key}. Press Enter without typing anything to stop.")
                values = []
                while True:
                    item = input(f"Add a value to {key}: ").strip()
                    if item:
                        values.append(item)
                    else:
                        pattern[key] = values
                        break
        else:
            if value:
                print(f"Please provide {key} (or press Enter to keep the default value '{value}'): ")
                pattern[key] = input(f"{key}: ").strip() or value
            else:
                pattern[key] = input(f"Please provide {key}: ").strip()
    # remove all empty patterns
    keys = list(pattern.keys())  # Make a copy of the keys
    for key in keys:
        if pattern[key] == "":
            pattern.pop(key)

    return pattern

def main(output_dir, output_filename = None):
    
    print("You will be asked to select schema type.")
    print("Please select from the following options:")
    for i, schema in enumerate(schemas, 1):
        print(f"{i}. {schema['@type']}")
    choice = int(input("Select an option (number): ")) - 1

    # select what to do with pattern 1. answer questions 2. save as jsonld 3. validate from file or inserted object
    action_options = ["Answer questions", "Save as JSON-LD", "IN PROGRESS Validate from file", "IN PROGRESS Validate with terminal"]
    print("Please select what you want to do:")
    for i, option in enumerate(action_options, 1):
        print(f"{i}. {option}")
    action = int(input("Select an option (number): ")) - 1
    
    if action == 0:
        pattern_data = ask_questions(schemas[choice])
    elif action == 1:
        pattern_data = schemas[choice]
    else:
        print("This option is not yet implemented.")
        return
    
    print("Here is your completed schema.org data:")
    print(json.dumps(pattern_data, indent=4))

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if output_filename is not None:
        filename = output_filename
    elif 'name' in pattern_data and '@type' in pattern_data:
        filename = f"{pattern_data['name']}.{pattern_data['@type']}.jsonld"
    elif '@type' in pattern_data:
        filename = f"{pattern_data['@type']}.jsonld"
    else:
        filename = "schema.org.jsonld"

    filename = os.path.join(output_dir, filename)

    # save file as jsonld
    with open(filename, "w") as f:
        json.dump(pattern_data, f, indent=4)

if __name__ == "__main__":
    # specify output dir as the current directory back to the root 1 time and then "output" directory
    output_dir = os.path.join(current_dir, "../output")
    main(output_dir, "default.jsonld")
