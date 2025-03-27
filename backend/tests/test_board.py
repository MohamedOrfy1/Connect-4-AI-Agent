import unittest
import numpy as np
from src.models.board import ConnectFourBoard

class TestConnectFourBoard(unittest.TestCase):
    def setUp(self):
        """Set up a new board for each test"""
        self.board = ConnectFourBoard()

    def test_initialization(self):
        """Test board initialization"""
        self.assertEqual(self.board.width, 7)
        self.assertEqual(self.board.height, 6)
        self.assertEqual(self.board.current_player, 1)
        self.assertTrue(np.all(self.board.board == 0))
        self.assertIsNone(self.board.last_move)

    def test_reset(self):
        """Test board reset functionality"""
        # Make some moves
        self.board.drop_piece(0)
        self.board.drop_piece(1)
        self.board.drop_piece(2)
        
        # Reset the board
        self.board.reset()
        
        # Check if board is reset properly
        self.assertEqual(self.board.current_player, 1)
        self.assertTrue(np.all(self.board.board == 0))
        self.assertIsNone(self.board.last_move)

    def test_valid_moves(self):
        """Test valid moves detection"""
        # Initially all moves should be valid
        self.assertEqual(self.board.get_valid_moves(), list(range(7)))
        
        # Fill up a column
        for _ in range(6):
            self.board.drop_piece(0)
        
        # Column 0 should no longer be valid
        self.assertNotIn(0, self.board.get_valid_moves())

    def test_drop_piece(self):
        """Test piece dropping functionality"""
        # Test valid move
        self.assertTrue(self.board.drop_piece(0))
        self.assertEqual(self.board.board[5, 0], 1)
        self.assertEqual(self.board.current_player, 2)
        
        # Test invalid move (column out of bounds)
        self.assertFalse(self.board.drop_piece(-1))
        self.assertFalse(self.board.drop_piece(7))

    def test_is_full(self):
        """Test board full detection"""
        # Fill up the board
        for col in range(7):
            for _ in range(6):
                self.board.drop_piece(col)
        
        self.assertTrue(self.board.is_full())

    def test_check_winner(self):
        """Test winner detection"""
        # Create a board state where player 2 has more connected fours
        # Player 2 will have two horizontal lines (8 fours total)
        # Player 1 will have one horizontal line (4 fours total)
        board_state = [
            [1, 2, 1, 2, 1, 2, 1],  # Top row
            [2, 1, 2, 1, 2, 1, 2],
            [1, 2, 1, 2, 1, 2, 1],
            [2, 2, 2, 2, 1, 1, 1],  # Player 2's first line
            [2, 2, 2, 2, 1, 1, 1],  # Player 2's second line
            [1, 1, 1, 1, 2, 2, 2],  # Player 1's line
        ]
        
        # Set up the board state
        for row in range(6):
            self.board.board[row] = board_state[row]
        
        print("Final board state:")
        print(self.board)
        
        # Print scores for debugging
        player1_score = self.board.count_fours(1)
        player2_score = self.board.count_fours(2)
        print(f"Player 1 score: {player1_score}")
        print(f"Player 2 score: {player2_score}")
        
        # Now player 2 should have more connected fours than player 1
        # Since the board is full, check_winner should return player 2 as winner
        self.assertTrue(self.board.is_full())
        winner = self.board.check_winner()
        self.assertEqual(winner, 2)
        
        # Test that check_winner returns None when board is not full
        self.board.board[0, 0] = 0  # Make one space empty
        self.assertFalse(self.board.is_full())
        winner = self.board.check_winner()
        self.assertIsNone(winner)

    def test_board_copy(self):
        """Test board copying functionality"""
        # Make some moves on the original board
        self.board.drop_piece(0)
        self.board.drop_piece(1)
        
        # Create a copy
        board_copy = self.board.copy()
        
        # Check if copy is identical
        self.assertTrue(np.array_equal(self.board.board, board_copy.board))
        self.assertEqual(self.board.current_player, board_copy.current_player)
        self.assertEqual(self.board.last_move, board_copy.last_move)
        
        # Modify copy and verify original is unchanged
        board_copy.drop_piece(2)
        self.assertNotEqual(self.board.current_player, board_copy.current_player)

if __name__ == '__main__':
    unittest.main() 