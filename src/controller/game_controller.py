import asyncio  # Importado para chamadas de sleep assíncronas
import pygame
from src.model.game_state import initialize_game, update_game_state
from src.model.moves import get_valid_moves
from src.view.board_view import render_game_state, draw_game_over
from src.view.menu_view import render_pause_menu, get_button_clicked
from src.config.settings import WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, SQUARE_SIZE
from src.controller.ai_controller import handle_ai_turn  # importa lógica da IA

# Converte o loop do jogo para uma função assíncrona.
async def handle_game_loop(screen, mode='pvp'):
    """
    Manipulador do loop principal do jogo de damas.
    Suporta modos PvP e IA.
    """
    print("[LOG] Entrando em handle_game_loop()")
    
    # Inicializa o estado do jogo e define o modo de jogo
    game_state = initialize_game()
    game_state['mode'] = mode
    if mode == 'ai':
        # No jogador vs IA, humano joga VERMELHO, IA joga PRETO.
        game_state['current_player'] = 'RED'
    
    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(60)
        
        # No modo IA: se for a vez da IA, executa seu movimento e cede o controle.
        if game_state.get('mode') == 'ai' and game_state['current_player'] == 'BLACK':
            handle_ai_turn(game_state)
            render_game_state(screen, game_state)
            # Substitui espera bloqueante por sleep assíncrono (500ms de atraso)
            await asyncio.sleep(0.5)
            continue
        
        # Processa eventos para entrada humana.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("[LOG] handle_game_loop retornando: 'exit' (evento de saída)")
                return "exit"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Chama o menu de pausa assíncrono.
                    action = await handle_pause_menu(screen)
                    if action:
                        print(f"[LOG] handle_game_loop retornando: '{action}' (do menu de pausa)")
                        return action
            elif event.type == pygame.MOUSEBUTTONDOWN:
                handle_game_input(event, game_state)
        
        # Atualiza exibição.
        render_game_state(screen, game_state)
        
        # Verifica fim de jogo.
        if game_state.get('game_over'):
            draw_game_over(screen, game_state.get('winner', 'Ninguém'))
            await asyncio.sleep(2)  # Substitui espera bloqueante por sleep assíncrono (2 segundos)
            print("[LOG] handle_game_loop retornando: 'menu' (fim de jogo)")
            return "menu"
        
        pygame.display.flip()
        # Cede controle ao loop de eventos para que o navegador permaneça responsivo.
        await asyncio.sleep(0)
    
    print("[LOG] handle_game_loop retornando: 'exit' (loop encerrado)")
    return "exit"

def handle_game_input(event, game_state):
    """Manipula a entrada do jogador durante o jogo."""
    print("[LOG] Entrando em handle_game_input()")
    
    if event.type != pygame.MOUSEBUTTONDOWN:
        print("[LOG] Saindo de handle_game_input (não é clique do mouse)")
        return
    
    # Converte posição do mouse para coordenadas do tabuleiro.
    mouse_pos = pygame.mouse.get_pos()
    col = mouse_pos[0] // SQUARE_SIZE
    row = mouse_pos[1] // SQUARE_SIZE
    print(f"[LOG] handle_game_input: Posição clicada ({row}, {col})")
    
    board = game_state['board']
    current_player = game_state['current_player']
    
    # Se nenhuma peça estiver selecionada, tenta selecionar uma.
    if not game_state.get('selected_piece'):
        piece = board[row][col]
        print(f"[LOG] handle_game_input: Tentando selecionar peça {piece}")
        
        # Verifica se a peça clicada pertence ao jogador atual.
        if piece.lower() == current_player[0].lower():
            valid_moves = get_valid_moves(board, row, col)
            print(f"[LOG] handle_game_input: Movimentos válidos encontrados: {valid_moves}")
            if valid_moves:
                game_state['selected_piece'] = (row, col)
                game_state['valid_moves'] = valid_moves
                print("[LOG] handle_game_input: Peça selecionada com sucesso")
            else:
                return
        else:
            return
    else:
        start_row, start_col = game_state['selected_piece']
        # Desseleciona se a mesma peça for clicada.
        if (row, col) == (start_row, start_col):
            game_state['selected_piece'] = None
            game_state['valid_moves'] = []
            print("[LOG] handle_game_input: Peça desselecionada")
            return
        
        # Procura por um movimento válido entre os disponíveis.
        valid_move = None
        for move in game_state['valid_moves']:
            if move[0] == row and move[1] == col:
                valid_move = move
                break
        
        if valid_move:
            print("[LOG] handle_game_input: Fazendo movimento")
            update_game_state(game_state, valid_move)
            print(f"[LOG] handle_game_input: Movimento concluído, jogador atual: {game_state['current_player']}")
        else:
            # Desseleciona se o movimento for inválido e nenhuma captura for obrigatória.
            if not game_state.get('must_capture'):
                game_state['selected_piece'] = None
                game_state['valid_moves'] = []
                print("[LOG] handle_game_input: Movimento inválido - peça desselecionada")
    
    print("[LOG] Saindo de handle_game_input()")

# Converte o menu de pausa para assíncrono para que seu loop ceda o controle.
async def handle_pause_menu(screen):
    """Manipula a interação do menu de pausa de forma assíncrona."""
    print("[LOG] Entrando em handle_pause_menu()")
    while True:
        button_positions = render_pause_menu(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("[LOG] handle_pause_menu retornando: 'exit'")
                return "exit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                action = get_button_clicked(button_positions, event.pos)
                if action:
                    print(f"[LOG] handle_pause_menu retornando: '{action}'")
                    if action == "resume":
                        return None
                    return action
        # Cede para garantir que o navegador permaneça responsivo.
        await asyncio.sleep(0)

# Atualiza as funções de início do jogo para serem assíncronas e aguardar o loop do jogo.
async def start_game():
    """Inicializa e inicia um jogo jogador contra jogador de forma assíncrona."""
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(WINDOW_TITLE)
    result = await handle_game_loop(screen, mode='pvp')
    print(f"[LOG] start_game retornando: '{result}'")
    return result

async def start_ai_game():
    """Inicializa e inicia um jogo jogador contra IA de forma assíncrona."""
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(WINDOW_TITLE)
    result = await handle_game_loop(screen, mode='ai')
    print(f"[LOG] start_ai_game retornando: '{result}'")
    return result