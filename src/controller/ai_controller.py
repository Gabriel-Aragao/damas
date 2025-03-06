from copy import deepcopy  # Para criar estados de tabuleiro independentes durante a busca
from src.model.game_state import update_game_state  # Usa lógica padrão de atualização de estado
from src.model import moves  # Usa utilitários de geração de movimentos

# Função de avaliação: retorna uma pontuação da perspectiva da IA (PRETO).
def evaluate_state(game_state):
    board = game_state['board']
    red_val = 0
    black_val = 0
    # Conta peças – damas contam como 1,5 pontos.
    for row in board:
        for cell in row:
            if cell.lower() == 'r':
                if cell.isupper():
                    red_val += 1.5
                else:
                    red_val += 1
            elif cell.lower() == 'b':
                if cell.isupper():
                    black_val += 1.5
                else:
                    black_val += 1
    return black_val - red_val  # Positivo significa vantagem para PRETO (IA)

# Função auxiliar para gerar todos os movimentos válidos para um jogador.
def get_all_valid_moves(game_state, player):
    moves_list = []
    board = game_state['board']
    board_size = len(board)
    # Se uma cadeia de captura estiver em andamento, use apenas os movimentos pré-armazenados.
    if game_state.get('selected_piece') is not None:
        from_pos = game_state['selected_piece']
        valid_moves = game_state.get('valid_moves', [])
        for move in valid_moves:
            moves_list.append((from_pos, move))
        return moves_list
    # Caso contrário, escaneie o tabuleiro para peças pertencentes ao jogador.
    for r in range(board_size):
        for c in range(board_size):
            piece = board[r][c]
            if player == 'BLACK' and piece.lower() == 'b':
                piece_moves = moves.get_valid_moves(board, r, c)
                if piece_moves:
                    for m in piece_moves:
                        moves_list.append(((r, c), m))
            elif player == 'RED' and piece.lower() == 'r':
                piece_moves = moves.get_valid_moves(board, r, c)
                if piece_moves:
                    for m in piece_moves:
                        moves_list.append(((r, c), m))
    return moves_list

# Algoritmo minimax com profundidade de busca fixa.
def minimax(state, depth, maximizing):
    # Se a profundidade for zero ou o jogo acabar, retorne a avaliação heurística.
    if depth == 0 or state['game_over']:
        return evaluate_state(state), None

    if maximizing:
        max_eval = float('-inf')
        best_move = None
        # IA (PRETO) tenta maximizar sua pontuação.
        possible_moves = get_all_valid_moves(state, 'BLACK')
        if not possible_moves:
            return evaluate_state(state), None
        for from_pos, move in possible_moves:
            new_state = deepcopy(state)  # Copia o estado para simulação
            new_state['selected_piece'] = from_pos
            update_game_state(new_state, move)
            eval_score, _ = minimax(new_state, depth - 1, False)
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = (from_pos, move)
        return max_eval, best_move
    else:
        min_eval = float('inf')
        best_move = None
        # Oponente (VERMELHO) minimiza a pontuação da IA.
        possible_moves = get_all_valid_moves(state, 'RED')
        if not possible_moves:
            return evaluate_state(state), None
        for from_pos, move in possible_moves:
            new_state = deepcopy(state)
            new_state['selected_piece'] = from_pos
            update_game_state(new_state, move)
            eval_score, _ = minimax(new_state, depth - 1, True)
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = (from_pos, move)
        return min_eval, best_move

# Retorna o melhor movimento (como uma tupla: (from_pos, move)) buscando até uma profundidade fixa.
def calculate_ai_move(game_state, depth=5):
    score, best_move = minimax(game_state, depth, True)
    return best_move

# Função para lidar com o turno da IA
def handle_ai_turn(game_state):
    print("[LOG] Turno da IA iniciado")
    from src.config.settings_manager import get_ai_difficulty
    
    # Obtém a configuração atual de dificuldade da IA (1-5)
    ai_difficulty = get_ai_difficulty()
    print(f"[LOG] IA usando nível de dificuldade {ai_difficulty} (profundidade = {ai_difficulty})")
    
    best_move = calculate_ai_move(game_state, depth=ai_difficulty)
    if best_move is not None:
        from_pos, move = best_move
        # Define a peça selecionada para o processamento adequado da atualização.
        game_state['selected_piece'] = from_pos
        game_state['valid_moves'] = [move]  # Armazena temporariamente o movimento escolhido para atualização
        update_game_state(game_state, move)
        print(f"[LOG] IA realizou movimento de {from_pos} para {(move[0], move[1])}")
    else:
        print("[LOG] IA não tem movimentos válidos")
    print("[LOG] Turno da IA finalizado")