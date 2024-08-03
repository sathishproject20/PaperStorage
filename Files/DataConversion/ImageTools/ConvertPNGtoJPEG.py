from PIL import Image
import os

def convert_png_to_jpeg(png_file_path, jpeg_output_path, quality=10):
    try:
        # Open the PNG image
        png_image = Image.open(png_file_path)

        # Convert to RGB mode (if it's not already in RGB)
        rgb_image = png_image.convert('RGB')

        # Save as JPEG with compression quality
        rgb_image.save(jpeg_output_path, 'JPEG', quality=quality)

        print(f"Converted {png_file_path} to JPEG and saved to {jpeg_output_path}.")

    except IOError as e:
        print(f"Error: Cannot open or save {e}.")
    except Exception as e:
        print(f"Error: {e}")

# Example usage:
if __name__ == "__main__":
    png_file_path = 'PNG_FILE_PATH.png'  # Replace with your PNG file path
    jpeg_output_path = 'output_image.jpg'  # Replace with desired JPEG output path
    convert_png_to_jpeg(png_file_path, jpeg_output_path)
