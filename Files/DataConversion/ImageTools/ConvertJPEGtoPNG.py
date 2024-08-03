from PIL import Image
import os

def convert_jpeg_to_png(jpeg_file_path, png_output_path):
    try:
        # Open the JPEG image
        jpeg_image = Image.open(jpeg_file_path)

        # Convert to RGB mode (if it's not already in RGB)
        rgb_image = jpeg_image.convert('RGB')

        # Save as PNG
        rgb_image.save(png_output_path, 'PNG')

        print(f"Converted {jpeg_file_path} to PNG and saved to {png_output_path}.")

    except IOError as e:
        print(f"Error: Cannot open or save {e}.")
    except Exception as e:
        print(f"Error: {e}")

# Example usage:
if __name__ == "__main__":
    jpeg_file_path = 'PATH_TO_IMAGE.jpg'  # Replace with your JPEG file path
    png_output_path = 'output_image.png'  # Replace with desired PNG output path
    convert_jpeg_to_png(jpeg_file_path, png_output_path)
