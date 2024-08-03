import json
import os
import shutil

# Define maximum limits for different operating systems
MAX_FILENAME_LENGTH = 255
MAX_PATH_LENGTH = 260  # Windows limit, other systems may have different limits

def process_files_from_json(json_file_path, new_location):
    """
    Reads file details from a JSON file, processes each file, renames, and moves them to a new location.
    Saves the details of original and new file paths in a JSON document and records long file names separately.

    :param json_file_path: Path to the JSON file containing file details
    :param new_location: Directory path where the files will be saved with new names
    """
    # Read the JSON file
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    # Ensure the new location exists
    os.makedirs(new_location, exist_ok=True)

    # To store file name mappings and long file names
    file_name_mappings = []
    long_file_names = []

    # Process each file entry in the JSON data
    for idx, entry in enumerate(data):
        folder_title = entry.get("Folder Title")
        file_path = entry.get("File Path")

        # Get the base name of the file (e.g., '1024x1024.jpg')
        base_name = os.path.basename(file_path)
        # Construct the new file name
        new_file_name = f"{folder_title}_{idx}{os.path.splitext(base_name)[1]}"

        # Check if the file name length exceeds the maximum allowed limit
        if len(new_file_name) > MAX_FILENAME_LENGTH:
            # Save the original file name in the long_file_names list
            long_file_names.append({
                "file_id": idx,
                "original_file_path": file_path,
                "original_file_name": base_name
            })
            # Truncate the file name to fit within the limit
            new_file_name = f"{folder_title}_{idx}"

        # Define the new file path
        new_file_path = os.path.join(new_location, new_file_name)

        # Check if the total path length exceeds the maximum allowed limit
        if len(new_file_path) > MAX_PATH_LENGTH:
            print(f"Path '{new_file_path}' exceeds the maximum allowed length and cannot be processed.")
            continue

        # Check if the file exists at the given path
        if os.path.exists(file_path):
            # Copy and rename the file
            shutil.copy(file_path, new_file_path)
            print(f"File '{file_path}' has been renamed to '{new_file_path}' and copied.")
            # Save the file name mapping
            file_name_mappings.append({
                "file_id": idx,
                "original_file_path": file_path,
                "new_file_path": new_file_path,
                "new_file_name": new_file_name
            })
        else:
            print(f"File '{file_path}' does not exist.")

    # Save the file name mappings in a JSON document
    file_names_in_folder_path = os.path.join(new_location, "FileNamesinFolder.json")
    with open(file_names_in_folder_path, 'w') as file:
        json.dump(file_name_mappings, file, indent=4)
    print(f"File name mappings saved to '{file_names_in_folder_path}'.")

    # Save the long file names in a JSON document if any
    if long_file_names:
        long_file_names_path = os.path.join(new_location, "long_file_names.json")
        with open(long_file_names_path, 'w') as file:
            json.dump(long_file_names, file, indent=4)
        print(f"Long file names saved to '{long_file_names_path}'.")

# Example usage
json_file_path = 'files_in_a_folder.json'
new_location = 'FolderPath'
process_files_from_json(json_file_path, new_location)
