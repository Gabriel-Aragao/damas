from copy import deepcopy  # To simulate board changes during captures

def get_valid_moves(board, row, col, chain_capture=False):
    """
    Returns a list of valid moves for the piece at (row, col).
    Each move is a tuple (target_row, target_col, move_value, captured_positions) where:
      • move_value == 0 for a normal (non-capturing) move,
      • a positive integer indicates the total number of opponents captured along the chain,
      • or the string "end" indicates the option to end a capture chain.
    captured_positions is a list of (row, col) for pieces captured along the route.
    When chain_capture is True only capturing moves (and the optional "end"
    move, if captures exist) are returned.
    """
    moves = []
    piece = board[row][col]
    if piece == '.':
        return moves

    board_size = len(board)
    is_king = piece.isupper()

    if chain_capture:
        captures = get_piece_captures(board, row, col)
        if captures:
            for cap in captures:
                moves.append(cap)
            # Only add the "end" move if there is at least one capture option.
            moves.append((row, col, "end", []))
    else:
        # Non-capturing moves:
        if is_king:
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
            for dr, dc in directions:
                r, c = row + dr, col + dc
                while 0 <= r < board_size and 0 <= c < board_size and board[r][c] == '.':
                    moves.append((r, c, 0, []))
                    r += dr
                    c += dc
        else:
            if piece.lower() == 'r':
                directions = [(-1, -1), (-1, 1)]
            else:
                directions = [(1, -1), (1, 1)]
            for dr, dc in directions:
                r, c = row + dr, col + dc
                if 0 <= r < board_size and 0 <= c < board_size and board[r][c] == '.':
                    moves.append((r, c, 0, []))
        # Also add capturing moves.
        captures = get_piece_captures(board, row, col)
        capture_moves = {}
        for cap in captures:
            dest = (cap[0], cap[1])
            count = cap[2]
            captured = cap[3]
            if dest not in capture_moves or (isinstance(count, int) and count > capture_moves[dest][2]):
                capture_moves[dest] = (cap[0], cap[1], count, captured)
        for move in capture_moves.values():
            moves.append(move)
    return moves

def get_piece_captures(board, row, col):
    """
    Returns a list of capturing moves for the piece at (row, col).
    Each move is a tuple (end_row, end_col, capture_count, captured_positions)
    representing the landing square after one or more jumps,
    the total captures count, and the list of captured piece positions.
    """
    piece = board[row][col]
    if piece == '.':
        return []
    return _get_multi_captures(board, row, col, piece)

def _get_multi_captures(board, row, col, piece):
    """
    Recursive helper to compute capture moves that may include multiple jumps.
    Returns a list of moves as tuples: (end_row, end_col, capture_count, captured_positions).
    """
    board_size = len(board)
    moves = []
    opponent = 'b' if piece.lower() == 'r' else 'r'

    if piece.isupper():
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            found_opponent = False
            captured_r, captured_c = None, None
            while 0 <= r < board_size and 0 <= c < board_size:
                if not found_opponent:
                    if board[r][c] == '.':
                        r += dr
                        c += dc
                        continue
                    elif board[r][c].lower() == opponent:
                        found_opponent = True
                        captured_r, captured_c = r, c
                        r += dr
                        c += dc
                        continue
                    else:
                        break
                else:
                    if board[r][c] == '.':
                        new_board = deepcopy(board)
                        new_board[row][col] = '.'
                        new_board[captured_r][captured_c] = '.'
                        new_board[r][c] = piece
                        subsequent = _get_multi_captures(new_board, r, c, piece)
                        if subsequent:
                            for move in subsequent:
                                moves.append((move[0], move[1], move[2] + 1, [(captured_r, captured_c)] + move[3]))
                        else:
                            moves.append((r, c, 1, [(captured_r, captured_c)]))
                        r += dr
                        c += dc
                    else:
                        break
    else:
        # Regular piece capturing.
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dr, dc in directions:
            mid_r, mid_c = row + dr, col + dc
            end_r, end_c = row + 2 * dr, col + 2 * dc
            if (0 <= mid_r < board_size and 0 <= mid_c < board_size and
                0 <= end_r < board_size and 0 <= end_c < board_size):
                if board[mid_r][mid_c] != '.' and board[mid_r][mid_c].lower() == opponent and board[end_r][end_c] == '.':
                    new_board = deepcopy(board)
                    new_board[row][col] = '.'
                    new_board[mid_r][mid_c] = '.'
                    new_board[end_r][end_c] = piece
                    subsequent = _get_multi_captures(new_board, end_r, end_c, piece)
                    if subsequent:
                        for move in subsequent:
                            moves.append((move[0], move[1], move[2] + 1, [(mid_r, mid_c)] + move[3]))
                    else:
                        moves.append((end_r, end_c, 1, [(mid_r, mid_c)]))
    return moves

def has_captures_available(board, current_player):
    """
    Checks if any piece belonging to the current player has a valid capturing move.
    """
    board_size = len(board)
    for r in range(board_size):
        for c in range(board_size):
            piece = board[r][c]
            if (piece != '.' and 
                ((current_player == 'RED' and piece.lower() == 'r') or 
                 (current_player == 'BLACK' and piece.lower() == 'b'))):
                if get_piece_captures(board, r, c):
                    return True
    return False