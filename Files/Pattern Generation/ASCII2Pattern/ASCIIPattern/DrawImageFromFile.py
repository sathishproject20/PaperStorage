from PIL import Image
import numpy as np
import math

def read_binary_data(file_path):
    """Read binary data from a text file."""
    with open(file_path, 'r') as file:
        return file.read().strip()

def calculate_dimensions(binary_length):
    """Calculate the dimensions of the image based on the binary data length."""
    total_pixels = binary_length

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

    # Convert 1s and 0s to 0 (black) and 255 (white)
    array = np.where(array == 1, 0, 255)

    # Create an image from the NumPy array
    image = Image.fromarray(array, mode='L')
    return image

def save_image(image, output_file):
    """Save the image to a file."""
    image.save(output_file)

# Example usage
input_file_path = 'ImageDataPattern_File.txt'  # Path to the text file containing the binary data
output_file_path = 'ASCIIPatternImage.png'  # Path to the output image file

# Read binary data from the file
binary_string = read_binary_data(input_file_path)

# Calculate the width and height of the image
width, height = calculate_dimensions(len(binary_string))

# Generate the bitmap image
image = binary_to_image(binary_string, width)

# Save the image to a file
save_image(image, output_file_path)

print(f"Bitmap image saved to {output_file_path} with width {width} and height {height}")
