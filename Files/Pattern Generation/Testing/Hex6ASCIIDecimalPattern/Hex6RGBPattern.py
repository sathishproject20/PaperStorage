from PIL import Image

def read_rgb_values_from_file(file_path):
    rgb_values = []
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                # Remove parentheses and split by comma
                rgb_tuple_str = line.strip('()')
                rgb_tuple = tuple(map(int, rgb_tuple_str.split(',')))
                if len(rgb_tuple) == 3:
                    rgb_values.append(rgb_tuple)
    return rgb_values

def draw_image_from_rgb(rgb_values, output_image_path):
    # Calculate image dimensions based on the number of pixels
    num_pixels = len(rgb_values)
    width = int(num_pixels ** 0.5)  # Square root for a roughly square image
    height = (num_pixels + width - 1) // width  # Round up for height
    
    # Create a new image with RGB mode
    image = Image.new('RGB', (width, height))
    
    # Load pixel data into the image
    pixels = image.load()
    for i in range(num_pixels):
        x = i % width
        y = i // width
        pixels[x, y] = rgb_values[i]
    
    # Save the image with PNG optimization
    image.save(output_image_path, optimize=True)
    print(f"Image saved as {output_image_path}")

# Example usage:
input_file_path = 'Hex6RGBColor.txt'
output_image_path = 'Hex6Pattern.png'

# Read RGB values from file
rgb_values = read_rgb_values_from_file(input_file_path)

# Draw image using RGB values and save it
draw_image_from_rgb(rgb_values, output_image_path)
