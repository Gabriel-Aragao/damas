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
        'last_move': None,
        'game_over': False,
        'winner': None,
        'must_capture': False,
    }
    return game_state

def update_game_state(game_state, move):
    """
    Update the game state after a move is executed.
    The move is a 4-tuple: (dest_row, dest_col, move_value, captured_positions),
      • move_value == 0 indicates a non‐capturing move,
      • a positive integer indicates a capturing move (the total capture count),
      • and "end" indicates the player has chosen to end his capturing chain.
      
    - For non‐capturing moves, the piece is moved, promotion is checked,
      selection is cleared, and the turn switches.
    - For capturing moves, all jumped pieces (listed in captured_positions) are removed from the board.
      After the move, promotion is checked. If further captures are available from the new position,
      the piece remains selected (with valid chain‐capture moves, including an optional "end" move);
      otherwise, the selection is cleared and the turn is switched.
    - For an "end" move, the capture chain is terminated and the turn passes to the opponent.
    Finally, the board is scanned to see if one color has no pieces left – if so, the game ends.
    """
    # Get the starting square of the move.
    selected = game_state.get('selected_piece')
    if not selected:
        return game_state  # Nothing to do if no piece is selected.
    
    dest_row, dest_col, move_value, captured_positions = move
    board = game_state['board']
    piece = board[selected[0]][selected[1]]
    
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
    
    if move_value == 0:
        # Non-capturing move: clear selection, switch turn.
        game_state['selected_piece'] = None
        game_state['valid_moves'] = []
        game_state['current_player'] = 'BLACK' if game_state['current_player'] == 'RED' else 'RED'
    
    elif move_value == "end":
        # Ending a capturing chain: clear selection and switch turn.
        game_state['selected_piece'] = None
        game_state['valid_moves'] = []
        game_state['current_player'] = 'BLACK' if game_state['current_player'] == 'RED' else 'RED'
    
    else:
        # Capturing move:
        # Check for further captures from the new position.
        if get_piece_captures(board, dest_row, dest_col):
            game_state['selected_piece'] = (dest_row, dest_col)
            game_state['valid_moves'] = get_valid_moves(board, dest_row, dest_col, chain_capture=True)
        else:
            game_state['selected_piece'] = None
            game_state['valid_moves'] = []
            game_state['current_player'] = 'BLACK' if game_state['current_player'] == 'RED' else 'RED'
    
    # Check if one side has no pieces left.
    check_game_over(game_state)
    
    return game_state

def check_game_over(game_state):
    """
    Scan the board to count pieces. If one side has no remaining pieces, mark game_over True
    and set the winner.
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
    if red_count == 0:
        game_state['game_over'] = True
        game_state['winner'] = 'BLACK'
    elif black_count == 0:
        game_state['game_over'] = True
        game_state['winner'] = 'RED'

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