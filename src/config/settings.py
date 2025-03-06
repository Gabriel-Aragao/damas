# Configurações do Jogo
WINDOW_TITLE = "Jogo de Damas"
FPS = 60
ANIMATION_SPEED = 5

# Configurações do Tabuleiro
BOARD_SIZE = 8
SQUARE_SIZE = 80
PIECE_PADDING = 10  # Espaço entre a peça e a borda do quadrado

# Configurações de Exibição
WINDOW_WIDTH = BOARD_SIZE * SQUARE_SIZE
WINDOW_HEIGHT = BOARD_SIZE * SQUARE_SIZE
SHOW_VALID_MOVES = True
SHOW_LAST_MOVE = True

# Cores
COLORS = {
    'BOARD_LIGHT': (255, 255, 255),  # Quadrados brancos
    'BOARD_DARK': (128, 128, 128),   # Quadrados cinza escuro
    'RED_PIECE': (220, 20, 60),      # Peças vermelhas
    'BLACK_PIECE': (0, 0, 0),        # Peças pretas
    'HIGHLIGHT': (255, 255, 0, 128), # Destaque amarelo com transparência
    'VALID_MOVE': (0, 255, 0, 128),  # Pontos verdes para movimentos válidos
    'SELECTED': (0, 0, 255, 128)     # Destaque azul para peça selecionada
}

# Regras do Jogo


# Configurações da IA
AI_DIFFICULTY = 3  # Dificuldade padrão (1-5) - controla a profundidade do minimax

# Configurações de Depuração
DEBUG_MODE = False
SHOW_COORDINATES = False