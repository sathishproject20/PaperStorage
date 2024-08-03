import sys

"""

python ValidateHexData.py /PATH_TO_FOLDER/INPUTHEX.txt


"""

def verify_hex_file(file_path):
    valid_hex_chars = set("0123456789ABCDEFabcdef")
    total_chars = 0
    single_length_hex_values = 0
    two_length_hex_values = 0

    with open(file_path, 'r') as file:
        sequence = file.read().strip()
        total_chars = len(sequence)

        # Verify each character
        for char in sequence:
            if char not in valid_hex_chars:
                print(f"Invalid character found: {char}")
                return
        
        # Count single-length hex values (each individual character)
        single_length_hex_values = total_chars

        # Count two-length hex values (pairs of characters)
        two_length_hex_values = total_chars // 2

    print(f"Total number of characters: {total_chars}")
    print(f"Number of single-length hex values: {single_length_hex_values}")
    print(f"Number of two-length hex values: {two_length_hex_values}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python verify_hex_file.py <path_to_file>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    verify_hex_file(file_path)
