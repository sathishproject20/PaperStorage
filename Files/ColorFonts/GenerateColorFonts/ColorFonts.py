import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageColor
import threading
import asyncio
import aiofiles

class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Color Fonts Generator")
        self.master.geometry("300x400")

        # Initialize Model
        self.model = ImageModel(64, 64)  # 64x64 grid

        # Color input
        self.color_label = tk.Label(self.master, text="Color (hex):")
        self.color_label.pack(padx=10, pady=5)
        self.color_entry = tk.Entry(self.master, width=10)
        self.color_entry.pack(padx=10, pady=5)

        # Button to set color
        self.set_color_button = tk.Button(self.master, text="Set Color", command=self.set_color)
        self.set_color_button.pack(padx=10, pady=5)

        # Button to upload file
        self.upload_button = tk.Button(self.master, text="Upload File", command=self.upload_file)
        self.upload_button.pack(padx=10, pady=5)

        # Canvas to display image
        self.canvas = tk.Canvas(self.master, width=64, height=64, bg='white')
        self.canvas.pack(padx=10, pady=10)

        # Button to save image
        self.save_button = tk.Button(self.master, text="Save Image", command=self.save_image)
        self.save_button.pack(padx=10, pady=5)

    def set_color(self):
        color_code = self.color_entry.get()
        if not color_code.startswith('#'):
            color_code = '#' + color_code

        try:
            color = ImageColor.getrgb(color_code)
            self.model.fill_color(color_code)
            self.show_image()
        except ValueError:
            messagebox.showerror("Invalid Color", "Please enter a valid hex color code.")

    def show_image(self):
        image = self.model.get_image()
        self.photo = ImageTk.PhotoImage(image.resize((64, 64), Image.NEAREST))
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)

    def save_image(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if file_path:
            self.model.save_image(file_path)

    def upload_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            asyncio.run(self.process_file(file_path))

    async def process_file(self, file_path):
        async with aiofiles.open(file_path, 'r') as file:
            tasks = []
            async for line in file:
                color_code = line.strip()
                if color_code:
                    task = asyncio.create_task(self.create_and_save_image(color_code))
                    tasks.append(task)
            await asyncio.gather(*tasks)
            messagebox.showinfo("Processing Complete", "All images have been saved to the desktop.")

    async def create_and_save_image(self, color_code):
        await asyncio.to_thread(self.model.fill_color, color_code)
        file_name = f"{color_code.strip('#')}.png"
        file_path = f"{file_name}"
        await asyncio.to_thread(self.model.save_image, file_path)

class ImageModel:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.image = Image.new('RGB', (width, height), 'white')

    def get_image(self):
        return self.image

    def fill_color(self, color):
        self.image = Image.new('RGB', (self.width, self.height), color)

    def save_image(self, file_path):
        try:
            self.image.save(file_path)
        except IOError:
            messagebox.showerror("Save Image", f"Could not save the image {file_path}.")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()

