import tkinter as tk
from tkinter import Canvas, Text, messagebox, Scrollbar, VERTICAL, HORIZONTAL
from PIL import Image, ImageDraw, ImageTk
import json
import logging
import threading

logging.basicConfig(level=logging.INFO)

class AppData:
    hexColorIndex = {}
    hexValuePxPosition = {}
    hexValueSequence = {}

    @classmethod
    def read_json_data(cls, json_file):
        try:
            with open(json_file, 'r') as file:
                data = json.load(file)

            # Logging to check data loaded from JSON
            logging.info(f"Loaded JSON data: {data}")

            # Assign class variables
            cls.hexColorIndex = data['hexColorIndex']
            cls.hexValuePxPosition = {k: {eval(k2): v2 for k2, v2 in v.items()} for k, v in data['hexValuePxPosition'].items()}
            cls.hexValueSequence = data['hexValueSequence']

            # Logging to check initialized attributes
            logging.info(f"hexColorIndex: {cls.hexColorIndex}")
            logging.info(f"hexValuePxPosition: {cls.hexValuePxPosition}")

        except FileNotFoundError:
            logging.error(f"File '{json_file}' not found.")
        except KeyError as e:
            logging.error(f"Key error: {str(e)}")
        except json.JSONDecodeError as e:
            logging.error(f"JSON decode error: {str(e)}")
        except Exception as e:
            logging.error(f"Error reading JSON data: {str(e)}")

# Initialize AppData with JSON data
AppData.read_json_data('HexLargePatternData.json')

class HexPatternGenerator:
    def __init__(self, app_template, app_data):
        self.file_path = ''
        self.app_data = app_data
        self.app_template = app_template
        self.hexLargeString = ""
        self.image_generation_thread = None

    def set_hex_large_string(self, hex_large_string):
        # Limit to 960 characters
        if len(hex_large_string) > 960:
            messagebox.showerror("Error", "Please enter a hexadecimal string with up to 960 characters.")
            return
        
        self.hexLargeString = hex_large_string.upper()

    def validate_hex(self, hex_string):
        return all(c in '0123456789abcdefABCDEF' for c in hex_string)

    def generate_image(self):
        hex_string = self.hexLargeString.strip()
        if not self.validate_hex(hex_string):
            messagebox.showerror("Error", "Invalid Hex Input. Please enter a valid hexadecimal string.")
            return

        # Clear previous image
        self.app_template.image_canvas.delete("all")

        errors = False
        segment_size = 48
        canvas_width, canvas_height = 1024, 384
        pixel_size = 16  # Adjust pixel size as needed
        row_height = 24

        for start_index in range(0, min(len(hex_string), 960), segment_size):
            hex_segment = hex_string[start_index:start_index + segment_size]

            hex_parts = {
                'hexOne': hex_segment[0:6],
                'hexTwo': hex_segment[6:12],
                'hexThree': hex_segment[12:18],
                'hexFour': hex_segment[18:24],
                'hexFive': hex_segment[24:30],
                'hexSix': hex_segment[30:36],
                'hexSeven': hex_segment[36:42],
                'hexEight': hex_segment[42:48]
            }

            for i, (part_name, hex_part) in enumerate(hex_parts.items()):
                if errors:
                    break  # Exit loop if there are errors to show only one error message

                pixel_position_key = f"{part_name}Position"
                color_index_key = f"{part_name}ColorIndex"

                for j, hexChar in enumerate(hex_part):
                    pixel_position = self.app_data.hexValuePxPosition[pixel_position_key]
                    color_index = self.app_data.hexColorIndex[color_index_key]
                    pixelcolor = color_index.get(hexChar, '#FFFFFF')

                    found_position = False
                    for pos, value in pixel_position.items():
                        if value == str(j):
                            row, col = pos  # Unpack the tuple
                            x0, y0 = col * pixel_size, (start_index // segment_size * 1 + row) * row_height
                            x1, y1 = (col + 1) * pixel_size, (start_index // segment_size * 1 + row + 1) * row_height
                            self.app_template.image_canvas.create_rectangle(x0, y0, x1, y1, fill=pixelcolor)
                            found_position = True
                            break  # Exit loop once position is found

                    if not found_position:
                        errors = True

        if errors:
            messagebox.showerror("Error", "Invalid Hex Input. Please enter a valid hexadecimal string (up to 960 characters).")

    def start_image_generation(self):
        if self.image_generation_thread and self.image_generation_thread.is_alive():
            messagebox.showinfo("Info", "Image generation is already in progress.")
            return

        self.image_generation_thread = threading.Thread(target=self.generate_image)
        self.image_generation_thread.start()

    def save_image_as_png(self):
        # Ensure the canvas is updated with the latest drawing
        self.app_template.image_canvas.update()

        # Create a PIL image from the tkinter canvas
        image = Image.new("RGB", (self.app_template.image_canvas.winfo_width(), self.app_template.image_canvas.winfo_height()), "white")
        draw = ImageDraw.Draw(image)
        self.app_template.image_canvas.update()
        image.save("pattern_image.png")

class AppTemplate:
    def __init__(self, root):
        self.root = root
        self.app_data = AppData
        self.pattern_generator = HexPatternGenerator(self, self.app_data)
        self.root.title("Hex Large Pattern Generator")

        # Main Frame
        self.main_view = tk.Frame(self.root, width=1200, height=800)
        self.main_view.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Adding input box in the main view horizontally
        self.hex_input = Text(self.main_view, width=100, height=10)
        self.hex_input.pack(pady=20, padx=20, side=tk.TOP, fill=tk.X)

        tk.Button(self.main_view, text="Generate Pattern", command=self.generate_pattern).pack(pady=10, padx=20, side=tk.TOP)
        tk.Button(self.main_view, text="Download Image", command=self.save_image).pack(pady=10, padx=20, side=tk.TOP)

        # Scrollable canvas for the image
        self.canvas_frame = tk.Frame(self.main_view)
        self.canvas_frame.pack(expand=True, pady=10, fill=tk.BOTH)

        self.image_canvas = Canvas(self.canvas_frame, width=1024, height=384)
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
        if self.pattern_generator.validate_hex(hex_large_string):
            self.pattern_generator.set_hex_large_string(hex_large_string)
            self.pattern_generator.start_image_generation()
            self.update_scroll_region()
        else:
            messagebox.showerror("Error", "Invalid Hex Input. Please enter a valid hexadecimal string.")

    def save_image(self):
        self.pattern_generator.save_image_as_png()

    def update_scroll_region(self):
        # Update the scroll region to encompass the entire drawn area
        self.image_canvas.update_idletasks()  # Ensure all items are updated
        bbox = self.image_canvas.bbox("all")
        if bbox:
            self.image_canvas.config(scrollregion=bbox)
        else:
            self.image_canvas.config(scrollregion=self.image_canvas.bbox(tk.ALL))

def main():
    root = tk.Tk()
    root.geometry("1200x800")
    root.title("Hex Large Pattern Generator")
    app = AppTemplate(root)
    root.mainloop()

if __name__ == "__main__":
    main()
