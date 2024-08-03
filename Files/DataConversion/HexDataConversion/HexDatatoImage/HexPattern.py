import tkinter as tk
from tkinter import filedialog, Canvas, Text, messagebox, Scrollbar
from PIL import Image, ImageDraw, ImageGrab
import re
import os
import json
import logging
import threading

logging.basicConfig(level=logging.INFO)

class AppData:
    hexColorIndex = {}

    @classmethod
    def read_json_data(cls, json_file):
        try:
            with open(json_file, 'r') as file:
                data = json.load(file)

            # Logging to check data loaded from JSON
            logging.info(f"Loaded JSON data: {data}")

            # Assign class variables
            cls.hexColorIndex = data['hexColorIndex']

            # Logging to check initialized attributes
            logging.info(f"hexColorIndex: {cls.hexColorIndex}")

        except FileNotFoundError:
            logging.error(f"File '{json_file}' not found.")
        except KeyError as e:
            logging.error(f"Key error: {str(e)}")
        except json.JSONDecodeError as e:
            logging.error(f"JSON decode error: {str(e)}")
        except Exception as e:
            logging.error(f"Error reading JSON data: {str(e)}")

# Initialize AppData with JSON data
AppData.read_json_data('hex_color_data.json')

# Define the maximum dimensions for the canvas
max_width = 512
max_height = 512

class HexPatternGenerator:
    def __init__(self, app_template, app_data):
        self.app_data = app_data
        self.app_template = app_template
        self.hexLargeString = ""
        # Move hexTwoValueArray initialization inside __init__ method
        self.hexTwoValueArray = [f"{i:02X}" for i in range(256)]

    def set_hex_large_string(self, hex_large_string):
        # Limit to 1024 characters
        if len(hex_large_string) > 512:
            messagebox.showerror("Error", "Please enter an ASCII string with up to 1024 characters.")
            return

        self.hexLargeString = hex_large_string.upper()

    @classmethod
    def is_valid_hex(cls, hex_value):
        # Check if the hex_value matches the two-character hexadecimal format
        return bool(re.fullmatch(r'[0-9A-Fa-f]{2}', hex_value))


    def validate_hex_data(hex_data):
        # Iterate through the hex data and validate each value
        for key, value in hex_data.items():
            if not HexPatternGenerator.is_valid_hex(key):
                print(f"Invalid key: {key}")
                return False
            if not HexPatternGenerator.is_valid_hex(value):
                print(f"Invalid value: {value}")
                return False
        return True

    def draw_pixel(self, canvas, x, y, pixel_size, color):
        canvas.create_rectangle(x, y, x + pixel_size, y + pixel_size, outline=color, fill=color)

    def draw_image_canvas(self, canvas, data, max_width, max_height):
        # Calculate dimensions based on the length of data
        num_chars = len(data)
        sqrt_chars = int(num_chars ** 0.5)

        # Determine the best-fit canvas size
        if sqrt_chars * sqrt_chars < num_chars:
            sqrt_chars += 1

        pixel_size = min(max_width // sqrt_chars, max_height // sqrt_chars)
        canvas_size = pixel_size * sqrt_chars

        # Resize the canvas
        canvas.config(width=canvas_size, height=canvas_size)

        # Retrieve hexadecimal color index from app_data
        hex_color_index = self.app_data.hexColorIndex

        # Draw each pixel on the canvas based on hex values
        for y in range(sqrt_chars):
            for x in range(sqrt_chars):
                index = y * sqrt_chars + x
                if index < num_chars:
                    hex_value = data[index * 2:index * 2 + 2]  # Get two-character hex value from data
                    color = hex_color_index.get(hex_value, '#000000')  # Get color from hexColorIndex
                    self.draw_pixel(canvas, x * pixel_size, y * pixel_size, pixel_size, color)

    def start_drawing(self, canvas, max_width, max_height):
        self.draw_image_canvas(canvas, self.hexLargeString, max_width, max_height)


class AppTemplate:
    def __init__(self, root):
        self.root = root
        self.app_data = AppData()
        self.pattern_generator = HexPatternGenerator(self, self.app_data)
        self.root.title("Hex Large Pattern Generator")

        # Main Frame
        self.main_view = tk.Frame(self.root, width=1200, height=1200)
        self.main_view.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Adding input box in the main view horizontally
        self.hex_input = Text(self.main_view, width=100, height=10)
        self.hex_input.pack(pady=20, padx=20, side=tk.TOP, fill=tk.X)

        tk.Button(self.main_view, text="Generate Pattern", command=self.generate_pattern).pack(pady=10, padx=20, side=tk.TOP)
        tk.Button(self.main_view, text="Save Image", command=self.save_image).pack(pady=10, padx=20, side=tk.TOP)

        # Scrollable canvas for the image
        self.canvas_frame = tk.Frame(self.main_view)
        self.canvas_frame.pack(expand=True, pady=10, fill=tk.BOTH)

        self.image_canvas = Canvas(self.canvas_frame, width=512, height=512)
        self.image_canvas.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        self.scroll_y = Scrollbar(self.canvas_frame, orient=tk.VERTICAL, command=self.image_canvas.yview)
        self.scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        self.scroll_x = Scrollbar(self.canvas_frame, orient=tk.HORIZONTAL, command=self.image_canvas.xview)
        self.scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

        self.image_canvas.configure(yscrollcommand=self.scroll_y.set, xscrollcommand=self.scroll_x.set)

        # Initialize scroll region
        self.image_canvas.update_idletasks()  # Ensure all items are updated
        bbox = self.image_canvas.bbox("all")
        if bbox:
            self.image_canvas.config(scrollregion=bbox)
        else:
            self.image_canvas.config(scrollregion=self.image_canvas.bbox(tk.ALL))

    def generate_pattern(self):
        hex_large_string = self.hex_input.get("1.0", tk.END).strip()
        if self.pattern_generator.is_valid_hex(hex_large_string):
            self.pattern_generator.set_hex_large_string(hex_large_string)
            self.pattern_generator.start_drawing(self.image_canvas, max_width, max_height)
            self.update_scroll_region()
        else:
            messagebox.showerror("Error", "Invalid Hex Value Input. Please enter a valid Hex string.")

    def update_scroll_region(self):
        # Update the scroll region to encompass the entire drawn area
        self.image_canvas.update_idletasks()  # Ensure all items are updated
        bbox = self.image_canvas.bbox("all")
        if bbox:
            self.image_canvas.config(scrollregion=bbox)
        else:
            self.image_canvas.config(scrollregion=self.image_canvas.bbox(tk.ALL))

    def save_image(self, file_path=None):
        self.image_canvas.update_idletasks()

        if not file_path:
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])

        if file_path:
            try:
                num_chars = len(self.pattern_generator.asciiLargeString)
                sqrt_chars = int(num_chars ** 0.5)
                if sqrt_chars * sqrt_chars < num_chars:
                    sqrt_chars += 1

                pixel_size = 1
                canvas_size = pixel_size * sqrt_chars

                image = Image.new("RGB", (canvas_size, canvas_size), "black")
                draw = ImageDraw.Draw(image)

                # Draw each pixel on the canvas based on hex values
                for y in range(sqrt_chars):
                    for x in range(sqrt_chars):
                        index = y * sqrt_chars + x
                        if index < num_chars:
                            hex_value = self.pattern_generator.hexLargeString.data[index * 2:index * 2 + 2]  # Get two-character hex value from data
                            color = self.app_data.hexColorIndex.get(hex_value, '#000000')  # Get color from hexColorIndex
                            draw.rectangle([x * pixel_size, y * pixel_size, (x + 1) * pixel_size, (y + 1) * pixel_size], fill=color)

                image.save(file_path)
                messagebox.showinfo("Success", f"Image saved as {file_path}.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image: {str(e)}")

def main():
    root = tk.Tk()
    root.geometry("1200x1200")
    root.title("Hex Large Pattern Generator")
    app = AppTemplate(root)
    root.mainloop()

if __name__ == "__main__":
    main()
