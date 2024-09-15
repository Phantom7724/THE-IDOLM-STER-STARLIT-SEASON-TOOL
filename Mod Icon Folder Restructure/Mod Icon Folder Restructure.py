import os
import shutil
import re

def move_files(base_dir):
    for subfolder_name in os.listdir(base_dir):
        subfolder_path = os.path.join(base_dir, subfolder_name)
        
        if os.path.isdir(subfolder_path):
            # Create target directory
            target_folder = os.path.join(subfolder_path, 'StarlitSeason', 'Content', 'Widget', 'LoadTexture', 'UnitDress')
            os.makedirs(target_folder, exist_ok=True)

            for file_name in os.listdir(subfolder_path):
                file_path = os.path.join(subfolder_path, file_name)
                
                # Handle .tga, .uasset, and .uexp files
                if file_name.lower().endswith(('.tga', '.uasset', '.uexp')):
                    # Extract the variable part from the filename for .uasset and .uexp files
                    if file_name.lower().endswith(('.uasset', '.uexp')):
                        match = re.match(r'^(WDT_cos\d+)[A-Z]\.(uasset|uexp)$', file_name)
                        if match:
                            base_name = match.group(1)
                            # We are still using the same target folder for simplicity
                        
                    shutil.move(file_path, os.path.join(target_folder, file_name))
                    print(f"Moved {file_name} to {target_folder}")

if __name__ == "__main__":
    base_directory = os.getcwd()  # Use current directory
    move_files(base_directory)
