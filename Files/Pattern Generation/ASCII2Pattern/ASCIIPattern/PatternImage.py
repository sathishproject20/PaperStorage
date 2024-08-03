from PIL import Image
import numpy as np
import math

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

def calculate_dimensions(binary_length, bits_per_pixel=1):
    """Calculate the dimensions of the image based on the binary data length."""
    total_pixels = binary_length // bits_per_pixel

    # Calculate the width and height
    width = int(math.ceil(math.sqrt(total_pixels)))
    height = int(math.ceil(total_pixels / width))

    return width, height

def binary_to_image(binary_string, width):
    """Generate a bitmap image from a binary string."""
    # Calculate the height of the image
    height = len(binary_string) // width
    if len(binary_string) % width != 0:
        # Add padding if needed
        padding_length = (width - len(binary_string) % width) % width
        binary_string += '0' * padding_length

    # Calculate the height with padding
    height = len(binary_string) // width

    # Create a NumPy array from the binary string
    array = np.array([int(bit) for bit in binary_string], dtype=np.uint8)
    array = array.reshape((height, width))

    # Convert 1s and 0s to 255 (white) and 0 (black)
    array = array * 255

    # Create an image from the NumPy array
    image = Image.fromarray(array, mode='L')
    return image

def save_and_show_image(image, output_file):
    """Save the image to a file and display it."""
    image.save(output_file)
    image.show()

# Example usage
input_file_path = 'ASCIIData_File.txt.txt'  # Path to the text file containing the input string
binary_string = string_to_binary(read_input_string(input_file_path), bitmap_pattern)

# Calculate the width and height of the image
width, height = calculate_dimensions(len(binary_string), bits_per_pixel=1)

# Generate the bitmap image
image = binary_to_image(binary_string, width)

# Save and display the image
output_file = 'ASCIIPattern_Image_File.png'
save_and_show_image(image, output_file)

print(f"Bitmap image saved to {output_file} with width {width} and height {height}")
