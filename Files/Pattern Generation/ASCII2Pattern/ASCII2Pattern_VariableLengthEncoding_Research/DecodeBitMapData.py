def decode_bitmap_to_decimal(input_file_path, output_file_path, pattern_dict):
    # Read the binary data from the input file
    with open(input_file_path, 'r') as file:
        data = file.read().strip()

    # Create a reverse pattern dictionary for decoding
    reverse_pattern_dict = {v: k for k, v in pattern_dict.items()}

    decoded_values = []
    buffer = ""
    
    # Decode the data using the reverse pattern dictionary
    for bit in data:
        buffer += bit
        if buffer in reverse_pattern_dict:
            decoded_value = reverse_pattern_dict[buffer]
            decoded_values.append(decoded_value)
            buffer = ""
    
    # Ensure the entire data was decoded
    if buffer:
        raise ValueError("Decoding failed. The remaining buffer does not match any pattern.")
    
    # Map the decoded values to the sequence 1 to 65536
    sequence_mapping = {str(i): str(i) for i in range(1, 65537)}
    
    # Convert the mapped keys back to their decimal values
    result = []
    for value in decoded_values:
        if value in sequence_mapping:
            result.append(sequence_mapping[value])
        else:
            raise ValueError(f"Value '{value}' not found in the sequence mapping.")
    
    # Save the result to the output file
    with open(output_file_path, 'w') as file:
        file.write(' '.join(result))

# Example usage
input_file_path = 'ImageBitMapPattern.txt'
output_file_path = 'DecodetoDecimalData.txt'
bitmap_pattern = {
    "0": "0",
    "1": "000",
    "2": "0010",
    "3": "00010",
    "4": "00",
    "5": "01000",
    "6": "010",
    "7": "0100",
    "8": "0000",
    "9": "00100",
    "A": "11",  # Delimiter pattern for values in dictionary
}

decode_bitmap_to_decimal(input_file_path, output_file_path, bitmap_pattern)
