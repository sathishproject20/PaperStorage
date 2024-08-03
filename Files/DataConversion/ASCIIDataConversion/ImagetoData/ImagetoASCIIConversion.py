import json
from PIL import Image

class AppData:
    imageASCIIColorIndex = {}

    @classmethod
    def read_json_data(cls, json_file):
        try:
            with open(json_file, 'r') as file:
                data = json.load(file)

            cls.asciiColorIndex = data['imageASCIIColorIndex']
        except FileNotFoundError:
            print(f"File '{json_file}' not found.")
        except KeyError as e:
            print(f"Key error: {str(e)}")
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {str(e)}")
        except Exception as e:
            print(f"Error reading JSON data: {str(e)}")

# Initialize AppData with JSON data
AppData.read_json_data('imageASCIIColorIndex.json')

def decode_image_to_ascii(image_path, imageASCIIColorIndex):
    try:
        image = Image.open(image_path)
        width, height = image.size
        pixels = image.load()

        ascii_string = ""
        for y in range(height):
            for x in range(width):
                color = pixels[x, y]
                # Convert the RGB color to a hexadecimal string
                color_hex = '#{:02x}{:02x}{:02x}'.format(*color).upper()
                # Find the corresponding ASCII character
                for char, color_code in imageASCIIColorIndex.items():
                    if color_code.upper() == color_hex:
                        ascii_string += chr(int(char))
                        break

        return ascii_string
    except Exception as e:
        print(f"Error decoding image: {str(e)}")
        return None

def save_ascii_to_text_file(ascii_string, file_path):
    try:
        with open(file_path, 'w') as file:
            file.write(ascii_string)
        print(f"ASCII string saved to '{file_path}'")
    except Exception as e:
        print(f"Error saving ASCII string to file: {str(e)}")

# Example usage
decoded_ascii = decode_image_to_ascii("1MBASCIIPatternData.png", AppData.imageASCIIColorIndex)
if decoded_ascii:
    print("Decoded ASCII String:")
    print(decoded_ascii)
    save_ascii_to_text_file(decoded_ascii, "decoded_ascii.txt")
