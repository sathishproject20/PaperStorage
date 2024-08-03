from PIL import Image

def count_different_colors(image_path):
    try:
        # Open the image
        img = Image.open(image_path)

        # Ensure the image is in RGB mode
        img = img.convert('RGB')

        width, height = img.size

        # Initialize set to store unique pixel colors
        unique_colors = set()

        # Iterate through each pixel
        for y in range(height):
            for x in range(width):
                pixel = img.getpixel((x, y))
                # Convert pixel tuple (R, G, B) to a hex color string (e.g., '#RRGGBB')
                hex_color = f'#{pixel[0]:02x}{pixel[1]:02x}{pixel[2]:02x}'
                # Add hex_color to set of unique colors
                unique_colors.add(hex_color)

        num_unique_colors = len(unique_colors)
        print(f"Number of different colors in the image: {num_unique_colors}")

        return num_unique_colors

    except IOError as e:
        print(f"Error: Cannot open {e}.")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

# Example usage:
if __name__ == "__main__":
    image_path = 'PATH_TO_IMAGE'  # Replace with your image file path
    num_colors = count_different_colors(image_path)
    if num_colors is not None:
        print(f"Number of different colors: {num_colors}")
