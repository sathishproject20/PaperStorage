from PIL import Image, ImageDraw

# Define the 4x4 bitmap fonts for hexadecimal characters with custom patterns
hex_chars = {
    '0': [
        0b1000,
        0b0000,
        0b0000,
        0b0000
    ],
    '1': [
        0b0100,
        0b0000,
        0b0000,
        0b0000
    ],
    '2': [
        0b0010,
        0b0000,
        0b0000,
        0b0000
    ],
    '3': [
        0b0001,
        0b0000,
        0b0000,
        0b0000
    ],
    '4': [
        0b0000,
        0b1000,
        0b0000,
        0b0000
    ],
    '5': [
        0b0000,
        0b0100,
        0b0000,
        0b0000
    ],
    '6': [
        0b0000,
        0b0010,
        0b0000,
        0b0000
    ],
    '7': [
        0b0000,
        0b0001,
        0b0000,
        0b0000
    ],
    '8': [
        0b0000,
        0b0000,
        0b1000,
        0b0000
    ],
    '9': [
        0b0000,
        0b0000,
        0b0100,
        0b0000
    ],
    'A': [
        0b0000,
        0b0000,
        0b0010,
        0b0000
    ],
    'B': [
        0b0000,
        0b0000,
        0b0001,
        0b0000
    ],
    'C': [
        0b0000,
        0b0000,
        0b0000,
        0b1000
    ],
    'D': [
        0b0000,
        0b0000,
        0b0000,
        0b0100
    ],
    'E': [
        0b0000,
        0b0000,
        0b0000,
        0b0010
    ],
    'F': [
        0b0000,
        0b0000,
        0b0000,
        0b0001
    ]
}

def draw_bitmap(draw, bitmap, x, y, size=10):
    for i, row in enumerate(bitmap):
        for j in range(4):
            if (row >> (3 - j)) & 1:
                draw.rectangle([x + j * size, y + i * size, x + (j + 1) * size, y + (i + 1) * size], fill="black")

def render_hex_fonts():
    font_size = 10
    width = 4 * font_size
    height = 4 * font_size
    image = Image.new("1", (width * 16, height), "white")  # '1' for black-and-white
    draw = ImageDraw.Draw(image)

    x_offset = 0
    y_offset = 0

    for char, bitmap in hex_chars.items():
        draw_bitmap(draw, bitmap, x_offset, y_offset, size=font_size)
        x_offset += width
        if x_offset >= width * 16:
            x_offset = 0
            y_offset += height

    image.save("hexadecimal_spritesheet.png")
    image.show()

render_hex_fonts()
