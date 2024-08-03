import os
import json
from collections import defaultdict

class CompactJSONEncoder(json.JSONEncoder):
    def encode(self, o):
        if isinstance(o, dict):
            pieces = []
            for k, v in o.items():
                pieces.append(f'"{k}":{self.encode(v)}')
            return '{' + ','.join(pieces) + '}'
        elif isinstance(o, list):
            return '[' + ','.join(map(self.encode, o)) + ']'
        else:
            return json.JSONEncoder.encode(self, o)

def read_file_and_process_ascii(input_file):
    # Read the file in binary mode
    with open(input_file, 'rb') as f:
        binary_data = f.read()

    # Convert the binary data to ASCII decimal values
    ascii_decimal_values = [str(b) for b in binary_data]

    # Create the output text file name
    base_name = os.path.basename(input_file)
    output_text_file = f'ASCIIData_{base_name}.txt'

    # Write the ASCII decimal values to the text file
    ascii_data = '/'.join(ascii_decimal_values)
    with open(output_text_file, 'w') as f:
        f.write(ascii_data)

    # Create the JSON structure
    ascii_dict = defaultdict(lambda: {"PositionIndex": [], "Occurrences": 0})

    # Process every two ASCII decimal values
    for i in range(0, len(ascii_decimal_values) - 1, 2):
        key = f"{ascii_decimal_values[i]},{ascii_decimal_values[i + 1]}"
        position = (i // 2) + 1  # 1-based index
        ascii_dict[key]["PositionIndex"].append(position)
        ascii_dict[key]["Occurrences"] += 1

    json_data = {
        "ASCIIData": ascii_dict
    }

    # Create the output JSON file name
    output_json_file = f'ASCIIData_{base_name}.json'

    # Write the JSON data to the file with custom formatting
    with open(output_json_file, 'w') as f:
        json.dump(json_data, f, cls=CompactJSONEncoder, indent=4, separators=(',', ': '), ensure_ascii=False)

    # Create the ascii sequence text output
    asciisequence_data = ''
    for key, value in ascii_dict.items():
        asciisequence_data += f"({key})@" + "@".join(map(str, value["PositionIndex"])) + '/'

    # Remove the trailing slash
    asciisequence_text = asciisequence_data.rstrip('/')

    # Write the ascii sequence text to a file
    asciisequence_text_file = f'ASCIISequenceData_{base_name}.txt'
    with open(asciisequence_text_file, 'w') as ascii_file:
        ascii_file.write(asciisequence_text)

    print(f"ASCII data saved to {output_text_file}")
    print(f"JSON data saved to {output_json_file}")
    print(f"ASCII Sequence text data saved to {asciisequence_text_file}")

# Example usage
input_file = 'File.txt'  # Replace with your input file path
read_file_and_process_ascii(input_file)
