import json
import os

def process_json_to_text(input_json_file):
    # Read the JSON file
    with open(input_json_file, 'r') as f:
        json_data = json.load(f)

    hex_data = json_data.get('HexData', {})
    text_sequence = []

    # Process each hex key in the data
    for hex_key, details in hex_data.items():
        position_indices = details.get("PositionIndex", [])
        
        if position_indices:
            # Construct the sequence for the current hex key
            positions = ''.join([f'@{pos}' for pos in position_indices])
            sequence = f'{hex_key}{positions}'
            text_sequence.append(sequence)
    
    # Join the sequences with delimiter '/'
    final_text = '/'.join(text_sequence)

    # Create the output text file name
    base_name = os.path.basename(input_json_file)
    output_text_file = f'Processed_{base_name}.txt'

    # Write the final text to the output file
    with open(output_text_file, 'w') as f:
        f.write(final_text)

    print(f"Processed text saved to {output_text_file}")

# Example usage
input_json_file = 'HexData_HexDataFrequency.py.json'  # Replace with the path to your JSON file
process_json_to_text(input_json_file)
