from colorama import Fore
from copy import deepcopy


class SudokuBoard:
    """
    Represents a Sudoku board and provides functionality to solve it.

    Attributes:
        initialBoard (list[list[int]]): The initial state of the Sudoku board.
        solvedBoard (list[list[int]]): A copy of the initial board, used to track the solution.

    Methods:
        solveSudoku(): Solves the Sudoku board using backtracking.
        solve(board, i=0, j=0): Recursive helper function for solveSudoku().
        __str__(): Returns a string representation of the solved board with color-coded values.
    """
    @staticmethod
    def is_valid_num(board, i, j, num):
        for x in range(9):
            if board[i][x] == num:
                return False

            if board[x][j] == num:
                return False

        # Gets the top left coordinates of the section containing the i,j cell
        square_top_x, square_top_y = 3 * (i//3), 3 * (j//3)
        for x in range(square_top_x, square_top_x + 3):
            for y in range(square_top_y, square_top_y + 3):
                if board[x][y] == num:
                    return False

        return True

    def __init__(self, board):
        """
        Initializes a SudokuBoard object.

        Args:
            board (list[list[int]]): A 9x9 2D list representing the initial Sudoku board.
        """
        self.initial_board = board
        self.empty_indexes = []
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == 0:
                    self.empty_indexes.append((i, j))
                    
        # Deep copy to avoid modifying original board
        self.solved_board = deepcopy(board)

    def solve(self, next_empty_index=0):
        """
        Recursive function to solve the Sudoku board using backtracking.

        Args:
            next_empty_index (int, optional): The index of self.empty_indexes to get the next coordinate pair from

        Returns:
            bool: True if a solution is found, False otherwise.
        """
        
        if next_empty_index == len(self.empty_indexes):
            return True
        
        i, j = self.empty_indexes[next_empty_index]
        for num in range(1, 10):
            if not SudokuBoard.is_valid_num(self.solved_board, i, j, num):
                continue
            
            self.solved_board[i][j] = num
            if self.solve(next_empty_index + 1):
                return True
            
        self.solved_board[i][j] = 0
        return False

    def __str__(self) -> str:
        """
        Returns a string representation of the solved Sudoku board, color-coding given and solved numbers.

        Returns:
            str: The color-coded string representation of the solved board.
        """
        board_str = ""
        for i, row in enumerate(self.solved_board):
            line = ""
            for j, num in enumerate(row):
                if self.initial_board[i][j] == 0:
                    line += f"{Fore.GREEN}{num}{Fore.RESET} "
                else:
                    line += f"{num} "
                    
            board_str += line + "\n"
            
        return board_str.strip()


def solve_sudoku(board):
    """
    Solve a Sudoku board using backtracking.
    Prints the solution if found, otherwise prints "No solution found."

    Args:
        board (List): A 9x9 2D list representing the initial Sudoku board.
    """
    s = SudokuBoard(board)
    if s.solve():
        print(s)
    else:
        print("No solution found.")


def auto_sudoku(board):
    """
    Solve a Sudoku board automatically.

    Args:
        board (List): A 9x9 2D list representing the initial Sudoku board.

    Returns:
        List: A 9x9 2D list representing the solved Sudoku board.
    """
    s = SudokuBoard(board)
    if s.solve():
        return s.solved_board

    return None


def play_sudoku():
    """
    Play a game of Sudoku by inputting the initial board state.
    """
    print("Enter the sudoku board one line at a time")
    print("A line e.g. '100030058'")

    board = []
    for _ in range(9):
        input_str = input()
        if input_str == "q":
            return

        board.append([int(char) for char in input_str])

    solve_sudoku(board)
