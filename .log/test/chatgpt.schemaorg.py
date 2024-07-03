import json

# Define the schema.org patterns in an editable array
schema_patterns = {
    "Organization": {
        "@type": "Organization",
        "name": "",
        "url": "",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "",
            "addressLocality": "",
            "addressRegion": "",
            "postalCode": "",
            "addressCountry": ""
        },
        "products": [],
        "offers": [],
        "warranties": []
    },
    "Offer": {
        "@type": "Offer",
        "price": "",
        "priceCurrency": "",
        "itemOffered": ""
    },
    "Warranty": {
        "@type": "WarrantyPromise",
        "durationOfWarranty": {
            "@type": "QuantitativeValue",
            "value": "",
            "unitCode": ""
        },
        "warrantyScope": ""
    },
    "Product": {
        "@type": "Product",
        "name": "",
        "description": "",
        "sku": "",
        "brand": {
            "@type": "Brand",
            "name": ""
        }
    },
    "LocalBusiness": {
        "@type": "LocalBusiness",
        "name": "",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "",
            "addressLocality": "",
            "addressRegion": "",
            "postalCode": "",
            "addressCountry": ""
        },
        "telephone": "",
        "openingHours": ""
    }
}

def ask_questions(pattern):
    for key, value in pattern.items():
        if isinstance(value, dict):
            print(f"Please provide details for {key}:")
            pattern[key] = ask_questions(value)
        elif isinstance(value, list):
            add_more = input(f"Do you want to add items to {key}? (yes/no): ").strip().lower()
            while add_more == 'yes':
                item_type = input(f"What type of item do you want to add to {key}? ").strip()
                if item_type in schema_patterns:
                    item = ask_questions(schema_patterns[item_type].copy())
                    pattern[key].append(item)
                else:
                    print(f"Unknown item type: {item_type}. Please choose from {list(schema_patterns.keys())}.")
                add_more = input(f"Do you want to add another item to {key}? (yes/no): ").strip().lower()
        else:
            pattern[key] = input(f"Please provide {key}: ").strip()
    return pattern

def main():
    print("Available schema.org patterns:")
    for pattern in schema_patterns.keys():
        print(f"- {pattern}")

    selected_pattern = input("Please select a schema.org pattern: ").strip()
    if selected_pattern in schema_patterns:
        print(f"You have selected: {selected_pattern}")
        pattern_data = ask_questions(schema_patterns[selected_pattern].copy())

        print("Here is your completed schema.org data:")
        print(json.dumps(pattern_data, indent=4))
    else:
        print(f"Unknown pattern: {selected_pattern}")

if __name__ == "__main__":
    main()
