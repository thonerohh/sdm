import os
import json

# import optional.py's get_user_input() function
from optional import get_user_input

current_dir = os.path.abspath(os.path.dirname(__file__))
# add dir of init file
project_dir = os.path.join(current_dir, "..")
output_dir = os.path.join(project_dir, "output")

def get_file_path():
    directory = input("Enter the directory containing .json or .jsonld files: ")
    while not os.path.isdir(directory):
        print("Invalid directory. Please try again.")
        directory = input("Enter the directory containing .json or .jsonld files: ")

    files = [f for f in os.listdir(directory) if f.endswith('.json') or f.endswith('.jsonld')]
    if not files:
        print("No .json or .jsonld files found in the directory.")
        return None
    
    print("Select a file to edit:")
    for i, file in enumerate(files):
        print(f"{i+1}. {file}")
    
    file_index = int(input("Enter the number of the file: ")) - 1
    if file_index < 0 or file_index >= len(files):
        print("Invalid selection. Exiting.")
        return None
    
    return os.path.join(directory, files[file_index])

def edit_json(data):
    for key in list(data.keys()):
        if key.startswith('@'):
            if isinstance(data[key], str):
                if not data[key]:
                    new_value = input(f"{key} is empty. Enter value or enter nothing to delete key: ")
                    if new_value:
                        data[key] = new_value
                    else:
                        del data[key]
            elif isinstance(data[key], list):
                print(f"{key} has the following options:")
                for i, option in enumerate(data[key]):
                    print(f"{i+1}. {option}")
                new_value = input(f"Enter the number of the option or enter nothing to delete key: ")
                if new_value:
                    data[key] = data[key][int(new_value) - 1]
                else:
                    del data[key]
            continue
        
        if isinstance(data[key], dict):
            # if dict have no keys
            if not data[key]:
                answer = input(f"{key} is an empty object.\nDo you want to fill this object? (y/n) or enter nothing to delete: ").lower()
                if answer == 'n':
                  continue # pass this key
                elif answer == 'y':
                  if input(f"Do you want to add keys to this empty object? (y/n): ").lower() == 'y':
                    data[key] = get_user_input()
                else:
                  del data[key]
                continue
            elif input(f"{key} is an nested object.\n Do you want to edit this object? (y/n): ").lower() == 'y':
                edit_json(data[key])
            else:
                continue
        
        elif isinstance(data[key], list):
            if all(isinstance(item, str) for item in data[key]):
                if any(data[key]):
                    if all(data[key]):
                        print(f"{key} has the following predefined options:")
                        for i, option in enumerate(data[key]):
                            print(f"{i+1}. {option}")
                        new_value = input(f"Enter the number of the option or enter nothing to delete key: ")
                        if new_value:
                            data[key] = data[key][int(new_value) - 1]
                        else:
                            del data[key]
                    else:
                        print(f"{key} has the following options, with an option to enter a custom value:")
                        for i, option in enumerate(data[key]):
                            print(f"{i+1}. {option if option else 'Enter your value'}")
                        new_value = input(f"Enter the number of the option or enter nothing to delete key: ")
                        if new_value:
                            selected_option = data[key][int(new_value) - 1]
                            if not selected_option:
                                data[key] = input("Enter your custom value: ")
                            else:
                                data[key] = selected_option
                        else:
                            del data[key]
                else:
                    print(f"{key} is an empty array. Enter values or enter nothing to stop.")
                    new_values = []
                    while True:
                        new_value = input("Enter value or enter nothing to stop: ")
                        if new_value:
                            new_values.append(new_value)
                        else:
                            break
                    if new_values:
                        data[key] = new_values
                    else:
                        del data[key]
            else:
                print(f"{key} contains non-string elements. Skipping.")
        
        elif isinstance(data[key], str):
            if data[key]:
                new_value = input(f"{key} contains data '{data[key]}'. Do you want to remain it or enter different? (y/n): ")
                if new_value.lower() == 'n':
                    data[key] = input("Enter new value or enter nothing to delete key: ")
                    if not data[key]:
                        del data[key]
                elif not new_value:
                    del data[key]
            else:
                new_value = input(f"{key} is empty. Enter value or enter nothing to delete key: ")
                if new_value:
                    data[key] = new_value
                else:
                    del data[key]
        
        elif isinstance(data[key], int):
            new_value = input(f"{key} is an integer. Enter digit or number or enter nothing to delete key: ")
            if new_value:
                data[key] = int(new_value)
            else:
                del data[key]

def main():
    try:
        file_path = get_file_path()
        if not file_path:
            return
        
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        edit_json(data)
        
        filename = input("Enter the filename to save the updated data or enter nothing to use default: ")
        if not filename:
            filename = os.path.basename(file_path)
        
        output_path = os.path.join(output_dir, filename)

        with open(output_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        
        print("File has been updated.")
    except KeyboardInterrupt:
        print("\nKeyboardInterrupt detected. Saving the file with current data.")
        try:
            if not filename:
                filename = os.path.basename(file_path)
            output_path = os.path.join(output_dir, filename)
            with open(output_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
            print("File has been saved.")
        except Exception as e:
            print(f"Failed to save file. Error: {e}")

if __name__ == "__main__":
    """This script was generated with the assistance of ChatGPT and Gemini, a language model developed by OpenAI and Bard at Google at Alphabet."""
    main()