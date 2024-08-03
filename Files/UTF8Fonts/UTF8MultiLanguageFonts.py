import os

def generate_bmp_characters_html(output_folder, range_size=4096):
    os.makedirs(output_folder, exist_ok=True)

    start = 0x0000
    end = 0xFFFF

    total_characters = 0

    for i in range(start, end + 1, range_size):
        range_start = i
        range_end = min(i + range_size - 1, end)
        file_path = os.path.join(output_folder, f'bmp_characters_{range_start:04X}_to_{range_end:04X}.html')

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write('<!DOCTYPE html>\n')
            file.write('<html lang="en">\n')
            file.write('<head>\n')
            file.write('<meta charset="UTF-8">\n')
            file.write(f'<title>Characters from {range_start:04X} to {range_end:04X} (Total: {range_end - range_start + 1})</title>\n')
            file.write('<style>\n')
            file.write('  body { font-family: Arial, sans-serif; }\n')
            file.write('  .character { font-size: 24px; display: inline-block; margin: 5px; text-align: center; }\n')
            file.write('</style>\n')
            file.write('</head>\n')
            file.write('<body>\n')
            file.write(f'<h1>Characters from {range_start:04X} to {range_end:04X} (Total: {range_end - range_start + 1})</h1>\n')

            for codepoint in range(range_start, range_end + 1):
                if 0xD800 <= codepoint <= 0xDFFF:  # Skip surrogate pair range
                    continue
                char = chr(codepoint)
                file.write(f'<div class="character">{char}<br>U+{codepoint:04X}</div>\n')
                total_characters += 1

            file.write('</body>\n')
            file.write('</html>\n')

        print(f'HTML file for characters from {range_start:04X} to {range_end:04X} has been saved to {file_path}')

    print(f'Total characters generated: {total_characters}')

# Usage example
generate_bmp_characters_html('output_bmp1', range_size=4096)
