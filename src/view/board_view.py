import pygame
from src.config.settings import *

def draw_board(screen):
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            x = col * SQUARE_SIZE
            y = row * SQUARE_SIZE
            
            color = COLORS['BOARD_LIGHT'] if (row + col) % 2 == 0 else COLORS['BOARD_DARK']

            pygame.draw.rect(screen, color, (x, y, SQUARE_SIZE, SQUARE_SIZE))
            

def draw_pieces(screen, board):

    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            piece = board[row][col]

            if piece not in ['.', 'e']:
                draw_piece(screen, piece, row, col)

def draw_piece(screen, piece, row, col):
    x = col * SQUARE_SIZE + SQUARE_SIZE // 2
    y = row * SQUARE_SIZE + SQUARE_SIZE // 2
    radius = (SQUARE_SIZE // 2) - PIECE_PADDING
    
    color = COLORS['RED_PIECE'] if piece.lower() == 'r' else COLORS['BLACK_PIECE']
    
    pygame.draw.circle(screen, color, (x, y), radius)
    
    if piece.isupper():
        crown_radius = radius - 10
        pygame.draw.circle(screen, COLORS['BOARD_LIGHT'], (x, y), crown_radius)
        pygame.draw.circle(screen, color, (x, y), crown_radius - 5)


def highlight_selected(screen, row, col):
    if (row + col) % 2 == 1:
        surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
        pygame.draw.rect(surface, COLORS['SELECTED'], surface.get_rect())
        screen.blit(surface, (col * SQUARE_SIZE, row * SQUARE_SIZE))


def highlight_valid_moves(screen, valid_moves):
    for move in valid_moves:
        row, col, capture_val, _ = move
        x = col * SQUARE_SIZE + SQUARE_SIZE // 2
        y = row * SQUARE_SIZE + SQUARE_SIZE // 2
        radius = SQUARE_SIZE // 4
        

        # Desenha um círculo verde indicando um destino de movimento válido
        surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(surface, COLORS['VALID_MOVE'], (radius, radius), radius)
        screen.blit(surface, (x - radius, y - radius))
        # Se este for um movimento de captura, exibe o número de peças capturadas
        if isinstance(capture_val, int) and capture_val > 0:
            font = pygame.font.SysFont('Arial', radius)
            text = font.render(str(capture_val), True, (255, 255, 255))
            text_rect = text.get_rect(center=(x, y))
            screen.blit(text, text_rect)

def highlight_last_move(screen, last_move):
    if not last_move:
        return
    start_pos, end_pos = last_move
    highlight_selected(screen, start_pos[0], start_pos[1])
    highlight_selected(screen, end_pos[0], end_pos[1])

def render_game_state(screen, game_state):
    draw_board(screen)
    draw_pieces(screen, game_state['board'])
    
    if game_state['selected_piece']:
        row, col = game_state['selected_piece']
        highlight_selected(screen, row, col)
    
    highlight_valid_moves(screen, game_state['valid_moves'])
    highlight_last_move(screen, game_state['last_move'])
    
    pygame.display.flip()

def draw_game_over(screen, winner):
    surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    surface.fill((0, 0, 0, 128))
    screen.blit(surface, (0, 0))
    
    font = pygame.font.SysFont('Arial', 48)
    text = font.render(f'{winner} vencem!', True, COLORS['BOARD_LIGHT'])
    text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
    screen.blit(text, text_rect)
    
    pygame.display.flip()