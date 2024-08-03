from PIL import Image
import os

def generate_unique_colors(file_path):
    with open(file_path, 'w') as file:
        for color in range(1048576):
            r = (color >> 16) & 0xFF
            g = (color >> 8) & 0xFF
            b = color & 0xFF
            hex_color = f'#{r:02X}{g:02X}{b:02X}\n'
            file.write(hex_color)

"""
# Generate unique colors and save to a text file
colors_file_path = 'unique_colors.txt'
generate_unique_colors(colors_file_path)
print(f"Colors saved to {colors_file_path}")
"""

def read_colors(file_path):
    with open(file_path, 'r') as file:
        colors = file.readlines()
    return [color.strip() for color in colors]

def generate_image_from_colors(colors, width, height):
    if len(colors) != width * height:
        raise ValueError("The number of colors must match the number of pixels in the image.")

    image = Image.new("RGB", (width, height))
    pixels = image.load()

    color_index = 0
    for y in range(height):
        for x in range(width):
            hex_color = colors[color_index]
            r = int(hex_color[1:3], 16)
            g = int(hex_color[3:5], 16)
            b = int(hex_color[5:7], 16)
            pixels[x, y] = (r, g, b)
            color_index += 1

    return image

def save_image(image, file_path):
    image.save(file_path)
    file_size = os.path.getsize(file_path)
    print(f"File saved at {file_path}, size: {file_size} bytes")

# Read colors from the text file
colors = read_colors("/unique_colors.txt")

# Generate a 1024x1024 image from the colors
width, height = 1024, 1024
image = generate_image_from_colors(colors, width, height)

# Save the image to a file
image_file_path = 'UniqueImage.png'
save_image(image, image_file_path)
