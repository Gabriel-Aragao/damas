# File: /home/gabriel/code/IFPB/projeto p1/damas/src/controller/game_controller.py
import pygame
from model.game_state import initialize_game, update_game_state
from model.moves import get_valid_moves
from view.board_view import render_game_state, draw_game_over
from view.menu_view import render_pause_menu, get_button_clicked
from config.settings import WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, SQUARE_SIZE

def handle_game_loop(screen, mode='pvp'):
    """
    Main game loop handler for the checkers game.
    The 'mode' parameter can be 'pvp' (player vs player) or 'ai' (player vs AI).
    In AI mode, the current_player is expected to be 'RED' for the human and 'BLACK' for AI.
    """
    print("[LOG] Entering handle_game_loop()")
    
    # Initialize game state and set game mode
    game_state = initialize_game()
    game_state['mode'] = mode
    if mode == 'ai':
        # In player vs AI, human plays RED, AI plays BLACK.
        game_state['current_player'] = 'RED'
    
    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(60)
        
        # If in AI mode and it's AI's turn (BLACK), process the AI move.
        if game_state.get('mode') == 'ai' and game_state['current_player'] == 'BLACK':
            from controller.ai_controller import handle_ai_turn  # import AI logic
            handle_ai_turn(game_state)
            render_game_state(screen, game_state)
            pygame.time.wait(500)  # brief pause to observe AI move
            continue
        
        # Process events for human input.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("[LOG] handle_game_loop returning: 'exit' (quit event)")
                return "exit"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    action = handle_pause_menu(screen)
                    if action:
                        print(f"[LOG] handle_game_loop returning: '{action}' (from pause menu)")
                        return action
            elif event.type == pygame.MOUSEBUTTONDOWN:
                handle_game_input(event, game_state)
    
        # Update display
        render_game_state(screen, game_state)
    
        # Check for game over
        if game_state.get('game_over'):
            draw_game_over(screen, game_state.get('winner', 'No one'))
            pygame.time.wait(2000)
            print("[LOG] handle_game_loop returning: 'menu' (game over)")
            return "menu"
    
        pygame.display.flip()
    
    print("[LOG] handle_game_loop returning: 'exit' (loop ended)")
    return "exit"

def handle_game_input(event, game_state):
    """Handle player input during the game."""
    print("[LOG] Entering handle_game_input()")
    
    if event.type != pygame.MOUSEBUTTONDOWN:
        print("[LOG] Exiting handle_game_input (not mouse button down)")
        return
    
    # Get board coordinates from mouse position.
    mouse_pos = pygame.mouse.get_pos()
    col = mouse_pos[0] // SQUARE_SIZE
    row = mouse_pos[1] // SQUARE_SIZE
    
    print(f"[LOG] handle_game_input: Clicked position ({row}, {col})")
    
    board = game_state['board']
    current_player = game_state['current_player']
    
    # If no piece is currently selected, attempt to select one.
    if not game_state.get('selected_piece'):
        piece = board[row][col]
        print(f"[LOG] handle_game_input: Attempting to select piece {piece}")
    
        # Check if the clicked piece belongs to the current player.
        if piece.lower() == current_player[0].lower():
            valid_moves = get_valid_moves(board, row, col)
            print(f"[LOG] handle_game_input: Valid moves found: {valid_moves}")
    
            if valid_moves:  # If there are any valid moves, select the piece.
                game_state['selected_piece'] = (row, col)
                game_state['valid_moves'] = valid_moves
                print("[LOG] handle_game_input: Piece selected successfully")
            else:
                return
    else:
        start_row, start_col = game_state['selected_piece']
        # If the same piece is clicked again, deselect it.
        if (row, col) == (start_row, start_col):
            game_state['selected_piece'] = None
            game_state['valid_moves'] = []
            print("[LOG] handle_game_input: Piece deselected")
            return
        
        # Look for a valid move among the available moves.
        valid_move = None
        for move in game_state['valid_moves']:
            if move[0] == row and move[1] == col:
                valid_move = move
                break
        
        if valid_move:
            print("[LOG] handle_game_input: Making move")
            update_game_state(game_state, valid_move)
            print(f"[LOG] handle_game_input: Move completed, current player: {game_state['current_player']}")
        else:
            # If no valid move is found and capturing is not forced, then deselect.
            if not game_state.get('must_capture'):
                game_state['selected_piece'] = None
                game_state['valid_moves'] = []
                print("[LOG] handle_game_input: Invalid move - piece deselected")
    
    print("[LOG] Exiting handle_game_input()")

def handle_pause_menu(screen):
    """Handle pause menu interaction."""
    print("[LOG] Entering handle_pause_menu()")
    button_positions = render_pause_menu(screen)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("[LOG] handle_pause_menu returning: 'exit'")
                return "exit"
    
            if event.type == pygame.MOUSEBUTTONDOWN:
                action = get_button_clicked(button_positions, event.pos)
                if action:
                    print(f"[LOG] handle_pause_menu returning: '{action}'")
                    if action == "resume":
                        return None
                    return action
    
        # Update button hover states.
        button_positions = render_pause_menu(screen)

def start_game():
    """Initialize and start a player vs player game."""
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(WINDOW_TITLE)
    
    result = handle_game_loop(screen, mode='pvp')
    print(f"[LOG] start_game returning: '{result}'")
    return result

def start_ai_game():
    """Initialize and start a player vs AI game."""
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(WINDOW_TITLE)
    
    result = handle_game_loop(screen, mode='ai')
    print(f"[LOG] start_ai_game returning: '{result}'")
    return result