import os
import json

def create_json_from_text_files(keys_folder, values_folder, output_folder='ascii2pattern_files'):
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)
    
    # Get sorted list of files from both folders
    keys_files = sorted([f for f in os.listdir(keys_folder) if f.startswith('ASCII2Permutations_') and f.endswith('.txt')])
    values_files = sorted([f for f in os.listdir(values_folder) if f.startswith('SequenceNumbers_') and f.endswith('.txt')])
    
    # Check if both folders have the same number of files
    if len(keys_files) != len(values_files):
        print("Mismatch in the number of files in keys and values folders.")
        return
    
    # Create JSON dictionary files for each pair of files
    for key_file, value_file in zip(keys_files, values_files):
        key_file_path = os.path.join(keys_folder, key_file)
        value_file_path = os.path.join(values_folder, value_file)
        
        data = {}
        
        with open(key_file_path, 'r') as f1, open(value_file_path, 'r') as f2:
            lines1 = f1.readlines()
            lines2 = f2.readlines()
            
            # Assuming both files have the same number of lines
            for key, value in zip(lines1, lines2):
                key = key.strip()  # Remove any leading/trailing whitespace
                value = value.strip()  # Remove any leading/trailing whitespace
                data[key] = value
        
        output_file = os.path.join(output_folder, f'ASCII2Pattern_{key_file.split("_")[1].split(".")[0]}.json')

        with open(output_file, 'w') as outfile:
            json.dump(data, outfile, indent=4)
        
        print(f"JSON document created with key-value pairs from {key_file} and {value_file}, saved to {output_file}")

# Example usage:
keys_folder = 'ascii2'
values_folder = 'sequencenumbers'
create_json_from_text_files(keys_folder, values_folder)
