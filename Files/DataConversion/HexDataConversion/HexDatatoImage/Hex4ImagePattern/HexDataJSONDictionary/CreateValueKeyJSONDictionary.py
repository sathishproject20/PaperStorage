import json

def swap_json_key_value(input_file, output_file):
    with open(input_file, 'r') as infile:
        data = json.load(infile)
    
    swapped_data = {value: key for key, value in data.items()}
    
    with open(output_file, 'w') as outfile:
        json.dump(swapped_data, outfile, indent=4)
    
    print(f"Swapped JSON document saved to {output_file}")

# Example usage:
input_file = 'hex_4_dict_encode.json'
output_file = 'hex_4_dict_decode.json'
swap_json_key_value(input_file, output_file)
