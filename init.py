import os

current_directory = os.path.dirname(os.path.abspath(__file__))

# Get the absolute path of the schema.py file
schema_path = os.path.abspath("input/schema.py")
og_path = os.path.abspath("input/og.py")

actions = {
    "schema": schema_path,
    "og": og_path
}

def main():
    print("Please select script to run:")
    for i, action in enumerate(actions, 1):
        print(f"{i}. {action}")
    choice = int(input("Select an option (number): ")) - 1

    output_directory = input("Enter the output directory or enter nothing for default: ")
    output_filename = input("Enter the output filename or enter nothing for default: ")

    # if entered nothing output in current directory
    if output_directory == '':
        output_directory = current_directory+"/output"
    if output_filename == '':
        output_filename = "schema.org.jsonld"

    if choice == 0:
        # run schema.py
        os.system(f"python {actions['schema']} --output_directory {output_directory} --output_filename {output_filename}")
    elif choice == 1:
        # run og.py
        os.system(f"python {actions['og']} --output_directory {output_directory} --output_filename {output_filename}")

if __name__ == "__main__":
    main()