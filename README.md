# How to Run Block Blast Buddy
## Prerequisites
- Python 3.8+
- Uses only the Python standard library
## Run
From the project directory:
```bash
python main.py
```
Make sure `main.py`, `grid.py`, and `solve.py` are all in the same folder so imports work correctly.

# How to Use Block Blast Buddy
Follow these steps once the GUI opens:
## 1. Set Up the Main Grid
- Use your mouse to recreate your current Block Blast board.
- Left-click to select a block space (blue).
- Right-click to deselect a block space (gray).
## 2. Define Your Pieces
For each piece:
- Enter the number of rows and columns needed to create the piece.
- Click "Submit."
    - A grid should appear to represent a canvas to recreate the piece, similar to the main grid.
-  Left-click to mark which cells contain blocks (blue).
-  Right-click to unmark the block (gray).
## 3. Generate the Solution
- Click "Generate moves" at the bottom of the GUI.
    - A new window should appear to show the solved board with the steps to reach the solution.
### Key
- Red blocks represent the pieces the solution has placed.
- Purple blocks represent a row/column cleared.
- Blue blocks represent remaining blocks in the board.
- Gray blocks represent empty spaces on the board.
## Alt. If No Solution Exists
- A new window should appear to show a "Game Over" screen, meaning no valid solution was found.

# Files
## main.py
### Purpose
- Controls the graphical user interface (GUI) using Tkinter.
- Handles all user input including grid/piece editing and submission.
- Passes all grid/piece data to `solve.py`.
- Displays solved grid and solution steps to user.
- Depends on:
    - `grid.py` for grid initialization and rendering
    - `solve.py` for AI logic
## solve.py
### Purpose
- Implements A* search algorithm using an evaluation function.
- Searches for the best placement, and order of placement, of pieces.
## grid.py
### Purpose
- Defines the GridBlock class for rendering individual blocks on a Tkinter canvas.

# Dependencies
- `tkinter` for GUI
- `heapq` for priority queue
