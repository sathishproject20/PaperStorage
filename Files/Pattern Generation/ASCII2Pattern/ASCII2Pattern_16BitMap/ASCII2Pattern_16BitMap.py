import json
import os
from PIL import Image

def draw_image_from_binary(file_path, bitmap_json_path, remainder_json_path, output_image_path):
    # Load bitmap and remainder JSON dictionaries
    with open(bitmap_json_path, 'r') as bitmap_file:
        bitmap_dict = json.load(bitmap_file)
    with open(remainder_json_path, 'r') as remainder_file:
        remainder_dict = json.load(remainder_file)
    
    # Read the file content as binary data
    with open(file_path, 'rb') as binary_file:
        binary_data = binary_file.read()

    # Convert binary data to ASCII decimal values
    ascii_decimals = [byte for byte in binary_data]
    
    # Initialize variables
    two_sequence_count = 0
    one_sequence_count = 0
    bitmaps = []
    
    # Process ASCII decimals
    i = 0
    while i < len(ascii_decimals):
        if i < len(ascii_decimals) - 1:
            two_sequence = (ascii_decimals[i], ascii_decimals[i + 1])
            if str(two_sequence) in bitmap_dict:
                bitmaps.append(bitmap_dict[str(two_sequence)])
                two_sequence_count += 1
                i += 2
                continue
        one_sequence = str(ascii_decimals[i])
        if one_sequence in remainder_dict:
            bitmaps.append(remainder_dict[one_sequence])
            one_sequence_count += 1
        i += 1

    # Check bitmaps length consistency
    if bitmaps:
        bitmap_length = len(bitmaps[0])
        for b in bitmaps:
            if len(b) != bitmap_length:
                print(f'Inconsistent bitmap length found: {len(b)} vs expected {bitmap_length}')
                return
        bitmap_width = int(bitmap_length ** 0.5)
        if bitmap_width ** 2 != bitmap_length:
            print(f'Bitmap length {bitmap_length} is not a perfect square.')
            return
        bitmap_height = bitmap_width

        # Calculate image dimensions
        total_pixels = len(bitmaps) * bitmap_length
        image_width = int(total_pixels ** 0.5)
        image_height = (total_pixels + image_width - 1) // image_width  # Ensure enough height to fit all pixels
    else:
        image_width = image_height = 0

    # Create a new image with the calculated dimensions
    image = Image.new('1', (image_width, image_height))
    pixels = image.load()

    # Fill the image with the bitmaps
    x, y = 0, 0
    for bitmap in bitmaps:
        for i in range(bitmap_height):
            for j in range(bitmap_width):
                if x + j < image_width and y + i < image_height:
                    if bitmap[i * bitmap_width + j] == '1':
                        pixels[x + j, y + i] = 1
                    else:
                        pixels[x + j, y + i] = 0
        x += bitmap_width
        if x >= image_width:
            x = 0
            y += bitmap_height

    # Save the image
    image.save(output_image_path)
    
    # Print counts
    print(f'Two-sequence ASCII decimal count: {two_sequence_count}')
    print(f'One-sequence ASCII decimal count: {one_sequence_count}')
    print(f'Image saved to: {output_image_path}')
    print(f'Image dimensions: {image_width}x{image_height}')

# Example usage
binary_file_path = 'File.txt'
bitmap_json_path = 'ASCII2Pattern_16BitMap.json'
remainder_json_path = 'ASCII1Pattern_8BitMap.json'
output_image_path = 'ASCII2Pattern_16BitImage_File.png'

draw_image_from_binary(binary_file_path, bitmap_json_path, remainder_json_path, output_image_path)
