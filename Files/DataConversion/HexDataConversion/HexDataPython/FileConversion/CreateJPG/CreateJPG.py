from PIL import Image, ImageDraw

# Define a dictionary to map hexadecimal characters to colors
hex_color_map = {
    '0': (0, 0, 0),     # Black
    '1': (255, 0, 0),   # Red
    '2': (0, 255, 0),   # Green
    '3': (0, 0, 255),   # Blue
    '4': (255, 255, 0), # Yellow
    '5': (255, 0, 255), # Magenta
    '6': (0, 255, 255), # Cyan
    '7': (192, 192, 192), # Light Gray
    '8': (128, 128, 128), # Dark Gray
    '9': (128, 0, 0),   # Brown
    'A': (255, 165, 0), # Orange
    'B': (0, 128, 0),   # Dark Green
    'C': (0, 128, 128), # Teal
    'D': (0, 0, 128),   # Navy
    'E': (128, 0, 128), # Purple
    'F': (255, 192, 203), # Pink
}

def generate_hex_image_from_file(file_path, width=1024, height=1024, pixel_size=1):
    # Read sequence of hexadecimal characters from file
    with open(file_path, 'r') as file:
        sequence = file.read().strip()

    # Create a new image with white background
    image = Image.new('RGB', (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)

    # Calculate number of pixels to draw
    total_pixels = width * height
    if len(sequence) != total_pixels:
        raise ValueError(f"Sequence length ({len(sequence)}) does not match image size ({total_pixels})")

    # Draw pixels based on the sequence of hexadecimal characters
    for i, hex_char in enumerate(sequence):
        x = i % width
        y = i // width
        color = hex_color_map.get(hex_char.upper(), (255, 255, 255))
        draw.rectangle([x, y, x + pixel_size, y + pixel_size], fill=color)

    return image

# Example usage:
if __name__ == "__main__":
    file_path = "hexdata1.txt"  # Replace with your file path of 1MB Hex File
    img = generate_hex_image_from_file(file_path)

    # Save the image to a file
    img.save("hex_image_from_file.jpg", "JPEG")
    print("Image generated and saved as 'hex_image_from_file.jpg'")
