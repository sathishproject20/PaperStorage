from PIL import Image

def count_pixels(image):
    width, height = image.size
    return width * height

# Example usage:
image_path = '/your_image.png'  # Replace with your image file path
image = Image.open(image_path)

# Count pixels
num_pixels = count_pixels(image)

print(f"The image '{image_path}' has {num_pixels} pixels.")
