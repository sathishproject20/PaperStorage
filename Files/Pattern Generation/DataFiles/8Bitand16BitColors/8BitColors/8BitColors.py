from PIL import Image

def generate_and_save_8bit_colors(output_image_path, rgb_txt_path, hex_txt_path, width=256, height=256):
    # Create an image with 256 colors
    image = Image.new("P", (width, height))  # 'P' mode for palette-based image

    # Generate a palette of 256 colors
    palette = []
    rgb_colors = []
    hex_colors = []
    for i in range(256):
        # Generate a color (e.g., grayscale for simplicity)
        color = (i, i, i)
        palette.extend(color)  # R, G, B values
        hex_color = '#{:02X}{:02X}{:02X}'.format(*color)
        rgb_colors.append(color)
        hex_colors.append(hex_color)

    # Set the palette in the image
    image.putpalette(palette)

    # Fill the image with colors from the palette
    pixels = [i % 256 for i in range(width * height)]
    image.putdata(pixels)

    # Save the image
    image.save(output_image_path)

    # Save the RGB colors to a text file in line-by-line format
    with open(rgb_txt_path, 'w') as rgb_file:
        for rgb in rgb_colors:
            rgb_file.write(f"{rgb}\n")

    # Save the hex colors to a text file in line-by-line format
    with open(hex_txt_path, 'w') as hex_file:
        for hex_color in hex_colors:
            hex_file.write(f"{hex_color}\n")

    image.show()

# Generate and save an 8-bit color palette image and text files for RGB and Hex colors
generate_and_save_8bit_colors("8bit_palette.png", "8bit_rgb_colors.txt", "8bit_hex_colors.txt")
