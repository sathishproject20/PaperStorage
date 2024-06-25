import tkinter as tk
from tkinter import Canvas, filedialog, messagebox
import os
import asyncio
import logging
from PIL import Image

# Example input string of 12 ASCII characters.
Hex12String = "0123456789AB"

# Array containing hexadecimal digits [0-9, A-F].
HexValues = [str(i) for i in range(10)] + ['A', 'B', 'C', 'D', 'E', 'F']

# Mapping of rows and columns on the canvas.
RowIndex = {i: i * 16 for i in range(16)}
ColumnIndex = {i: i * 16 for i in range(16)}

def validate_hex(P):
    # Allow empty string
    if P == "":
        return True
    # Check if the input string is a valid hex and within 12 characters
    if all(c in "0123456789abcdefABCDEF" for c in P) and len(P) <= 12:
        return True
    return False

# Define color mappings for HexOne and HexTwo
HexOneColorIndex = {'0': '#7CB9E8', '1': '#00FA9A', '2': '#87CEFA', '3': '#F0F8FF', '4': '#00FFFF', '5': '#7FFFD4',
                    '6': '#0000CD', '7': '#9370DB', '8': '#90EE90', '9': '#ADFF2F', 'A': '#FF8C00', 'B': '#008000',
                    'C': '#0000CD', 'D': '#9370DB', 'E': '#90EE90', 'F': '#ADFF2F', 'W': '#FFFFFF',
                    }

HexTwoColorIndex = {'0': '#EE82EE', '1': '#4B0082', '2': '#0000FF', '3': '#008000', '4': '#FFFF00', '5': '#FFA500',
                    '6': '#FF0000', '7': '#008000', '8': '#0000FF', '9': '#00FFFF', 'A': '#800080', 'B': '#FFFF00',
                    'C': '#FF0000', 'D': '#008000', 'E': '#0000FF', 'F': '#00FFFF', 'W': '#FFFFFF',
                    }


class DrawPattern:
    def __init__(self, canvas):
        self.canvas = canvas
        self.HexOnePxPosition = {
            (2, 2): '0', (2, 3): '0', (2, 4): '1', (2, 5): '1', (2, 6): '2', (2, 7): '2',
            (3, 2): '0', (3, 3): '0', (3, 4): '1', (3, 5): '1', (3, 6): '2', (3, 7): '2',
            (4, 2): '3', (4, 3): '3', (4, 4): '4', (4, 5): '4', (4, 6): '5', (4, 7): '5',
            (5, 2): '3', (5, 3): '3', (5, 4): '4', (5, 5): '4', (5, 6): '5', (5, 7): '5',
            (6, 2): '6', (6, 3): '6', (6, 4): '7', (6, 5): '7', (6, 6): '8', (6, 7): '8',
            (7, 2): '6', (7, 3): '6', (7, 4): '7', (7, 5): '7', (7, 6): '8', (7, 7): '8',
            (8, 2): '9', (8, 3): '9', (8, 4): 'A', (8, 5): 'A', (8, 6): 'B', (8, 7): 'B',
            (9, 2): '9', (9, 3): '9', (9, 4): 'A', (9, 5): 'A', (9, 6): 'B', (9, 7): 'B',
            (10, 2): 'C', (10, 3): 'C', (10, 4): 'D', (10, 5): 'D', (10, 6): 'E', (10, 7): 'E',
            (11, 2): 'C', (11, 3): 'C', (11, 4): 'D', (11, 5): 'D', (11, 6): 'E', (11, 7): 'E',
            (12, 2): 'F', (12, 3): 'F', (12, 4): 'W', (12, 5): 'W', (12, 6): 'W', (12, 7): 'W',
            (13, 2): 'F', (13, 3): 'F', (13, 4): 'W', (13, 5): 'W', (13, 6): 'W', (13, 7): 'W',
        }
        self.HexTwoPxPosition = {
            (2, 8): '0', (2, 9): '0', (2, 10): '1', (2, 11): '1', (2, 12): '2', (2, 13): '2',
            (3, 8): '0', (3, 9): '0', (3, 10): '1', (3, 11): '1', (3, 12): '2', (3, 13): '2',
            (4, 8): '3', (4, 9): '3', (4, 10): '4', (4, 11): '4', (4, 12): '5', (4, 13): '5',
            (5, 8): '3', (5, 9): '3', (5, 10): '4', (5, 11): '4', (5, 12): '5', (5, 13): '5',
            (6, 8): '6', (6, 9): '6', (6, 10): '7', (6, 11): '7', (6, 12): '8', (6, 13): '8',
            (7, 8): '6', (7, 9): '6', (7, 10): '7', (7, 11): '7', (7, 12): '8', (7, 13): '8',
            (8, 8): '9', (8, 9): '9', (8, 10): 'A', (8, 11): 'A', (8, 12): 'B', (8, 13): 'B',
            (9, 8): '9', (9, 9): '9', (9, 10): 'A', (9, 11): 'A', (9, 12): 'B', (9, 13): 'B',
            (10, 8): 'C', (10, 9): 'C', (10, 10): 'D', (10, 11): 'D', (10, 12): 'E', (10, 13): 'E',
            (11, 8): 'C', (11, 9): 'C', (11, 10): 'D', (11, 11): 'D', (11, 12): 'E', (11, 13): 'E',
            (12, 8): 'F', (12, 9): 'F', (12, 10): 'W', (12, 11): 'W', (12, 12): 'W', (12, 13): 'W',
            (13, 8): 'F', (13, 9): 'F', (13, 10): 'W', (13, 11): 'W', (13, 12): 'W', (13, 13): 'W',
        }

    def draw_pattern(self):
        self.canvas.delete("all")  # Clear the canvas before drawing
        for (row, col), color in self.HexOnePxPosition.items():
            if color in HexOneColorIndex:
                x = ColumnIndex[col]
                y = RowIndex[row]
                self.canvas.create_rectangle(x, y, x + 16, y + 16, fill=HexOneColorIndex[color], outline='')
            else:
                logging.warning(f"Color '{color}' not found in HexOneColorIndex.")

        for (row, col), color in self.HexTwoPxPosition.items():
            if color in HexTwoColorIndex:
                x = ColumnIndex[col]
                y = RowIndex[row]
                self.canvas.create_rectangle(x, y, x + 16, y + 16, fill=HexTwoColorIndex[color], outline='')
            else:
                logging.warning(f"Color '{color}' not found in HexTwoColorIndex.")

# Call draw_pattern to draw on the canvas
app = DrawPattern(Canvas)

# Function to update Hex12String and redraw canvas
def generateImage():
    global Hex12String
    hexInput = hexEntry.get().strip().upper()
    if not validate_hex(hexInput):
        messagebox.showerror("Error", "Please enter a valid hex string (1 to 12 characters).")
        return
    Hex12String = hexInput
    app.draw_pattern()
    canvas.update_idletasks()  # Update the canvas to reflect changes


# Function to handle file upload
async def handleFileUpload():
    global FilePath
    FilePath = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if not FilePath:
        return
    filePathLabel.config(text=f"File Path: {FilePath}", wraplength=180)

# Function to generate multiple images based on uploaded file
async def generateMultipleImages():
    if not FilePath or not os.path.isfile(FilePath):
        messagebox.showerror("Error", "Please specify a valid file path.")
        return
    try:
        with open(FilePath, 'r') as file:
            lines = file.readlines()
            for line in lines:
                hexString = line.strip().upper()
                if validate_hex(hexString):
                    global Hex12String
                    Hex12String = hexString
                    app.draw_pattern()
                    saveCanvasAsImage(hexString, 'png')
            messagebox.showinfo("Success", "All images generated successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Error generating images: {e}")

# Function to save canvas as image
def saveCanvasAsImage(filename, filetype):
    ps_filename = filename + ".ps"
    canvas.postscript(file=ps_filename, colormode='color')
    image = Image.open(ps_filename)
    if filetype == 'png':
        image.save(f"{filename}.png")
    elif filetype == 'jpeg':
        image.save(f"{filename}.jpeg")
    os.remove(ps_filename)
    logging.info(f"Saved image: {filename}.{filetype}")

# Initialize Tkinter
root = tk.Tk()
root.title("Hex 12 Pattern Generator")
root.geometry("800x800")

# Header
header = tk.Frame(root, bg='#0000FF', height=50)
header.pack(side='top', fill='x')
header_label = tk.Label(header, text="Hex 12 Pattern Generator", bg='#0000FF', fg='White', font=('Arial', 40, 'bold'), anchor='w')
header_label.pack(pady=10, fill='x')

# Side View
side_view = tk.Frame(root, bg='lightgrey', width=200, height=600)
side_view.pack(side='left', fill='y')
side_view.pack_propagate(False)

# Main View
main_view = tk.Frame(root, bg='white', width=600, height=600)
main_view.pack(side='right', expand=True, fill='both')

# Canvas Widget
canvas = tk.Canvas(root, width=256, height=256, bg='white')
canvas.pack()

# Label and Entry for Hex Input
hexLabel = tk.Label(side_view, text="Enter Hex String:", bg='lightgrey')
hexLabel.pack(pady=5)

hexEntry = tk.Entry(side_view, validate='key', validatecommand=(root.register(validate_hex), '%P'))
hexEntry.pack(pady=5)

# Generate Button
generateButton = tk.Button(side_view, text="Generate Image", command=generateImage)
generateButton.pack(pady=5)

# Upload File UI
uploadLabel = tk.Label(side_view, text="Upload Hex File:", bg='white')
uploadLabel.pack(pady=5)

uploadButton = tk.Button(side_view, text="Upload File", command=lambda: asyncio.run(handleFileUpload()))
uploadButton.pack(pady=5)

filePathLabel = tk.Label(side_view, text="File Path: ", bg='white', wraplength=190, justify='left')
filePathLabel.pack(pady=5)

# Button to Generate Multiple Images
generateMultipleButton = tk.Button(side_view, text="Generate Multiple Images", command=lambda: asyncio.run(generateMultipleImages()))
generateMultipleButton.pack(pady=5)

# Function to start Tkinter event loop
def start_gui():
    root.mainloop()

# Start GUI
start_gui()

# Call draw_pattern to draw on the canvas
app = DrawPattern(Canvas)
app.draw_pattern()

# Start the main event loop
root.mainloop()
