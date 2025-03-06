from copy import deepcopy  # Para simular alterações no tabuleiro durante capturas

def get_valid_moves(board, row, col, chain_capture=False):
    """
    Retorna uma lista de movimentos válidos para a peça em (row, col).
    Cada movimento é uma tupla (target_row, target_col, move_value, captured_positions) onde:
      • move_value == 0 para um movimento normal (sem captura),
      • um inteiro positivo indica o número total de oponentes capturados ao longo da cadeia.
    captured_positions é uma lista de (row, col) para peças capturadas ao longo da rota.
    Quando chain_capture é True apenas movimentos de captura são retornados.
    """
    moves = []
    piece = board[row][col]
    if piece == '.':
        return moves

    board_size = len(board)
    is_king = piece.isupper()

    if chain_capture:
        captures = get_piece_captures(board, row, col)
        if captures:
            for cap in captures:
                moves.append(cap)
            # Não adiciona mais a opção "fim" - turnos terminarão automaticamente após capturas parciais
    else:
        # Movimentos sem captura:
        if is_king:
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
            for dr, dc in directions:
                r, c = row + dr, col + dc
                while 0 <= r < board_size and 0 <= c < board_size and board[r][c] == '.':
                    moves.append((r, c, 0, []))
                    r += dr
                    c += dc
        else:
            if piece.lower() == 'r':
                directions = [(-1, -1), (-1, 1)]
            else:
                directions = [(1, -1), (1, 1)]
            for dr, dc in directions:
                r, c = row + dr, col + dc
                if 0 <= r < board_size and 0 <= c < board_size and board[r][c] == '.':
                    moves.append((r, c, 0, []))
        
        # Adiciona todos os movimentos de captura, incluindo capturas intermediárias
        captures = get_piece_captures(board, row, col)
        # Em vez de selecionar apenas os movimentos com capturas máximas em cada destino,
        # incluiremos todas as sequências de captura válidas (incluindo as parciais)
        for move in captures:
            moves.append(move)
    return moves

def get_piece_captures(board, row, col):
    """
    Retorna uma lista de movimentos de captura para a peça em (row, col).
    Cada movimento é uma tupla (end_row, end_col, capture_count, captured_positions)
    representando o quadrado de destino após um ou mais saltos,
    a contagem total de capturas e a lista de posições das peças capturadas.
    """
    piece = board[row][col]
    if piece == '.':
        return []
    return _get_multi_captures(board, row, col, piece)

def _get_multi_captures(board, row, col, piece):
    """
    Auxiliar recursivo para calcular movimentos de captura que podem incluir múltiplos saltos.
    Retorna uma lista de movimentos como tuplas: (end_row, end_col, capture_count, captured_positions).
    Agora inclui posições de captura intermediárias como movimentos válidos.
    """
    board_size = len(board)
    moves = []
    opponent = 'b' if piece.lower() == 'r' else 'r'

    if piece.isupper():
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            found_opponent = False
            captured_r, captured_c = None, None
            while 0 <= r < board_size and 0 <= c < board_size:
                if not found_opponent:
                    if board[r][c] == '.':
                        r += dr
                        c += dc
                        continue
                    elif board[r][c].lower() == opponent:
                        found_opponent = True
                        captured_r, captured_c = r, c
                        r += dr
                        c += dc
                        continue
                    else:
                        break
                else:
                    if board[r][c] == '.':
                        new_board = deepcopy(board)
                        new_board[row][col] = '.'
                        new_board[captured_r][captured_c] = '.'
                        new_board[r][c] = piece
                        
                        # Sempre adiciona a captura única atual como um movimento válido
                        moves.append((r, c, 1, [(captured_r, captured_c)]))
                        
                        subsequent = _get_multi_captures(new_board, r, c, piece)
                        if subsequent:
                            for move in subsequent:
                                moves.append((move[0], move[1], move[2] + 1, [(captured_r, captured_c)] + move[3]))
                        
                        r += dr
                        c += dc
                    else:
                        break
    else:
        # Captura de peça regular.
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dr, dc in directions:
            mid_r, mid_c = row + dr, col + dc
            end_r, end_c = row + 2 * dr, col + 2 * dc
            if (0 <= mid_r < board_size and 0 <= mid_c < board_size and
                0 <= end_r < board_size and 0 <= end_c < board_size):
                if board[mid_r][mid_c] != '.' and board[mid_r][mid_c].lower() == opponent and board[end_r][end_c] == '.':
                    new_board = deepcopy(board)
                    new_board[row][col] = '.'
                    new_board[mid_r][mid_c] = '.'
                    new_board[end_r][end_c] = piece
                    
                    # Sempre adiciona a captura única atual como um movimento válido
                    moves.append((end_r, end_c, 1, [(mid_r, mid_c)]))
                    
                    subsequent = _get_multi_captures(new_board, end_r, end_c, piece)
                    if subsequent:
                        for move in subsequent:
                            moves.append((move[0], move[1], move[2] + 1, [(mid_r, mid_c)] + move[3]))
    
    return moves

def has_captures_available(board, current_player):
    """
    Verifica se alguma peça pertencente ao jogador atual tem um movimento de captura válido.
    """
    board_size = len(board)
    for r in range(board_size):
        for c in range(board_size):
            piece = board[r][c]
            if (piece != '.' and 
                ((current_player == 'RED' and piece.lower() == 'r') or 
                 (current_player == 'BLACK' and piece.lower() == 'b'))):
                if get_piece_captures(board, r, c):
                    return True
    return False