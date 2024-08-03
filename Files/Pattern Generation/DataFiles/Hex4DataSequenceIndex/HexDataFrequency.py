import json
import os
from collections import defaultdict

class CompactJSONEncoder(json.JSONEncoder):
    def __init__(self, *args, **kwargs):
        super(CompactJSONEncoder, self).__init__(*args, **kwargs)

    def iterencode(self, o, _one_shot=False):
        if isinstance(o, list):
            return '[' + ', '.join(json.dumps(i) for i in o) + ']'
        return super(CompactJSONEncoder, self).iterencode(o, _one_shot)

def read_file_and_process_hex(input_file):
    # Read the file in binary mode
    with open(input_file, 'rb') as f:
        binary_data = f.read()

    # Convert the binary data to a hex string
    hex_data = binary_data.hex().upper()

    # Create the output text file name
    base_name = os.path.basename(input_file)
    output_text_file = f'HexData_{base_name}.txt'

    # Write the hex data to the text file
    with open(output_text_file, 'w') as f:
        f.write(hex_data)

    # Create the JSON structure
    hex_dict = defaultdict(lambda: {"PositionIndex": [], "Occurrences": 0})

    for i in range(0, len(hex_data), 4):
        hex_key = hex_data[i:i+4]
        if len(hex_key) == 4:
            position = (i // 4) + 1  # 1-based index
            hex_dict[hex_key]["PositionIndex"].append(position)
            hex_dict[hex_key]["Occurrences"] += 1

    json_data = {
        "HexData": hex_dict
    }

    # Create the output JSON file name
    output_json_file = f'HexData_{base_name}.json'

    # Write the JSON data to the file with custom formatting
    with open(output_json_file, 'w') as f:
        json.dump(json_data, f, cls=CompactJSONEncoder, indent=4, separators=(',', ': '), ensure_ascii=False)

    print(f"Hex data saved to {output_text_file}")
    print(f"JSON data saved to {output_json_file}")

# Example usage
input_file = 'Path_to_File'  # Replace with the path to your file
read_file_and_process_hex(input_file)
