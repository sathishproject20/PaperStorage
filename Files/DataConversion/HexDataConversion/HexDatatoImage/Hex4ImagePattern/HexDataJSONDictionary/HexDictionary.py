import json
import os

def generate_hex_color_dict():
    """
    Generates a dictionary of hexadecimal values from '0000' to 'FFFF' with colors as values.

    Returns:
    dict: A dictionary with hexadecimal values as keys and color values as values.
    """
    start = 458752
    end = 524288

    hex_values = ['{:04X}'.format(i) for i in range(65536)]
    hex_colors = ['#{:06X}'.format(i) for i in range(start, end)]

    hex_color_dict = dict(zip(hex_values, hex_colors))
    return hex_color_dict

def save_dict_to_json(data, file_path):
    """
    Saves the dictionary to a JSON file.

    Parameters:
    data (dict): The dictionary to save.
    file_path (str): The path of the JSON file where the dictionary will be saved.
    """
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

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

if __name__ == "__main__":
    # Example usage for generating the hex color dictionary
    hex_color_dict = generate_hex_color_dict()
    save_dict_to_json(hex_color_dict, 'hex_json_dict_stage8.json')
