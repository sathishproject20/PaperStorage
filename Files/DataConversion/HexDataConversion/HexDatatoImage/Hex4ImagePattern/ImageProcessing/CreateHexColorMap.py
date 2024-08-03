import json
from PIL import Image, ImageDraw, ImageColor

def load_dict_from_json(file_path):
    """
    Loads a dictionary from a JSON file.

    Parameters:
    file_path (str): The path of the JSON file to load.

    Returns:
    dict: The loaded dictionary.
    """
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def save_dict_to_json(data, file_path):
    """
    Saves a dictionary to a JSON file.

    Parameters:
    data (dict): The dictionary to save.
    file_path (str): The path of the JSON file to save.
    """
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def calculate_canvas_size(total_characters):
    """
    Calculates the width and height of the image canvas based on the total number of characters.

    Parameters:
    total_characters (int): The total number of characters.

    Returns:
    (int, int): A tuple containing the width and height of the canvas.
    """
    num_pixels = total_characters // 4
    remainder = total_characters % 4

    width = int(num_pixels ** 0.5)
    height = width

    # Adjust width and height based on remainder
    if remainder == 3:
        width += 3
        height += 1
    elif remainder == 2:
        width += 2
        height += 1
    elif remainder == 1:
        width += 1
        height += 1

    return width, height

def generate_image_from_hex_data(hex_data, hex_color_dict, width=None, height=None):
    """
    Generates an image from hexadecimal data using a given color dictionary.

    Parameters:
    hex_data (str): The sequence of hexadecimal characters.
    hex_color_dict (dict): The dictionary mapping hex values to colors.
    width (int, optional): The width of the image.
    height (int, optional): The height of the image.

    Returns:
    Image: The generated image.
    """
    total_characters = len(hex_data)

    if width is None or height is None:
        width, height = calculate_canvas_size(total_characters)
    else:
        if width * height < total_characters // 4:
            raise ValueError("Provided dimensions are too small for the given hex data.")

    image = Image.new('RGB', (width, height))
    pixels = image.load()

    # Dictionary to store hex values and their corresponding colors
    hex_to_color_dict = {}

    for i in range(0, total_characters, 4):
        hex_value = hex_data[i:i+4]
        if len(hex_value) == 4:
            color = hex_color_dict.get(hex_value, "#000000")  # Default to black if not found
            color_tuple = ImageColor.getrgb(color)
            x = (i // 4) % width
            y = (i // 4) // width
            pixels[x, y] = color_tuple

            # Store the hex value and its color in the dictionary
            hex_to_color_dict[hex_value.upper()] = color

    return image, hex_to_color_dict

if __name__ == "__main__":
    # Example usage for generating an image from hex data
    hex_data_file = '/PATH_TO_FILE/HexData.txt'  # Replace with your hex data file path
    with open(hex_data_file, 'r') as file:
        hex_data = file.read().strip()

    hex_color_dict = load_dict_from_json('/PATH_TO_CREATE_IMAGE_DICTIONARY/hex_color_dict_stage.json')  # Replace with your hex color dict file path

    # Specify custom width and height or set them to None for automatic calculation
    custom_width = None  # Replace with desired width or leave as None for automatic
    custom_height = None  # Replace with desired height or leave as None for automatic

    image, hex_to_color_dict = generate_image_from_hex_data(hex_data, hex_color_dict, custom_width, custom_height)
    image.save('generated_image.png')
    print("Image generated and saved as 'generated_image.png'")

    # Save the hex to color dictionary to a JSON file
    output_json_file = '/PATH_TO_SAVE_FILE/ColorMap_Of_GeneratedImage.json'  # Replace with your output json file path
    save_dict_to_json(hex_to_color_dict, output_json_file)
    print(f"Hex to color dictionary saved as '{output_json_file}'")
