def read_and_convert_hexdata(input_file_path, output_file_path):
    try:
        with open(input_file_path, 'r') as file:
            hex_data = file.read().strip()
        
        # Split the hex data into chunks of 6 characters
        hex_array = [hex_data[i:i+6] for i in range(0, len(hex_data), 6)]

        with open(output_file_path, 'w') as file:
            for hex_value in hex_array:
                file.write(f"{hex_value}\n")
        
        print(f"Successfully converted and saved hex data to {output_file_path}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage:
input_file = 'HexData.txt'
output_file = 'Hex6Data.txt'
read_and_convert_hexdata(input_file, output_file)
