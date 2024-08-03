import json
import os

def convert_ascii_to_pattern(input_file, json_file, output_dir="output"):
    # Read the JSON dictionary
    with open(json_file, 'r') as jf:
        ascii_dict = json.load(jf)

    # Read the input text file
    with open(input_file, 'r') as f:
        text_data = f.read()

    # Ensure output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Initialize the result string
    result_string = ""
    delimiter = "A"

    # Convert every two ASCII decimals to the corresponding dictionary value and add delimiters
    for i in range(0, len(text_data) - 1, 2):
        key = f"({ord(text_data[i])}, {ord(text_data[i+1])})"
        if key in ascii_dict:
            result_string += ascii_dict[key] + delimiter

    # Create the output filename
    base_name = os.path.basename(input_file)
    output_filename = f"ASCII2PatternData_{base_name}"
    output_file_path = os.path.join(output_dir, output_filename)

    # Save the result string to a text file
    with open(output_file_path, 'w') as of:
        of.write(result_string)

    print(f"Converted data saved to {output_file_path}")

# Example usage
input_file = "File.txt"  # Path to your input text file
json_file = "ASCII2Pattern.json"  # Path to your JSON dictionary file
convert_ascii_to_pattern(input_file, json_file)
