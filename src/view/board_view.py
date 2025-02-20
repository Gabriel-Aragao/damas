import pygame
from config.settings import *
from config.constants import *

def draw_board(screen):
    """Draw the checkerboard pattern."""
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            # Calculate square position
            x = col * SQUARE_SIZE
            y = row * SQUARE_SIZE
            
            # Alternate colors for checkerboard pattern
            # White squares are unplayable, dark squares are playable
            color = COLORS['BOARD_LIGHT'] if (row + col) % 2 == 0 else COLORS['BOARD_DARK']
            
            # Draw square
            pygame.draw.rect(screen, color, (x, y, SQUARE_SIZE, SQUARE_SIZE))
            
            # Draw coordinates if debug mode is on
            if DEBUG_MODE and SHOW_COORDINATES:
                font = pygame.font.SysFont('Arial', 12)
                text = font.render(f'({row},{col})', True, (128, 128, 128))
                screen.blit(text, (x + 5, y + 5))

def draw_pieces(screen, board):
    """Draw all pieces on the board."""
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            piece = board[row][col]
            # Only draw if it's a valid piece (not empty or unplayable)
            if piece not in ['.', 'e']:
                draw_piece(screen, piece, row, col)

def draw_piece(screen, piece, row, col):
    """Draw a single piece."""
    x = col * SQUARE_SIZE + SQUARE_SIZE // 2
    y = row * SQUARE_SIZE + SQUARE_SIZE // 2
    radius = (SQUARE_SIZE // 2) - PIECE_PADDING
    
    # Determine piece color
    color = COLORS['RED_PIECE'] if piece.lower() == 'r' else COLORS['BLACK_PIECE']
    
    # Draw the main piece circle
    pygame.draw.circle(screen, color, (x, y), radius)
    
    # Draw king indicator if the piece is a king
    if piece.isupper():
        crown_radius = radius - 10
        pygame.draw.circle(screen, COLORS['BOARD_LIGHT'], (x, y), crown_radius)
        pygame.draw.circle(screen, color, (x, y), crown_radius - 5)

def highlight_square(screen, row, col, color):
    """Highlight a square with a semi-transparent color."""
    if (row + col) % 2 == 1:
        surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
        pygame.draw.rect(surface, color, surface.get_rect())
        screen.blit(surface, (col * SQUARE_SIZE, row * SQUARE_SIZE))

def highlight_selected(screen, row, col):
    """Highlight the selected piece."""
    highlight_square(screen, row, col, COLORS['SELECTED'])

def highlight_valid_moves(screen, valid_moves):
    """
    Highlight all valid moves.
    For a normal move (capture_val is 0 or a positive integer) a green circle is drawn.
    If the move's capture_val is a positive number the number of captured pieces is shown.
    If capture_val is "end", the word 'end' is drawn over the selected piece
    to indicate the option to end the capturing chain.
    """
    if not SHOW_VALID_MOVES:
        return
    
    for move in valid_moves:
        # Unpack the 4-tuple: destination row, destination col, capture value, captured_positions (ignored)
        row, col, capture_val, _ = move
        x = col * SQUARE_SIZE + SQUARE_SIZE // 2
        y = row * SQUARE_SIZE + SQUARE_SIZE // 2
        radius = SQUARE_SIZE // 4
        
        if capture_val == "end":
            # Draw the "end" option over the piece itself
            font = pygame.font.SysFont('Arial', radius)
            text = font.render("end", True, (255, 255, 255))
            text_rect = text.get_rect(center=(x, y))
            screen.blit(text, text_rect)
        else:
            # Draw a green circle indicating a valid move destination
            surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(surface, COLORS['VALID_MOVE'], (radius, radius), radius)
            screen.blit(surface, (x - radius, y - radius))
            # If this is a capturing move, display the number of pieces captured.
            if isinstance(capture_val, int) and capture_val > 0:
                font = pygame.font.SysFont('Arial', radius)
                text = font.render(str(capture_val), True, (255, 255, 255))
                text_rect = text.get_rect(center=(x, y))
                screen.blit(text, text_rect)

def highlight_last_move(screen, last_move):
    """Highlight the last move made."""
    if not SHOW_LAST_MOVE or not last_move:
        return
    start_pos, end_pos = last_move
    highlight_square(screen, start_pos[0], start_pos[1], (*COLORS['HIGHLIGHT'][:3], 60))
    highlight_square(screen, end_pos[0], end_pos[1], (*COLORS['HIGHLIGHT'][:3], 60))

def render_game_state(screen, game_state):
    """Render the complete game state."""
    draw_board(screen)
    draw_pieces(screen, game_state['board'])
    
    if game_state['selected_piece']:
        row, col = game_state['selected_piece']
        highlight_selected(screen, row, col)
    
    highlight_valid_moves(screen, game_state['valid_moves'])
    highlight_last_move(screen, game_state['last_move'])
    
    pygame.display.flip()

def draw_game_over(screen, winner):
    """Draw the game over screen."""
    surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    surface.fill((0, 0, 0, 128))  # Semi-transparent overlay
    screen.blit(surface, (0, 0))
    
    font = pygame.font.SysFont('Arial', 48)
    text = font.render(f'{winner} Wins!', True, COLORS['BOARD_LIGHT'])
    text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
    screen.blit(text, text_rect)
    
    pygame.display.flip()