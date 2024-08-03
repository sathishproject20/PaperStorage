import os
import json

def load_existing_folder_data(json_file_path):
    with open(json_file_path, 'r') as json_file:
        return json.load(json_file)

def list_files_recursive(folder_data, file_list, folder_title_prefix=""):
    for folder in folder_data:
        folder_title = folder["Folder Title"]
        folder_path = folder["Folder Path"]

        for root, _, files in os.walk(folder_path):
            files.sort()
            for file in files:
                file_path = os.path.join(root, file)
                file_size = os.path.getsize(file_path)
                file_info = {
                    "Index No": len(file_list) + 1,
                    "Folder Title": folder_title,
                    "File Path": file_path,
                    "File Size": file_size
                }
                file_list.append(file_info)

        if "Sub Folders" in folder:
            list_files_recursive(folder["Sub Folders"], file_list, folder_title)

def create_file_list_json(existing_json_file_path, output_json_file_path):
    folder_data = load_existing_folder_data(existing_json_file_path)
    file_list = []
    list_files_recursive(folder_data, file_list)
    
    with open(output_json_file_path, 'w') as json_file:
        json.dump(file_list, json_file, indent=4)
    
    print(f"File data saved to {output_json_file_path}")

# Example usage:
existing_json_file_path = "folder_and_subfolders_data.json"
output_json_file_path = "files_in_folder_data.json"
create_file_list_json(existing_json_file_path, output_json_file_path)
