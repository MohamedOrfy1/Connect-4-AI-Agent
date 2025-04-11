from src.models.board import ConnectFourBoard

def eval(board: ConnectFourBoard) -> int:
    """
    Evaluate the current board state.
    Returns positive value if the current player is winning, negative if opponent is winning.
    The magnitude indicates how good/bad the position is.
    
    Evaluation factors:
    1. Connected fours (highest weight)
    2. Three in a row with space
    3. Center column control
    4. Two in a row with empty spaces
    """
    # Terminal state check
    if board.is_full():
        winner = board.check_winner()
        if winner == board.current_player:
            return 10000  # Current player wins
        elif winner == 3 - board.current_player:
            return -10000  # Opponent wins
        return 0  # Draw
    
    # Check for immediate wins (four in a row)
    current_fours = board.count_fours(board.current_player)
    opponent_fours = board.count_fours(3 - board.current_player)
    if current_fours > 0:
        return 10000
    if opponent_fours > 0:
        return -10000
    
    score = 0
    current_player = board.current_player
    opponent = 3 - current_player
    
    # Check for winning threats (three in a row with space)
    opponent_can_win = False
    
    # Check horizontal threats
    for row in range(board.height):
        for col in range(board.width - 3):
            window = board.board[row, col:col+4]
            if sum(window == opponent) == 3 and sum(window == 0) == 1:
                opponent_can_win = True
                break
        if opponent_can_win:
            break
    
    # Check vertical threats
    if not opponent_can_win:
        for row in range(board.height - 3):
            for col in range(board.width):
                window = board.board[row:row+4, col]
                if sum(window == opponent) == 3 and sum(window == 0) == 1:
                    opponent_can_win = True
                    break
            if opponent_can_win:
                break
    
    # Check diagonal threats (positive slope)
    if not opponent_can_win:
        for row in range(board.height - 3):
            for col in range(board.width - 3):
                window = [board.board[row+i, col+i] for i in range(4)]
                if sum(x == opponent for x in window) == 3 and sum(x == 0 for x in window) == 1:
                    opponent_can_win = True
                    break
            if opponent_can_win:
                break
    
    # Check diagonal threats (negative slope)
    if not opponent_can_win:
        for row in range(3, board.height):
            for col in range(board.width - 3):
                window = [board.board[row-i, col+i] for i in range(4)]
                if sum(x == opponent for x in window) == 3 and sum(x == 0 for x in window) == 1:
                    opponent_can_win = True
                    break
            if opponent_can_win:
                break
    
    if opponent_can_win:
        return -9000  # Almost as bad as losing
    
    # 2. Three in a row with space (weight: 500)
    # Check horizontal threes
    for row in range(board.height):
        for col in range(board.width - 3):
            window = board.board[row, col:col+4]
            # Check for current player's threes
            if sum(window == current_player) == 3 and sum(window == 0) == 1:
                score += 500
            # Check for opponent's threes (higher weight to prioritize blocking)
            if sum(window == opponent) == 3 and sum(window == 0) == 1:
                score -= 750
    
    # Check vertical threes
    for row in range(board.height - 3):
        for col in range(board.width):
            window = board.board[row:row+4, col]
            if sum(window == current_player) == 3 and sum(window == 0) == 1:
                score += 500
            if sum(window == opponent) == 3 and sum(window == 0) == 1:
                score -= 750
    
    # 3. Center column control (weight: 50)
    center = board.width // 2
    for row in range(board.height):
        if board.board[row][center] == current_player:
            score += 50
        elif board.board[row][center] == opponent:
            score -= 50
    
    # 4. Two in a row with empty spaces (weight: 10)
    for row in range(board.height):
        for col in range(board.width - 1):
            if board.board[row][col] == current_player and board.board[row][col + 1] == current_player:
                score += 10
            elif board.board[row][col] == opponent and board.board[row][col + 1] == opponent:
                score -= 10
    
    return score

def maximize(state: ConnectFourBoard, k: int, current_depth: int = 0
             , use_alpha_beta: bool = False, 
             alpha: float = float('-inf'), 
             beta: float = float('inf')):
    
    is_terminal = state.is_full()
    if current_depth == k or is_terminal:
        return None, None, eval(state)
    
    max_move, max_child, max_utility = None, None, float('-inf')

    valid_moves = state.get_valid_moves()
    for move in valid_moves:
        new_board = state.copy()
        new_board.drop_piece(move) # child state 
        
        _, _, utility = minimize(new_board, k, current_depth + 1, use_alpha_beta, alpha, beta)
        if utility > max_utility:
            max_utility = utility
            max_move = move
            max_child = new_board

        if use_alpha_beta:
            if max_utility >= beta:
                break  # Beta cut-off (since alpha >= beta)
            if max_utility > alpha:
                alpha = max_utility
                        
    return max_move, max_child.__str__(), max_utility

def minimize(state: ConnectFourBoard, k: int, current_depth: int = 0,
             use_alpha_beta: bool = False,
             alpha: float = float('-inf'),
             beta: float = float('inf')):
    
    is_terminal = state.is_full()
    if current_depth == k or is_terminal:
        return None, None, eval(state)
    
    min_move, min_child, min_utility = None, None, float('inf')

    valid_moves = state.get_valid_moves()
    for move in valid_moves:
        new_board = state.copy()
        new_board.drop_piece(move)  # child state

        _, _, utility = maximize(new_board, k, current_depth + 1, use_alpha_beta, alpha, beta)
        if utility < min_utility:
            min_utility = utility
            min_move = move
            min_child = new_board

        if use_alpha_beta:
            if min_utility <= alpha:
                break
            if min_utility < beta:
                beta = min_utility

    return min_move, min_child.__str__(), min_utility

def decision(state: ConnectFourBoard, k: int, 
             use_alpha_beta: bool = False, 
             use_expected_minimax: bool = False) -> int:
    if use_alpha_beta:
        alpha = float('-inf')
        beta = float('inf')
        best_move, _, _ = maximize(state, k, 0, True, alpha, beta)

    elif use_expected_minimax:
        best_move, _, _ = expected_max(state, k, 0)
    
    else:
        # Regular minimax without pruning
        best_move, _, _ = maximize(state, k, 0, False)
        
    if best_move is not None:
        return best_move
    else:
        return -1
    

def expected_max(state: ConnectFourBoard, k: int, current_depth: int = 0):
    if current_depth == k or state.is_full():
        return None, None, eval(state)

    best_move = None
    best_child_str = None
    best_expected_utility = float('-inf')

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
            _, _, utility = expected_min(new_state, k, current_depth + 1)
            expected_utility += prob * utility

        if expected_utility > best_expected_utility:
            best_expected_utility = expected_utility
            best_move = move
            best_child_str = new_state.__str__()

    return best_move, best_child_str, best_expected_utility



def expected_min(state: ConnectFourBoard, k: int, current_depth: int = 0):
    if current_depth == k or state.is_full():
        return None, None, eval(state)

    best_move = None
    best_child_str = None
    best_expected_utility = float('inf')

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
            _, _, utility = expected_max(new_state, k, current_depth + 1)
            expected_utility += prob * utility

        if expected_utility < best_expected_utility:
            best_expected_utility = expected_utility
            best_move = move
            best_child_str = new_state.__str__()

    return best_move, best_child_str, best_expected_utility

