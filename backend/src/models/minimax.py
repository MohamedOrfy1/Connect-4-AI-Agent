from board import ConnectFourBoard

def eval(board: ConnectFourBoard) -> int:
    ### Need heuristic
    # winner = board.check_winner()
    # if winner == 1:
    #     return 1000
    # elif winner == 2:
    #     return -1000
    # return board.count_fours(1) - board.count_fours(2)
    pass

def maximize(state: ConnectFourBoard, k: int, current_depth: int = 0) :
    is_terminal = state.is_full()
    if current_depth == k or is_terminal:
        return None, None, eval(state)
    
    max_move, max_child, max_utility = None, None, float('-inf')

    valid_moves = state.get_valid_moves()
    for move in valid_moves:
        new_board = state.copy()
        new_board.drop_piece(move) # child state 

        _, _, utility = minimize(new_board, k, current_depth + 1)
        if utility > max_utility:
            max_utility = utility
            max_move = move ## could store moves
            max_child = new_board ## store state in strings
        
    return max_move, max_child.__str__(), max_utility

def minimize(state: ConnectFourBoard, k: int, current_depth: int = 0):
    is_terminal = state.is_full()
    if current_depth == k or is_terminal:
        return None, None, eval(state)
    
    min_move, min_child, min_utility = None, None, float('inf')

    valid_moves = state.get_valid_moves()
    for move in valid_moves:
        new_board = state.copy()
        new_board.drop_piece(move)  # child state

        _, _, utility = maximize(new_board, k, current_depth + 1)
        if utility < min_utility:
            min_utility = utility
            min_move = move  # Best move
            min_child = new_board  # Best board state

    return min_move, min_child.__str__(), min_utility

def decision(state: ConnectFourBoard, k: int):
    best_move, _, _ = maximize(state, k)
    if best_move is not None:
        return best_move
    else:
        return -1
    


board = ConnectFourBoard()
search_depth = 3  # AI search depth

while True:
    print("\nCurrent Board:")
    print(board)

    # Check if game is over
    winner = board.check_winner()
    if winner:
        print("Player X (AI) wins!" if winner == 1 else "Player O (You) win!")
        break
    if board.is_full():
        print("It's a draw!")
        break

    # Player's turn
    if board.current_player == 2:
        while True:
            try:
                col = int(input("Enter your move (0-4): "))
                if col in board.get_valid_moves():
                    board.drop_piece(col)
                    break
                else:
                    print("Invalid move. Try again.")
            except ValueError:
                print("Enter a number between 0-4.")
    else:
        # AI's turn
        ai_move = decision(board, search_depth)
        print(f"AI chooses column {ai_move}")
        board.drop_piece(ai_move)
