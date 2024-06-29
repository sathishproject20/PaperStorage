import tkinter as tk
from tkinter import filedialog, Canvas, messagebox
from PIL import Image, ImageDraw, ImageTk
import json
import logging

logging.basicConfig(level=logging.INFO)

class AppData:
    def __init__(self):
        self.hexColorIndex = None
        self.hexValuePxPosition = None
        self.hexOneSequence = None

    @classmethod
    def read_json_data(cls, json_file):
        try:
            with open(json_file, 'r') as file:
                data = json.load(file)
            cls.hexColorIndex = type('hexColorIndex', (object,), data['hexColorIndex'])
            cls.hexValuePxPosition = type('hexValuePxPosition', (object,), {k: {eval(k2): v2 for k2, v2 in v.items()} for k, v in data['hexValuePxPosition'].items()})
            cls.hexOneSequence = data['hexOneSequence']
            cls.hexTwoSequence = data['hexTwoSequence']
            cls.hexThreeSequence = data['hexThreeSequence']
            cls.hexFourSequence = data['hexFourSequence']
            cls.hexFiveSequence = data['hexFiveSequence']
            cls.hexSixSequence = data['hexSixSequence']
            cls.hexSevenSequence = data['hexSevenSequence']
            cls.hexEightSequence = data['hexEightSequence']
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
    def __init__(self, app_template, app_data, file_handle):
        self.file_path = ''
        self.app_data = app_data
        self.app_template = app_template
        self.file_handle = file_handle
        self.hexLargeString = ""

    def set_hexLargeString(self, hexLargeString):
        self.hexLargeString = hexLargeString.upper()

    def validate_hex(self, hex_string):
        return all(c in '0123456789abcdefABCDEF' for c in hex_string)

    def generate_image(self):
        segments = [self.hexLargeString[i:i+48] for i in range(0, len(self.hexLargeString), 48)]

        for hexString in segments:
            if self.validate_hex(hexString):
                image_canvas = Image.new('RGB', (512, 192), 'white')
                draw = ImageDraw.Draw(image_canvas)

                hexOne = hexString[0:6]
                hexTwo = hexString[6:12]
                hexThree = hexString[12:18]
                hexFour = hexString[18:24]
                hexFive = hexString[24:30]
                hexSix = hexString[30:36]
                hexSeven = hexString[36:42]
                hexEight = hexString[42:48]

                # Drawing patterns
                self.draw_pattern(draw, hexOne, self.app_data.hexValuePxPosition.hexOnePosition, self.app_data.hexColorIndex.hexOneColorIndex)
                self.draw_pattern(draw, hexTwo, self.app_data.hexValuePxPosition.hexOnePosition, self.app_data.hexColorIndex.hexTwoColorIndex)
                self.draw_pattern(draw, hexThree, self.app_data.hexValuePxPosition.hexTwoPosition, self.app_data.hexColorIndex.hexThreeColorIndex)
                self.draw_pattern(draw, hexFour, self.app_data.hexValuePxPosition.hexTwoPosition, self.app_data.hexColorIndex.hexFourColorIndex)
                self.draw_pattern(draw, hexFive, self.app_data.hexValuePxPosition.hexThreePosition, self.app_data.hexColorIndex.hexFiveColorIndex)
                self.draw_pattern(draw, hexSix, self.app_data.hexValuePxPosition.hexThreePosition, self.app_data.hexColorIndex.hexSixColorIndex)
                self.draw_pattern(draw, hexSeven, self.app_data.hexValuePxPosition.hexFourPosition, self.app_data.hexColorIndex.hexSevenColorIndex)
                self.draw_pattern(draw, hexEight, self.app_data.hexValuePxPosition.hexFourPosition, self.app_data.hexColorIndex.hexEightColorIndex)
                
                self.app_template.tk_image = ImageTk.PhotoImage(image_canvas)
                self.app_template.image_canvas.create_image(0, 0, anchor=tk.NW, image=self.app_template.tk_image)

            else:
                messagebox.showerror("Error", "Invalid Hex Input. Please enter a valid hexadecimal string (up to 960 characters).")

    def draw_pattern(self, draw, hex_segment, position_data, color_index):
        for key, hexValue in position_data.items():
            row, col = key
            colorIndex = int(hexValue)
            if 0 <= colorIndex < len(hex_segment):
                hexSequence = hex_segment[colorIndex]
                color = color_index.get(hexSequence, '#FFFFFF')
                draw.rectangle([col * 8, row * 8, (col + 1) * 8, (row + 1) * 8], fill=color)

class FileHandle:
    def __init__(self, app_template):
        self.app_template = app_template
        self.pattern_generator = None
        self.file_name = ''
        self.file_path = ''

    def validate_hex(self, hex_string):
        return all(c in '0123456789abcdefABCDEF' for c in hex_string)

class AppTemplate:
    def __init__(self, root):
        self.root = root
        self.app_data = AppData()
        self.file_handle = FileHandle(self)
        self.pattern_generator = HexPatternGenerator(self, self.app_data, self.file_handle)
        self.file_handle.pattern_generator = self.pattern_generator
        self.root.title("Hex Large Pattern Generator")
        self.hexLargeString = ""  # Initialize hexLargeString attribute in AppTemplate
        self.pattern_generator.set_hexLargeString(self.hexLargeString)  # Pass hex12String to PatternGenerator

        # Side Frame
        self.side_view = tk.Frame(self.root, width=200, height=800)
        self.side_view.pack(side=tk.LEFT, fill=tk.Y)

        # Main Frame
        self.main_view = tk.Frame(self.root, width=600, height=800)
        self.main_view.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Adding input box in the side view
        self.hex_input = tk.Text(self.side_view, width=25, height=10)
        self.hex_input.pack(pady=20)

        tk.Button(self.side_view, text="Generate Pattern", command=self.generate_pattern).pack(pady=10)

        # Centering elements in the main frame
        self.image_canvas = Canvas(self.main_view, width=512, height=192)
        self.image_canvas.pack(expand=True, pady=10)

    def generate_pattern(self):
        hex_large_string = self.hex_input.get("1.0", tk.END).strip()
        if self.file_handle.validate_hex(hex_large_string) and len(hex_large_string) <= 960:
            self.pattern_generator.set_hexLargeString(hex_large_string)
            self.pattern_generator.generate_image()
        else:
            messagebox.showerror("Error", "Invalid Hex Input. Please enter a valid hexadecimal string (up to 960 characters).")

def test_image_generation():
    root = tk.Tk()
    app = AppTemplate(root)

    test_hex_string = "1234567890ABCDEF" * 60  # 960 characters
    app.hex_input.insert(tk.END, test_hex_string)
    app.generate_pattern()

    # Check if image is created and displayed
    assert hasattr(app, 'tk_image'), "Image was not created."
    assert app.tk_image is not None, "Image object is None."

    print("Test passed: Image generated and displayed successfully.")
    root.destroy()

def test_invalid_hex_input():
    root = tk.Tk()
    app = AppTemplate(root)

    # Test case: Invalid hex input
    app.hex_input.insert(tk.END, "G12345")  # Invalid hex characters
    app.generate_pattern()

    # Check if error message is displayed
    assert messagebox.called, "Error message not displayed for invalid hex input."

    root.destroy()

def test_long_hex_input():
    root = tk.Tk()
    app = AppTemplate(root)

    # Test case: Long hex input (more than 960 characters)
    test_hex_string = "1234567890ABCDEF" * 61  # 976 characters
    app.hex_input.insert(tk.END, test_hex_string)
    app.generate_pattern()

    # Check if error message is displayed
    assert messagebox.called, "Error message not displayed for long hex input."

    root.destroy()

def test_empty_hex_input():
    root = tk.Tk()
    app = AppTemplate(root)

    # Test case: Empty hex input
    app.hex_input.insert(tk.END, "")
    app.generate_pattern()

    # Check if error message is displayed
    assert messagebox.called, "Error message not displayed for empty hex input."

    root.destroy()
    

def main():
    root = tk.Tk()
    app = AppTemplate(root)
    root.mainloop()

if __name__ == "__main__":
    # Comment out `main()` and uncomment `test_image_generation()` to run the test case instead of the main application.
    # main()
    test_image_generation()
