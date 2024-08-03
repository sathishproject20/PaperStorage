def convert_to_bitmap_pattern(input_file_path, output_file_path, pattern_dict):
    # Read the data from the input file
    with open(input_file_path, 'r') as file:
        data = file.read().strip()

    # Initialize an empty string to store the converted pattern
    converted_pattern = ""

    # Convert each character in the data to its corresponding pattern
    for char in data:
        if char in pattern_dict:
            converted_pattern += pattern_dict[char]
        else:
            raise ValueError(f"Character '{char}' not found in pattern dictionary.")

    # Save the converted pattern to the output file
    with open(output_file_path, 'w') as file:
        file.write(converted_pattern)

# Example usage
input_file_path = 'ASCII2PatternData_File.txt'
output_file_path = 'ImageBitMapPattern.txt'
bitmap_pattern = {
        "0": "0",
        "1": "000",
        "2": "0010",
        "3": "00010",
        "4": "00",
        "5": "01000",
        "6": "010",
        "7": "0100",
        "8": "0000",
        "9": "00100",
        "A": "11",  # Delimiter pattern for values in dictionary
    }

convert_to_bitmap_pattern(input_file_path, output_file_path, bitmap_pattern)
