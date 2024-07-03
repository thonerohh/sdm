import json

# Define the schema.org pattern for a Person
person_schema = {
    "@context": "https://schema.org",
    "@type": "Person",
    "name": "",
    "names": [],
    "surname": "",
    "email": "",
    "telephone": "",
    "address": {
        "@type": "PostalAddress",
        "streetAddress": "",
        "addressLocality": "",
        "addressRegion": "",
        "postalCode": "",
        "addressCountry": ""
    },
    "sleepingHours": "",
    "sleepingMinutes": "",
    "startSlep": [
        "21:00",
        "21:30",
        "22:00",
        "22:30",
        "23:00",
        "23:30",
        ""
    ],
    "startSleep": [
        "21:00",
        "21:30",
        "22:00",
        "22:30",
        "23:00",
        "23:30",
        ""
    ]
}

def ask_questions(pattern):
    for key, value in pattern.items():
        if key.startswith('@'):
            continue  # Skip keys that start with '@'
        if isinstance(value, dict):
            print(f"Please provide details for {key}:")
            pattern[key] = ask_questions(value)
        elif isinstance(value, list):
            print(value)
            if len(value) > 0:
                # make a list of options
                print(f"Please select a {key} from the following options:")
                for i, option in enumerate(pattern[key], 1):
                    print(f"{i}. {option}")
                # make a choice
                choice = int(input("Select an option (number): ")) - 1
                # check if pattern[choice] is not empty
                if pattern[key][choice] != "":
                    print (f"You have selected: {pattern[key][choice]}")
                    pattern[key] = pattern[key][choice]
                else:
                    # if empty, ask for input
                    pattern[key] = input(f"Please provide {key}: ").strip()
            else:
                print(f"Please provide values for {key}. Press Enter without typing anything to stop.")
                values = []
                while True:
                    item = input(f"Add a value to {key}: ").strip()
                    if item:
                        values.append(item)
                    else:
                        break
            pattern[key] = values
        else:
            if key == "sleepingHours":
                while True:
                    try:
                        sleep_hours = input(f"Please provide hours of sleep or nothing (decimal): ")
                        if sleep_hours == "" or 0 <= float(sleep_hours) <= 24:
                            pattern[key] = sleep_hours
                            break
                        else:
                            print("Invalid input. Sleeping hours must be between 0 and 24.")
                    except ValueError:
                        print("Invalid input. Please enter a numeric value.")
            elif key == "sleepingMinutes":
                while True:
                    try:
                        sleep_minutes = input(f"Please provide minutes or nothing (decimal): ")
                        if sleep_minutes == "" or 0 <= float(sleep_minutes) <= 60:
                            pattern[key] = sleep_minutes
                            break
                        else:
                            print("Invalid input. Sleeping minutes must be between 0 and 60.")
                    except ValueError:
                        print("Invalid input. Please enter a numeric value.")
            elif key == "startSleep":
                start_sleep_options = pattern[key]
                print(f"Please select a {key} from the following options:")
                for i, option in enumerate(start_sleep_options, 1):
                    print(f"{i}. {option if option else 'Custom value'}")
                
                while True:
                    try:
                        selection = int(input("Enter the number of your choice: ").strip())
                        if 1 <= selection <= len(start_sleep_options):
                            if start_sleep_options[selection - 1]:
                                pattern[key] = start_sleep_options[selection - 1]
                            else:
                                pattern[key] = input("Please provide a custom startSleep value: ").strip()
                            break
                        else:
                            print("Invalid selection. Please choose a valid option number.")
                    except ValueError:
                        print("Invalid input. Please enter a number corresponding to your choice.")
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
