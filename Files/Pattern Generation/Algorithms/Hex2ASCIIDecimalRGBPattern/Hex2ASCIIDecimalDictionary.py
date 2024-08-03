import os
import json
from PIL import Image, ImageDraw

"""
To Test the Algorithm to fetch ASCII Decimal Values for 2 Length Hex Keys from JSON Files.
Run the following command for your python version in Terminal, python Hex2AsciiDictionary.py

"""

class Hex2AsciiDictionary:

    def load_hex_ascii_dictionary(self, base_folder):
        self.base_folder = base_folder
        self.hex2AsciiEncodeDict = {}
        self.hex2AsciiDecodeDict = {}

        hex2AsciiEncode_path = os.path.join(self.base_folder, 'Hex_ASCIIDecimal_Encode_Dict.json')
        hex2AsciiDecode_path = os.path.join(self.base_folder, 'Hex_ASCIIDecimal_Decode_Dict.json')

        if os.path.exists(hex2AsciiEncode_path):
            with open(hex2AsciiEncode_path, 'r') as file:
                self.hex2AsciiEncodeDict = json.load(file)
        else:
            print(f'File not found: {hex2AsciiEncode_path}')

        if os.path.exists(hex2AsciiDecode_path):
            with open(hex2AsciiDecode_path, 'r') as file:
                self.hex2AsciiDecodeDict = json.load(file)
        else:
            print(f'File not found: {hex2AsciiDecode_path}')


    def get_hex2AsciiEncode(self, hex_key):
        value = self.hex2AsciiEncodeDict.get(hex_key)
        if value is None:
            print(f"Error: ASCII Decimal Value for the given Hex Key '{hex_key}' not found.")
        return value

    def get_hex2AsciiDecode(self, ascii_key):
        value = self.hex2AsciiDecodeDict.get(ascii_key)
        if value is None:
            print(f"Error: Hex Value for the given ASCII Key '{ascii_key}' not found.")
        return value


if __name__ == "__main__":
    hex2_ascii_dict = Hex2AsciiDictionary()

    base_folder = "Data"
    hex2_ascii_dict.load_hex_ascii_dictionary(base_folder)

    hex_key = '0A'
    asciidecimal_value = hex2_ascii_dict.get_hex2AsciiEncode(hex_key)
    print(f"ASCII Decimal Value for the given Hex Value {hex_key}: {asciidecimal_value}")

    ascii_key = "64"
    hex_value = hex2_ascii_dict.get_hex2AsciiDecode(ascii_key)
    print(f"Hex Value for the given Ascii Key {ascii_key}: {hex_value}")
