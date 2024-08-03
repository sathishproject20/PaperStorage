from PIL import Image
import json

def read_image_and_map_colors(image_path, json_output_path):
    try:
        # Open the image
        img = Image.open(image_path)

        # Ensure the image is in RGB mode
        img = img.convert('RGB')

        width, height = img.size

        # Initialize dictionary to store pixel colors
        pixel_colors = {}

        # Iterate through each pixel
        for y in range(height):
            for x in range(width):
                pixel = img.getpixel((x, y))
                # Convert pixel tuple (R, G, B) to a hex color string (e.g., '#RRGGBB')
                hex_color = f'#{pixel[0]:02x}{pixel[1]:02x}{pixel[2]:02x}'
                # Map pixel position to hex color in dictionary
                pixel_colors[y * width + x + 1] = hex_color

        # Save pixel_colors dictionary to JSON file
        with open(json_output_path, 'w') as json_file:
            json.dump(pixel_colors, json_file, indent=4)

        print(f"Pixel colors mapped and saved to {json_output_path}.")

    except IOError as e:
        print(f"Error: Cannot open or save {e}.")
    except Exception as e:
        print(f"Error: {e}")

# Example usage:
if __name__ == "__main__":
    image_path = 'IMAGE_PATH'  # Replace with your image file path
    json_output_path = 'pixel_colors.json'  # Replace with desired JSON output path
    read_image_and_map_colors(image_path, json_output_path)
