import json
from fontTools.ttLib import TTFont

def generate_utf8_code_points():
    valid_code_points = []
    
    # Add BMP code points, skipping the surrogate pair range
    for codepoint in range(0x0000, 0xD800):
        valid_code_points.append(codepoint)
    for codepoint in range(0xE000, 0xFFFF + 1):
        valid_code_points.append(codepoint)
    
    # Add emoji ranges
    emoji_ranges = [
        (0x1F600, 0x1F64F),  # Emoticons
        (0x1F300, 0x1F5FF),  # Miscellaneous Symbols and Pictographs
        (0x1F680, 0x1F6FF),  # Transport and Map Symbols
        (0x1F700, 0x1F77F),  # Alchemical Symbols
        (0x1F780, 0x1F7FF),  # Geometric Shapes Extended
        (0x1F800, 0x1F8FF),  # Supplemental Arrows-C
        (0x1F900, 0x1F9FF),  # Supplemental Symbols and Pictographs
        (0x1FA00, 0x1FA6F),  # Chess Symbols
        (0x1FA70, 0x1FAFF),  # Symbols and Pictographs Extended-A
        (0x2600, 0x26FF),    # Miscellaneous Symbols
        (0x2700, 0x27BF),    # Dingbats
        (0x1F1E6, 0x1F1FF),  # Regional Indicator Symbols
    ]
    
    for start, end in emoji_ranges:
        for codepoint in range(start, end + 1):
            valid_code_points.append(codepoint)
    
    return valid_code_points

def generate_hex_permutations():
    hex_permutations = []
    for i in range(0x0000, 0xFFFF + 1):
        hex_str = f'{i:04X}'
        hex_permutations.append(hex_str)
    return hex_permutations

def filter_code_points_with_glyphs(font_paths, code_points):
    valid_code_points = set(code_points)
    for font_path in font_paths:
        font = TTFont(font_path)
        cmap = font['cmap'].getBestCmap()
        glyf_table = font['glyf']
        
        for codepoint in list(valid_code_points):
            if codepoint not in cmap:
                valid_code_points.remove(codepoint)
                continue
            
            glyph_name = cmap[codepoint]
            glyph = glyf_table[glyph_name]
            
            # Check if the glyph has no contours (empty space)
            if glyph.isComposite():
                continue
            if glyph.numberOfContours <= 0:
                valid_code_points.remove(codepoint)
    
    return list(valid_code_points)

def map_hex_to_utf8(font_paths):
    utf8_code_points = generate_utf8_code_points()
    utf8_code_points = filter_code_points_with_glyphs(font_paths, utf8_code_points)
    hex_permutations = generate_hex_permutations()

    # Ensure we have enough code points for the permutations
    assert len(utf8_code_points) >= len(hex_permutations), "Not enough code points to cover all permutations."

    mapping = {hex_str: f'U+{codepoint:04X}' for hex_str, codepoint in zip(hex_permutations, utf8_code_points)}

    # Save the mapping to a JSON file
    with open('hex_to_utf8_mapping.json', 'w', encoding='utf-8') as json_file:
        json.dump(mapping, json_file, ensure_ascii=False, indent=2)
    
    print(f'Mapping of {len(hex_permutations)} hexadecimal permutations to UTF-8 code points saved to hex_to_utf8_mapping.json')

# Paths to your font files
font_paths = ['NotoSans-VariableFont_wdth,wght.ttf', 'NotoEmoji-VariableFont_wght.ttf']

# Generate the mapping
map_hex_to_utf8(font_paths)
