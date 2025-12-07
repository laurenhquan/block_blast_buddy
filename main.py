# main.py
# controls program

import tkinter as tk
from grid import GridBlock
from solve import astar_solve

# screen size
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# grid dimensions
GRID_ROWS = 8
GRID_COLS = 8

# block size
BLOCK_SIZE = 45

# grid size
GRID_WIDTH = GRID_COLS * BLOCK_SIZE
GRID_HEIGHT = GRID_ROWS * BLOCK_SIZE

# number of pieces
PIECE_NUM = 3

class Buddy:
    # MARK: INPUT -------------------------------------------------------------------------------------------
    def __init__(self, root):
        # initialize window
        self.root = root
        self.root.title("Block Blast Buddy")

        # MARK: GRID ----------------------------------------------------------------------------------------
        # initialize grid frame
        grid_frame = tk.Frame(self.root)
        grid_frame.pack(expand=True)

        # label grid
        grid_label = tk.Label(grid_frame, text="Your Grid", font=("Helvetica", 12, "bold", "underline"))
        grid_label.pack()

        # load grid canvas
        grid_canvas = tk.Canvas(grid_frame, width=GRID_WIDTH, height=GRID_HEIGHT, bg="white")
        grid_canvas.pack()

        # load grid
        self.grid_data = [[0 for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]
        grid_blocks = self.create_grid(grid_canvas, self.grid_data)

        # bind mouse controls
        grid_canvas.bind("<Button-1>", lambda event: self.left_click(event, self.grid_data, grid_blocks, GRID_ROWS, GRID_COLS))
        grid_canvas.bind("<Button-3>", lambda event: self.right_click(event, self.grid_data, grid_blocks, GRID_ROWS, GRID_COLS))
        # ---------------------------------------------------------------------------------------------------

        # MARK: PIECES --------------------------------------------------------------------------------------
        # initiliaze piece frame
        pieces_frame = tk.Frame(self.root)
        pieces_frame.pack(expand=True)

        # label pieces
        piece_label = tk.Label(pieces_frame, text="Your Pieces", font=("Helvetica", 12, "bold", "underline"))
        piece_label.pack()

        # declare empty list for pieces
        self.pieces_data = {}

        # load pieces
        for i in range(PIECE_NUM):
            self.load_pieces(i, pieces_frame)
        # ---------------------------------------------------------------------------------------------------

        # MARK: SUBMISSION ----------------------------------------------------------------------------------
        # initialize submit frame
        submit_frame = tk.Frame(self.root)
        submit_frame.pack(expand=True)

        # provide submit button
        submit_btn = tk.Button(submit_frame, text="Generate moves", command=self.generate_solution)
        submit_btn.pack()
        # ---------------------------------------------------------------------------------------------------

    def create_grid(self, canvas, data):
        blocks = []

        for row in range(GRID_ROWS):
            row_list = []

            for col in range(GRID_COLS):
                x = col * (BLOCK_SIZE)
                y = row * (BLOCK_SIZE)
                block = GridBlock(canvas, x, y, BLOCK_SIZE)
                row_list.append(block)

                value = data[row][col]
                if value == 0:
                    block.set_color("gray")
                elif value == 1:
                    block.set_color("blue")
                elif value == 2:
                    block.set_color("red")
                elif value == -1:
                    block.set_color("purple")

            blocks.append(row_list)

            # draw column labels
            for col in range(GRID_COLS):
                x = col * BLOCK_SIZE + BLOCK_SIZE / 2
                y = 10
                canvas.create_text(x, y, text=str(col+1))

            # draw row labels
            for row in range(GRID_ROWS):
                x = 10
                y = row * BLOCK_SIZE + BLOCK_SIZE / 2
                canvas.create_text(x, y, text=str(row+1))


        return blocks

    def load_pieces(self, piece_number, parent_frame):
        # initialize piece frame
        piece_frame = tk.Frame(parent_frame)
        piece_frame.pack(side="left")

        # declare piece rows, cols
        piece_rows_var = tk.IntVar()
        piece_cols_var = tk.IntVar()

        # label piece
        piece_label = tk.Label(piece_frame, text=f"Piece #{piece_number+1}")
        piece_label.grid(row=0, column=0, columnspan=5)

        # label piece rows
        piece_rows_label = tk.Label(piece_frame, text="Rows:")
        piece_rows_label.grid(row=1, column=0)

        # get piece rows
        piece_rows = tk.Entry(piece_frame, textvariable=piece_rows_var)
        piece_rows.grid(row=1, column=1)

        # label piece cols
        piece_cols_label = tk.Label(piece_frame, text="Columns:")
        piece_cols_label.grid(row=1, column=2)

        # get piece cols
        piece_cols = tk.Entry(piece_frame, textvariable=piece_cols_var)
        piece_cols.grid(row=1, column=3)

        # submit piece rows, cols
        piece_submit = tk.Button(piece_frame, text="Submit", command=lambda: self.create_piece(piece_canvas, piece_blocks, piece_rows_var.get(), piece_cols_var.get(), piece_number))
        piece_submit.grid(row=1, column=4)

        # load piece canvas
        piece_canvas = tk.Canvas(piece_frame, width=(piece_rows_var.get() * BLOCK_SIZE), height=(piece_cols_var.get() * BLOCK_SIZE), bg="white")
        piece_canvas.grid(row=4, column=0, columnspan=5)

        # initialize block list
        piece_blocks = []
    
    def create_piece(self, canvas, blocks, rows, cols, piece_number):
        # ignore invalid inputs
        if rows <= 0 or cols <= 0:
            return

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

        piece_data = [[0 for _ in range(cols)] for _ in range(rows)]

        # store piece
        self.pieces_data[piece_number] = piece_data

        # bind mouse controls
        canvas.bind("<Button-1>", lambda event: self.left_click(event, piece_data, blocks, rows, cols))
        canvas.bind("<Button-3>", lambda event: self.right_click(event, piece_data, blocks, rows, cols))

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
                    data[row][col] = set_value # 1=occupied, 0=vacant, 2=placed
                    return
    # -------------------------------------------------------------------------------------------------------
    
    # MARK: SOLUTION ----------------------------------------------------------------------------------------
    def generate_solution(self):
        solution_window = tk.Toplevel(self.root)
        solution_window.title("Block Blast Buddy: Solved")

        # grab solution from solve.py
        self.solution = astar_solve(self.grid_data, self.pieces_data)

        # MARK: GAME OVER -----------------------------------------------------------------------------------
        if self.solution is None:
            solution_window.title("Block Blast Buddy: UNSolved")
            game_over_label = tk.Label(solution_window, text="GAME OVER!\nNo solution was found.", font=("Helvetica", 12, "bold", "underline"), fg="red")
            game_over_label.pack()
            return
        # ---------------------------------------------------------------------------------------------------

        # MARK: SOLVED GRID ---------------------------------------------------------------------------------
        # initialize solution grid frame
        solution_grid_frame = tk.Frame(solution_window)
        solution_grid_frame.pack(side="left", expand=True)

        # label solution grid
        solution_grid_label = tk.Label(solution_grid_frame, text="Your Solution", font=("Helvetica", 12, "bold", "underline"))
        solution_grid_label.pack()

        # load solution grid canvas
        solution_grid_canvas = tk.Canvas(solution_grid_frame, width=GRID_WIDTH, height=GRID_HEIGHT, bg="white")
        solution_grid_canvas.pack()

        # load solution grid
        solution_grid_data = self.solution['grid']
        self.create_grid(solution_grid_canvas, solution_grid_data)
        # ---------------------------------------------------------------------------------------------------

        # MARK: SOLVED STEPS --------------------------------------------------------------------------------
        # initialize solution steps frame
        solution_steps_frame = tk.Frame(solution_window)
        solution_steps_frame.pack(side="right", expand=True)

        # label solution steps
        solution_steps_label = tk.Label(solution_steps_frame, text="Your Steps", font=("Helvetica", 12, "bold", "underline"))
        solution_steps_label.pack()

        # load solution steps text
        solution_steps = tk.Text(solution_steps_frame, bg="white", wrap=tk.WORD)

        # load solution steps
        solution_steps.insert(tk.END, self.insert_solution_steps())
        solution_steps.config(state=tk.DISABLED)
        solution_steps.pack()
        # ---------------------------------------------------------------------------------------------------

    def insert_solution_steps(self):
        steps = ""

        solution_moves = self.solution['moves']
        for i, (piece_index, y, x) in enumerate(solution_moves):
            steps += f"Step {i+1}: Place Piece #{piece_index+1} at row {y+1}, column {x+1}.\n"

        return steps
    # -------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    root = tk.Tk()
    buddy = Buddy(root)
    root.mainloop()