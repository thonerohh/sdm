import os
import json
import argparse

current_dir = os.path.dirname(os.path.abspath(__file__))

def get_string_value():
    value = input("Enter a string value: ")
    if not (value.startswith('"') and value.endswith('"')):
        value = f'"{value}"'
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
        if value == "":
            break
        array.append(value)
    return array

def get_object_value():
    return get_user_input()

def get_value(value_type):
    if value_type == "string":
        return get_string_value()
    elif value_type == "integer":
        return get_integer_value()
    elif value_type == "array":
        return get_array_value()
    elif value_type == "object":
        return get_object_value()
    else:
        print("Invalid value type.")
        return None

def get_user_input():
    obj = {}
    while True:
        key = input("Enter key name (or press enter to finish): ")
        if key == "":
            break
        value_type = input("What type of value do you want to add? (string, integer, array, object): ").lower()
        value = get_value(value_type)
        obj[key] = value
    return obj

# drop values from object save only keys and formats
def drop_values(obj):
    pattern = {}
    for key, value in obj.items():
        if isinstance(value, dict):
            pattern[key] = drop_values(value)
        elif isinstance(value, list):
            pattern[key] = []
        else:
            pattern[key] = type(value).__name__
    return pattern

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate schema.org data")
    parser.add_argument("--output_directory", type=str, help="Output directory")
    parser.add_argument("--output_filename", type=str, help="Output filename")
    args = parser.parse_args()

    if args.output_directory is not None:
        output_dir = args.output_directory
    else:
        output_dir = current_dir
    
    if args.output_filename is not None:
        output_filename = args.output_filename
    else:
        output_filename = "data"

    user_data = get_user_input()
    print("User data:", user_data)
    # drop all values from user_data and save as pattern
    pattern = drop_values(user_data)

    # save pattern to file in directory ../output as pattern[n] and user_data as user_data[n]
    output_directory = current_dir+"../output"
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # get all files in output directory
    files = os.listdir(output_directory)
    # get all pattern files
    pattern_files = [file for file in files if file.startswith("pattern")]
    # get all user_data files
    user_data_files = [file for file in files if file.startswith("user_data")]

    # get the highest number of pattern files
    if pattern_files:
        pattern_file = max([int(file.split("_")[1]) for file in pattern_files])
    else:
        pattern_file = 0
    
    # get the highest number of user_data files
    if user_data_files:
        user_data_file = max([int(file.split("_")[1]) for file in user_data_files])
    else:
        user_data_file = 0
    
    # save pattern and user_data
    with open(f"{output_directory}/pattern_{pattern_file+1}.json", "w") as f:
        json.dump(pattern, f, indent=4)
    with open(f"{output_directory}/{output_filename}_{user_data_file+1}.json", "w") as f:
        json.dump(user_data, f, indent=4)