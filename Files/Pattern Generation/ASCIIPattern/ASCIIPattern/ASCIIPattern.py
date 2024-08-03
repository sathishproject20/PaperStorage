import json
from PIL import Image

def read_document(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def text_to_decimal(text):
    return [ord(char) for char in text]

def load_json_dict(json_file_path):
    with open(json_file_path, 'r') as file:
        return json.load(file)

def draw_image_from_dict(text_file_path, json_dict_path, output_image_path):
    # Read the document and convert to decimal values
    text = read_document(text_file_path)
    print(f"Text content: {text}")
    decimal_values = text_to_decimal(text)
    print(f"Decimal values: {decimal_values}")
    
    # Load the JSON dictionary
    mapping_dict = load_json_dict(json_dict_path)
    print(f"Loaded mapping dictionary with {len(mapping_dict)} entries.")
    
    # Generate pairs of decimal values
    decimal_pairs = [(decimal_values[i], decimal_values[i+1]) for i in range(0, len(decimal_values)-1, 2)]
    print(f"Decimal pairs: {decimal_pairs}")
    
    # Initialize image size
    img_width = 1024
    img_height = 1024
    img = Image.new('1', (img_width, img_height), "white")  # '1' for 1-bit pixels (black and white)
    pixels = img.load()

    # Draw the image based on the mapping dictionary
    x, y = 0, 0
    for pair in decimal_pairs:
        key = f"{pair[0]:03}{pair[1]:03}"
        if key in mapping_dict:
            value = mapping_dict[key]
            print(f"Processing key: {key} with value: {value}")
            for bit in value:
                if x < img_width and y < img_height:
                    pixels[x, y] = 0 if bit == '1' else 1
                    x += 1
                    if x >= img_width:
                        x = 0
                        y += 1
                if y >= img_height:
                    break
        else:
            print(f"Key {key} not found in dictionary.")
        if y >= img_height:
            break
    
    # Save the image
    img.save(output_image_path)
    print(f"Image saved to {output_image_path}")

# Example usage
text_file_path = 'ASCIICharacters.txt'
json_dict_path = 'ASCII2CharacterSequence.json'
output_image_path = 'ASCIICharacters.bmp'

draw_image_from_dict(text_file_path, json_dict_path, output_image_path)
