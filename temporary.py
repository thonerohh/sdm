import os
import shutil
import re

# Define the base path
base_path = r"C:\rohhs\scripts\python\sdm\structureddataminified\input\pattern\schema\thing"

# Regex pattern to identify directories ending with "thing"
pattern = re.compile(r'.*thing$')

# Function to remove empty directories
def remove_empty_dirs(root):
    for dirpath, dirnames, filenames in os.walk(root, topdown=False):
        if not dirnames and not filenames:
            os.rmdir(dirpath)

# Traverse the directory structure
for root, dirs, files in os.walk(base_path):
    for dir_name in dirs:
        if pattern.match(dir_name):
            dir_path = os.path.join(root, dir_name)
            new_dir_name = dir_name[:-5]  # Remove the last 5 characters "thing"
            new_dir_path = os.path.join(root, new_dir_name)
            
            if not os.path.exists(new_dir_path):
                os.makedirs(new_dir_path)
            
            # Traverse the directory to find .json files
            for sub_root, sub_dirs, sub_files in os.walk(dir_path):
                for file_name in sub_files:
                    if file_name.endswith('.jsonld'):
                        file_path = os.path.join(sub_root, file_name)
                        # Move the .json file to the root of the renamed directory
                        new_file_path = os.path.join(new_dir_path, file_name)
                        shutil.move(file_path, new_file_path)
            
            # Remove the old .thing directory
            shutil.rmtree(dir_path)

# Remove any empty directories that may have been left behind
remove_empty_dirs(base_path)

print("Completed processing the directories.")
