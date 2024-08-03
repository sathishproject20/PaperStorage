import os

def generate_chinese_characters_html(folder_path):
    # Ensure the folder exists
    os.makedirs(folder_path, exist_ok=True)
    
    # File path for the HTML file
    file_path = os.path.join(folder_path, 'chinese_characters.html')
    
    # Unicode range for Chinese characters
    start = 0x4E00
    end = 0x9FFF
    
    # Create and write to the HTML file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write('<!DOCTYPE html>\n')
        file.write('<html lang="zh">\n')
        file.write('<head>\n')
        file.write('<meta charset="UTF-8">\n')
        file.write('<title>Chinese Characters</title>\n')
        file.write('<style>\n')
        file.write('  body { font-family: Arial, sans-serif; }\n')
        file.write('  .character { font-size: 24px; display: inline-block; margin: 5px; }\n')
        file.write('</style>\n')
        file.write('</head>\n')
        file.write('<body>\n')
        file.write('<h1>All Chinese Characters</h1>\n')
        
        for codepoint in range(start, end + 1):
            char = chr(codepoint)
            file.write(f'<span class="character">{char}</span>\n')
        
        file.write('</body>\n')
        file.write('</html>\n')

    print(f'HTML file containing Chinese characters has been saved to {file_path}')

# Usage example
generate_chinese_characters_html('output_folder')
