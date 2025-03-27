import pytest
from src.algorithms.minimax import eval, maximize, minimize, decision
from src.models.board import ConnectFourBoard

def test_eval_terminal_states():
    """Test evaluation of terminal states"""
    board = ConnectFourBoard()
    
    # Test draw
    for col in range(board.width):
        for _ in range(board.height):
            board.drop_piece(col)
    assert eval(board) == 0
    
    # Test player 1 win
    board = ConnectFourBoard()
    for i in range(4):
        board.board[5][i] = 1  # Four in a row for player 1
    assert eval(board) > 0
    
    # Test player 2 win
    board = ConnectFourBoard()
    for i in range(4):
        board.board[5][i] = 2  # Four in a row for player 2
    assert eval(board) < 0

def test_center_control():
    """Test evaluation of center control"""
    board = ConnectFourBoard()
    center = board.width // 2
    
    # Test player 1 center control
    board.board[5][center] = 1
    score1 = eval(board)
    
    # Reset and test player 2 center control
    board = ConnectFourBoard()
    board.board[5][center] = 2
    score2 = eval(board)
    
    assert score1 > 0 and score2 < 0
    assert score1 > score2

def test_maximize():
    """Test maximize function chooses winning move"""
    board = ConnectFourBoard()
    
    # Set up a position where player 1 can win
    for i in range(3):
        board.board[5][i] = 1  # Three in a row for player 1
    board.current_player = 1  # Set current player to 1 (AI)
    
    print("\nInitial board state:")
    print(board)
    print(f"Current player: {board.current_player}")
    
    # Try each possible move and print its evaluation
    for col in board.get_valid_moves():
        test_board = board.copy()
        test_board.drop_piece(col)
        test_board.current_player = 2  # Switch to opponent's turn after our move
        score = eval(test_board)
        print(f"Move {col} evaluation: {score}")
        print(test_board)
        print()
    
    move, _, _ = maximize(board, 1)  # Depth 1 is enough to see immediate win
    print(f"Chosen move: {move}")
    assert move == 3  # Should choose the winning move

def test_minimize():
    """Test minimize function blocks winning move"""
    board = ConnectFourBoard()
    
    # Set up a position where player 2 needs to block
    for i in range(3):
        board.board[5][i] = 1  # Three in a row for player 1
    board.current_player = 2  # Set current player to 2 (opponent)
    
    print("\nInitial board state:")
    print(board)
    print(f"Current player: {board.current_player}")
    
    # Try each possible move and print its evaluation
    for col in board.get_valid_moves():
        test_board = board.copy()
        test_board.drop_piece(col)
        # Keep player 2's perspective for evaluation
        score = eval(test_board)
        print(f"Move {col} evaluation: {score}")
        print(test_board)
        print()
    
    move, _, _ = minimize(board, 1)  # Depth 1 is enough to see immediate threat
    print(f"Chosen move: {move}")
    assert move == 3  # Should choose to block

def test_decision():
    """Test decision function returns valid move"""
    board = ConnectFourBoard()
    move = decision(board, 3)
    assert move in board.get_valid_moves()

def test_depth_limit():
    """Test that search respects depth limit"""
    board = ConnectFourBoard()
    
    # Fill most of the board to reduce search space
    for col in range(board.width):
        for _ in range(board.height - 1):
            board.drop_piece(col)
            
    # Search with different depths should still complete
    move1 = decision(board, 1)
    move2 = decision(board, 3)
    
    assert move1 in board.get_valid_moves()
    assert move2 in board.get_valid_moves() 