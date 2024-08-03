from PIL import Image

def draw_pattern_from_hex_data(sprite_sheet_path, hex_data_path, output_image_path, char_width=40, char_height=40, chars_per_row=32):
    # Load the sprite sheet
    sprite_sheet = Image.open(sprite_sheet_path)
    
    # Dimensions of a single character sprite
    sprite_width, sprite_height = char_width, char_height

    # Read hex data from the file
    with open(hex_data_path, 'r') as file:
        hex_data = file.read().strip()

    # Dimensions of the output image
    num_chars = len(hex_data)
    output_width = chars_per_row * sprite_width
    output_height = ((num_chars + chars_per_row - 1) // chars_per_row) * sprite_height

    # Create the output image
    output_image = Image.new("1", (output_width, output_height), "white")  # '1' for black-and-white

    # Draw each character from the hex data
    for i, char in enumerate(hex_data):
        x = (i % chars_per_row) * sprite_width
        y = (i // chars_per_row) * sprite_height

        # Calculate the position of the character sprite in the sprite sheet
        sprite_x = int(char, 16) * sprite_width
        sprite_y = 0

        # Crop the sprite from the sprite sheet
        sprite = sprite_sheet.crop((sprite_x, sprite_y, sprite_x + sprite_width, sprite_y + sprite_height))
        output_image.paste(sprite, (x, y))

    # Save the output image
    output_image.save(output_image_path)
    output_image.show()

# Example usage
draw_pattern_from_hex_data("hexadecimal_spritesheet.png", "hex_data.txt", "pattern_image.png")
