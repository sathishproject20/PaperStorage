import os
import json
import requests
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk

# Constants to specify JSON file location
LOCAL = 'local'
REMOTE = 'remote'
JSON_FILE_LOCATION = REMOTE  # Change to REMOTE if fetching from a URL
JSON_FILE_PATH = "http://127.0.0.1:8000/image_mapping.json"  # Local file path or remote URL

class ImageDisplayApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Image Display App")

        self.label = tk.Label(self, text="Enter color codes separated by commas:")
        self.label.pack(pady=10)

        self.entry = tk.Entry(self, width=50)
        self.entry.pack(pady=5)

        self.display_button = tk.Button(self, text="Display Images", command=self.display_images)
        self.display_button.pack(pady=10)

        self.image_frame = tk.Frame(self)
        self.image_frame.pack(pady=20)

        self.image_mapping = self.load_image_mapping()

    def load_image_mapping(self):
        if JSON_FILE_LOCATION == LOCAL:
            # Load image mappings from a local JSON file
            with open(JSON_FILE_PATH, "r") as file:
                return json.load(file)
        elif JSON_FILE_LOCATION == REMOTE:
            try:
                # Load image mappings from a remote JSON file
                response = requests.get(JSON_FILE_PATH)
                response.raise_for_status()  # Raise an exception for HTTP errors
                return response.json()
            except requests.exceptions.RequestException as e:
                print(f"Error fetching JSON from {JSON_FILE_PATH}: {e}")
                return {}
        else:
            raise ValueError("Invalid JSON_FILE_LOCATION value")

    def fetch_image_from_api(self, code):
        api_url = f"http://127.0.0.1:8000/api/images/{code}"
        response = requests.get(api_url)
        if response.status_code == 200:
            return response.json().get("image_url")
        return None

    def display_images(self):
        # Clear the previous images
        for widget in self.image_frame.winfo_children():
            widget.destroy()

        # Get the input codes and split by comma
        codes = self.entry.get().split(',')

        for code in codes:
            code = code.strip()  # Remove any extra whitespace
            image_path = self.image_mapping.get(code)

            if not image_path:
                # Try to fetch the image URL from the API
                image_path = self.fetch_image_from_api(code)

            if image_path:
                try:
                    img = Image.open(image_path)
                except Exception as e:
                    print(f"Error loading image for code {code}: {e}")
                    continue
                img = img.resize((50, 50))  # Adjust size as needed
                photo = ImageTk.PhotoImage(img)

                # Create a label to display the image
                image_label = tk.Label(self.image_frame, image=photo)
                image_label.image = photo  # Keep a reference to avoid garbage collection
                image_label.pack(side=tk.LEFT, padx=5)
            else:
                print(f"Code {code} not found.")

if __name__ == "__main__":
    app = ImageDisplayApp()
    app.mainloop()
