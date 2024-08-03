from PIL import Image

def save_pixels_as_jpeg(png_file_path, jpeg_output_path):
    try:
        # Open the PNG image
        png_image = Image.open(png_file_path)

        # Convert to RGB mode (if it's not already in RGB)
        rgb_image = png_image.convert('RGB')

        # Save as JPEG with compression quality (adjust quality as needed, 1 is lowest quality)
        rgb_image.save(jpeg_output_path, 'JPEG', quality=80)

        print(f"Pixels from {png_file_path} saved as JPEG to {jpeg_output_path}.")

    except IOError as e:
        print(f"Error: Cannot open or save {e}.")
    except Exception as e:
        print(f"Error: {e}")

# Example usage:
if __name__ == "__main__":
    png_file_path = 'PNG_IMAGE_PATH.png'  # Replace with your PNG file path
    jpeg_output_path = 'output_image.jpg'  # Replace with desired JPEG output path
    save_pixels_as_jpeg(png_file_path, jpeg_output_path)
