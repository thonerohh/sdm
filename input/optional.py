import subprocess
import os

import requests
from request.gemini import get_structured_data

import json
import argparse

current_dir = os.path.abspath(os.path.dirname(__file__))
# add dir of init file
project_dir = os.path.join(current_dir, "..")

def get_string_value():
    value = input("Enter a string value: ")
    if (value.startswith('"') and value.endswith('"')):
        value = f'{value}'
    return value

def get_integer_value():
    while True:
        value = input("Enter an integer value: ")
        if value.isdigit():
            return int(value)
        else:
            print("Invalid input. Please enter an integer.")

def get_array_value():
    array = []
    while True:
        value = input("Add your value or enter nothing to finish: ")
        if value.startswith('[') and value.endswith(']'):
            # if value have separator "," split and append each value to array
            value = value[1:-1].split(",")
            for val in value:
                if val.isdigit():
                    array.append(int(val))
                else:
                    array.append(val)
        elif value == "":
            break
        else:
            array.append(value)
    return array

def get_object_value():
    return get_user_input()


def enter_file():
    file_path = input("Enter the file path: ")
    
    # Check for valid extensions
    if not (file_path.endswith('.py') or file_path.endswith('.bat')):
        return "Invalid file extension. Only .py or .bat files are accepted."

    # Check if file exists
    if not os.path.isfile(file_path):
        return "File does not exist."

    try:
        # Run the file and capture the output
        if file_path.endswith('.py'):
            # Run Python file
            result = subprocess.run(['python', file_path], capture_output=True, text=True)
        elif file_path.endswith('.bat'):
            # Run batch file
            result = subprocess.run([file_path], capture_output=True, text=True, shell=True)
        
        # Return the response of the file
        return result.stdout if result.returncode == 0 else result.stderr
    except Exception as e:
        return f"An error occurred: {e}"

def enter_link():
    while True:
        try:
            link = input("Enter the link or enter nothing to stop: ")
            # validate link
            if not link.startswith("http"):
                print("Invalid link. Please enter a valid URL.")
                continue
            elif link == "":
                return None
            return get_structured_data(link)
        except Exception as e:
            print(f"An error occurred: {e}")
            continue
    
# Example usage
# print(enter_file())


# def enter_function():
    # ask if it is link or file
    # if link, ask for url
    # if file, ask for file path
    # return the value

def get_value(value_type):
    value_types = {
        "string": get_string_value,
        "integer": get_integer_value,
        "array": get_array_value,
        "object": get_object_value,
        "link": enter_link,
        # "script": enter_file,
    }
    return value_types[value_type]()

def get_user_input():
    types = {
        "string": str,
        "integer": int,
        "array": list,
        "object": dict,
        "link": str,
        # "script": str,
    }
    obj = {}
    while True:
        print (obj)
        key = input("Enter key name (or press enter to finish): ")
        if key == "":
            break
        # ask "What type of value do you want to add?" and list the types 1 2 3 4
        print("What type of value do you want to add?")
        for i, (type_key, _) in enumerate(types.items(), 1):
            print(f"{i}. {type_key}")
        choice = int(input("Select an option (number): ")) - 1

        # get value based on the selected type
        value = get_value(list(types.keys())[choice])
        obj[key] = value
    return obj

# drop values from object save only keys and formats
def drop_values(obj):
    pattern = {}
    for key, value in obj.items():
        # if key started with @ pass it
        if key.startswith("@"):
            # add entirely key:value to pattern, then continue
            pattern[key] = value
            continue
        elif isinstance(value, dict):
            pattern[key] = drop_values(value)
        elif isinstance(value, list):
            # make pattern with options
            list_pattern = set()
            at_symbol_found = False
            for item in value:
                if isinstance(item, str):
                    if item.startswith("@"):
                        list_pattern.add(item[1:])
                        at_symbol_found = True
                    else:
                        list_pattern.add("")
                elif isinstance(item, dict):
                    for subkey in item.keys():
                        if subkey.startswith("@"):
                            list_pattern.add(subkey[1:])
                            at_symbol_found = True
                        else:
                            list_pattern.add(subkey)
            # If no "@" symbol was found, set pattern[key] to an empty list
            if not at_symbol_found:
                pattern[key] = []
            else:
                pattern[key] = list(list_pattern)
        elif isinstance(value, str):
            pattern[key] = ""
        elif isinstance(value, int):
            pattern[key] = 0
    return pattern


def main(output_directory, output_filename):
    user_data = get_user_input()
    print("Inserted:", user_data)

    # Drop all values from user_data and save as pattern
    pattern = drop_values(user_data)

    # Ensure output directory exists
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Get all files in output directory
    files = os.listdir(output_directory)

    # Get the highest number of pattern files
    pattern_files = [file for file in files if file.startswith("pattern_")]
    if pattern_files:
        pattern_file_num = max([int(file.split("_")[1].split(".")[0]) for file in pattern_files])
    else:
        pattern_file_num = 0

    # Get the highest number of user_data files
    user_data_files = [file for file in files if file.startswith(f"{output_filename}_")]
    if user_data_files:
        user_data_file_num = max([int(file.split("_")[1].split(".")[0]) for file in user_data_files])
    else:
        user_data_file_num = 0

    # Save pattern and user_data
    with open(f"{output_directory}/pattern_{pattern_file_num+1}.json", "w") as f:
        json.dump(pattern, f, indent=4)
    with open(f"{output_directory}/{output_filename}_{user_data_file_num+1}.json", "w") as f:
        json.dump(user_data, f, indent=4)

    print(f"Pattern saved as pattern_{pattern_file_num+1}.json")
    print(f"Data saved as {output_filename}_{user_data_file_num+1}.json")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate schema.org data")
    parser.add_argument("--output_directory", type=str, default=f"{project_dir}/output", help="Output directory")
    parser.add_argument("--output_filename", type=str, default="data", help="Output filename")
    args = parser.parse_args()

    output_dir = os.path.abspath(args.output_directory)
    output_filename = args.output_filename

    main(output_dir, output_filename)