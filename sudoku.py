def is_valid(grid):
    """
    Check if a given 9x9 Sudoku grid is a valid solution.
    """

    def check_row(r):
        """Check if the r-th row contains unique numbers from 1 to 9."""
        return sorted(grid[r]) == list(range(1, 10))

    def check_col(c):
        """Check if the c-th column contains unique numbers from 1 to 9."""
        col = [grid[r][c] for r in range(9)]
        return sorted(col) == list(range(1, 10))

    def check_box(start_row, start_col): 
        """Check if the 3x3 sub-box starting at (start_row, start_col) is valid."""
        box = []
        for r in range(start_row, start_row + 3):
            for c in range(start_col, start_col + 3):
                box.append(grid[r][c])
        return sorted(box) == list(range(1, 10))
    
    # Check for incomplete solution (presence of zeros)
    for row in grid:
        if 0 in row:
            return False


    # Validate rows, columns, and 3x3 boxes
    for i in range(9):
        if not check_row(i) or not check_col(i):
            return False

    for r in range(0, 9, 3):
        for c in range(0, 9, 3):
            if not check_box(r, c):
                return False

    return True



def solve_nefario(grid, idx=0):
    """Recursive Sudoku solver."""
    # Base case: all cells filled
    if idx == 81:
        return is_valid(grid) # Then we check to see if our completed grid is valid or not.

    # Calculate row and column from linear index
    row = idx // 9
    col = idx % 9

    if grid[row][col] != 0:  # If cell is not empty move to the next cell
        return solve_nefario(grid, idx + 1)

    for num in range(1, 10):  # Try all numbers from 1 to 9
        grid[row][col] = num
        if solve_nefario(grid, idx + 1):
            return True
        # Backtrack: Reset the cell
        grid[row][col] = 0

    return False  # No valid number found for this cell





def backtrack(grid):
    """
    Solve the Sudoku puzzle using the backtracking algorithm.
    """

    def accept(grid):
        """
        Check if the grid is completely filled and valid.
        """
        return is_valid(grid)

    def reject(grid):
        """
        Check if there are any duplicates in rows, columns, or 3x3 sub-grids.
        """
        # Check rows and columns
        for r in range(9):
            for c in range(9):
                num = grid[r][c]
                if num == 0:
                    continue
                # Check row
                if grid[r].count(num) > 1:
                    return True
                # Check column
                if [grid[row][c] for row in range(9)].count(num) > 1:
                    return True
                # Check 3x3 sub-grid
                start_row, start_col = 3 * (r // 3), 3 * (c // 3)
                count = 0
                for i in range(start_row, start_row + 3):
                    for j in range(start_col, start_col + 3):
                        if grid[i][j] == num:
                            count += 1
                if count > 1:
                    return True
        return False
    
    def extend(grid):
        """
        Find the next empty cell in the grid (denoted by 0).
        Returns a tuple (row, col) of the next empty cell.
        """
        for r in range(9):
            for c in range(9):
                if grid[r][c] == 0:
                    return r, c
        return None  # No empty cells, puzzle is complete
    
    # Base case: If grid is complete and valid
    if accept(grid):
        return True

    # If grid is invalid (has duplicates or invalid entries), reject
    if reject(grid):
        return False

    # Recursive case: Extend the partial solution
    row, col = extend(grid)
    
    if row is None:  # No empty cell found, solution is complete
        return False
    
    # Try different values for grid[row][col]
    for num in range(1, 10):
        grid[row][col] = num
        if backtrack(grid):
            return True
        # Reset the cell if no solution found with this number
        grid[row][col] = 0
    return False  # Backtrack if no number fits

