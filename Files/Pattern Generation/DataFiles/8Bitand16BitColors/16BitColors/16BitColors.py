import json
from PIL import Image

def generate_and_save_16bit_colors(output_image_path, json_rgb_path, json_hex_path, width=256, height=256):
    # Create an image with RGB mode
    image = Image.new("RGB", (width, height))

    # Generate 16-bit colors
    pixels = []
    rgb_colors = []
    hex_colors = []
    index = 0
    for r in range(32):  # 5 bits for red (32 levels)
        for g in range(64):  # 6 bits for green (64 levels)
            for b in range(32):  # 5 bits for blue (32 levels)
                red = (r << 3) | (r >> 2)  # 5-bit to 8-bit conversion
                green = (g << 2) | (g >> 4)  # 6-bit to 8-bit conversion
                blue = (b << 3) | (b >> 2)  # 5-bit to 8-bit conversion
                color = (red, green, blue)
                hex_color = '#{:02X}{:02X}{:02X}'.format(*color)
                pixels.append(color)
                rgb_colors.append(color)
                hex_colors.append(hex_color)
                index += 1

    # Fill the image with the 16-bit colors
    image.putdata(pixels[:width * height])  # Use only as many pixels as needed

    # Save the image
    image.save(output_image_path)

    # Save the RGB colors to a file in single line tuple format
    with open(json_rgb_path, 'w') as rgb_file:
        for rgb in rgb_colors:
            rgb_file.write(f"{rgb}\n")

    # Save the hex colors to a file in line-by-line format
    with open(json_hex_path, 'w') as hex_file:
        for hex_color in hex_colors:
            hex_file.write(f"{hex_color}\n")

    image.show()

# Generate and save a 16-bit color palette image and two separate files for RGB and Hex colors
generate_and_save_16bit_colors("16bit_palette.png", "16bit_rgb_colors.txt", "16bit_hex_colors.txt")
