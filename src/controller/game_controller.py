import pygame
from model.game_state import initialize_game, update_game_state
from model.moves import get_valid_moves
from view.board_view import render_game_state, draw_game_over
from view.menu_view import render_pause_menu, get_button_clicked
from config.settings import *

def handle_game_loop(screen):
    """
    Main game loop handler for the checkers game
    """
    print("[LOG] Entering handle_game_loop()")
    
    # Initialize game state
    game_state = initialize_game()
    clock = pygame.time.Clock()
    
    running = True
    while running:
        clock.tick(60)
        
        # Process all events
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
        if game_state['game_over']:
            draw_game_over(screen, game_state['winner'])
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
    
    # Get board coordinates from mouse position
    mouse_pos = pygame.mouse.get_pos()
    col = mouse_pos[0] // SQUARE_SIZE
    row = mouse_pos[1] // SQUARE_SIZE
    
    print(f"[LOG] handle_game_input: Clicked position ({row}, {col})")
    
    board = game_state['board']
    current_player = game_state['current_player']
    
    # If no piece is currently selected, attempt to select one
    if not game_state['selected_piece']:
        piece = board[row][col]
        print(f"[LOG] handle_game_input: Attempting to select piece {piece}")
        
        # Check if clicked on current player's piece
        if piece.lower() == current_player[0].lower():
            valid_moves = get_valid_moves(board, row, col)
            print(f"[LOG] handle_game_input: Valid moves found: {valid_moves}")
            
            if valid_moves:  # If there are any valid moves
                game_state['selected_piece'] = (row, col)
                game_state['valid_moves'] = valid_moves
                print("[LOG] handle_game_input: Piece selected successfully")
    else:
        start_row, start_col = game_state['selected_piece']
        
        # If clicked on the same piece, deselect it
        if (row, col) == (start_row, start_col):
            game_state['selected_piece'] = None
            game_state['valid_moves'] = []
            print("[LOG] handle_game_input: Piece deselected")
            return
        
        # Look for a valid move from the list (each valid move is a (dest_row, dest_col, move_value) tuple)
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
            # Clicked elsewhere – if not forced to capture, then deselect the piece.
            if not game_state['must_capture']:
                game_state['selected_piece'] = None
                game_state['valid_moves'] = []
                print("[LOG] handle_gam: Invalid move - piece deselected")
    
    print("[LOG] Exiting handle_game_input")

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
            
            # Update button hover states
            button_positions = render_pause_menu(screen)

def start_game():
    """Initialize and start the game."""
    print("[LOG] Entering start_game()")

def start_game():
    """Initialize and start the game."""
    print("[LOG] Entering start_game()")
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(WINDOW_TITLE)
    
    result = handle_game_loop(screen)
    print(f"[LOG] start_game returning: '{result}'")
    return result

def handle_ai_turn(game_state):
    """Handle AI move when implemented."""
    print("[LOG] Entering handle_ai_turn() - NOT IMPLEMENTED")
    # TODO: Implement AI logic
    print("[LOG] Exiting handle_ai_turn()")
    pass
