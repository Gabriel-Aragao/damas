from .board import create_board, initialize_pieces
from .moves import get_valid_moves, get_piece_captures, has_captures_available

def initialize_game():
    """
    Inicializa o estado do jogo.
    O tabuleiro é criado via create_board() e inicializado com peças usando initialize_pieces().
    """
    board = create_board()                  # Cria tabuleiro com dimensões adequadas
    board = initialize_pieces(board)        # Coloca peças iniciais no tabuleiro
    game_state = {
        'board': board,
        'current_player': 'RED',            # ou 'BLACK'
        'selected_piece': None,
        'valid_moves': [],
        'original_valid_moves': [],         # Armazena os movimentos válidos da posição original
        'last_move': None,
        'game_over': False,
        'winner': None,
        'must_capture': False,
    }
    return game_state

def update_game_state(game_state, move):
    """
    Atualiza o estado do jogo após um movimento ser executado.
    O movimento é uma tupla de 4 elementos: (dest_row, dest_col, move_value, captured_positions).
    - move_value == 0 indica um movimento sem captura.
    - Um número inteiro positivo indica um movimento de captura (o número de peças capturadas).
    
    Para capturas parciais, o turno termina imediatamente após o movimento.
    """
    # Obtém o quadrado inicial do movimento.
    selected = game_state.get('selected_piece')
    if not selected:
        return game_state  # Nada a fazer se nenhuma peça estiver selecionada.
    
    dest_row, dest_col, move_value, captured_positions = move
    board = game_state['board']
    piece = board[selected[0]][selected[1]]
    
    board[selected[0]][selected[1]] = '.'
    
    # Se for um movimento de captura, remove todas as peças capturadas.
    if captured_positions:
        for pos in captured_positions:
            board[pos[0]][pos[1]] = '.'
    
    # Verificação de promoção para dama:
    # Peças vermelhas são promovidas ao alcançar a linha 0.
    # Peças pretas são promovidas ao alcançar a linha inferior.
    board_size = len(board)
    if piece.lower() == 'r' and dest_row == 0:
        piece = 'R'
    elif piece.lower() == 'b' and dest_row == board_size - 1:
        piece = 'B'
    
    # Coloca a peça em movimento no seu destino.
    board[dest_row][dest_col] = piece
    game_state['last_move'] = (selected, (dest_row, dest_col))
    
    # Flag para verificar se há mais capturas disponíveis
    has_further_captures = False
    
    # Para movimentos de captura, encontra a captura máxima da posição inicial
    max_capture_from_start = 0
    if move_value > 0:
        # Armazena valid_moves originais para calcular a captura máxima
        original_valid_moves = game_state.get('original_valid_moves', [])
        if not original_valid_moves:
            # Se não estiver já armazenado, usa os valid_moves de antes deste movimento
            original_valid_moves = game_state.get('valid_moves', [])
            game_state['original_valid_moves'] = original_valid_moves
        
        # Encontra a contagem máxima de capturas da posição original
        for vm in original_valid_moves:
            if isinstance(vm[2], int) and vm[2] > max_capture_from_start:
                max_capture_from_start = vm[2]
        
        # Verifica se este movimento tem mais capturas disponíveis
        further_captures = get_piece_captures(board, dest_row, dest_col)
        has_further_captures = len(further_captures) > 0
    
    # Regra direta para finalização de turno:
    # 1. Movimentos sem captura sempre terminam o turno
    # 2. Se foi uma captura parcial (menos que max_capture_from_start), termina o turno
    # 3. Se não houver mais capturas disponíveis, termina o turno
    if move_value == 0 or move_value < max_capture_from_start or not has_further_captures:
        # Finaliza o turno
        game_state['selected_piece'] = None
        game_state['valid_moves'] = []
        game_state['original_valid_moves'] = []  # Limpa os movimentos armazenados
        game_state['current_player'] = 'BLACK' if game_state['current_player'] == 'RED' else 'RED'
    else:
        # Só continua a sequência de captura se esta foi uma captura máxima até agora
        # e há mais capturas disponíveis
        game_state['selected_piece'] = (dest_row, dest_col)
        game_state['valid_moves'] = get_valid_moves(board, dest_row, dest_col, chain_capture=True)
    
    # Verifica se um lado não tem mais peças.
    check_game_over(game_state)
    
    return game_state

def has_any_valid_moves(game_state, player):
    """
    Verifica se um jogador tem algum movimento válido com qualquer uma de suas peças.
    Retorna True se pelo menos um movimento válido existir, False caso contrário.
    """
    board = game_state['board']
    board_size = len(board)
    piece_char = 'r' if player == 'RED' else 'b'
    
    for row in range(board_size):
        for col in range(board_size):
            piece = board[row][col]
            if piece.lower() == piece_char:
                # Verifica se esta peça tem algum movimento válido
                if get_valid_moves(board, row, col):
                    return True
    return False

def check_game_over(game_state):
    board = game_state['board']
    red_count = 0
    black_count = 0
    for row in board:
        for cell in row:
            if cell.lower() == 'r':
                red_count += 1
            elif cell.lower() == 'b':
                black_count += 1
    
    if red_count == 0:
        game_state['game_over'] = True
        game_state['winner'] = 'Pretas'
        return
    elif black_count == 0:
        game_state['game_over'] = True
        game_state['winner'] = 'Vermelhas'
        return
    

    current_player = game_state['current_player']
    if not has_any_valid_moves(game_state, current_player):
        game_state['game_over'] = True
        game_state['winner'] = 'Vermelhas' if current_player == 'RED' else 'Vermelhas'
        return

def select_piece(game_state, row, col):
    board = game_state['board']
    piece = board[row][col]
    # Deve ser uma peça válida para o jogador atual.
    if piece == '.' or (game_state['current_player'] == 'RED' and piece.lower() == 'b') or \
       (game_state['current_player'] == 'BLACK' and piece.lower() == 'r'):
        return False
    
    valid_moves = get_valid_moves(board, row, col)
    if not valid_moves:
        return False
    
    game_state['selected_piece'] = (row, col)
    game_state['valid_moves'] = valid_moves
    game_state['original_valid_moves'] = valid_moves.copy()  # Armazena uma cópia dos movimentos válidos originais
    game_state['must_capture'] = has_captures_available(board, game_state['current_player'])
    return True

def get_game_status(game_state):
    status = {
        'current_player': game_state['current_player'],
        'game_over': game_state['game_over'],
        'winner': game_state['winner'],
        'selected_piece': game_state['selected_piece'],
        'valid_moves': game_state['valid_moves'],
        'must_capture': game_state['must_capture']
    }
    return status

def can_select_piece(game_state, row, col):
    if game_state['game_over']:
        return False
    
    piece = game_state['board'][row][col]
    if piece == '.':
        return False
    
    allowed = (game_state['current_player'] == 'RED' and piece.lower() == 'r') or \
              (game_state['current_player'] == 'BLACK' and piece.lower() == 'b')
    return allowed

def process_click(game_state, row, col):
    if game_state['selected_piece'] is not None:
        for move in game_state['valid_moves']:
            if move[0] == row and move[1] == col:
                return update_game_state(game_state, move)
        game_state['selected_piece'] = None
        game_state['valid_moves'] = []
        return game_state
    else:
        select_piece(game_state, row, col)
        return game_state