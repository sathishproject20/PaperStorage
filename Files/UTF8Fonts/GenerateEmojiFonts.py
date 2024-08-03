import os

def generate_emoji_html(output_folder):
    os.makedirs(output_folder, exist_ok=True)
    
    file_path = os.path.join(output_folder, 'emoji_characters.html')

    # Unicode ranges for emoji
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

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write('<!DOCTYPE html>\n')
        file.write('<html lang="en">\n')
        file.write('<head>\n')
        file.write('<meta charset="UTF-8">\n')
        file.write('<title>Emoji Characters</title>\n')
        file.write('<style>\n')
        file.write('  body { font-family: Arial, sans-serif; }\n')
        file.write('  .character { font-size: 24px; display: inline-block; margin: 5px; }\n')
        file.write('</style>\n')
        file.write('</head>\n')
        file.write('<body>\n')
        file.write('<h1>Emoji Characters</h1>\n')

        for start, end in emoji_ranges:
            for codepoint in range(start, end + 1):
                char = chr(codepoint)
                file.write(f'<span class="character">{char}</span>\n')

        file.write('</body>\n')
        file.write('</html>\n')

    print(f'HTML file containing emoji characters has been saved to {file_path}')

# Usage example
generate_emoji_html('output_emoji')
