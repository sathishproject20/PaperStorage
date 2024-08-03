import os
import json

def list_subfolders_and_save_json(folder_path, json_file_path):
    def get_num_files(path):
        return len([f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))])

    def list_subfolders_recursive(current_path, prefix="", folder_list=[]):
        subfolders = [f.path for f in os.scandir(current_path) if f.is_dir()]
        subfolders.sort()

        for idx, subfolder in enumerate(subfolders, start=1):
            subfolder_title = f"{prefix}{idx}"
            subfolder_path = subfolder
            num_files = get_num_files(subfolder)

            subfolder_info = {
                "Index No": len(folder_list) + 1,
                "Folder Title": f"SUB{subfolder_title}",
                "Folder Path": subfolder_path,
                "No of Files": num_files
            }

            folder_list.append(subfolder_info)
            list_subfolders_recursive(subfolder, f"{subfolder_title}", folder_list)

        return folder_list

    root_folder_title = os.path.basename(folder_path)
    root_num_files = get_num_files(folder_path)

    data = [
        {
            "Index No": 0,
            "Folder Title": root_folder_title,
            "Folder Path": folder_path,
            "No of Files": root_num_files
        }
    ]

    data.extend(list_subfolders_recursive(folder_path))

    with open(json_file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

    print(f"Data saved to {json_file_path}")

# Example usage:
folder_path = "PATH TO FOLDER"
json_file_path = "folder_and_subfolders_data.json"
list_subfolders_and_save_json(folder_path, json_file_path)
