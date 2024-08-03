import json

def generate_hex_color_dict():
    """
    Generates a dictionary of hexadecimal values from '0000' to 'FFFF' with colors as values.

    Returns:
    dict: A dictionary with hexadecimal values as keys and color values as values.
    """
    hex_values = ['{:04X}'.format(i) for i in range(65536)]
    hex_colors = ['#{:06X}'.format(i) for i in range(65536)]
    
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

if __name__ == "__main__":
    hex_color_dict = generate_hex_color_dict()
    output_file_path = 'hex_color_dict.json'
    save_dict_to_json(hex_color_dict, output_file_path)
    print(f"Hexadecimal color dictionary saved to '{output_file_path}'")
