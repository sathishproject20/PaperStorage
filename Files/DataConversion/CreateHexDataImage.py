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

def calculate_canvas_size(hex_data):
    """
    Calculates the width and height of the image canvas based on the total number of characters.

    Parameters:
    hex_data (str): The hex data string.

    Returns:
    (int, int): A tuple containing the width and height of the canvas.
    """
    total_characters = len(hex_data)
    num_pixels = total_characters // 4
    remainder = total_characters % 4

    width = int(num_pixels ** 0.5)
    height = width

    # Adjust width and height based on remainder
    if remainder == 1:
        width += 1
    elif remainder == 2:
        width += 2
    elif remainder == 3:
        width += 3

    return width, height

def draw_image_with_color_dicts(hex_data, hex_color_dict, remainder_color_dict):
    width, height = calculate_canvas_size(hex_data)
    total_characters = len(hex_data)
    num_pixels = total_characters // 4
    remainder = total_characters % 4

    image = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(image)

    for i in range(num_pixels):
        x = i % width
        y = i // width
        hex_value = hex_data[i*4:(i+1)*4]
        color = hex_color_dict.get(hex_value.upper(), (255, 255, 255))  # Default to white if color not found
        draw.point((x, y), fill=color)

    # Fill remainder pixels with remainder color if any
    if remainder > 0:
        remainder_hex = hex_data[num_pixels*4:]
        remainder_color = remainder_color_dict.get(remainder_hex.upper(), (0, 0, 0))  # Default to black if color not found
        for i in range(remainder):
            x = (num_pixels + i) % width
            y = (num_pixels + i) // width
            draw.point((x, y), fill=remainder_color)

    return image


# Example usage:
if __name__ == "__main__":
    # Example usage for generating an image from hex data
    hex_data_path = 'HexData_of_File.txt'  # Replace with your hex data file path
    with open(hex_data_path, 'r') as file:
        hex_data = file.read().strip()

    hex_color_dict = load_dict_from_json('hex_color_dict_stage1.json')  # Replace with your hex color dict file path
    remainder_color_dict = load_dict_from_json('Remainder_HexData_Color_Dict.json') # Replace with your remainder color dict file path

    # Specify custom width and height or set them to None for automatic calculation
    custom_width = None  # Replace with desired width or leave as None for automatic
    custom_height = None  # Replace with desired height or leave as None for automatic

    image = draw_image_with_color_dicts(hex_data, hex_color_dict, remainder_color_dict)
    image.save('Stage1Image.png')
    print("Image generated and saved as 'Stage1Image.png'")
    image.show()
