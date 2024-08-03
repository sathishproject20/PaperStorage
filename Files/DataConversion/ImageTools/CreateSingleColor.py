from PIL import Image
import os

def generate_image_single_color(hex_color, width, height):
    image = Image.new("RGB", (width, height), hex_color)
    return image

def save_image(image, file_path):
    image.save(file_path)
    file_size = os.path.getsize(file_path)
    print(f"File saved at {file_path}, size: {file_size} bytes")

# Define a single hex color (e.g., black)
single_color = "#FFFFFF"

# Generate a 1024x1024 image with the single color
width, height = 1024, 1024
image = generate_image_single_color(single_color, width, height)

# Save the image to a file
image_file_path = 'SingleColorImage.png'
save_image(image, image_file_path)
