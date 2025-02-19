def create_board():
    """
    Creates an 8x8 board where each square is initialized to '.' (empty).
    """
    board = [['.' for _ in range(8)] for _ in range(8)]
    return board

def initialize_pieces(board):
    """
    Sets up the initial pieces on the board.
    Red pieces ('r') are placed on the bottom rows and Black pieces ('b') on the top rows.
    Pieces occupy only playable squares ((row + col) % 2 != 0).
    """
    for row in range(8):
        for col in range(8):
            if (row + col) % 2 != 0:
                if row < 3:
                    board[row][col] = 'b'
                elif row > 4:
                    board[row][col] = 'r'
    return board

def make_move(board, start_row, start_col, end_row, end_col):
    """
    Moves a piece from (start_row, start_col) to (end_row, end_col).
    Supports:
      • Flying king moves: king pieces can travel multiple squares along a diagonal.
      • Capturing: if an opponent piece is jumped over, it is removed.
    The function traverses the move path along its diagonal and removes a single captured piece.
    """
    piece = board[start_row][start_col]
    board[start_row][start_col] = '.'
    dr = end_row - start_row
    dc = end_col - start_col
    abs_dr = abs(dr)
    abs_dc = abs(dc)
    
    # Ensure the move is diagonal.
    if abs_dr != abs_dc:
        print("Invalid move: Not a diagonal move")
        return
    
    # For king moves or any move spanning more than one square, check the path.
    if piece.isupper() or abs_dr > 1:
        step_r = dr // abs_dr  # Unit step for row.
        step_c = dc // abs_dc  # Unit step for column.
        r, c = start_row + step_r, start_col + step_c
        captured = False
        while (r, c) != (end_row, end_col):
            if board[r][c] != '.':
                if captured:
                    print("Invalid move: More than one piece encountered along the path")
                    return
                if board[r][c].lower() != piece.lower():
                    # Capture the opponent piece encountered along the diagonal.
                    board[r][c] = '.'
                    captured = True
                else:
                    print("Invalid move: Cannot jump over your own piece")
                    return
            r += step_r
            c += step_c
    else:
        # For a simple capture move spanning two squares.
        if abs_dr == 2:
            mid_row = (start_row + end_row) // 2
            mid_col = (start_col + end_col) // 2
            board[mid_row][mid_col] = '.'
    
    # Place the moving piece at the destination.
    board[end_row][end_col] = piece
    
    # Promote to king if the piece reaches the opposite end.
    if piece == 'r' and end_row == 0:
        board[end_row][end_col] = 'R'
    elif piece == 'b' and end_row == len(board) - 1:
        board[end_row][end_col] = 'B'

def get_winner(board):
    """
    Determines the winner of the game based on the remaining pieces.
    Returns 'RED' if only red pieces remain, 'BLACK' if only black pieces remain,
    or None if both are present.
    """
    red_exists = any(piece.lower() == 'r' for row in board for piece in row)
    black_exists = any(piece.lower() == 'b' for row in board for piece in row)
    if not red_exists:
        return 'BLACK'
    elif not black_exists:
        return 'RED'
    return None