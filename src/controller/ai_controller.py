from copy import deepcopy  # To create independent board states during search
from src.model.game_state import update_game_state  # Use standard state update logic
from src.model import moves  # Use move-generation utilities

# Evaluation function: returns a score from AI's (BLACK) perspective.
def evaluate_state(game_state):
    board = game_state['board']
    red_val = 0
    black_val = 0
    # Count pieces – kings count as 1.5 points.
    for row in board:
        for cell in row:
            if cell.lower() == 'r':
                if cell.isupper():
                    red_val += 1.5
                else:
                    red_val += 1
            elif cell.lower() == 'b':
                if cell.isupper():
                    black_val += 1.5
                else:
                    black_val += 1
    return black_val - red_val  # Positive means advantage for BLACK (AI)

# Helper function to generate all valid moves for a player.
def get_all_valid_moves(game_state, player):
    moves_list = []
    board = game_state['board']
    board_size = len(board)
    # If a capture chain is in progress, use only the pre‐stored moves.
    if game_state.get('selected_piece') is not None:
        from_pos = game_state['selected_piece']
        valid_moves = game_state.get('valid_moves', [])
        for move in valid_moves:
            moves_list.append((from_pos, move))
        return moves_list
    # Otherwise, scan the board for pieces belonging to the player.
    for r in range(board_size):
        for c in range(board_size):
            piece = board[r][c]
            if player == 'BLACK' and piece.lower() == 'b':
                piece_moves = moves.get_valid_moves(board, r, c)
                if piece_moves:
                    for m in piece_moves:
                        moves_list.append(((r, c), m))
            elif player == 'RED' and piece.lower() == 'r':
                piece_moves = moves.get_valid_moves(board, r, c)
                if piece_moves:
                    for m in piece_moves:
                        moves_list.append(((r, c), m))
    return moves_list

# Minimax algorithm with fixed search depth.
def minimax(state, depth, maximizing):
    # If depth is zero or the game is over, return the heuristic evaluation.
    if depth == 0 or state['game_over']:
        return evaluate_state(state), None

    if maximizing:
        max_eval = float('-inf')
        best_move = None
        # AI (BLACK) attempts to maximize its score.
        possible_moves = get_all_valid_moves(state, 'BLACK')
        if not possible_moves:
            return evaluate_state(state), None
        for from_pos, move in possible_moves:
            new_state = deepcopy(state)  # Copy state for simulation
            new_state['selected_piece'] = from_pos
            update_game_state(new_state, move)
            eval_score, _ = minimax(new_state, depth - 1, False)
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = (from_pos, move)
        return max_eval, best_move
    else:
        min_eval = float('inf')
        best_move = None
        # Opponent (RED) minimizes AI's score.
        possible_moves = get_all_valid_moves(state, 'RED')
        if not possible_moves:
            return evaluate_state(state), None
        for from_pos, move in possible_moves:
            new_state = deepcopy(state)
            new_state['selected_piece'] = from_pos
            update_game_state(new_state, move)
            eval_score, _ = minimax(new_state, depth - 1, True)
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = (from_pos, move)
        return min_eval, best_move

# Returns the best move (as a tuple: (from_pos, move)) by searching to a fixed depth.
def calculate_ai_move(game_state, depth=1):
    score, best_move = minimax(game_state, depth, True)
    return best_move

# This function directly applies the chosen move on the real game state.
def handle_ai_turn(game_state):
    print("[LOG] AI turn started")
    best_move = calculate_ai_move(game_state, depth=1)
    if best_move is not None:
        from_pos, move = best_move
        # Set the selected piece for proper update processing.
        game_state['selected_piece'] = from_pos
        game_state['valid_moves'] = [move]  # Temporarily store the chosen move for update
        update_game_state(game_state, move)
        print(f"[LOG] AI performed move from {from_pos} to {(move[0], move[1])}")
    else:
        print("[LOG] AI has no valid moves")
    print("[LOG] AI turn ended")