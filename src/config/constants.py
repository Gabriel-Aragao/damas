# Estados do Jogo
MENU = 'MENU'
PLAYING = 'PLAYING'
GAME_OVER = 'GAME_OVER'
PAUSED = 'PAUSED'

# Tipos de Jogadores
PLAYER_1 = 'PLAYER_1'
PLAYER_2 = 'PLAYER_2'
AI_PLAYER = 'AI'

# Tipos de Peças
EMPTY = '.'
RED_PIECE = 'r'
BLACK_PIECE = 'b'
RED_KING = 'R'
BLACK_KING = 'B'

# Tipos de Movimentos
NORMAL_MOVE = 'NORMAL'
CAPTURE_MOVE = 'CAPTURE'
INVALID_MOVE = 'INVALID'

# Direções do Tabuleiro
DIRECTIONS = {
    'UP_LEFT': (-1, -1),
    'UP_RIGHT': (-1, 1),
    'DOWN_LEFT': (1, -1),
    'DOWN_RIGHT': (1, 1)
}

# Resultados do Jogo
RED_WINS = 'RED_WINS'
BLACK_WINS = 'BLACK_WINS'
DRAW = 'DRAW'

# Tipos de Eventos
PIECE_SELECTED = 'PIECE_SELECTED'
PIECE_MOVED = 'PIECE_MOVED'
PIECE_CAPTURED = 'PIECE_CAPTURED'
KING_CROWNED = 'KING_CROWNED'

# Posições do Tabuleiro
FIRST_ROW = 0
LAST_ROW = 7
FIRST_COL = 0
LAST_COL = 7

# Mensagens de Erro
INVALID_POSITION = 'Posição inválida no tabuleiro'
INVALID_PIECE = 'Seleção de peça inválida'
INVALID_MOVE = 'Movimento inválido'