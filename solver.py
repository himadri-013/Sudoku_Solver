def find_empty(bo):
    """Finds an empty cell (represented by 0) in the board."""
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0:
                return (i, j)  # row, col
    return None

def is_valid_move(bo, num, pos):
    """Checks if placing a number in a given position is valid."""
    row, col = pos

    # Check row
    for j in range(len(bo[0])):
        if bo[row][j] == num and col != j:
            return False

    # Check column
    for i in range(len(bo)):
        if bo[i][col] == num and row != i:
            return False

    # Check 3x3 box
    box_x = col // 3
    box_y = row // 3
    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if bo[i][j] == num and (i, j) != pos:
                return False

    return True

def solve_sudoku(bo):
    """
    Solves the Sudoku board using backtracking.
    This is a generator function that yields the board state at each step.
    """
    find = find_empty(bo)
    if not find:
        yield bo # Solution found
        return

    row, col = find

    for num in range(1, 10):
        if is_valid_move(bo, num, (row, col)):
            bo[row][col] = num
            yield bo # Yield the board after placing a valid number

            yield from solve_sudoku(bo)

            if find_empty(bo) is not None:
                 bo[row][col] = 0
                 yield bo

def check_initial_board(bo):
    """Checks if the initial board configuration is valid."""
    for i in range(9):
        for j in range(9):
            num = bo[i][j]
            if num != 0:
                bo[i][j] = 0
                if not is_valid_move(bo, num, (i, j)):
                    bo[i][j] = num
                    return False, (i, j)
                bo[i][j] = num
    return True, None
