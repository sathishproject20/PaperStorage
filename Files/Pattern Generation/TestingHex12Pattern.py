import tkinter as tk
import logging

# Mocked data similar to what draw_pattern() uses
HexOnePxPosition = {
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

HexTwoPxPosition = {
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

RowIndex = {i: i * 16 for i in range(16)}
ColumnIndex = {i: i * 16 for i in range(16)}

HexOneColorIndex = {'0': '#7CB9E8', '1': '#00FA9A', '2': '#87CEFA', '3': '#F0F8FF', '4': '#00FFFF', '5': '#7FFFD4',
                    '6': '#0000CD', '7': '#9370DB', '8': '#90EE90', '9': '#ADFF2F', 'A': '#FF8C00', 'B': '#008000',
                    'C': '#0000CD', 'D': '#9370DB', 'E': '#90EE90', 'F': '#ADFF2F', 'W': '#FFFFFF',
                    }

HexTwoColorIndex = {'0': '#EE82EE', '1': '#4B0082', '2': '#0000FF', '3': '#008000', '4': '#FFFF00', '5': '#FFA500',
                    '6': '#FF0000', '7': '#008000', '8': '#0000FF', '9': '#00FFFF', 'A': '#800080', 'B': '#FFFF00',
                    'C': '#FF0000', 'D': '#008000', 'E': '#0000FF', 'F': '#00FFFF', 'W': '#FFFFFF',
                    }
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Canvas Test App")

        self.canvas = tk.Canvas(self, width=256, height=256)
        self.canvas.pack()

    def draw_pattern(self):
        self.canvas.delete("all")  # Clear the canvas before drawing
        for (row, col), color in HexOnePxPosition.items():
            if color in HexOneColorIndex:
                x = ColumnIndex[col]
                y = RowIndex[row]
                self.canvas.create_rectangle(x, y, x + 16, y + 16, fill=HexOneColorIndex[color], outline='')
            else:
                logging.warning(f"Color '{color}' not found in HexOneColorIndex.")

        for (row, col), color in HexTwoPxPosition.items():
            if color in HexTwoColorIndex:
                x = ColumnIndex[col]
                y = RowIndex[row]
                self.canvas.create_rectangle(x, y, x + 16, y + 16, fill=HexTwoColorIndex[color], outline='')
            else:
                logging.warning(f"Color '{color}' not found in HexTwoColorIndex.")



# Create the application instance
app = App()

# Call draw_pattern to draw on the canvas
app.draw_pattern()

# Start the main event loop
app.mainloop()
