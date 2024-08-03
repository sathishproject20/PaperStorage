from PIL import Image

def image_to_binary_text(image_path, output_text_path):
    # Open the image
    image = Image.open(image_path).convert('1')  # Convert image to 1-bit pixels (black and white)
    
    # Get image dimensions
    width, height = image.size
    
    # Create a list to store the binary values
    binary_values = []

    # Iterate over every pixel in the image
    for y in range(height):
        for x in range(width):
            pixel = image.getpixel((x, y))
            binary_value = 0 if pixel == 255 else 1  # Assign 0 for white, 1 for black
            binary_values.append(binary_value)
    
    # Save the binary values to a text file
    with open(output_text_path, 'w') as output_file:
        for value in binary_values:
            output_file.write(f"{value}")
    
    print(f"Binary values saved to {output_text_path}")

# Example usage
image_to_binary_text('ASCIIPatternImage.png', 'ImageData_File.txt')
