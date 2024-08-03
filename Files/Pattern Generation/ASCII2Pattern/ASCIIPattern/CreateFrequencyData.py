import json
from collections import Counter

def count_frequency_and_generate_bitmap_from_file(input_file, json_output_file):
    # Read the text data from the input file
    with open(input_file, 'r') as f:
        text_data = f.read()
    
    # Count the frequency of each integer and delimiter in the text
    frequency_counter = Counter(text_data)
    
    # Sort the items by frequency (descending) and then by character (ascending)
    sorted_items = sorted(frequency_counter.items(), key=lambda x: (-x[1], x[0]))
    
    # Define the frequency pattern for bitmap
    frequency_pattern = [
        "0", "1", "00", "01", "10", "11", "000", "001", "010", "100", "111"
    ]
    
    # Assign bitmap patterns based on frequency
    bitmap_pattern = {}
    for i, (char, _) in enumerate(sorted_items):
        if i < len(frequency_pattern):
            bitmap_pattern[char] = frequency_pattern[i]
        else:
            # If more unique characters than frequency patterns, use a generic pattern
            bitmap_pattern[char] = f'pattern_{i}'

    # Create the final dictionary
    result = {
        "DataFrequency": dict(frequency_counter),
        "BitMapPattern": bitmap_pattern
    }
    
    # Save the result to a JSON file
    with open(json_output_file, 'w') as f:
        json.dump(result, f, indent=4)

# Example usage
input_file = 'ASCIIData_File.txt.txt'  # Path to the text input file
json_output_file = 'frequency_bitmap.json'  # Path to the JSON output file

count_frequency_and_generate_bitmap_from_file(input_file, json_output_file)
