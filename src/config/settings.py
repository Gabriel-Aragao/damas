# Game Settings
WINDOW_TITLE = "Checkers Game"
FPS = 60
ANIMATION_SPEED = 5

# Board Settings
BOARD_SIZE = 8
SQUARE_SIZE = 80
PIECE_PADDING = 10  # Space between piece and square edge

# Display Settings
WINDOW_WIDTH = BOARD_SIZE * SQUARE_SIZE
WINDOW_HEIGHT = BOARD_SIZE * SQUARE_SIZE
SHOW_VALID_MOVES = True
SHOW_LAST_MOVE = True

# Colors
COLORS = {
    'BOARD_LIGHT': (255, 255, 255),  # White squares
    'BOARD_DARK': (64, 64, 64),      # Dark gray squares
    'RED_PIECE': (220, 20, 60),      # Red pieces
    'BLACK_PIECE': (0, 0, 0),        # Black pieces
    'HIGHLIGHT': (255, 255, 0, 128), # Yellow highlight with transparency
    'VALID_MOVE': (0, 255, 0, 128),  # Green dots for valid moves
    'SELECTED': (0, 0, 255, 128)     # Blue highlight for selected piece
}

# Game Rules
FORCE_CAPTURE = True  # Force player to capture when possible
MULTIPLE_JUMPS = False # Allow multiple captures in one turn
KINGS_MOVE_MULTIPLE = True  # Allow kings to move multiple squares

# AI Settings
AI_DIFFICULTY = 3  # Default difficulty (1-5) - controls minimax depth

# Debug Settings
DEBUG_MODE = False
SHOW_COORDINATES = False