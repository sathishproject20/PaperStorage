import os

def split_hex_file(input_file_path, output_dir, chunk_size=1048576):
    """
    Splits a large hex file into multiple files, each with exactly 1,048,576 hexadecimal characters.

    Parameters:
    input_file_path (str): The path to the input hex file.
    output_dir (str): The directory where the output files will be saved.
    chunk_size (int): The size of each chunk in terms of characters. Default is 1,048,576 characters.

    Terminal Command:
    python split_hex_file.py /PATH_TO_FILE/HexFile.txt /PATH_TO_OUTPUTFOLDER

    """
    try:
        with open(input_file_path, 'r', encoding='latin-1') as file:
            hex_data = file.read().strip()

        # Ensure the output directory exists
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        total_size = len(hex_data)  # Total number of characters

        # Calculate the number of chunks
        num_chunks = (total_size + chunk_size - 1) // chunk_size

        for i in range(num_chunks):
            start = i * chunk_size
            end = min(start + chunk_size, len(hex_data))
            chunk_data = hex_data[start:end]

            output_file_path = os.path.join(output_dir, f'chunk_{i + 1}.txt')
            with open(output_file_path, 'w') as output_file:
                output_file.write(chunk_data)
        
        print(f"Hex file split into {num_chunks} chunks of exactly 1,048,576 characters each.")

    except FileNotFoundError:
        print(f"Error: File not found at {input_file_path}")
    except Exception as e:
        print(f"Error: {e}")

# Example usage:
if __name__ == "__main__":
    input_file_path = '/PATH_TO_FILE_/HexValue.txt'  # Replace with your file path
    output_dir = 'Output_Folder'  # Replace with your output directory path
    split_hex_file(input_file_path, output_dir)
