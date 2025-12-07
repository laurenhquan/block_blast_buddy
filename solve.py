# solve.py
# implements ai search and decision-making
# https://docs.python.org/3/library/heapq.html
import heapq
import time

class BoardState:
    lines_cleared: int
    space_cleared: int   #diff placements could clear same amt of lines but free different amt of space
    empty_space: int
    fragmentation: int   #how many different regions of empty space exist
    is_full_clear: bool
    is_game_over: bool

    def __init__(self):
        self.lines_cleared = 0
        self.space_cleared = 0
        self.empty_space = 0
        self.fragmentation = 0
        self.is_full_clear = False
        self.is_game_over = False

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
        if grid[y][x] > 0:
            return False
        
    return True

#place piece on board and return updated board, along with lines/space cleared
def update_board(grid, piece, pos):
    lines_cleared = 0
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
    new_grid, lines_cleared, space_cleared = clear_full_lines(new_grid)

    return (new_grid, lines_cleared, space_cleared)

def clear_full_lines(grid):
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    lines_cleared = 0
    rows_to_clear = []
    cols_to_clear = []
    space_cleared = 0
    new_grid = [row[:] for row in grid]  #make a copy to avoid mutating original

    #find full rows
    for r in range(rows):
        if all(new_grid[r][c] > 0 for c in range(cols)):
            rows_to_clear.append(r)
            lines_cleared += 1
    #find full columns
    for c in range(cols):
        if all(new_grid[r][c] > 0 for r in range(rows)):
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

#func to set all board spaces to 0,1
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

#convert pieces from 2d array to offset list
def convert_piece_format(pieces_2d):
    converted_pieces = {}

    for key,piece in pieces_2d.items():
        offsets = []
        base = None
        for y in range(len(piece)):
            for x in range(len(piece[0])):
                if piece[y][x] != 0:
                    if base is None:
                        base = (y, x)
                        offsets.append((0, 0))
                    else:
                        oy = y - base[0]
                        ox = x - base[1]
                        offsets.append((oy, ox))
        converted_pieces[key] = (offsets)
    
    return converted_pieces

#=========================solve without AI evaluation=========================#
def brute_force(grid, pieces):
    best_solution = {
        'lines_cleared': 0,
        'space_cleared': 0,
        'grid': None,
        'moves': []
    }
    
    states_checked = [0]

    brute_force_helper(grid, pieces, [], 0, 0, best_solution, states_checked)
    
    return (best_solution, states_checked[0])

def brute_force_helper(grid, remaining_pieces, moves_so_far, total_lines, total_spaces, best_solution, states_checked):
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
                    
                    brute_force_helper(
                        cleaned_grid,
                        other_pieces,
                        moves_so_far + [(piece, (y, x))],
                        total_lines + lines_cleared,
                        total_spaces + space_cleared,
                        best_solution,
                        states_checked
                    )

#=========================solve with AI evaluation=========================#
def evaluate_board_state(grid, piece, where):
    state, new_grid = calc_board_metrics(grid, piece, where)

    score = 0.0
    
    if state.is_full_clear:
        score += 10000.0
    score += state.lines_cleared * 1000.0
    score += state.space_cleared * 2.0
    score += state.empty_space * 1.5
    score -= state.fragmentation * 5.0
    if state.is_game_over:
        score -= 1000000000000.0

    return (score, state, new_grid)

#helper funcs for evaluation
def calc_board_metrics(grid, piece, where):
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    state = BoardState()

    new_grid, lines_cleared, space_cleared = update_board(grid, piece, where)
    state.lines_cleared = lines_cleared
    state.space_cleared = space_cleared
    state.empty_space = count_empty_space(new_grid)
    state.fragmentation = find_fragmentation(new_grid)
    state.is_game_over = (state.empty_space == 0)
    state.is_full_clear = (state.empty_space == (rows * cols))


    return (state, new_grid)

def count_empty_space(grid):
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    
    return sum(1 for r in range(rows) for c in range(cols) if grid[r][c] <= 0)

def flood_fill(grid, start, visited):
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    stack = [start]
    while stack:
        r, c = stack.pop()
        #1=True, 0=False
        if c < 0 or c >= cols or r < 0 or r >= rows:
            continue
        if visited[r][c] or grid[r][c] > 0:
            continue
        visited[r][c] = True

        stack.append((r+1, c))
        stack.append((r-1, c))
        stack.append((r, c+1))
        stack.append((r, c-1))

def find_fragmentation(grid):
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    visited = [[False] * cols for _ in range(rows)]
    regions = 0

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] <= 0 and not visited[r][c]:
                flood_fill(grid, (r, c), visited)
                regions += 1

    return regions

def get_metrics(grid, piece, where):
    score, state, new_grid = evaluate_board_state(grid, piece, where)
    
    print(f"Board State:")
    print(f"  Lines cleared: {state.lines_cleared}")
    print(f"  Space cleared: {state.space_cleared}")
    print(f"  Empty cells: {state.empty_space}")
    print(f"  Fragmentation: {state.fragmentation}")
    print(f"  Full clear: {state.is_full_clear}")
    print(f"  Game over: {state.is_game_over}")
    print(f"  Eval score: {score:.2f}")
    print("\nResulting Grid:")
    print_matrix("rows   ", "columns", new_grid)
    
    return state, score


#return best move found
#moves are tuples of (piece_index, y, x) -> use piece_index to match piece key
def astar_solve(grid, pieces_2d):
    pieces = convert_piece_format(pieces_2d)

    init_state = {
        'grid': tuple(tuple(row) for row in grid),
        'pieces_left': tuple(range(len(pieces))),
        'moves': (),
        'lines': 0,
        'spaces': 0,
        'depth': 0
    }
    
    prio_q = [(0, 0, init_state)]
    visited = set()
    state_counter = 1
    states_explored = 0
    
    while prio_q:
        prio, _, state = heapq.heappop(prio_q)
        
        grid_list = [list(row) for row in state['grid']]
        
        state_key = (state['grid'], state['pieces_left'])
        if state_key in visited:
            continue
        visited.add(state_key)
        
        print(f"\n{'─'*70}")
        print(f"Exploring state #{states_explored} (priority={prio:.2f})")
        print(f"  Depth: {state['depth']}/3 pieces placed")
        print(f"  Remaining pieces: {list(state['pieces_left'])}")
        print(f"  Lines cleared so far: {state['lines']}")
        print(f"  Spaces cleared so far: {state['spaces']}")
        if state['moves']:
            print(f"  Path so far: {list(state['moves'])}")

        if len(state['pieces_left']) == 0:
            print(f"Solution found! Explored {states_explored} states")
            return {
                'lines_cleared': state['lines'],
                'space_cleared': state['spaces'],
                'grid': grid_list,
                'moves': list(state['moves']),
                'states_explored': states_explored
            }
        
        rows = len(grid_list)
        cols = len(grid_list[0])
        
        for piece_idx in state['pieces_left']:
            piece = pieces[piece_idx]
            
            for y in range(rows):
                for x in range(cols):
                    if grid_list[y][x] <= 0 and does_piece_fit(grid_list, piece, (y, x)):
                        
                        states_explored += 1

                        eval_score, metrics, cleaned_grid = evaluate_board_state(grid_list, piece, (y, x))
                        print("  Current grid:")
                        print_matrix("rows   ", "columns", cleaned_grid)

                        lines_cleared = metrics.lines_cleared
                        space_cleared = metrics.space_cleared
                        
                        new_remaining = tuple(i for i in state['pieces_left'] if i != piece_idx)

                        #cleaned_grid = clean_board(cleaned_grid)
                        new_state = {
                            'grid': tuple(tuple(row) for row in cleaned_grid),
                            'pieces_left': new_remaining,
                            'moves': state['moves'] + ((piece_idx, y, x),),
                            'lines': state['lines'] + lines_cleared,
                            'spaces': state['spaces'] + space_cleared,
                            'depth': state['depth'] + 1
                        }
                        
                        # A* priority calculation
                        priority = (
                            - eval_score                # Maximize board quality
                            + new_state['depth'] * 10    # Minimize depth
                        )
                        
                        heapq.heappush(prio_q, (priority, state_counter, new_state))
                        state_counter += 1
    
    print(f"No solution found after {states_explored} states")
    return None


def main():
    grid1 = [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 1, 1],
        [0, 0, 1, 1, 1, 0, 1, 1],
        [0, 0, 0, 0, 0, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 1, 1],
        [1, 1, 1, 1, 0, 0, 1, 0],
    ]
    pieces1 = [
        [(0,0), (0,1), (1,1), (1,2)],
        [(0,0), (0,1), (0,2), (1,2)],
        [(0,0), (0,1), (0,2), (0,3)]
    ]
    pieces_2d1 = {
        0: [
            [1, 1, 0],
            [0, 1, 1]
        ],
        1: [
            [1, 1, 1],
            [0, 0, 1]
        ],
        2: [
            [1, 1, 1, 1]
        ]
    }

    # print(f"{find_fragmentation(grid)} fragments found in initial grid.")
    

    # print("\n===== Showing Move Options =====")
    # show_move_options(grid, pieces)

    
    # print("\n===== Searching all states for best possible result =====")
    # print("Current best -> Lines cleared: 0, Space cleared: 0")
    start_time1 = time.time()
    result = brute_force(grid1, pieces1)
    end_time1 = time.time()
    elapsed_time1 = end_time1 - start_time1
    # print(f"States checked: {result[1]}")
    # print(f"\nFinal Solution-> Lines cleared: {result[0]['lines_cleared']}, Spaces cleared: {result[0]['space_cleared']}")
    # moves_str = '\n  '.join(f"{i+1}. {piece} at {pos}" 
    #                     for i, (piece, pos) in enumerate(result[0]['moves']))
    # print(f"\n{len(result[0]['moves'])} Moves made:\n  {moves_str}")
    # print("\nFinal grid state:")
    # print_matrix("rows   ", "columns", result[0]['grid'])

    # print("\n===== Thinking about moves for best possible result =====")
    # print(f"\nMove 1: {result[0]['moves'][0][0]} at {result[0]['moves'][0][1]}")
    # get_metrics(grid, result[0]['moves'][0][0], result[0]['moves'][0][1])
    # print(f"\nMove 2: {result[0]['moves'][1][0]} at {result[0]['moves'][1][1]}")
    # get_metrics(grid, result[0]['moves'][1][0], result[0]['moves'][1][1])
    # print(f"\nMove 3: {result[0]['moves'][2][0]} at {result[0]['moves'][2][1]}")
    # get_metrics(grid, result[0]['moves'][2][0], result[0]['moves'][2][1])
    start_time12 = time.time()
    result12 = astar_solve(grid1, pieces_2d1)
    end_time12 = time.time()
    elapsed_time12 = end_time12 - start_time12

    grid2 = [
        [1, 1, 1, 0, 0, 0, 1, 1],
        [0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 1, 1, 1, 0, 1, 1],
        [0, 0, 0, 0, 0, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 1, 1],
        [1, 1, 1, 1, 0, 0, 1, 0],
    ]
    pieces2 = [
        [(0,0), (1,1), (0,1), (0,2)],  #square
        [(0,0), (1,2), (0,1), (0,2)],  #line
        [(0,0), (1,2), (0,1), (0,2)],  #L shape
    ]
    pieces_2d2 = {
        0: [
            [1, 1, 1],
            [0, 1, 0]
        ],
        1: [
            [1, 1, 1],
            [0, 0, 1],
        ],
        2: [
            [1, 1, 1],
            [0, 0, 1]
        ]
    }
    start_time2 = time.time()
    result2 = brute_force(grid2, pieces2)
    end_time2 = time.time()
    elapsed_time2 = end_time2 - start_time2

    start_time22 = time.time()
    result22 = astar_solve(grid2, pieces_2d2)
    end_time22 = time.time()
    elapsed_time22 = end_time22 - start_time22

    print("\n===== End of testing =====")

    print("\n~~~~~~~~~Grid1 test case results: ~~~~~~~~~")
    print("\nBrute force: ")
    print(f"States checked: {result[1]}")
    print(f"\nElapsed time: {elapsed_time1:.2f} seconds")
    print("\nA* search: ")
    print(f"States checked: {result12['states_explored']}")
    print(f"\nElapsed time: {elapsed_time12:.2f} seconds")

    print("\n~~~~~~~~~Grid2 test case results: ~~~~~~~~~")
    print("\nBrute force: ")
    print(f"States checked: {result2[1]}")
    print(f"\nElapsed time: {elapsed_time2:.2f} seconds")
    print("\nA* search: ")
    print(f"States checked: {result22['states_explored']}")
    print(f"\nElapsed time: {elapsed_time22:.2f} seconds")
    # print("\n~~~~~~~~~Grid3 test case results: ~~~~~~~~~")
    # print("\nBrute force: ")
    # print(f"States checked: {result[1]}")
    # print("\nA* search: ")
    # print(f"States checked: {result12['states_explored']}")
    # print("\n~~~~~~~~~Grid4 test case results: ~~~~~~~~~")
    # print("\nBrute force: ")
    # print(f"States checked: {result[1]}")
    # print("\nA* search: ")
    # print(f"States checked: {result12['states_explored']}")
    # print("\n~~~~~~~~~Grid5 test case results: ~~~~~~~~~")
    # print("\nBrute force: ")
    # print(f"States checked: {result[1]}")
    # print("\nA* search: ")
    # print(f"States checked: {result12['states_explored']}")


    print('\n this is only for testing. run program from main.py.\n')

if __name__ == "__main__":
    main()