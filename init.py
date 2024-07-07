import os

current_directory = os.path.dirname(os.path.abspath(__file__))

# Get the absolute path of the schema.py file
schema_path = os.path.abspath("input/schema.py")
og_path = os.path.abspath("input/og.py")
optional_path = os.path.abspath("input/optional.py")
pattern_path = os.path.abspath("input/pattern.py")

actions = {
    "optional": optional_path,
    "pattern": pattern_path,
    "schema": schema_path,
    "og": og_path,
}

def main():
    print("Please select script to run:")
    for i, action in enumerate(actions, 1):
        print(f"{i}. {action}")
    choice = int(input("Select an option (number): ")) - 1

    output_directory = input("Enter the output directory or enter nothing to use default: ")
    output_filename = input("Enter the output filename or enter nothing to use default: ")

    # if entered nothing output in current directory
    if output_directory == '':
        output_directory = current_directory+"/output"
    if output_filename == '':
        # parse files in output directory to get the number of files with the same name
        files = [f for f in os.listdir(output_directory) if f.endswith('.json')]
        output_filename = f"default_{len(files)+1}.json"

    # create output directory if it does not exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    if choice == 2:
        # run schema.py
        os.system(f"python {actions['schema']} --output_directory {output_directory} --output_filename {output_filename}")
    elif choice == 3:
        # run og.py
        os.system(f"python {actions['og']} --output_directory {output_directory} --output_filename {output_filename}")
    elif choice == 0:
        # run optional.py
        os.system(f"python {actions['optional']} --output_directory {output_directory} --output_filename {output_filename}")
    elif choice == 1:
        # run pattern.py
        os.system(f"python {actions['pattern']} --output_directory {output_directory} --output_filename {output_filename}")
    else :
        print("Invalid selection. Exiting.")

if __name__ == "__main__":
    main()