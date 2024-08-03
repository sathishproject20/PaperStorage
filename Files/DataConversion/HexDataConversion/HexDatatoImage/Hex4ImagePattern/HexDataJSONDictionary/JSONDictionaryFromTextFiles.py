import json

def create_json_from_text_files(file1, file2, output_file='Dictionary.json'):
    data = {}
    
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        lines1 = f1.readlines()
        lines2 = f2.readlines()
        
        # Assuming both files have the same number of lines
        for key, value in zip(lines1, lines2):
            key = key.strip()  # Remove any leading/trailing whitespace
            value = value.strip()  # Remove any leading/trailing whitespace
            data[key] = value
    
    with open(output_file, 'w') as outfile:
        json.dump(data, outfile, indent=4)
    
    print(f"JSON document created with key-value pairs from {file1} and {file2}, saved to {output_file}")

# Example usage:
file1 = 'Keys.txt'
file2 = 'Values.txt'
output_file = 'Dictionary.json'
create_json_from_text_files(file1, file2, output_file)
