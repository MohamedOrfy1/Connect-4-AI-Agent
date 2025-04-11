import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
import numpy as np
import logging
from src.models.board import ConnectFourBoard
from src.algorithms.minimax import eval

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def print_board(board):
    """Helper function to print the board state."""
    for row in board:
        print(' '.join(['X' if x == 1 else 'O' if x == 2 else '.' for x in row]))
    print('0 1 2 3 4 5 6')
    print()

def test_api(board_state, current_player, expected_move=None, description=""):
    """Test the API with a given board state and current player."""
    print(f"\nTest: {description}")
    print("Board State:")
    print_board(board_state)
    
    # Create board and evaluate score
    board = ConnectFourBoard()
    board.board = np.array(board_state, dtype=int)
    board.current_player = current_player
    score = eval(board)
    print(f"Initial board evaluation score: {score}")
    
    response = requests.post(
        "http://localhost:8000/ai/move",
        json={
            "board": board_state,
            "current_player": current_player
        }
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"AI Move: {result['move']}")
        if expected_move is not None:
            print(f"Expected Move: {expected_move}")
            print(f"Test {'PASSED' if result['move'] == expected_move else 'FAILED'}")
            
            # Evaluate score after making the AI's move
            board.drop_piece(result['move'])
            new_score = eval(board)
            print(f"Score after AI move: {new_score}")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
    
    print("-" * 50)

def main():
    # Test 1: Empty board - AI should choose center
    test_api(
        [[0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0]],
        current_player=1,
        expected_move=3,
        description="Empty board - should choose center"
    )

    # Test 2: Block opponent's winning move
    test_api(
        [[0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0],
         [1, 1, 1, 0, 0, 0, 0]],
        current_player=2,
        expected_move=3,
        description="Block opponent's horizontal three"
    )

    # Test 3: Make winning move
    test_api(
        [[0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0],
         [2, 2, 2, 0, 0, 0, 0]],
        current_player=2,
        expected_move=3,
        description="Make winning move (horizontal)"
    )

    # Test 4: Block vertical threat
    test_api(
        [[0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 1, 0, 0, 0],
         [0, 0, 0, 1, 0, 0, 0],
         [0, 0, 0, 1, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0]],
        current_player=2,
        expected_move=3,
        description="Block vertical three"
    )

    # Test 5: Block diagonal threat
    test_api(
        [[0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 1, 0, 0, 0],
         [0, 0, 1, 0, 0, 0, 0],
         [0, 1, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0]],
        current_player=2,
        expected_move=0,
        description="Block diagonal three"
    )

    # Test 6: Create two threats
    test_api(
        [[0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0],
         [2, 2, 0, 0, 0, 0, 0]],
        current_player=2,
        expected_move=2,
        description="Create two threats"
    )

if __name__ == "__main__":
    main() 