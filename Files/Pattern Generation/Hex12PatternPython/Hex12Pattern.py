import tkinter as tk
from tkinter import filedialog, Canvas, messagebox
import asyncio
import os
from PIL import Image, ImageDraw, ImageTk
import json
import logging

logging.basicConfig(level=logging.INFO)

class AppData:
    def __init__(self, root):
        self.root = root

    @classmethod
    def read_json_data(cls, json_file):
        with open(json_file, 'r') as file:
            data = json.load(file)
        cls.hexOneColorIndex = data['hexOneColorIndex']
        cls.hexTwoColorIndex = data['hexTwoColorIndex']
        cls.hexOnePxPosition = {eval(k): v for k, v in data['hexOnePxPosition'].items()}
        cls.hexTwoPxPosition = {eval(k): v for k, v in data['hexTwoPxPosition'].items()}
        cls.hexOneSequence = data['hexOneSequence']
        cls.hexTwoSequence = data['hexTwoSequence']

# Initialize AppData with JSON data
AppData.read_json_data('Hex12PatternData.json')


class PatternGenerator:
    def __init__(self, app_template, app_data, file_handle):
        self.app_template = app_template
        self.app_data = app_data
        self.file_handle = file_handle
        self.hex12String = ""
        self.file_handle.pattern_generator = self

    def set_hex12String(self, hex12String):
        self.hex12String = hex12String

    def draw_pattern(self):
        self.app_template.image_canvas.delete("all")  # Clear the canvas before drawing

        hexString = self.hex12String

        if self.file_handle.validate_hex(hexString):
            image_canvas = Image.new('RGB', (256, 256), 'white')
            draw = ImageDraw.Draw(image_canvas)

            hexOne = hexString[:6]
            hexTwo = hexString[6:]

            # Draw HexOne pattern
            for key, hexValue in self.app_data.hexOnePxPosition.items():
                row, col = key
                colorIndex = int(hexValue)
                if 0 <= colorIndex < len(hexOne):
                    hexOneSequence = hexOne[colorIndex]
                    color = self.app_data.hexOneColorIndex.get(hexOneSequence, '#FFFFFF')
                    draw.rectangle([col * 16, row * 16, (col + 1) * 16, (row + 1) * 16], fill=color)

            # Draw HexTwo pattern
            for key, hexValue in self.app_data.hexTwoPxPosition.items():
                row, col = key
                colorIndex = int(hexValue)
                if 0 <= colorIndex < len(hexTwo):
                    hexTwoSequence = hexTwo[colorIndex]
                    color = self.app_data.hexTwoColorIndex.get(hexTwoSequence, '#FFFFFF')
                    draw.rectangle([col * 16, row * 16, (col + 1) * 16, (row + 1) * 16], fill=color)

            self.image = image_canvas
            self.generate_image(image_canvas)
        else:
            messagebox.showerror("Error", "Invalid Hex Input. Please enter a valid hexadecimal string (up to 12 characters).")

    def generate_image(self, image):
        self.app_template.tk_image = ImageTk.PhotoImage(image)
        self.app_template.image_canvas.create_image(0, 0, anchor=tk.NW, image=self.app_template.tk_image)

class GenerateMultipleImages:
    def __init__(self, pattern_generator, file_handle, app_template, app_data):
        self.pattern_generator = pattern_generator
        self.file_handle = file_handle
        self.app_template = app_template
        self.app_data = app_data

    async def generate_multiple_images(self):
        await asyncio.sleep(1)  # Simulating async operation

        hexString = self.pattern_generator.hex12String

        if not self.file_handle.file_path or not os.path.isfile(self.file_handle.file_path):
            messagebox.showerror("Error", "Please specify a valid file path.")
            return

        try:
            with open(self.file_handle.file_path, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    hexString = line.strip().upper()
                    if self.file_handle.validate_hex(hexString):
                        self.pattern_generator.set_hex12String(hexString)
                        self.app_template.pattern_generator.draw_pattern()
                        folder_path = self.file_handle.folder_path
                        filename = os.path.join(folder_path, hexString)
                        await self.process_and_save_hex_string(hexString, filename)
                messagebox.showinfo("Success", "All images generated successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Error generating images: {e}")

    async def process_and_save_hex_string(self, hexString, filename):
        self.app_template.pattern_generator.draw_pattern()
        self.app_template.pattern_generator.generate_image(self.app_template.pattern_generator.image)
        self.file_handle.save_canvas_as_image(filename, 'png')


class FileHandle:
    def __init__(self, app_template):
        self.app_template = app_template
        self.pattern_generator = None
        self.file_path = ''
        self.folder_path = ''

    def set_output_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.app_template.output_entry.delete(0, tk.END)
            self.app_template.output_entry.insert(0, folder_path)
            self.folder_path = folder_path
            messagebox.showinfo("Success", f"Output folder set to: {folder_path}")
        else:
            messagebox.showerror("Error", "Output folder selection cancelled.")

    async def handle_file_upload(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if not self.file_path:
            return
        self.app_template.file_path_label.config(text=f"File Path: {self.file_path}", wraplength=190)

    def download_png(self):
        hexString = self.app_template.hex12String  # Access hex12String from app_template
        if not self.validate_hex(hexString):
            messagebox.showerror("Error", "Invalid hex string. Please generate a valid image first.")
            return

        # Prompt user to select a folder to save the PNG
        path_to_savepng = filedialog.askdirectory()
        if not path_to_savepng:
            messagebox.showerror("Error", "Folder selection cancelled.")
            return

        # Prompt user to enter a filename
        filename = tk.simpledialog.askstring("Save PNG", "Enter filename (without extension):")
        if not filename:
            messagebox.showerror("Error", "Filename input cancelled.")
            return

        # Construct the full filename with path and extension
        filename = os.path.join(path_to_savepng, filename + ".png")

        try:
            self.process_and_save_png(filename)
            messagebox.showinfo("Success", "PNG image saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Error saving PNG image: {e}")

    def download_jpeg(self):
        hexString = self.app_template.hex12String  # Access hex12String from app_template
        if not self.validate_hex(hexString):
            messagebox.showerror("Error", "Invalid hex string. Please generate a valid image first.")
            return

        # Prompt user to select a folder to save the JPEG
        path_to_savejpeg = filedialog.askdirectory()
        if not path_to_savejpeg:
            messagebox.showerror("Error", "Folder selection cancelled.")
            return

        # Prompt user to enter a filename
        filename = tk.simpledialog.askstring("Save JPEG", "Enter filename (without extension):")
        if not filename:
            messagebox.showerror("Error", "Filename input cancelled.")
            return

        # Construct the full filename with path and extension
        filename = os.path.join(path_to_savejpeg, filename + ".jpeg")

        try:
            self.process_and_save_jpeg(filename)
            messagebox.showinfo("Success", "JPEG image saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Error saving JPEG image: {e}")

    def process_and_save_png(self, filename):
        self.app_template.pattern_generator.draw_pattern()
        self.app_template.pattern_generator.generate_image(self.app_template.pattern_generator.image)
        self.save_canvas_as_image(filename, 'png')

    def process_and_save_jpeg(self, filename):
        self.app_template.pattern_generator.draw_pattern()
        self.app_template.pattern_generator.generate_image(self.app_template.pattern_generator.image)
        self.save_canvas_as_image(filename, 'jpeg')

    def validate_hex(self, hexString):
        return all(c in "0123456789abcdefABCDEF" for c in hexString) and len(hexString) <= 12

    def save_canvas_as_image(self, filename, filetype):
        try:
            ps_filename = filename + ".ps"
            self.app_template.image_canvas.postscript(file=ps_filename, colormode='color')
            image = Image.open(ps_filename)

            if filetype == 'png':
                image.save(filename + ".png", 'PNG')  # Save as PNG with .png extension
            elif filetype == 'jpeg':
                image.save(filename + ".jpeg", 'JPEG')  # Save as JPEG with .jpeg extension
            else:
                messagebox.showerror("Error", "Unsupported file type.")
                return False

            os.remove(ps_filename)
            logging.info(f"Saved image: {filename}.{filetype}")
            return True

        except Exception as e:
            messagebox.showerror("Error", f"Error saving image: {e}")
            return False


class AppTemplate:
    def __init__(self, root):
        self.root = root
        self.app_data = AppData(root)
        self.file_handle = FileHandle(self)
        self.pattern_generator = PatternGenerator(self, self.app_data, self.file_handle)
        self.file_handle.pattern_generator = self.pattern_generator
        self.hex12String = ""  # Initialize hex12String attribute in AppTemplate
        self.pattern_generator.set_hex12String(self.hex12String)  # Pass hex12String to PatternGenerator
        self.generate_multiple_images = GenerateMultipleImages(self.pattern_generator, self.file_handle, self, self.app_data)

        # Set up GUI components
        self.setup_gui()

    def setup_gui(self):
        # Header
        header = tk.Frame(root, bg='#0000FF', height=50)
        header.pack(side='top', fill='x')
        header_label = tk.Label(header, text="Hex 12 Pattern Generator", bg='#0000FF', fg='White', font=('Arial', 20, 'bold'))
        header_label.pack(pady=10)

        # Side View
        side_view = tk.Frame(root, bg='lightgrey', width=200, height=600)
        side_view.pack(side='left', fill='y')
        side_view.pack_propagate(False)

        # Main View
        main_view = tk.Frame(root, bg='white', width=600, height=600)
        main_view.pack(side='right', expand=True, fill='both')

        # Hex String Input Field
        hex_input_label = tk.Label(side_view, text="Enter 12-character Hex String:", font=('Arial', 12))
        hex_input_label.pack(pady=5)

        vcmd = (self.root.register(self.file_handle.validate_hex), '%P')
        self.hex_input = tk.Entry(side_view, font=('Arial', 12), width=20, validate='key', validatecommand=vcmd)
        self.hex_input.pack(pady=5)

        # Generate Pattern Button
        generate_button = tk.Button(side_view, text="Generate Pattern", font=('Arial', 12), command=self.generate_pattern)
        generate_button.pack(pady=10)

        # Upload File Button
        upload_button = tk.Button(side_view, text="Upload File", font=('Arial', 12), command=lambda: asyncio.run(self.file_handle.handle_file_upload()))
        upload_button.pack(pady=10)

        self.file_path_label = tk.Label(side_view, text="File Path", font=('Arial', 12), wraplength=190)
        self.file_path_label.pack()

        # Output Folder Selection
        self.output_entry = tk.Entry(side_view, font=('Arial', 12), width=50)
        self.output_entry.pack(pady=10)

        output_button = tk.Button(side_view, text="Set Output Folder", font=('Arial', 12), command=lambda: self.file_handle.set_output_folder())
        output_button.pack()

        # Generate Multiple Images Button
        generate_multiple_button = tk.Button(side_view, text="Generate Multiple Images", font=('Arial', 12), command=lambda: asyncio.run(self.generate_multiple_images.generate_multiple_images()))
        generate_multiple_button.pack(pady=10)

        # Canvas for Image Display
        self.image_canvas = Canvas(main_view, width=256, height=256, bg='white')
        self.image_canvas.pack(pady=10)

        downloadPngButton = tk.Button(main_view, text="Download as PNG", command=self.file_handle.download_png)
        downloadPngButton.place(relx=0.35, rely=0.8, anchor='center')

        downloadJpegButton = tk.Button(main_view, text="Download as JPEG", command=self.file_handle.download_jpeg)
        downloadJpegButton.place(relx=0.65, rely=0.8, anchor='center')

    def generate_pattern(self):
        hex_string = self.hex_input.get().strip()
        self.pattern_generator.set_hex12String(hex_string)
        self.pattern_generator.draw_pattern()

    def run(self):
        self.root.mainloop()


root = tk.Tk()
root.geometry("800x800")
root.title("Hex 12 Pattern Generator")

app_template = AppTemplate(root)
app_template.run()
