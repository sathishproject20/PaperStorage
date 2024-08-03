import json
import os
from collections import Counter

"""
The ASCII Decimal Values are converted into number keys for 2 ASCII Values in sequence using numbers from 0 to 65535.
The ASCII File with converted data is calculated for integers 0- 9 frequency to assign bit maps in a frequency pattern.
The least bit is assigned to most frequent number in the data and the process is continued for other numbers also.
There are 3,628,800 different frequency patterns emerge for integers 0-9.

"""

def create_frequency_and_bitmap(input_file, output_json_file):
    # Define the frequency pattern array
    frequency_pattern = [
         "0", "00", "010", "0010", "0100", "0010", "00010", "00100", "01000", "01010"
    ]

    # Initialize dictionaries for frequency and bit map pattern
    data_frequency = {str(i): 0 for i in range(10)}
    bit_map_pattern = {str(i): "" for i in range(10)}

    # Read the input text file and count the frequency of each integer
    with open(input_file, 'r') as f:
        text_data = f.read()
        frequency_count = Counter(text_data)

    # Update the data frequency dictionary
    for key, count in frequency_count.items():
        if key.isdigit():
            data_frequency[key] = count

    # Sort the frequencies in descending order
    sorted_frequencies = sorted(data_frequency.items(), key=lambda x: x[1], reverse=True)

    # Assign bit map values based on frequency
    for i, (number, _) in enumerate(sorted_frequencies):
        bit_map_pattern[number] = frequency_pattern[i]

    # Combine the dictionaries into a single dictionary
    combined_data = {
        "DataFrequency": data_frequency,
        "BitMapPattern": bit_map_pattern
    }

    # Save the combined data to a JSON file
    with open(output_json_file, 'w') as jf:
        json.dump(combined_data, jf, indent=4)

    print(f"Data frequency and bit map pattern saved to {output_json_file}")

# Example usage
input_file = "File.txt"  # Path to your input text file containing ASCII decimal data
output_json_file = "frequency_and_bitmap.json"  # Path to the output JSON file
create_frequency_and_bitmap(input_file, output_json_file)
