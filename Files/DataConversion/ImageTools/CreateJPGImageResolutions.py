from PIL import Image
import os

def convert_image_to_resolutions(input_file_path, output_dir, resolutions):
    """
    Converts a JPG image to multiple resolutions.

    Parameters:
    input_file_path (str): The path to the input JPG image.
    output_dir (str): The directory where the output images will be saved.
    resolutions (list of tuples): List of desired resolutions (width, height).
    """
    try:
        with Image.open(input_file_path) as img:
            # Ensure the output directory exists
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            original_resolution = img.size  # Get original image resolution

            # Resize to each resolution in the list
            for resolution in resolutions:
                width, height = resolution
                resized_img = img.resize((width, height))

                output_file_path = os.path.join(output_dir, f'{width}x{height}.jpg')
                resized_img.save(output_file_path, 'JPEG')

                print(f"Image saved at resolution {width}x{height} as '{output_file_path}'.")

            # Resize back to original resolution (1024x1024)
            resized_back_img = img.resize(original_resolution)
            output_file_path = os.path.join(output_dir, 'original_resolution.jpg')
            resized_back_img.save(output_file_path, 'JPEG')
            print(f"Image resized back to original resolution {original_resolution} as '{output_file_path}'.")

    except FileNotFoundError:
        print(f"Error: File not found at {input_file_path}")
    except Exception as e:
        print(f"Error: {e}")

# Example usage:
if __name__ == "__main__":
    input_file_path = 'IMAGE_PATH_1024x1024.jpg'  # Replace with your file path
    output_dir = '/PATH_TO_FOLDER'  # Replace with your output directory path
    resolutions = [(512, 512)]  # Replace with desired resolutions

    convert_image_to_resolutions(input_file_path, output_dir, resolutions)
