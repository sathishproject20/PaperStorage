import os
import json

def load_encoding_dictionary(dictionary_file_path):
    with open(dictionary_file_path, 'r') as file:
        encoding_dict = json.load(file)
    return encoding_dict

def convert_hex_data(input_file_path, encoding_dict, output_file_path):
    unmapped_values = []

    def hex_to_encoded_value(hex_value):
        return encoding_dict.get(hex_value.upper(), None)  # Convert hex_value to uppercase

    with open(input_file_path, 'r') as file:
        lines = file.readlines()

    with open(output_file_path, 'w') as outfile:
        for line in lines:
            line = line.strip()
            if len(line) % 6 != 0:
                unmapped_values.append(line)
                # Padding the line to make its length a multiple of 6
                line = line.ljust((len(line) // 6 + 1) * 6, '0')

            encoded_line = []
            for i in range(0, len(line), 6):
                hex_chunk = line[i:i+6]
                if len(hex_chunk) == 6:
                    red_value = hex_to_encoded_value(hex_chunk[0:2])
                    green_value = hex_to_encoded_value(hex_chunk[2:4])
                    blue_value = hex_to_encoded_value(hex_chunk[4:6])
                    if red_value is not None and green_value is not None and blue_value is not None:
                        rgb_tuple = (int(red_value), int(green_value), int(blue_value))
                        encoded_line.append(rgb_tuple)
                    else:
                        print(f"Warning: Value for hex '{hex_chunk}' not found in encoding dictionary.")
                        encoded_line.append((0, 0, 0))  # Adding a default RGB tuple if not found in the dictionary
                else:
                    unmapped_values.append(hex_chunk)

            for rgb in encoded_line:
                outfile.write(f"{rgb}\n")

    return unmapped_values

# Example usage:
input_file = 'Hex6Data.txt'
output_file = 'Hex6RGBColor.txt'
encoding_dict_file = 'Hex_ASCIIDecimal_Encode_Dict.json'

encoding_dict = load_encoding_dictionary(encoding_dict_file)
unmapped_values = convert_hex_data(input_file, encoding_dict, output_file)

print("Unmapped Values:")
for value in unmapped_values:
    print(value)
