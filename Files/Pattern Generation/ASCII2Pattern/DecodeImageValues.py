import json

# Define the decode bitmap pattern dictionary
decode_bitmap_pattern = {
        "0000": "0",
        "0001": "1",
        "0010": "2",
        "0011": "3",
        "0100": "4",
        "0101": "5",
        "0110": "6",
        "0111": "7",
        "1000": "8",
        "1001": "9",
        "1111": "A"
    }

def read_binary_file(file_path):
    # Read binary values from the text file
    with open(file_path, 'r') as file:
        binary_values = file.read().splitlines()
    return binary_values

def group_binary_values(binary_values, group_size=4):
    # Group binary values into sets of specified size
    grouped_values = [''.join(binary_values[i:i+group_size]) for i in range(0, len(binary_values), group_size)]
    return grouped_values

def decode_binary_values(grouped_values, decode_map):
    # Decode grouped binary values to decimal values using the provided map
    decoded_values = [decode_map[group] for group in grouped_values if group in decode_map]
    return decoded_values

def write_decoded_values(file_path, decoded_values):
    # Write decoded values to a new text file
    with open(file_path, 'w') as file:
        for value in decoded_values:
            file.write(f"{value}\n")

# Example usage
input_file_path = 'ASCII2Pattern_Image.txt'
output_file_path = 'ASCII2Pattern_Decode_Values.txt'

# Step 1: Read binary values from file
binary_values = read_binary_file(input_file_path)

# Step 2: Group binary values into sets of four
grouped_values = group_binary_values(binary_values, 4)

# Step 3: Decode binary values to decimal values
decoded_values = decode_binary_values(grouped_values, decode_bitmap_pattern)

# Step 4: Write decoded values to a new file
write_decoded_values(output_file_path, decoded_values)

print(f"Decoded values saved to {output_file_path}")
