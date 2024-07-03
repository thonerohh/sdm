import json

# Define the schema.org pattern for a Person
person_schema = {
    "@context": "https://schema.org",
    "@type": "Person",
    "name": "",
    "givenName": "",
    "familyName": "",
    "email": "",
    "telephone": "",
    "address": {
        "@type": "PostalAddress",
        "streetAddress": "",
        "addressLocality": "",
        "addressRegion": "",
        "postalCode": "",
        "addressCountry": ""
    }
}

def ask_questions(pattern):
    for key, value in pattern.items():
        if key.startswith('@'):
            continue  # Skip keys that start with '@'
        if isinstance(value, dict):
            print(f"Please provide details for {key}:")
            pattern[key] = ask_questions(value)
        else:
            pattern[key] = input(f"Please provide {key}: ").strip()
    return pattern

def main():
    print("You will be asked to provide information for a Person schema.")

    pattern_data = ask_questions(person_schema.copy())

    print("Here is your completed schema.org data:")
    print(json.dumps(pattern_data, indent=4))

if __name__ == "__main__":
    main()