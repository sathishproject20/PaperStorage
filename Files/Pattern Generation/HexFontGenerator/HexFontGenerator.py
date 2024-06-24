import tkinter as tk
from tkinter import Canvas, filedialog, messagebox
import os
import asyncio
import logging
from PIL import Image

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Constants to store paths
FilePath = None
OutputFolder = None

# Initialize arrays
HexString = []
MapIndex = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]

# Initialize ImageMap with 16 rows of 16 elements
ImageMap = [[0] * 16 for _ in range(16)]

# Column index array for mapping hex characters to image positions
ColumnIndexArray = [
    [3, 4],
    [5, 6],
    [7, 8],
    [9, 10],
    [11, 12],
    [13, 14]
]

def validate_hex(P):
    # Allow empty string
    if P == "":
        return True
    # Check if the input string is a valid hex and within 6 characters
    if all(c in "0123456789abcdefABCDEF" for c in P) and len(P) <= 6:
        return True
    return False

# Default image setup
def defaultImage():
    global ImageMap
    ImageMap = [[0] * 16 for _ in range(16)]
    drawImageMap()

# Update ImageMap based on HexString
def updateImageMap():
    global ImageMap, HexString
    ImageMap = [[0] * 16 for _ in range(16)]

    truncatedHex = HexString[:6]

    for i in range(len(truncatedHex)):
        hexValue = truncatedHex[i]
        mapIndex = MapIndex[int(hexValue, 16)]

        columnIndex1, columnIndex2 = ColumnIndexArray[i]

        if mapIndex <= 16:
            ImageMap[mapIndex - 1][columnIndex1 - 1] = 1
            ImageMap[mapIndex - 1][columnIndex2 - 1] = 1

    drawImageMap()

# Draw ImageMap on Canvas
def drawImageMap():
    canvas.delete("all")

    pixelWidth = 16
    pixelHeight = 16
    xOffset = (canvas.winfo_width() - pixelWidth * 16) / 2
    yOffset = (canvas.winfo_height() - pixelHeight * 16) / 2

    for i in range(len(ImageMap)):
        for j in range(len(ImageMap[i])):
            color = '#000' if ImageMap[i][j] == 1 else '#fff'
            canvas.create_rectangle(
                xOffset + j * pixelWidth,
                yOffset + i * pixelHeight,
                xOffset + (j + 1) * pixelWidth,
                yOffset + (i + 1) * pixelHeight,
                fill=color,
                outline=color
            )

def generateImage():
    hexInput = hexEntry.get().strip().upper()
    if len(hexInput) == 0 or len(hexInput) > 6:
        messagebox.showerror("Error", "Please enter a valid hex string (1 to 6 characters).")
        return
    global HexString
    HexString = list(hexInput)
    updateImageMap()

def saveCanvasAsImage(filename, filetype):
    ps_filename = filename + ".ps"
    canvas.postscript(file=ps_filename, colormode='color')

    # Open the PostScript file and convert it to the desired image format
    image = Image.open(ps_filename)

    if filetype == 'png':
        image.save(f"{filename}.png")
    elif filetype == 'jpeg':
        image.save(f"{filename}.jpeg")

    # Optionally, delete the intermediate PostScript file
    os.remove(ps_filename)

    logging.info(f"Saved image: {filename}.{filetype}")

def downloadPng():
    if len(HexString) == 0:
        messagebox.showerror("Error", "Please generate an image first.")
        return
    saveCanvasAsImage('hex_image', 'png')
    messagebox.showinfo("Success", "PNG image saved as hex_image.png")

def downloadJpeg():
    if len(HexString) == 0:
        messagebox.showerror("Error", "Please generate an image first.")
        return
    saveCanvasAsImage('hex_image', 'jpeg')
    messagebox.showinfo("Success", "JPEG image saved as hex_image.jpeg")

async def handleFileUpload():
    global FilePath
    FilePath = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if not FilePath:
        return
    filePathLabel.config(text=f"File Path: {FilePath}", wraplength=180)

def setOutputFolder():
    global OutputFolder
    OutputFolder = outputEntry.get().strip()
    if not OutputFolder:
        messagebox.showerror("Error", "Please enter a valid output folder path.")
        return
    messagebox.showinfo("Success", "Output folder set successfully!")

async def generateMultipleImages():
    if not FilePath or not OutputFolder:
        messagebox.showerror("Error", "Please specify both the file path and output folder.")
        return

    try:
        with open(FilePath, 'r') as file:
            lines = file.readlines()
            tasks = [process_and_save_hex_string(line.strip().upper(), OutputFolder) for line in lines if len(line.strip()) == 6]
            await asyncio.gather(*tasks)
        messagebox.showinfo("Success", "All images generated successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Error generating images: {e}")

async def process_and_save_hex_string(hexString, output_folder):
    global HexString
    HexString = list(hexString)
    updateImageMap()
    
    # Redraw canvas to reflect the updated ImageMap
    drawImageMap()
    
    # Save canvas as image
    saveCanvasAsImage(os.path.join(output_folder, hexString), 'png')

# Function to create the context menu
def create_context_menu(entry_widget):
    context_menu = tk.Menu(entry_widget, tearoff=0)
    context_menu.add_command(label="Cut", command=lambda: entry_widget.event_generate("<<Cut>>"))
    context_menu.add_command(label="Copy", command=lambda: entry_widget.event_generate("<<Copy>>"))
    context_menu.add_command(label="Paste", command=lambda: entry_widget.event_generate("<<Paste>>"))
    
    def show_context_menu(event):
        context_menu.tk_popup(event.x_root, event.y_root)
        
    entry_widget.bind("<Button-3>", show_context_menu)

# Function to handle Cut, Copy, and Paste keyboard shortcuts
def bind_entry_shortcuts(entry_widget):
    entry_widget.bind("<Control-x>", lambda event: entry_widget.event_generate("<<Cut>>"))
    entry_widget.bind("<Control-c>", lambda event: entry_widget.event_generate("<<Copy>>"))
    entry_widget.bind("<Control-v>", lambda event: entry_widget.event_generate("<<Paste>>"))

# Set up the Tkinter window
root = tk.Tk()
root.title("Hex Pattern Generator")
root.geometry("800x800")

header = tk.Frame(root, bg='#0000FF', height=50)
header.pack(side='top', fill='x')
header_label = tk.Label(header, text="Hex Pattern Generator", bg='#0000FF', fg='White', font=('Arial', 40, 'bold'), anchor='w')
header_label.pack(pady=10, fill='x')

side_view = tk.Frame(root, bg='lightgrey', width=200, height=600)
side_view.pack(side='left', fill='y')
side_view.pack_propagate(False)  # Prevent side view from resizing

main_view = tk.Frame(root, bg='white', width=600, height=600)
main_view.pack(side='right', expand=True, fill='both')

canvas = tk.Canvas(main_view, width=256, height=256, bg='white')
canvas.place(relx=0.5, y=50, anchor='n')

hexLabel = tk.Label(side_view, text="Enter Hex String:", bg='lightgrey')
hexLabel.pack(pady=5)

# Validation setup for the Entry widget
vcmd = (root.register(validate_hex), '%P')

# Hex entry
hexEntry = tk.Entry(side_view, validate='key', validatecommand=vcmd)
hexEntry.pack(pady=5)

# Bind context menu and keyboard shortcuts
create_context_menu(hexEntry)
bind_entry_shortcuts(hexEntry)

generateButton = tk.Button(side_view, text="Generate Image", command=generateImage)
generateButton.pack(pady=5)

uploadLabel = tk.Label(side_view, text="Upload Hex File:", bg='white')
uploadLabel.pack(pady=5)

uploadButton = tk.Button(side_view, text="Upload File", command=lambda: asyncio.run(handleFileUpload()))
uploadButton.pack(pady=5)

filePathLabel = tk.Label(side_view, text="File Path: ", bg='white', wraplength=190, justify='left')
filePathLabel.pack(pady=5)

outputLabel = tk.Label(side_view, text="Output Folder:", bg='white')
outputLabel.pack(pady=5)

outputEntry = tk.Entry(side_view)
outputEntry.pack(pady=5)

# Bind context menu and keyboard shortcuts
create_context_menu(outputEntry)
bind_entry_shortcuts(outputEntry)

saveOutputButton = tk.Button(side_view, text="Save", command=setOutputFolder)
saveOutputButton.pack(pady=5)

generateMultipleButton = tk.Button(side_view, text="Generate Multiple Images", command=lambda: asyncio.run(generateMultipleImages()))
generateMultipleButton.pack(pady=5)

downloadPngButton = tk.Button(main_view, text="Download as PNG", command=downloadPng)
downloadPngButton.place(relx=0.35, rely=0.8, anchor='center')

downloadJpegButton = tk.Button(main_view, text="Download as JPEG", command=downloadJpeg)
downloadJpegButton.place(relx=0.65, rely=0.8, anchor='center')

defaultImage()

root.mainloop()
