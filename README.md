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