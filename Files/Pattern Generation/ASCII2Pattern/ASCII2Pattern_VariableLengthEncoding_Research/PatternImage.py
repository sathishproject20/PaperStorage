from PIL import Image
import math

def text_to_bitmap(file_path, output_image_path):
    # Read the text data from the file
    with open(file_path, 'r') as file:
        data = file.read().replace('\n', '')

    # Calculate dimensions of the image
    data_length = len(data)
    width = math.ceil(math.sqrt(data_length))
    height = math.ceil(data_length / width)

    # Ensure the data length matches the width * height by padding with '0's if necessary
    padded_data = data.ljust(width * height, '0')

    # Create a new image with mode '1' (1-bit pixels, black and white)
    image = Image.new('1', (width, height))

    # Set the pixel values based on the 0s and 1s
    pixels = image.load()
    for y in range(height):
        for x in range(width):
            pixel_value = int(padded_data[y * width + x])
            pixels[x, y] = 1 - pixel_value  # 1 is white, 0 is black

    # Save the image
    image.save(output_image_path)

# Example usage
file_path = 'ImageBitMapPattern.txt'
output_image_path = 'PatternImage.png'

text_to_bitmap(file_path, output_image_path)
