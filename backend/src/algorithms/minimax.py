from src.models.board import ConnectFourBoard
from src.models.node import TreeNode

MAX_PLAYER = 2 # Ai player
MIN_PLAYER = 1 # Opponent player

def eval(board: ConnectFourBoard) -> int:
    """
    Evaluate the board state considering:
    1. Connected fours (winning conditions)
    2. Three-in-a-row threats
    3. Two-in-a-row potential
    4. Positional advantages
    """
    if board.is_full():
        if board.check_winner() == MAX_PLAYER:
            return 10000
        elif board.check_winner() == MIN_PLAYER:
            return -10000
        else:
            return 0
    
    score = 0
    max_threats = 0
    min_threats = 0

    # Count connected fours
    max_player_fours = board.count_fours(MAX_PLAYER)
    min_player_fours = board.count_fours(MIN_PLAYER)
    score = (max_player_fours - min_player_fours) * 1000

    # Check horizontal patterns
    for row in range(board.height):
        for col in range(board.width - 3):
            window = board.board[row, col:col+4]
            
            # Three in a row threats
            if sum(window == MAX_PLAYER) == 3 and sum(window == 0) == 1:
                max_threats += 1
                score += 600 + (row * 50)  # More points for lower rows
            if sum(window == MIN_PLAYER) == 3 and sum(window == 0) == 1:
                min_threats += 1
                score -= 600 + (row * 50)
                
            # Two in a row potential
            if sum(window == MAX_PLAYER) == 2 and sum(window == 0) == 2:
                if any(window[i:i+2].all() == MAX_PLAYER for i in range(3)):
                    score += 300
                else:
                    score += 200
                # score += 200 + (row * 25)
            if sum(window == MIN_PLAYER) == 2 and sum(window == 0) == 2:
                if any(window[i:i+2].all() == MIN_PLAYER for i in range(3)):
                    score += 300
                else:
                    score += 200
                # score -= 200 + (row * 25)

    # Check vertical patterns
    for row in range(board.height - 3):
        for col in range(board.width):
            window = board.board[row:row+4, col]
            
            # Three in a row threats
            if sum(window == MAX_PLAYER) == 3 and sum(window == 0) == 1:
                max_threats += 1
                score += 800
            if sum(window == MIN_PLAYER) == 3 and sum(window == 0) == 1:
                min_threats += 1
                score -= 800

    # Check diagonal patterns (positive slope)
    for row in range(board.height - 3):
        for col in range(board.width - 3):
            window = [board.board[row+i, col+i] for i in range(4)]
            
            # Three in a row threats
            if sum(x == MAX_PLAYER for x in window) == 3 and sum(x == 0 for x in window) == 1:
                max_threats += 1
                score += 700
            if sum(x == MIN_PLAYER for x in window) == 3 and sum(x == 0 for x in window) == 1:
                min_threats += 1
                score -= 700
                
    # Check diagonal patterns (negative slope)
    for row in range(3, board.height):
        for col in range(board.width - 3):
            window = [board.board[row-i, col+i] for i in range(4)]
            
            # Three in a row threats
            if sum(x == MAX_PLAYER for x in window) == 3 and sum(x == 0 for x in window) == 1:
                max_threats += 1
                score += 700
            if sum(x == MIN_PLAYER for x in window) == 3 and sum(x == 0 for x in window) == 1:
                min_threats += 1
                score -= 700

    # Center column control bonus
    center = board.width // 2
    for row in range(board.height):
        if board.board[row][center] == MAX_PLAYER:
            score += 50 + (row * 10)  # More value for center pieces in lower rows
        elif board.board[row][center] == MIN_PLAYER:
            score -= 50 + (row * 10)

    # Bonus for multiple threats
    if max_threats >= 2:
        score += 1000  # Bonus for having multiple threats
    if min_threats >= 2:
        score -= 1500  # Penalty for allowing multiple threats

    for row in range(board.height):
        if board.board[row][center-1] == MAX_PLAYER:
            score += 30 + (row * 5)
        if board.board[row][center+1] == MAX_PLAYER:
            score += 30 + (row * 5)
        if board.board[row][center-1] == MIN_PLAYER:
            score -= 30 + (row * 5)
        if board.board[row][center+1] == MIN_PLAYER:
            score -= 30 + (row * 5)

    return score

def maximize(state: ConnectFourBoard, k: int, current_depth: int = 0
             , use_alpha_beta: bool = False, 
             alpha: float = float('-inf'), 
             beta: float = float('inf')):
    
    is_terminal = state.is_full()
    board_str = str(state)  

    if current_depth == k or is_terminal:
        score = eval(state)
        print(f"Leaf node at depth {current_depth}, score: {score}")
        return None, TreeNode(move=None, score=score, player=state.current_player, depth=current_depth, board_str=board_str)
    
    best_move, best_child, max_utility = None, None, float('-inf')
    
    root_node = TreeNode(move=None, 
                         score=None, 
                         player=state.current_player, 
                         depth=current_depth, 
                         board_str=board_str)
    
    valid_moves = state.get_valid_moves()
    print(f"Depth {current_depth}, considering moves: {valid_moves}")
    
    for move in valid_moves:
        new_board = state.copy()
        new_board.drop_piece(move) # child state 
        
        _, child_node = minimize(new_board, k, current_depth + 1, use_alpha_beta, alpha, beta)
        root_node.add_child(child_node)
        child_node.move = move

        print(f"Depth {current_depth}, Move {move}, Utility: {child_node.score}")
        
        if child_node.score > max_utility:
            max_utility = child_node.score
            best_move = move
            best_child = child_node

        if use_alpha_beta:
            if max_utility >= beta:
                break
            if max_utility > alpha:
                alpha = max_utility

    root_node.move = best_move
    root_node.score = max_utility
    root_node.set_best_child(best_child)

    return best_move, root_node

def minimize(state: ConnectFourBoard, k: int, current_depth: int = 0,
             use_alpha_beta: bool = False,
             alpha: float = float('-inf'),
             beta: float = float('inf')):
    
    is_terminal = state.is_full()
    board_str = str(state)

    if current_depth == k or is_terminal:
        score = eval(state)
        print(f"Leaf node at depth {current_depth}, score: {score}")
        return None, TreeNode(move=None, score=score, player=state.current_player, depth=current_depth, board_str=board_str)

    best_move, best_child, min_utility = None, None, float('inf')    
    root_node = TreeNode(move=None, 
                         score=None, 
                         player=state.current_player, 
                         depth=current_depth, 
                         board_str=board_str)
    
    valid_moves = state.get_valid_moves()
    print(f"Depth {current_depth}, considering moves: {valid_moves}")
    
    for move in valid_moves:
        new_board = state.copy()
        new_board.drop_piece(move)  # child state

        _, child_node = maximize(new_board, k, current_depth + 1, use_alpha_beta, alpha, beta)
        root_node.add_child(child_node)
        child_node.move = move

        print(f"Depth {current_depth}, Move {move}, Utility: {child_node.score}")

        if child_node.score < min_utility:
            min_utility = child_node.score
            best_move = move
            best_child = child_node

        if use_alpha_beta:
            if min_utility <= alpha:
                break
            if min_utility < beta:
                beta = min_utility

    root_node.move = best_move
    root_node.score = min_utility
    root_node.set_best_child(best_child)

    return best_move, root_node

# def decision(state: ConnectFourBoard, k: int, 
#              use_alpha_beta: bool = False, 
#              use_expected_minimax: bool = False) -> int:
#     print(f"\nMaking decision for player {state.current_player}")
#     print(f"Current board state:\n{state}")
    
#     valid_moves = state.get_valid_moves()
    
#     # First, check if opponent has an immediate win and block it
#     opponent = 3 - state.current_player
#     for move in valid_moves:
#         test_board = state.copy()
#         test_board.current_player = opponent
#         test_board.drop_piece(move)
#         if test_board.check_winner() == opponent:
#             print(f"Found blocking move for immediate opponent win: {move}")
#             return move
    
#     # Then check for our immediate winning moves
#     for move in valid_moves:
#         test_board = state.copy()
#         test_board.drop_piece(move)
#         if test_board.check_winner() == state.current_player:
#             # Verify this move doesn't allow opponent to win first
#             if move in valid_moves:
#                 above_move_board = test_board.copy()
#                 if above_move_board.is_valid_move(move):  # Check if there's space above
#                     above_move_board.current_player = opponent
#                     above_move_board.drop_piece(move)
#                     if above_move_board.check_winner() != opponent:  # Make sure opponent can't win above our move
#                         print(f"Found safe winning move: {move}")
#                         return move
#             else:
#                 print(f"Found winning move: {move}")
#                 return move
    
#     # Check for opponent's two-move win threats
#     opponent_winning_moves = set()
#     for move in valid_moves:
#         test_board = state.copy()
#         test_board.current_player = opponent
#         test_board.drop_piece(move)
#         # Check if this move would give opponent a winning move next turn
#         next_valid_moves = test_board.get_valid_moves()
#         for next_move in next_valid_moves:
#             next_board = test_board.copy()
#             next_board.drop_piece(next_move)
#             if next_board.check_winner() == opponent:
#                 opponent_winning_moves.add(move)
#                 break
    
#     # If opponent has multiple winning moves, try to block one of them
#     if len(opponent_winning_moves) >= 2:
#         # Find the best blocking move using evaluation
#         best_block = None
#         best_score = float('-inf')
#         for move in opponent_winning_moves:
#             test_board = state.copy()
#             test_board.drop_piece(move)
#             score = eval(test_board)
#             if score > best_score:
#                 best_score = score
#                 best_block = move
#         if best_block is not None:
#             print(f"Found blocking move for multiple threats: {best_block}")
#             return best_block
    
#     # Check for moves that create multiple threats while preventing opponent wins
#     best_move = None
#     max_threats = -1
#     best_score = float('-inf')
    
#     for move in valid_moves:
#         # Skip moves that would give opponent an immediate win next turn
#         if move in opponent_winning_moves:
#             continue
            
#         test_board = state.copy()
#         test_board.drop_piece(move)
        
#         # Check if this move allows opponent to win in their next move
#         allows_opponent_win = False
#         for opp_move in test_board.get_valid_moves():
#             opp_board = test_board.copy()
#             opp_board.current_player = opponent
#             opp_board.drop_piece(opp_move)
#             if opp_board.check_winner() == opponent:
#                 allows_opponent_win = True
#                 break
        
#         if allows_opponent_win:
#             continue
        
#         threats = 0
        
#         # Check horizontal threats
#         for row in range(test_board.height):
#             for col in range(test_board.width - 3):
#                 window = test_board.board[row, col:col+4]
#                 if sum(window == state.current_player) == 3 and sum(window == 0) == 1:
#                     threats += 1
        
#         # Check vertical threats
#         for row in range(test_board.height - 3):
#             for col in range(test_board.width):
#                 window = test_board.board[row:row+4, col]
#                 if sum(window == state.current_player) == 3 and sum(window == 0) == 1:
#                     threats += 1
        
#         # Check diagonal threats
#         for row in range(test_board.height - 3):
#             for col in range(test_board.width - 3):
#                 # Positive slope
#                 window = [test_board.board[row+i, col+i] for i in range(4)]
#                 if sum(x == state.current_player for x in window) == 3 and sum(x == 0 for x in window) == 1:
#                     threats += 1
                
#                 # Negative slope
#                 if row >= 3:
#                     window = [test_board.board[row-i, col+i] for i in range(4)]
#                     if sum(x == state.current_player for x in window) == 3 and sum(x == 0 for x in window) == 1:
#                         threats += 1
        
#         # Consider potential threats (two in a row with two empty spaces)
#         for row in range(test_board.height):
#             for col in range(test_board.width - 3):
#                 window = test_board.board[row, col:col+4]
#                 if sum(window == state.current_player) == 2 and sum(window == 0) == 2:
#                     threats += 0.5
        
#         # Calculate position score
#         score = eval(test_board)
        
#         # Update best move if this creates more threats or has a better score
#         if threats > max_threats or (threats == max_threats and score > best_score):
#             max_threats = threats
#             best_score = score
#             best_move = move
#             print(f"Found move {move} with {threats} threats and score {score}")
    
#     if best_move is not None:
#         print(f"Chose move {best_move} creating {max_threats} threats with score {best_score}")
#         return best_move
    
#     # If no special moves found, use minimax
#     if use_alpha_beta:
#         alpha = float('-inf')
#         beta = float('inf')
#         best_move, root = maximize(state, k, 0, True, alpha, beta)
#         utility = root.score
#         print(f"Chose move {best_move} with utility {utility}")
#     elif use_expected_minimax:
#         best_move, root = expected_max(state, k, 0)
#         utility = root.score
#         print(f"Chose move {best_move} with utility {utility}")
#     else:
#         # Regular minimax without pruning
#         best_move, root = maximize(state, k, 0, False)
#         utility = root.score
#         print(f"Chose move {best_move} with utility {utility}")
    
#     if best_move is not None:
#         return best_move
    
#     # If no good move found, prefer center column, then columns closer to center
#     center = state.width // 2
#     for col in [center] + [center + i for i in range(1, center + 1) if center + i < state.width] + [center - i for i in range(1, center + 1) if center - i >= 0]:
#         if col in valid_moves:
#             return col
    
#     # If still no move found, return first valid move
#     return valid_moves[0] if valid_moves else -1

def expected_max(state: ConnectFourBoard, k: int, current_depth: int = 0):
    is_terminal = state.is_full()
    board_str = str(state)

    if current_depth == k or is_terminal:
        score = eval(state)
        return None, TreeNode(move=None, score=score, player=state.current_player, depth=current_depth, board_str=board_str)


    best_move, best_child, best_expected_utility = None, None, float('-inf')
    root_node = TreeNode(move=None,
                         score=None, 
                         player=state.current_player, 
                         depth=current_depth, 
                         board_str=board_str)
    

    for move in state.get_valid_moves():
        expected_utility = 0.0

        neighbors = [move]
        probs = [0.6]

        valid_moves = state.get_valid_moves()
        left = move - 1 if move - 1 in valid_moves else None
        right = move + 1 if move + 1 in valid_moves else None

        if left is not None and right is not None:
            neighbors += [left, right]
            probs += [0.2, 0.2]
        elif left is not None:
            neighbors.append(left)
            probs.append(0.4)
        elif right is not None:
            neighbors.append(right)
            probs.append(0.4)

        # Evaluate each possible outcome and accumulate expected utility
        for col, prob in zip(neighbors, probs):
            new_state = state.copy()
            new_state.drop_piece(col)

            _, child_node = expected_min(new_state, k, current_depth + 1)
            child_node.move = move
            root_node.add_child(child_node)

            expected_utility += prob * child_node.score

        if expected_utility > best_expected_utility:
            best_expected_utility = expected_utility
            best_move = move
            best_child = child_node

    root_node.move = best_move
    root_node.score = best_expected_utility
    root_node.set_best_child(best_child)

    return best_move, root_node

def expected_min(state: ConnectFourBoard, k: int, current_depth: int = 0):
    is_terminal = state.is_full()
    board_str = str(state)

    if current_depth == k or is_terminal:
        score = eval(state)
         
        return None, TreeNode(move=None, score=score, player=state.current_player, depth=current_depth, board_str=board_str) 

    best_move, best_child, best_expected_utility = None, None, float('inf')
    root_node = TreeNode(move=None,
                         score=None, 
                         player=state.current_player, 
                         depth=current_depth, 
                         board_str=board_str)

    for move in state.get_valid_moves():
        expected_utility = 0.0

        neighbors = [move]
        probs = [0.6]

        valid_moves = state.get_valid_moves()
        left = move - 1 if move - 1 in valid_moves else None
        right = move + 1 if move + 1 in valid_moves else None

        if left is not None and right is not None:
            neighbors += [left, right]
            probs += [0.2, 0.2]
        elif left is not None:
            neighbors.append(left)
            probs.append(0.4)
        elif right is not None:
            neighbors.append(right)
            probs.append(0.4)

        # Evaluate each possible outcome and accumulate expected utility
        for col, prob in zip(neighbors, probs):
            new_state = state.copy()
            new_state.drop_piece(col)

            _, child_node = expected_max(new_state, k, current_depth + 1)
            child_node.move = move
            root_node.add_child(child_node)

            expected_utility += prob * child_node.score

        if expected_utility < best_expected_utility:
            best_expected_utility = expected_utility
            best_move = move
            best_child = child_node
    
    root_node.move = best_move
    root_node.score = best_expected_utility
    root_node.set_best_child(best_child)

    return best_move, root_node

def decision(state: ConnectFourBoard, k: int, 
             use_alpha_beta: bool = False, 
             use_expected_minimax: bool = False) -> int:
    print(f"\nMaking decision for player {state.current_player}")
    print(f"Current board state:\n{state}")
    if use_alpha_beta:
        alpha = float('-inf')
        beta = float('inf')
        best_move, root = maximize(state, k, 0, True, alpha, beta)
    elif use_expected_minimax:
        best_move, root = expected_max(state, k, 0) 
    else:
         # Regular minimax without pruning
        best_move, root = maximize(state, k, 0, False)
    
    utility = root.score

    if best_move is not None:
        print(f"Chose move {best_move} with utility {utility}")
        return best_move
    else:
        return -1