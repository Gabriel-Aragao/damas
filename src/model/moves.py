def get_valid_moves(board, row, col):
    """
    Returns a list of valid move destinations for the piece at (row, col).
    Includes both non–capturing moves and capturing moves (capture is optional).
    For king pieces, allows multi–square moves ("flying kings").
    """
    moves = []
    piece = board[row][col]
    if piece == '.':
        return moves

    is_king = piece.isupper()
    board_size = len(board)
    
    if is_king:
        # King pieces can move along all four diagonals until blocked.
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            while 0 <= r < board_size and 0 <= c < board_size and board[r][c] == '.':
                moves.append((r, c))
                r += dr
                c += dc
    else:
        # Regular pieces: non–capturing moves move in the forward direction.
        if piece.lower() == 'r':  # Red moves upward.
            directions = [(-1, -1), (-1, 1)]
        else:  # Black moves downward.
            directions = [(1, -1), (1, 1)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < board_size and 0 <= c < board_size and board[r][c] == '.':
                moves.append((r, c))
                
    # Include capturing moves (optional for the player).
    captures = get_piece_captures(board, row, col)
    for cap in captures:
        if cap not in moves:
            moves.append(cap)
    
    return moves

def get_piece_captures(board, row, col):
    """
    Returns a list of capturing move destinations for the piece at (row, col).
    All pieces can capture backwards.
    For kings, multiple-square moves are allowed if an opponent piece is jumped over.
    """
    captures = []
    piece = board[row][col]
    if piece == '.':
        return captures
    
    is_king = piece.isupper()
    board_size = len(board)
    # Determine the opponent's piece (lowercase).
    opponent = 'b' if piece.lower() == 'r' else 'r'
    # Check all four diagonals.
    directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    
    if is_king:
        # Kings scan each diagonal until blocked.
        for dr, dc in directions:
            r, c = row + dr, col + dc
            found_opponent = False
            while 0 <= r < board_size and 0 <= c < board_size:
                if board[r][c] == '.':
                    if found_opponent:
                        # Valid landing square after capturing an opponent.
                        captures.append((r, c))
                    r += dr
                    c += dc
                elif board[r][c].lower() == piece.lower():
                    # Blocked by own piece.
                    break
                elif board[r][c].lower() == opponent:
                    if not found_opponent:
                        found_opponent = True
                        r += dr
                        c += dc
                    else:
                        # Cannot capture more than one piece in a single jump in this direction.
                        break
                else:
                    break
    else:
        # Regular pieces: check for a single jump capture in all four diagonal directions.
        for dr, dc in directions:
            mid_r, mid_c = row + dr, col + dc
            end_r, end_c = row + 2 * dr, col + 2 * dc
            if (0 <= mid_r < board_size and 0 <= mid_c < board_size and
                0 <= end_r < board_size and 0 <= end_c < board_size):
                mid_piece = board[mid_r][mid_c]
                if mid_piece != '.' and mid_piece.lower() == opponent and board[end_r][end_c] == '.':
                    captures.append((end_r, end_c))
    
    return captures

def has_captures_available(board, current_player):
    """
    Checks if any piece belonging to the current player has a valid capturing move.
    This flag is informational; capture is optional.
    """
    board_size = len(board)
    for r in range(board_size):
        for c in range(board_size):
            piece = board[r][c]
            if piece != '.' and ((current_player == 'RED' and piece.lower() == 'r') or 
                                 (current_player == 'BLACK' and piece.lower() == 'b')):
                if get_piece_captures(board, r, c):
                    return True
    return False