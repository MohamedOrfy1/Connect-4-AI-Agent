import numpy as np
from typing import List, Tuple, Optional

class ConnectFourBoard:
    def __init__(self, width: int = 7, height: int = 6):
        """
        Initialize the Connect 4 board
        
        Args:
            width: Board width (default 7)
            height: Board height (default 6)
        """
        self.width = width
        self.height = height
        self.board = np.zeros((height, width), dtype=int)
        self.current_player = 1
        self.last_move: Optional[Tuple[int, int]] = None
    
    def reset(self):
        """Reset the board to initial state"""
        self.board = np.zeros((self.height, self.width), dtype=int)
        self.current_player = 1
        self.last_move = None
        
    def is_valid_move(self, column: int) -> bool:
        """
        Check if a move is valid
        
        Args:
            column: Column to drop the piece
        
        Returns:
            Boolean indicating if the move is valid
        """
        return 0 <= column < self.width and self.board[0, column] == 0
    
    def get_valid_moves(self) -> List[int]:
        """
        Get list of valid moves (columns where a piece can be dropped)
        
        Returns:
            List of valid column indices
        """
        return [col for col in range(self.width) if self.is_valid_move(col)]
        
    def drop_piece(self, column: int) -> bool:
        """
        Drop a piece in the given column.

        Args:
            column: Column index (0-based).

        Returns:
            True if the move was successful, False otherwise.
        """
        if not self.is_valid_move(column):
            return False
        
        
        for row in range(self.height - 1, -1, -1):
            if self.board[row, column] == 0:
                self.board[row, column] = self.current_player
                self.last_move = (row, column)
                self.current_player = 3 - self.current_player 
                return True
        return False
    
    def is_full(self) -> bool:
        """
        Check if the board is full.

        Returns:
            True if no more moves can be made, False otherwise.
        """
        return np.all(self.board != 0)
    
    def get_board_state(self) -> np.ndarray:
        """
        Get a copy of the current board state.

        Returns:
            A NumPy array representing the board.
        """
        return self.board.copy()
    
    def copy(self) -> 'ConnectFourBoard':
        """
        Create a deep copy of the board.

        Returns:
            A new ConnectFourBoard instance with the same state.
        """
        new_board = ConnectFourBoard(self.width, self.height)
        new_board.board = self.board.copy()
        new_board.current_player = self.current_player
        new_board.last_move = self.last_move
        return new_board
    
    def __str__(self) -> str:
        """
        Returns a string representation of the board.
        """
        symbols = {0: '.', 1: 'X', 2: 'O'}
        board_str = '\n'.join(' '.join(symbols[cell] for cell in row) for row in self.board)
        return board_str + "\n" + " ".join(map(str, range(self.width)))
    
    def check_winner(self) -> Tuple[int, int]:
        """Count the number of connected fours for each player."""
        player1_score = self.count_fours(1)
        player2_score = self.count_fours(2)
        return player1_score, player2_score

    def count_fours(self, player: int) -> int:
        """Count all connected-four sequences for a given player."""
        score = 0
        for row in range(self.height):
            for col in range(self.width):
                if self.board[row, col] == player:
                    score += self.check_directions(row, col, player)
        return score

    def check_directions(self, row: int, col: int, player: int) -> int:
        """Check all four possible directions for a connected-four sequence."""
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)] 
        count = 0
        for d_row, d_col in directions:
            if self.count_direction(row, col, d_row, d_col, player):
                count += 1
        return count

    def count_direction(self, row: int, col: int, d_row: int, d_col: int, player: int) -> bool:
        """Check if there are exactly 4 pieces in a row in the given direction."""
        for i in range(4):
            r, c = row + i * d_row, col + i * d_col
            if not (0 <= r < self.height and 0 <= c < self.width and self.board[r, c] == player):
                return False
        return True