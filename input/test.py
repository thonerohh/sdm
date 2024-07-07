import os
import json

current_dir = os.path.abspath(os.path.dirname(__file__))
# add dir of init file
project_dir = os.path.join(current_dir, "..")
output_dir = os.path.join(project_dir, "output")

def ask_for_directory():
    while True:
        directory = input("Enter the directory containing .json or .jsonld files: ")
        if os.path.isdir(directory):
            return directory
        print("Invalid directory. Please try again.")

def process_array(key, value):
    if not value:
        return []
    
    if all(isinstance(item, str) and item for item in value):
        print(f"Options for {key}:")
        for i, option in enumerate(value):
            print(f"{i+1}. {option}")
        choice = input("Enter the number of your choice or nothing to delete key: ")
        if choice.isdigit() and 1 <= int(choice) <= len(value):
            return value[int(choice) - 1]
        return None
    
    result = []
    while True:
        entry = input(f"Enter value for {key} or press Enter to stop: ")
        if entry == "":
            break
        result.append(entry)
    return result

def process_string(key, value):
    if value:
        choice = input(f"The current value of '{key}' is '{value}'. Do you want to keep it? (y/n) or press Enter to delete key: ")
        if choice.lower() == 'y':
            return value
    return input(f"Enter new value for '{key}' or press Enter to delete key: ")

def process_integer(key, value):
    result = input(f"Enter a number for {key} or press Enter to delete key: ")
    return int(result) if result.isdigit() else None

def process_key(key, value):
    if key.startswith("@"):
        if isinstance(value, str):
            if value:
                return value
            else:
                return input(f"Enter value for '{key}' or press Enter to delete key: ")
        elif isinstance(value, list):
            return process_array(key, value)
    elif isinstance(value, dict):
        return process_json(value)
    elif isinstance(value, list):
        return process_array(key, value)
    elif isinstance(value, str):
        return process_string(key, value)
    elif isinstance(value, int):
        return process_integer(key, value)
    return value

def process_json(data):
    updated_data = {}
    for key, value in data.items():
        print(f"Processing key: {key}")
        updated_value = process_key(key, value)
        if updated_value is not None:
            updated_data[key] = updated_value
    return updated_data

def main():
    directory = ask_for_directory()
    
    for filename in os.listdir(directory):
        if filename.endswith(".json") or filename.endswith(".jsonld"):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r', encoding='utf-8') as file:
                data = json.load(file)
            
            print(f"\nEditing {filename}...\n")
            updated_data = process_json(data)
            
            filepath = os.path.join(output_dir, filename)
            with open(filepath, 'w', encoding='utf-8') as file:
                json.dump(updated_data, file, ensure_ascii=False, indent=4)
            print(f"{filename} has been updated.\n")

if __name__ == "__main__":
    main()
"""
This script was generated with the assistance of ChatGPT, a language model developed by OpenAI.
"""
