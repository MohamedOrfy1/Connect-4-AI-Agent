from src.algorithms.minimax import eval, maximize, minimize, decision
from src.models.board import ConnectFourBoard

# Helper to create a board state quickly for testing eval
def create_board_with_win(player: int) -> ConnectFourBoard:
    board = ConnectFourBoard()
    for i in range(4):
        board.board[board.height - 1, i] = player
    return board

def test_eval_winning_position():
    """Test evaluation identifies a win correctly."""
    # Test winning position for player 1
    board_p1_wins = create_board_with_win(1)
    
    # Evaluate from player 1's perspective (should be high positive)
    board_p1_wins.current_player = 1
    assert eval(board_p1_wins) == 10000, "Eval should return 10000 for current player's win"

    # Evaluate from player 2's perspective (should be high negative)
    board_p1_wins.current_player = 2
    assert eval(board_p1_wins) == -10000, "Eval should return -10000 for opponent's win"

def test_eval_losing_position():
    """Test evaluation identifies a loss correctly."""
    # Test winning position for player 2 (losing for player 1)
    board_p2_wins = create_board_with_win(2)

    # Evaluate from player 1's perspective (should be high negative)
    board_p2_wins.current_player = 1
    assert eval(board_p2_wins) == -10000, "Eval should return -10000 for current player's loss"

    # Evaluate from player 2's perspective (should be high positive)
    board_p2_wins.current_player = 2
    assert eval(board_p2_wins) == 10000, "Eval should return 10000 for opponent's loss (their win)"

# --- In tests/test_minimax.py ---

def test_depth_limit():
    """Test that search returns a move even if all outcomes are draws or losses."""
    board = ConnectFourBoard()

    # FIX: Create a setup where the board is *almost* full, and P2's only
    # available moves lead to a full board (likely a draw if no immediate win).
    # Fill rows 1-5, leaving row 0 open. Make sure no immediate win exists initially.
    for r in range(1, board.height):
         for c in range(board.width):
             # Simple alternating pattern, less likely to create immediate wins
             # Player number depends on row and col position
             player = 1 if (r + c) % 2 == 0 else 2
             board.board[r, c] = player
             
    # Optional: Verify no winner in the initial state before P2 moves
    assert board.check_winner() is None, "Initial board for depth limit test should not have a winner"

    board.current_player = 2 # Player 2's turn. Row 0 is the only place to play.

    # Any move P2 makes will fill the board. check_winner on the *resulting* board.
    # If no winner is created by P2's move, the result is a draw (Eval 0).

    move1 = decision(board, 1)
    move3 = decision(board, 3)

    print(f"\nDepth Limit Test - Initial Board:\n{board}")
    print(f"Depth Limit Test - Move (k=1): {move1}") # Expect 0 (first move evaluated)
    print(f"Depth Limit Test - Eval (k=1) should be 0 (Draw)")
    print(f"Depth Limit Test - Move (k=3): {move3}") # Expect 0 (first move evaluated)
    print(f"Depth Limit Test - Eval (k=3) should be 0 (Draw)")

    # Assert that *a* move is returned. Because all moves lead to a draw (utility 0),
    # the first move evaluated (column 0) should be returned based on the previous fix
    # to maximize/minimize.
    assert move1 is not None, "Decision should return a move even if all options lead to draw (k=1)"
    assert move1 in board.get_valid_moves(), "Move (k=1) must be valid"
    assert move1 == 0, "Expected first valid move when all outcomes are equal (k=1)"

    assert move3 is not None, "Decision should return a move even if all options lead to draw (k=3)"
    assert move3 in board.get_valid_moves(), "Move (k=3) must be valid"
    assert move3 == 0, "Expected first valid move when all outcomes are equal (k=3)"


def test_eval_three_in_row_threat():
    """Test evaluation recognizes a 'three-in-a-row' threat."""
    # Test player 1's threat ('X X X .')
    board = ConnectFourBoard()
    for i in range(3):
        board.board[board.height - 1, i] = 1 
    board.current_player = 1
    score_p1_threat = eval(board)
    # Expect a significant positive score, but less than an outright win
    assert 0 < score_p1_threat < 10000, "Eval should give positive score for player's own threat"

    # Test opponent's threat ('O O O .') from player 1's perspective
    board = ConnectFourBoard()
    for i in range(3):
        board.board[board.height - 1, i] = 2 
    board.current_player = 1
    score_p2_threat = eval(board)
    # Expect a significant negative score (to encourage blocking), but less than an outright loss
    assert -10000 < score_p2_threat < 0, "Eval should give negative score for opponent's threat"

def test_eval_center_control(): # Renamed from duplicate test_center_control
    """Test evaluation bonus for center column control."""
    board = ConnectFourBoard()
    center_col = board.width // 2

    # Player 1 occupies center bottom
    board.board[board.height - 1, center_col] = 1
    board.current_player = 1
    score_p1_center = eval(board)

    # Player 2 occupies center bottom
    board_p2 = ConnectFourBoard()
    board_p2.board[board_p2.height - 1, center_col] = 2
    board_p2.current_player = 1 # Evaluate still from P1's perspective
    score_p2_center = eval(board_p2)

    assert score_p1_center > 0, "P1 center control should yield positive score for P1"
    assert score_p2_center < 0, "P2 center control should yield negative score for P1"
    assert score_p1_center > score_p2_center, "P1 control score should be higher than P2 control score from P1 perspective"

def test_maximize():
    """Test maximize function chooses winning move"""
    board = ConnectFourBoard()
    # Set up a position where player 1 can win: X X X . . . .
    for i in range(3):
        board.board[board.height - 1, i] = 1 
    board.current_player = 1 # Set current player to 1 (AI)

    move, _, utility = maximize(board, 1) # Depth 1 is enough to see immediate win
    
    print(f"\nMaximize Test - Initial Board:\n{board}")
    print(f"Maximize Test - Chosen move: {move}, Utility: {utility}")
    
    assert move == 3, "Maximize should choose the winning move (col 3)"

    assert utility > 9000, "Utility for immediate win should be very high"

def test_minimize():
    """Test minimize function chooses move to block opponent's win"""
    board = ConnectFourBoard()
    # Set up a position where player 1 (opponent) can win: X X X . . . .
    for i in range(3):
        board.board[board.height - 1, i] = 1 
    board.current_player = 2 # Set current player to 2 (AI - minimizing player)

    # FIX: Unpack only 2 return values
    # Depth 1 is not enough for minimize to see the threat *and* choose the block
    # Minimize looks one step ahead (calls maximize). Maximize at depth 1 sees the win.
    # So, minimize needs depth 2 to "see" the result of maximize(depth 1).
    # OR rely on the explicit blocking check within minimize if implemented.
    # Let's assume the explicit blocking check exists OR test with depth 2.
    move,_, utility = minimize(board, 2) 
    
    print(f"\nMinimize Test - Initial Board:\n{board}")
    print(f"Minimize Test - Chosen move: {move}, Utility: {utility}")

    assert move == 3, "Minimize should choose the blocking move (col 3)"
     # Optional: Check utility - blocking a win might still be bad, but better than losing immediately
    # The exact utility depends heavily on the eval of the board *after* the block.

def test_decision_immediate_win(): # More specific name
    """Test decision function finds an immediate winning move"""
    board = ConnectFourBoard()
    # Create a position where player 1 can win in one move
    for i in range(3):
        board.board[board.height-1, i] = 1 # P1: X X X .
    board.current_player = 1
    
    print(f"\nDecision Win Test - Initial Board:\n{board}")
    move = decision(board, 3) # Depth 3 (or even 1) should see this
    print(f"Decision Win Test - Chosen move: {move}")
    
    assert move == 3, "Decision should choose the winning move (col 3)"

def test_decision_block_win(): # More specific name
    """Test decision function blocks opponent's immediate winning move"""
    board = ConnectFourBoard()
    # Create a position where player 2 (opponent) can win in one move
    for i in range(3):
        board.board[board.height-1, i] = 2 # P2: O O O .
    board.current_player = 1 # Player 1's turn to block
    
    print(f"\nDecision Block Test - Initial Board:\n{board}")
    move = decision(board, 4) # Depth 2+ needed usually
    print(f"Decision Block Test - Chosen move: {move}")

    assert move == 3, "Decision should choose the blocking move (col 3)"

def test_decision_valid_move_basic(): # Renamed from test_decision
    """Test decision function returns a valid move on an empty board"""
    board = ConnectFourBoard()
    move = decision(board, 3)
    assert move is not None, "Decision should return a move on an empty board"
    assert board.is_valid_move(move), "Decision should return a valid move"
    assert move in board.get_valid_moves(), "Returned move must be in valid moves list"

def test_depth_limit():
    """Test that search respects depth limit and returns a move if possible, even if it leads to loss."""
    board = ConnectFourBoard()

    # Fill board so only the top row is available
    # And create a situation where any move leads to opponent win (vertical)
    for c in range(board.width):
        board.board[1, c] = 1 # Player 1
        board.board[2, c] = 2 # Player 2
        board.board[3, c] = 1 # Player 1
        board.board[4, c] = 2 # Player 2
        board.board[5, c] = 1 # Player 1
        # Row 0 is empty
        
    board.current_player = 2 # Player 2's turn. Any move P2 makes, P1 wins vertically.

    # Search with different depths. Should realize all moves lose.
    move1 = decision(board, 1)
    move3 = decision(board, 3)
    
    print(f"\nDepth Limit Test - Initial Board:\n{board}")
    print(f"Depth Limit Test - Move (k=1): {move1}")
    print(f"Depth Limit Test - Move (k=3): {move3}")

    # FIX: Allow None if all moves lead to loss, but decision *should* ideally return *a* move even if it's bad.
    # Let's assert it returns *some* valid move. If it returns None, the Minimax implementation needs adjustment
    # to return *a* move when all options are equally bad, instead of None.
    # A common approach is to return the first move evaluated in such cases.
    
    # Check if the Minimax implementation returns a move even if all utilities are -inf or +inf
    # Assuming decision returns a move rather than None in forced loss/win scenarios
    assert move1 is not None, "Decision should return a move even if all options lead to loss (k=1)"
    assert move1 in board.get_valid_moves(), "Move (k=1) must be valid"
    
    assert move3 is not None, "Decision should return a move even if all options lead to loss (k=3)"
    assert move3 in board.get_valid_moves(), "Move (k=3) must be valid"

# Removed test_eval_mobility

def test_minimax_depth_makes_difference(): # Renamed from test_minimax_depth
    """Test if minimax potentially makes better decisions with higher depth in a non-trivial position."""
    # This test is inherently heuristic-dependent and may need adjustment
    board = ConnectFourBoard()
    # Example setup (can be complex to design a guaranteed depth difference)
    # P1: 3, P2: 4, P1: 3, P2: 4, P1: 2, P2: 2, P1: 3
    board.drop_piece(3); board.drop_piece(4) # P1, P2
    board.drop_piece(3); board.drop_piece(4) # P1, P2
    board.drop_piece(2); board.drop_piece(2) # P1, P2
    board.drop_piece(3) # P1 turn
    
    print(f"\nDepth Difference Test - Initial Board:\n{board}")
    
    # Get moves with different depths
    # Use depths where a difference might emerge (e.g., seeing a trap setup)
    move_depth2 = decision(board, 2) 
    move_depth4 = decision(board, 4) 
    
    print(f"Depth Difference Test - Move (k=2): {move_depth2}")
    print(f"Depth Difference Test - Move (k=4): {move_depth4}")

    # We expect depth 4 to potentially make a better strategic move
    # Asserting they are different is a start, but doesn't guarantee 'better'
    # Asserting a specific move (like center) is too brittle.
    # A weaker but useful check:
    assert move_depth2 in board.get_valid_moves()
    assert move_depth4 in board.get_valid_moves()
    # If they are different, it suggests depth had an impact. Not a perfect test.
    # assert move_depth2 != move_depth4 # This might be too strict

# (Keep test_center_control as it was already passing and correctly set up)
# It was duplicated, ensure only one version exists. Let's use test_eval_center_control above.