from .board import create_board, initialize_pieces, make_move, get_winner
from .moves import get_valid_moves, get_piece_captures, has_captures_available

def initialize_game():
    """
    Initialize the game state.
    The board is created via create_board() and initialized with pieces using initialize_pieces().
    """
    board = create_board()                  # Create board with proper dimensions
    board = initialize_pieces(board)        # Place initial pieces on the board
    game_state = {
        'board': board,
        'current_player': 'RED',            # or 'BLACK'
        'selected_piece': None,
        'valid_moves': [],
        'original_valid_moves': [],         # Stores the valid moves from the original position
        'last_move': None,
        'game_over': False,
        'winner': None,
        'must_capture': False,
    }
    return game_state

def update_game_state(game_state, move):
    """
    Update the game state after a move is executed.
    The move is a 4-tuple: (dest_row, dest_col, move_value, captured_positions).
    - move_value == 0 indicates a non-capturing move.
    - A positive integer indicates a capturing move (the number of pieces captured).
    
    For partial captures, the turn ends immediately after the move.
    """
    # Get the starting square of the move.
    selected = game_state.get('selected_piece')
    if not selected:
        return game_state  # Nothing to do if no piece is selected.
    
    dest_row, dest_col, move_value, captured_positions = move
    board = game_state['board']
    piece = board[selected[0]][selected[1]]
    start_row, start_col = selected
    
    # Save the original board state for debugging
    orig_board = [row[:] for row in board]
    
    # Clear the starting square.
    board[selected[0]][selected[1]] = '.'
    
    # If this is a capturing move, remove all captured pieces.
    if captured_positions:
        for pos in captured_positions:
            board[pos[0]][pos[1]] = '.'
    
    # King promotion check:
    # Red pieces are promoted when reaching row 0.
    # Black pieces are promoted when reaching the bottom row.
    board_size = len(board)
    if piece.lower() == 'r' and dest_row == 0:
        piece = 'R'
    elif piece.lower() == 'b' and dest_row == board_size - 1:
        piece = 'B'
    
    # Place the moving piece at its destination.
    board[dest_row][dest_col] = piece
    game_state['last_move'] = (selected, (dest_row, dest_col))
    
    # Flag for whether there are further captures available
    has_further_captures = False
    
    # For capture moves, find the maximum capture from the starting position
    max_capture_from_start = 0
    if move_value > 0:
        # Store original valid_moves to calculate max capture
        original_valid_moves = game_state.get('original_valid_moves', [])
        if not original_valid_moves:
            # If not already stored, use the valid_moves from before this move
            original_valid_moves = game_state.get('valid_moves', [])
            game_state['original_valid_moves'] = original_valid_moves
        
        # Find max capture count from the original position
        for vm in original_valid_moves:
            if isinstance(vm[2], int) and vm[2] > max_capture_from_start:
                max_capture_from_start = vm[2]
        
        # Check if this move has further captures available
        further_captures = get_piece_captures(board, dest_row, dest_col)
        has_further_captures = len(further_captures) > 0
    
    # Direct rule for turn ending:
    # 1. Non-capturing moves always end the turn
    # 2. If this was a partial capture (less than max_capture_from_start), end the turn
    # 3. If there are no further captures available, end the turn
    if move_value == 0 or move_value < max_capture_from_start or not has_further_captures:
        # End the turn
        game_state['selected_piece'] = None
        game_state['valid_moves'] = []
        game_state['original_valid_moves'] = []  # Clear stored moves
        game_state['current_player'] = 'BLACK' if game_state['current_player'] == 'RED' else 'RED'
    else:
        # Only continue capture sequence if this was a maximum capture so far
        # and there are further captures available
        game_state['selected_piece'] = (dest_row, dest_col)
        game_state['valid_moves'] = get_valid_moves(board, dest_row, dest_col, chain_capture=True)
    
    # Check if one side has no pieces left.
    check_game_over(game_state)
    
    return game_state

def has_any_valid_moves(game_state, player):
    """
    Check if a player has any valid moves with any of their pieces.
    Returns True if at least one valid move exists, False otherwise.
    """
    board = game_state['board']
    board_size = len(board)
    piece_char = 'r' if player == 'RED' else 'b'
    
    for row in range(board_size):
        for col in range(board_size):
            piece = board[row][col]
            if piece.lower() == piece_char:
                # Check if this piece has any valid moves
                if get_valid_moves(board, row, col):
                    return True
    return False

def check_game_over(game_state):
    """
    Check if the game is over due to:
    1. One side has no remaining pieces
    2. Current player has no valid moves with any of their pieces
    If game is over, mark game_over True and set the winner.
    """
    board = game_state['board']
    red_count = 0
    black_count = 0
    for row in board:
        for cell in row:
            if cell.lower() == 'r':
                red_count += 1
            elif cell.lower() == 'b':
                black_count += 1
    
    # Check for no pieces condition
    if red_count == 0:
        game_state['game_over'] = True
        game_state['winner'] = 'BLACK'
        return
    elif black_count == 0:
        game_state['game_over'] = True
        game_state['winner'] = 'RED'
        return
    
    # Check for no valid moves condition
    current_player = game_state['current_player']
    if not has_any_valid_moves(game_state, current_player):
        game_state['game_over'] = True
        game_state['winner'] = 'BLACK' if current_player == 'RED' else 'RED'
        return

def select_piece(game_state, row, col):
    """Select a piece and update valid moves."""
    board = game_state['board']
    piece = board[row][col]
    # Must be a valid piece for the current player.
    if piece == '.' or (game_state['current_player'] == 'RED' and piece.lower() == 'b') or \
       (game_state['current_player'] == 'BLACK' and piece.lower() == 'r'):
        return False
    
    valid_moves = get_valid_moves(board, row, col)
    if not valid_moves:
        return False
    
    game_state['selected_piece'] = (row, col)
    game_state['valid_moves'] = valid_moves
    game_state['original_valid_moves'] = valid_moves.copy()  # Store a copy of the original valid moves
    game_state['must_capture'] = has_captures_available(board, game_state['current_player'])
    return True

def get_game_status(game_state):
    """Return the current game status."""
    status = {
        'current_player': game_state['current_player'],
        'game_over': game_state['game_over'],
        'winner': game_state['winner'],
        'selected_piece': game_state['selected_piece'],
        'valid_moves': game_state['valid_moves'],
        'must_capture': game_state['must_capture']
    }
    return status

def can_select_piece(game_state, row, col):
    """Check if the piece at (row, col) can be selected."""
    if game_state['game_over']:
        return False
    
    piece = game_state['board'][row][col]
    if piece == '.':
        return False
    
    allowed = (game_state['current_player'] == 'RED' and piece.lower() == 'r') or \
              (game_state['current_player'] == 'BLACK' and piece.lower() == 'b')
    return allowed

def process_click(game_state, row, col):
    """
    Process a click on the board at (row, col):
      - If a piece is selected and the click matches one of its valid move destinations,
        execute that move.
      - Otherwise, attempt to select a new piece.
    """
    if game_state['selected_piece'] is not None:
        for move in game_state['valid_moves']:
            if move[0] == row and move[1] == col:
                return update_game_state(game_state, move)
        game_state['selected_piece'] = None
        game_state['valid_moves'] = []
        return game_state
    else:
        select_piece(game_state, row, col)
        return game_state