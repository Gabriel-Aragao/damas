def create_board():
    board = [['.' for _ in range(8)] for _ in range(8)]
    return board

def initialize_pieces(board):
    for row in range(8):
        for col in range(8):
            if (row + col) % 2 != 0:
                if row < 3:
                    board[row][col] = 'b'
                elif row > 4:
                    board[row][col] = 'r'
    return board
