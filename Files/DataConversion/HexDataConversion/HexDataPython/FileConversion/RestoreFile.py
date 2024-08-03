def read_hex_values(file_path):
    """
    Reads hexadecimal values from a file at the specified file path.

    Parameters:
    file_path (str): The path to the file.

    Returns:
    str: A string of hexadecimal values representing the file's contents.
    """
    hex_values = []
    try:
        with open(file_path, 'rb') as file:
            while (byte := file.read(1)):
                hex_values.append(byte.hex())
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
    except Exception as e:
        print(f"Error: {e}")
    
    return ' '.join(hex_values)

def hex_to_file(hex_data, output_file_path):
    """
    Converts a string of hexadecimal values back to a binary file.

    Parameters:
    hex_data (str): A string of hexadecimal values.
    output_file_path (str): The path to the output file.
    """
    try:
        with open(output_file_path, 'wb') as file:
            hex_bytes = bytes.fromhex(hex_data.replace(' ', ''))
            file.write(hex_bytes)
    except Exception as e:
        print(f"Error: {e}")

# Example usage:
input_file_path = 'FOLDER/PATH_TO/HEXVALUE.txt' # Hex Value of Any File
hex_data = read_hex_values(input_file_path)
print(hex_data)

output_file_path = 'FOLDER/PATH_TO/VIDEO.mp4' # Path to save the file with FileName and FileType
hex_to_file(hex_data, output_file_path)
