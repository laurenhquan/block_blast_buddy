# main.py
# controls program

import tkinter as tk
from grid import *

# screen size
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# grid dimensions
GRID_ROWS = 8
GRID_COLS = 8

# block size
BLOCK_SIZE = 45
# BLOCK_GAP = 1

# grid size
GRID_WIDTH = GRID_COLS * BLOCK_SIZE
GRID_HEIGHT = GRID_ROWS * BLOCK_SIZE

# number of pieces
PIECE_NUM = 3

class Game:
    def __init__(self, root):
        # initialize window
        self.root = root
        self.root.title("Block Blast Buddy")

        # MARK: GRID ----------------------------------------------------------------------------------------
        # initialize grid frame
        grid_frame = tk.Frame(self.root)
        grid_frame.pack(expand=True)

        # label grid
        grid_label = tk.Label(grid_frame, text="Your Grid")
        grid_label.pack()

        # load grid canvas
        self.grid_canvas = tk.Canvas(grid_frame, width=GRID_WIDTH, height=GRID_HEIGHT, bg="white")
        self.grid_canvas.pack()

        # load grid
        self.grid_data = [[0 for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]
        self.grid_blocks = []
        self.create_grid()

        # bind mouse controls
        self.grid_canvas.bind("<Button-1>", lambda event: self.left_click(event, self.grid_data, self.grid_blocks, GRID_ROWS, GRID_COLS))
        self.grid_canvas.bind("<Button-3>", lambda event: self.right_click(event, self.grid_data, self.grid_blocks, GRID_ROWS, GRID_COLS))
        # ---------------------------------------------------------------------------------------------------

        # MARK: PIECES --------------------------------------------------------------------------------------
        # initiliaze piece frame
        piece_frame = tk.Frame(self.root)
        piece_frame.pack(expand=True)

        # label pieces
        piece_label = tk.Label(piece_frame, text="Your Pieces")
        piece_label.pack()

        # load pieces
        for i in range(PIECE_NUM):
            self.load_pieces(i)
        # ---------------------------------------------------------------------------------------------------

    def create_grid(self):
        for row in range(GRID_ROWS):
            row_list = []

            for col in range(GRID_COLS):
                x = col * (BLOCK_SIZE)
                y = row * (BLOCK_SIZE)
                block = GridBlock(self.grid_canvas, x, y, BLOCK_SIZE)
                row_list.append(block)

            self.grid_blocks.append(row_list)

    def load_pieces(self, piece_number):
        # initialize piece 3 frame
        piece_frame = tk.Frame(self.root)
        piece_frame.pack(side="left")

        # declare piece 3 rows, cols
        piece_rows_var = tk.IntVar()
        piece_cols_var = tk.IntVar()

        # label piece 3
        piece_label = tk.Label(piece_frame, text=f"Piece #{piece_number+1}")
        piece_label.grid(row=0, column=0, columnspan=5)

        # label piece 3 rows
        piece_rows_label = tk.Label(piece_frame, text="Rows:")
        piece_rows_label.grid(row=1, column=0)

        # get piece 3 rows
        piece_rows = tk.Entry(piece_frame, textvariable=piece_rows_var)
        piece_rows.grid(row=1, column=1)

        # label piece 3 cols
        piece_cols_label = tk.Label(piece_frame, text="Columns:")
        piece_cols_label.grid(row=1, column=2)

        # get piece 3 cols
        piece_cols = tk.Entry(piece_frame, textvariable=piece_cols_var)
        piece_cols.grid(row=1, column=3)

        # submit piece 3 rows, cols
        piece_submit = tk.Button(piece_frame, text="Submit", command=lambda: self.create_piece(piece_canvas, piece_blocks, piece_rows_var.get(), piece_cols_var.get()))
        piece_submit.grid(row=1, column=4)

        # load piece 3 canvas
        piece_canvas = tk.Canvas(piece_frame, width=(piece_rows_var.get() * BLOCK_SIZE), height=(piece_cols_var.get() * BLOCK_SIZE), bg="white")
        piece_canvas.grid(row=4, column=0, columnspan=5)

        # load piece 3
        piece_data = [[0 for _ in range(piece_cols_var.get())] for _ in range(piece_rows_var.get())]
        piece_blocks = []

        # bind mouse controls
        piece_canvas.bind("<Button-1>", lambda event: self.left_click(event, piece_data, piece_blocks, piece_rows_var.get(), piece_cols_var.get()))
        piece_canvas.bind("<Button-3>", lambda event: self.right_click(event, piece_data, piece_blocks, piece_rows_var.get(), piece_cols_var.get()))
    
    def create_piece(self, canvas, blocks, rows, cols):
        canvas.config(width=cols*BLOCK_SIZE, height=rows*BLOCK_SIZE)
        blocks.clear()

        for row in range(rows):
            row_list = []

            for col in range(cols):
                x = col * (BLOCK_SIZE)
                y = row * (BLOCK_SIZE)
                block = GridBlock(canvas, x, y, BLOCK_SIZE)
                row_list.append(block)

            blocks.append(row_list)

    # select block
    def left_click(self, event, data, blocks, rows, cols):
        self.handle_click(data, blocks, rows, cols, event.x, event.y, fill_color="blue", set_value=1)
    
    # deselect block
    def right_click(self, event, data, blocks, rows, cols):
        self.handle_click(data, blocks, rows, cols, event.x, event.y, fill_color="gray", set_value=0)

    def handle_click(self, data, blocks, rows, cols, x, y, fill_color, set_value):
        for row in range(rows):
            for col in range(cols):
                block = blocks[row][col]

                if block.isWithinBounds(x,y):
                    block.set_color(fill_color)
                    data[row][col] = set_value # 1=occupied, 0=vacant
                    return

if __name__ == "__main__":
    root = tk.Tk()
    game = Game(root)
    root.mainloop()