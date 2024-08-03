# Define the bitmap pattern dictionary
bitmap_pattern = {
    "0": "100",
    "1": "010",
    "2": "001",
    "3": "000",
    "4": "1",
    "5": "0",
    "6": "00",
    "7": "11",
    "8": "01",
    "9": "10",
    "/": "111"
}

def read_input_string(file_path):
    """Read input string from a text file."""
    with open(file_path, 'r') as file:
        return file.read().strip()

def string_to_binary(string, pattern):
    """Convert the input string to a binary string using the pattern dictionary."""
    binary_string = ''.join(pattern[char] for char in string)
    return binary_string

def save_binary_string(binary_string, output_file_path):
    """Save the binary string to a text file."""
    with open(output_file_path, 'w') as file:
        file.write(binary_string)

# Example usage
input_file_path = 'ASCIIData_File.txt.txt'  # Path to the text file containing the input string
output_file_path = 'ImageDataPattern_File.txt'  # Path to the output text file to save the converted data

# Read input string from the file
input_string = read_input_string(input_file_path)

# Convert the input string to a binary string using the bitmap pattern
binary_string = string_to_binary(input_string, bitmap_pattern)

# Save the binary string to a new text file
save_binary_string(binary_string, output_file_path)

print(f"Converted data saved to {output_file_path}")
