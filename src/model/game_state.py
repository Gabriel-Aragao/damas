from .board import create_board, initialize_pieces, make_move, get_winner
from .moves import get_valid_moves, get_piece_captures, has_captures_available

def initialize_game():
    """Creates and returns the initial game state."""
    game_state = {
        'board': initialize_pieces(create_board()),
        'current_player': 'RED',
        'selected_piece': None,
        'game_over': False,
        'winner': None,
        'valid_moves': [],
        'must_capture': False,
        'last_move': None
    }
    return game_state

def update_game_state(game_state, start_pos, end_pos):
    """
    Updates the game state based on a move, with optional capture chaining.
    (Capture is not forced; if additional captures are available they are shown
    and the player may choose to chain or end the turn.)
    """
    board = game_state['board']
    start_row, start_col = start_pos
    end_row, end_col = end_pos
    
    # Determine if the move is a capturing move (covers more than one square)
    was_capture = abs(end_row - start_row) > 1
    
    # Execute the move; updated make_move supports multi–square king moves and captures.
    make_move(board, start_row, start_col, end_row, end_col)
    
    # Update last move
    game_state['last_move'] = (start_pos, end_pos)
    
    # Check for game over
    winner = get_winner(board)
    if winner:
        game_state['game_over'] = True
        game_state['winner'] = winner
        return True
    
    # OPTIONAL CAPTURE:
    # Check if additional capturing moves are available from the new position.
    additional_captures = get_piece_captures(board, end_row, end_col)
    if additional_captures:
        game_state['selected_piece'] = (end_row, end_col)
        game_state['valid_moves'] = additional_captures
        game_state['must_capture'] = True
        # The player may choose to continue capturing or end the turn.
    
    # End turn: clear selection and switch players if not chaining capture.
    game_state['selected_piece'] = None
    game_state['valid_moves'] = []
    game_state['must_capture'] = False
    game_state['current_player'] = 'BLACK' if game_state['current_player'] == 'RED' else 'RED'
    
    return was_capture

def select_piece(game_state, row, col):
    """Selects a piece and retrieves its valid moves."""
    board = game_state['board']
    piece = board[row][col]
    
    # Check if the selected square contains a valid piece.
    if piece == '.' or (game_state['current_player'] == 'RED' and piece.lower() == 'b') or \
       (game_state['current_player'] == 'BLACK' and piece.lower() == 'r'):
        return False
    
    # Get valid moves (both simple and capturing moves).
    valid_moves = get_valid_moves(board, row, col)
    if not valid_moves:
        return False
    
    game_state['selected_piece'] = (row, col)
    game_state['valid_moves'] = valid_moves
    game_state['must_capture'] = has_captures_available(board, game_state['current_player'])
    
    return True

def get_game_status(game_state):
    """Returns the current status of the game."""
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
    """Checks if the piece at (row, col) can be selected."""
    if game_state['game_over']:
        return False
    
    piece = game_state['board'][row][col]
    if piece == '.':
        return False
    
    allowed = (game_state['current_player'] == 'RED' and piece.lower() == 'r') or \
              (game_state['current_player'] == 'BLACK' and piece.lower() == 'b')
    return allowed