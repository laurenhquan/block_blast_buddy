# main.py
# controls of program

import tkinter as tk
from grid import GridBlock

# screen size
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# grid size
GRID_ROWS = 8
GRID_COLS = 8

# block size
BLOCK_SIZE = 45
# BLOCK_GAP = 1

class Game:
    def __init__(self, root):
        # initialize window
        self.root = root
        self.root.title("Block Blast Buddy")

        # load canvas
        self.canvas = tk.Canvas(root, width=SCREEN_WIDTH, height=SCREEN_HEIGHT, bg="white")
        self.canvas.pack()

        # load grid
        self.grid_data = [[0 for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]
        self.blocks = []
        self.create_grid()

        # mouse controls
        self.canvas.bind("<Button-1>", self.left_click)
        self.canvas.bind("<Button-3>", self.right_click)

    def create_grid(self):
        for row in range(GRID_ROWS):
            row_list = []

            for col in range(GRID_COLS):
                x = col * (BLOCK_SIZE)
                y = row * (BLOCK_SIZE)
                block = GridBlock(self.canvas, x, y, BLOCK_SIZE)
                row_list.append(block)

            self.blocks.append(row_list)

    # select block
    def left_click(self, event):
        self.handle_click(event.x, event.y, fill_color="blue", set_value=1)
    
    # deselect block
    def right_click(self, event):
        self.handle_click(event.x, event.y, fill_color="gray", set_value=0)

    def handle_click(self, x, y, fill_color, set_value):
        for row in range(GRID_ROWS):
            for col in range(GRID_COLS):
                block = self.blocks[row][col]

                if block.isWithinBounds(x,y):
                    block.set_color(fill_color)
                    self.grid_data[row][col] = set_value # 1=occupied, 0=vacant
                    return

if __name__ == "__main__":
    root = tk.Tk()
    game = Game(root)
    root.mainloop()