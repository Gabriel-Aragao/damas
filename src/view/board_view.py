import pygame
from src.config.settings import *
from src.config.constants import *

def draw_board(screen):
    """Desenha o padrão do tabuleiro de damas."""
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            # Calcula a posição do quadrado
            x = col * SQUARE_SIZE
            y = row * SQUARE_SIZE
            
            # Alterna cores para o padrão do tabuleiro
            # Quadrados brancos não são jogáveis, quadrados escuros são jogáveis
            color = COLORS['BOARD_LIGHT'] if (row + col) % 2 == 0 else COLORS['BOARD_DARK']
            
            # Desenha o quadrado
            pygame.draw.rect(screen, color, (x, y, SQUARE_SIZE, SQUARE_SIZE))
            
            # Desenha coordenadas se o modo de depuração estiver ativado
            if DEBUG_MODE and SHOW_COORDINATES:
                font = pygame.font.SysFont('Arial', 12)
                text = font.render(f'({row},{col})', True, (128, 128, 128))
                screen.blit(text, (x + 5, y + 5))

def draw_pieces(screen, board):
    """Desenha todas as peças no tabuleiro."""
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            piece = board[row][col]
            # Só desenha se for uma peça válida (não vazia ou não jogável)
            if piece not in ['.', 'e']:
                draw_piece(screen, piece, row, col)

def draw_piece(screen, piece, row, col):
    """Desenha uma peça individual."""
    x = col * SQUARE_SIZE + SQUARE_SIZE // 2
    y = row * SQUARE_SIZE + SQUARE_SIZE // 2
    radius = (SQUARE_SIZE // 2) - PIECE_PADDING
    
    # Determina a cor da peça
    color = COLORS['RED_PIECE'] if piece.lower() == 'r' else COLORS['BLACK_PIECE']
    
    # Desenha o círculo principal da peça
    pygame.draw.circle(screen, color, (x, y), radius)
    
    # Desenha o indicador de dama se a peça for uma dama
    if piece.isupper():
        crown_radius = radius - 10
        pygame.draw.circle(screen, COLORS['BOARD_LIGHT'], (x, y), crown_radius)
        pygame.draw.circle(screen, color, (x, y), crown_radius - 5)

def highlight_square(screen, row, col, color):
    """Destaca um quadrado com uma cor semi-transparente."""
    if (row + col) % 2 == 1:
        surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
        pygame.draw.rect(surface, color, surface.get_rect())
        screen.blit(surface, (col * SQUARE_SIZE, row * SQUARE_SIZE))

def highlight_selected(screen, row, col):
    """Destaca a peça selecionada."""
    highlight_square(screen, row, col, COLORS['SELECTED'])

def highlight_valid_moves(screen, valid_moves):
    """
    Destaca todos os movimentos válidos.
    Para um movimento normal (capture_val é 0 ou um número positivo) um círculo verde é desenhado.
    Se o capture_val do movimento for um número positivo, o número de peças capturadas é mostrado.
    Se capture_val for "end", a palavra 'fim' é desenhada sobre a peça selecionada
    para indicar a opção de encerrar a sequência de capturas.
    """
    if not SHOW_VALID_MOVES:
        return
    
    for move in valid_moves:
        # Desempacota a tupla de 4 elementos: linha de destino, coluna de destino, valor de captura, posições capturadas (ignoradas)
        row, col, capture_val, _ = move
        x = col * SQUARE_SIZE + SQUARE_SIZE // 2
        y = row * SQUARE_SIZE + SQUARE_SIZE // 2
        radius = SQUARE_SIZE // 4
        
        if capture_val == "end":
            # Desenha a opção "fim" sobre a própria peça
            font = pygame.font.SysFont('Arial', radius)
            text = font.render("fim", True, (255, 255, 255))
            text_rect = text.get_rect(center=(x, y))
            screen.blit(text, text_rect)
        else:
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
    """Destaca o último movimento feito."""
    if not SHOW_LAST_MOVE or not last_move:
        return
    start_pos, end_pos = last_move
    highlight_square(screen, start_pos[0], start_pos[1], (*COLORS['HIGHLIGHT'][:3], 60))
    highlight_square(screen, end_pos[0], end_pos[1], (*COLORS['HIGHLIGHT'][:3], 60))

def render_game_state(screen, game_state):
    """Renderiza o estado completo do jogo."""
    draw_board(screen)
    draw_pieces(screen, game_state['board'])
    
    if game_state['selected_piece']:
        row, col = game_state['selected_piece']
        highlight_selected(screen, row, col)
    
    highlight_valid_moves(screen, game_state['valid_moves'])
    highlight_last_move(screen, game_state['last_move'])
    
    pygame.display.flip()

def draw_game_over(screen, winner):
    """Desenha a tela de fim de jogo."""
    surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    surface.fill((0, 0, 0, 128))  # Sobreposição semi-transparente
    screen.blit(surface, (0, 0))
    
    font = pygame.font.SysFont('Arial', 48)
    text = font.render(f'{winner} Venceu!', True, COLORS['BOARD_LIGHT'])
    text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
    screen.blit(text, text_rect)
    
    pygame.display.flip()