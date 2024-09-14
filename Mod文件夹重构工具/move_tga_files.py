import os
import shutil

def move_tga_files(base_dir):
    for subfolder_name in os.listdir(base_dir):
        subfolder_path = os.path.join(base_dir, subfolder_name)
        
        if os.path.isdir(subfolder_path):
            target_folder = os.path.join(subfolder_path, 'StarlitSeason', 'Content', 'Widget', 'LoadTexture', 'UnitDress')
            os.makedirs(target_folder, exist_ok=True)

            for file_name in os.listdir(subfolder_path):
                if file_name.lower().endswith('.tga'):
                    file_path = os.path.join(subfolder_path, file_name)
                    shutil.move(file_path, os.path.join(target_folder, file_name))
                    print(f"Moved {file_name} to {target_folder}")

if __name__ == "__main__":
    base_directory = os.getcwd()  # Use current directory
    move_tga_files(base_directory)
