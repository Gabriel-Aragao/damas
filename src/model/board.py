def create_board():
    """
    Cria um tabuleiro 8x8 onde cada quadrado é inicializado como '.' (vazio).
    """
    board = [['.' for _ in range(8)] for _ in range(8)]
    return board

def initialize_pieces(board):
    """
    Configura as peças iniciais no tabuleiro.
    Peças vermelhas ('r') são colocadas nas linhas inferiores e peças pretas ('b') nas linhas superiores.
    As peças ocupam apenas quadrados jogáveis ((row + col) % 2 != 0).
    """
    for row in range(8):
        for col in range(8):
            if (row + col) % 2 != 0:
                if row < 3:
                    board[row][col] = 'b'
                elif row > 4:
                    board[row][col] = 'r'
    return board

def make_move(board, start_row, start_col, end_row, end_col):
    """
    Move uma peça de (start_row, start_col) para (end_row, end_col).
    Suporta:
      • Movimentos de dama voadora: peças de dama podem se mover múltiplos quadrados ao longo de uma diagonal.
      • Captura: se uma peça do oponente for saltada, ela é removida.
    A função percorre o caminho do movimento ao longo da diagonal e remove uma única peça capturada.
    """
    piece = board[start_row][start_col]
    board[start_row][start_col] = '.'
    dr = end_row - start_row
    dc = end_col - start_col
    abs_dr = abs(dr)
    abs_dc = abs(dc)
    
    # Garante que o movimento é diagonal.
    if abs_dr != abs_dc:
        print("Movimento inválido: Não é um movimento diagonal")
        return
    
    # Para movimentos de dama ou qualquer movimento que abrange mais de um quadrado, verifica o caminho.
    if piece.isupper() or abs_dr > 1:
        step_r = dr // abs_dr  # Passo unitário para linha.
        step_c = dc // abs_dc  # Passo unitário para coluna.
        r, c = start_row + step_r, start_col + step_c
        captured = False
        while (r, c) != (end_row, end_col):
            if board[r][c] != '.':
                if captured:
                    print("Movimento inválido: Mais de uma peça encontrada ao longo do caminho")
                    return
                if board[r][c].lower() != piece.lower():
                    # Captura a peça do oponente encontrada ao longo da diagonal.
                    board[r][c] = '.'
                    captured = True
                else:
                    print("Movimento inválido: Não pode pular sobre sua própria peça")
                    return
            r += step_r
            c += step_c
    else:
        # Para um movimento de captura simples que abrange dois quadrados.
        if abs_dr == 2:
            mid_row = (start_row + end_row) // 2
            mid_col = (start_col + end_col) // 2
            board[mid_row][mid_col] = '.'
    
    # Coloca a peça em movimento no destino.
    board[end_row][end_col] = piece
    
    # Promove para dama se a peça alcançar a extremidade oposta.
    if piece == 'r' and end_row == 0:
        board[end_row][end_col] = 'R'
    elif piece == 'b' and end_row == len(board) - 1:
        board[end_row][end_col] = 'B'

def get_winner(board):
    """
    Determina o vencedor do jogo com base nas peças restantes.
    Retorna 'RED' se apenas peças vermelhas permanecerem, 'BLACK' se apenas peças pretas permanecerem,
    ou None se ambas estiverem presentes.
    """
    red_exists = any(piece.lower() == 'r' for row in board for piece in row)
    black_exists = any(piece.lower() == 'b' for row in board for piece in row)
    if not red_exists:
        return 'BLACK'
    elif not black_exists:
        return 'RED'
    return None