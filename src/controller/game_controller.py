import asyncio
import pygame
from src.model.game_state import initialize_game, update_game_state
from src.model.moves import get_valid_moves
from src.view.board_view import render_game_state, draw_game_over
from src.view.menu_view import render_pause_menu, get_button_clicked
from src.config.settings import WINDOW_WIDTH, WINDOW_HEIGHT, SQUARE_SIZE
from src.controller.ai_controller import handle_ai_turn

async def handle_game_loop(screen, mode='pvp'):
    game_state = initialize_game()
    game_state['mode'] = mode
    if mode == 'ai':
        game_state['current_player'] = 'RED'
    
    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(60)
        
        if game_state.get('mode') == 'ai' and game_state['current_player'] == 'BLACK':
            handle_ai_turn(game_state)
            render_game_state(screen, game_state)
            await asyncio.sleep(0.5)
            continue
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    action = await handle_pause_menu(screen)
                    if action:
                        return action
            elif event.type == pygame.MOUSEBUTTONDOWN:
                handle_game_input(event, game_state)
        
        render_game_state(screen, game_state)
        
        if game_state.get('game_over'):
            draw_game_over(screen, game_state.get('winner', 'Ninguém'))
            await asyncio.sleep(2)
            return "menu"
        
        pygame.display.flip()
        await asyncio.sleep(0)
    
    return "exit"

def handle_game_input(event, game_state):
    if event.type != pygame.MOUSEBUTTONDOWN:
        return
    
    mouse_pos = pygame.mouse.get_pos()
    col = mouse_pos[0] // SQUARE_SIZE
    row = mouse_pos[1] // SQUARE_SIZE
    
    board = game_state['board']
    current_player = game_state['current_player']
    
    if not game_state.get('selected_piece'):
        piece = board[row][col]
        
        if piece.lower() == current_player[0].lower():
            valid_moves = get_valid_moves(board, row, col)
            if valid_moves:
                game_state['selected_piece'] = (row, col)
                game_state['valid_moves'] = valid_moves
            else:
                return
        else:
            return
    else:
        start_row, start_col = game_state['selected_piece']
        if (row, col) == (start_row, start_col):
            game_state['selected_piece'] = None
            game_state['valid_moves'] = []
            return
        
        valid_move = None
        for move in game_state['valid_moves']:
            if move[0] == row and move[1] == col:
                valid_move = move
                break
        
        if valid_move:
            update_game_state(game_state, valid_move)
        else:
            if not game_state.get('must_capture'):
                game_state['selected_piece'] = None
                game_state['valid_moves'] = []


async def handle_pause_menu(screen):
    while True:
        button_positions = render_pause_menu(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                action = get_button_clicked(button_positions, event.pos)
                if action:
                    if action == "resume":
                        return None
                    return action
        await asyncio.sleep(0)

async def start_game():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    result = await handle_game_loop(screen, mode='pvp')
    return result

async def start_ai_game():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    result = await handle_game_loop(screen, mode='ai')
    return result