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
            # White squares are unplayable (marked as '.' in board matrix)
            # Dark squares are playable (marked as 'e' or contain pieces)
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
            # Only draw if it's a piece (not empty 'e' or unplayable '.')
            if piece not in ['.', 'e']:
                draw_piece(screen, piece, row, col)

def draw_piece(screen, piece, row, col):
    """Draw a single piece."""
    x = col * SQUARE_SIZE + SQUARE_SIZE // 2
    y = row * SQUARE_SIZE + SQUARE_SIZE // 2
    radius = (SQUARE_SIZE // 2) - PIECE_PADDING
    
    # Determine piece color
    color = COLORS['RED_PIECE'] if piece.lower() == 'r' else COLORS['BLACK_PIECE']
    
    # Draw main piece circle
    pygame.draw.circle(screen, color, (x, y), radius)
    
    # Draw king indicator if piece is a king
    if piece.isupper():
        # Draw crown
        crown_radius = radius - 10
        pygame.draw.circle(screen, COLORS['BOARD_LIGHT'], (x, y), crown_radius)
        pygame.draw.circle(screen, color, (x, y), crown_radius - 5)

def highlight_square(screen, row, col, color):
    """Highlight a square with semi-transparent color."""
    # Only highlight squares that are playable (black squares)
    if (row + col) % 2 == 1:
        surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
        pygame.draw.rect(surface, color, surface.get_rect())
        screen.blit(surface, (col * SQUARE_SIZE, row * SQUARE_SIZE))

def highlight_selected(screen, row, col):
    """Highlight the selected piece."""
    highlight_square(screen, row, col, COLORS['SELECTED'])

def highlight_valid_moves(screen, valid_moves):
    """Highlight all valid moves."""
    if not SHOW_VALID_MOVES:
        return
        
    for row, col in valid_moves:
        # Only highlight squares that are playable (black squares)
        if (row + col) % 2 == 1:
            # Draw semi-transparent circle for valid move
            x = col * SQUARE_SIZE + SQUARE_SIZE // 2
            y = row * SQUARE_SIZE + SQUARE_SIZE // 2
            radius = SQUARE_SIZE // 4
            
            surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(surface, COLORS['VALID_MOVE'], (radius, radius), radius)
            screen.blit(surface, (x - radius, y - radius))

def highlight_last_move(screen, last_move):
    """Highlight the last move made."""
    if not SHOW_LAST_MOVE or not last_move:
        return
        
    start_pos, end_pos = last_move
    highlight_square(screen, start_pos[0], start_pos[1], (*COLORS['HIGHLIGHT'][:3], 60))
    highlight_square(screen, end_pos[0], end_pos[1], (*COLORS['HIGHLIGHT'][:3], 60))

def render_game_state(screen, game_state):
    """Render the complete game state."""
    # Draw base board
    draw_board(screen)
    
    # Draw pieces
    draw_pieces(screen, game_state['board'])
    
    # Highlight selected piece if any
    if game_state['selected_piece']:
        row, col = game_state['selected_piece']
        highlight_selected(screen, row, col)
        
        # Show valid moves for selected piece
        highlight_valid_moves(screen, game_state['valid_moves'])
    
    # Highlight last move
    highlight_last_move(screen, game_state['last_move'])
    
    # Update display
    pygame.display.flip()

def draw_game_over(screen, winner):
    """Draw game over screen."""
    surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    surface.fill((0, 0, 0, 128))  # Semi-transparent black
    screen.blit(surface, (0, 0))
    
    font = pygame.font.SysFont('Arial', 48)
    text = font.render(f'{winner} Wins!', True, COLORS['BOARD_LIGHT'])
    text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
    screen.blit(text, text_rect)
    
    pygame.display.flip()