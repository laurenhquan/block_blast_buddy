

class BoardState:
    lines_cleared: int
    space_cleared: int   #diff placements could clear same amt of lines but free different amt of space
    holes_created: int   #don't want to create holes that can't be filled by other pieces
    fragmentation: int   #how many different regions of empty space exist
    is_full_clear: bool
    is_game_over: bool

#piece should be a 2d array of (x,y) offsets representing the shape
def does_piece_fit(grid, piece, pos):
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    base_y, base_x = pos

    for offset in piece:
        y_offset, x_offset = offset
        x = base_x + x_offset
        y = base_y + y_offset

        #check out of bounds
        if x < 0 or x >= cols or y < 0 or y >= rows:
            return False

        #check for overlap
        if grid[y][x] != 0:
            return False
        
    return True

#place piece on board and return updated board, along with lines/space cleared
def update_board(grid, piece, pos):
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    lines_cleared = 0
    rows_to_clear = []
    cols_to_clear = []
    space_cleared = 0
    base_y, base_x = pos
    new_grid = [row[:] for row in grid]  #make a copy to avoid mutating original

#place block
    for offset in piece:
        y_offset, x_offset = offset
        x = base_x + x_offset
        y = base_y + y_offset

        new_grid[y][x] = 2

#check for full rows/columns and clear them
#find full rows
    for r in range(rows):
        if all(new_grid[r][c] != 0 for c in range(cols)):
            rows_to_clear.append(r)
            lines_cleared += 1
#find full columns
    for c in range(cols):
        if all(new_grid[r][c] != 0 for r in range(rows)):
            cols_to_clear.append(c)
            lines_cleared += 1
#clear full rows
    for r in rows_to_clear:
        for c in range(cols):
            if new_grid[r][c] >= 0:
                space_cleared += 1
            new_grid[r][c] = -1
#clear full columns
    for c in cols_to_clear:
        for r in range(rows):
            if new_grid[r][c] >= 0:
                space_cleared += 1
            new_grid[r][c] = -1

    return (new_grid, lines_cleared, space_cleared)

#temp func to help testing
def clean_board(grid):
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    new_grid = [row[:] for row in grid]  #make a copy to avoid mutating original

    for r in range(rows):
        for c in range(cols):
            if new_grid[r][c] <= 0:
                new_grid[r][c] = 0
            if new_grid[r][c] > 0:
                new_grid[r][c] = 1

    return new_grid

#return first pos where a piece can fit, along with all pieces that can fit there
def search_move(start_at, grid, pieces):
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    init_y, init_x = start_at
    valid_moves = []

    if init_x >= cols:
        init_x = 0
        init_y += 1
    else:
        init_x +=1

    for y in range(init_y, rows):
        for x in range(init_x if y == init_y else 0, cols):
            if grid[y][x] == 0:
                print(f"\nChecking cell (r:{y}, c:{x}) = {grid[y][x]}")
                for piece in pieces:
                    print(f"  Trying piece: {piece}")
                    if does_piece_fit(grid, piece, (y, x)):
                        valid_moves.append(piece)
                        print(f"    Piece fits!")
                    else:
                        print(f"    Piece does not fit.")
                if len(valid_moves) > 0:
                    return (valid_moves, (y, x))
    return (None, (y, x))

#solve without AI evaluation
def dirty_solve(grid, pieces):
    best_solution = {
        'lines_cleared': 0,
        'space_cleared': 0,
        'grid': None,
        'moves': []
    }
    
    states_checked = [0]

    dirty_solve_recursive(grid, pieces, [], 0, 0, best_solution, states_checked)
    
    return (best_solution, states_checked[0])

def dirty_solve_recursive(grid, remaining_pieces, moves_so_far, total_lines, total_spaces, best_solution, states_checked):
    if len(remaining_pieces) == 0:
        # Check if this is better than current best
        if (total_lines > best_solution['lines_cleared'] or 
            (total_lines == best_solution['lines_cleared'] and 
             total_spaces > best_solution['space_cleared'])):
            best_solution['lines_cleared'] = total_lines
            best_solution['space_cleared'] = total_spaces
            best_solution['grid'] = [row[:] for row in grid]
            best_solution['moves'] = moves_so_far[:]
            print(f"New best! Lines: {total_lines}, Space: {total_spaces}")
        return
    
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    
    for this_piece, piece in enumerate(remaining_pieces):
        for y in range(rows):
            for x in range(cols):
                if grid[y][x] != 0:
                    continue
                if does_piece_fit(grid, piece, (y, x)):
                    new_grid, lines_cleared, space_cleared = update_board(grid, piece, (y, x))
                    cleaned_grid = clean_board(new_grid)
                    other_pieces = remaining_pieces[:this_piece] + remaining_pieces[this_piece+1:]
                    states_checked[0] += 1
                    
                    dirty_solve_recursive(
                        cleaned_grid,
                        other_pieces,
                        moves_so_far + [(piece, (y, x))],
                        total_lines + lines_cleared,
                        total_spaces + space_cleared,
                        best_solution,
                        states_checked
                    )

#solve with AI evaluation
def evaluate_board_state(grid) -> BoardState:
    pass

#return best move found
def search_best_move(grid, pieces) -> tuple:
    pass

def show_move_options(grid, pieces):
    where = (0, -1)
    num_options = 0

    print("\n===== Initial Grid =====")
    print_matrix("rows   ", "columns", grid)
    
    while where != (7, 7):
        valid_moves, where = search_move(where, grid, pieces)

        if valid_moves is not None:
            for piece in valid_moves:
                print(f"\n----------- Option {num_options + 1} -----------")
                print(f"Piece {piece} fits at position {where}")
                new_grid, lines_cleared, space_cleared = update_board(grid, piece, where)
                print(f"Would clear: {lines_cleared} lines, {space_cleared} spaces")
                print_matrix("rows   ", "columns", new_grid)
                num_options += 1
        else:
            break
    
    print(f"\n{num_options} total valid placements found.")
    print("(This only shows first-move options, not solutions)")

def print_matrix(one, two, dist):
    cols = len(dist[0])
    print("           " + " ".join(f" {i:2} " for i in two))
    print("     " + " ".join(f" {i:2} " for i in range(cols)))
    print("     " + "-" * (5 * cols))
    for i, row in enumerate(dist):
        if i==0:
            print(f" {i:3} |" + " ".join(f"{x:2} :" for x in row))
        else:
            print(f"{one[i-1]}{i:3} |" + " ".join(f"{x:2} :" for x in row))

        print("     " + "-" * (5 * cols) + "")

def main():
    grid = [
        [0, 1, 0, 0, 1, 1, 1, 1],
        [1, 1, 0, 0, 1, 1, 1, 1],
        [0, 0, 1, 0, 1, 0, 1, 1],
        [0, 1, 1, 0, 0, 0, 1, 1],
        [0, 0, 1, 0, 1, 1, 1, 0],
        [0, 0, 1, 1, 1, 0, 0, 0],
        [0, 0, 1, 0, 1, 1, 1, 0],
        [0, 1, 1, 0, 0, 0, 0, 1],
    ]
    pieces = [
        [(0,0), (1,0), (0,1), (1,1)],  #square
        [(0,0), (1,0), (2,0), (3,0)],  #line
        [(0,0), (0,1), (0,2), (1,2)],  #L shape
    ]
    
    print("\n===== Showing Move Options =====")
    show_move_options(grid, pieces)

    
    print("\n===== Searching all states for best possible result =====")
    print("Current best -> Lines cleared: 0, Space cleared: 0")
    result = dirty_solve(grid, pieces)
    print(f"States checked: {result[1]}")
    print(f"\nFinal Solution-> Lines cleared: {result[0]['lines_cleared']}, Spaces cleared: {result[0]['space_cleared']}")
    moves_str = '\n  '.join(f"{i+1}. {piece} at {pos}" 
                        for i, (piece, pos) in enumerate(result[0]['moves']))
    print(f"\n{len(result[0]['moves'])} Moves made:\n  {moves_str}")
    print("\nFinal grid state:")
    print_matrix("rows   ", "columns", result[0]['grid'])
    print('\n this is only for testing. run program from main.py.\n')

if __name__ == "__main__":
    main()