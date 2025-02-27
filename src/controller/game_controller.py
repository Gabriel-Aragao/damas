import asyncio  # Imported for asynchronous sleep calls
import pygame
from src.model.game_state import initialize_game, update_game_state
from src.model.moves import get_valid_moves
from src.view.board_view import render_game_state, draw_game_over
from src.view.menu_view import render_pause_menu, get_button_clicked
from src.config.settings import WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, SQUARE_SIZE
from src.controller.ai_controller import handle_ai_turn  # import AI logic

# Convert the game loop to an async function.
async def handle_game_loop(screen, mode='pvp'):
    """
    Main game loop handler for the checkers game.
    Supports PvP and AI modes.
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
        
        # In AI mode: if it's AI's turn, perform its move and yield control.
        if game_state.get('mode') == 'ai' and game_state['current_player'] == 'BLACK':
            handle_ai_turn(game_state)
            render_game_state(screen, game_state)
            # Replace blocking wait with async sleep (500ms delay)
            await asyncio.sleep(0.5)
            continue
        
        # Process events for human input.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("[LOG] handle_game_loop returning: 'exit' (quit event)")
                return "exit"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Call the async pause menu.
                    action = await handle_pause_menu(screen)
                    if action:
                        print(f"[LOG] handle_game_loop returning: '{action}' (from pause menu)")
                        return action
            elif event.type == pygame.MOUSEBUTTONDOWN:
                handle_game_input(event, game_state)
        
        # Update display.
        render_game_state(screen, game_state)
        
        # Check for game over.
        if game_state.get('game_over'):
            draw_game_over(screen, game_state.get('winner', 'No one'))
            await asyncio.sleep(2)  # Replace blocking wait with async sleep (2 seconds)
            print("[LOG] handle_game_loop returning: 'menu' (game over)")
            return "menu"
        
        pygame.display.flip()
        # Yield control to the event loop so the browser remains responsive.
        await asyncio.sleep(0)
    
    print("[LOG] handle_game_loop returning: 'exit' (loop ended)")
    return "exit"

def handle_game_input(event, game_state):
    """Handle player input during the game."""
    print("[LOG] Entering handle_game_input()")
    
    if event.type != pygame.MOUSEBUTTONDOWN:
        print("[LOG] Exiting handle_game_input (not mouse button down)")
        return
    
    # Convert mouse position to board coordinates.
    mouse_pos = pygame.mouse.get_pos()
    col = mouse_pos[0] // SQUARE_SIZE
    row = mouse_pos[1] // SQUARE_SIZE
    print(f"[LOG] handle_game_input: Clicked position ({row}, {col})")
    
    board = game_state['board']
    current_player = game_state['current_player']
    
    # If no piece is selected, try to select one.
    if not game_state.get('selected_piece'):
        piece = board[row][col]
        print(f"[LOG] handle_game_input: Attempting to select piece {piece}")
        
        # Verify that the clicked piece belongs to the current player.
        if piece.lower() == current_player[0].lower():
            valid_moves = get_valid_moves(board, row, col)
            print(f"[LOG] handle_game_input: Valid moves found: {valid_moves}")
            if valid_moves:
                game_state['selected_piece'] = (row, col)
                game_state['valid_moves'] = valid_moves
                print("[LOG] handle_game_input: Piece selected successfully")
            else:
                return
        else:
            return
    else:
        start_row, start_col = game_state['selected_piece']
        # Deselect if the same piece is clicked.
        if (row, col) == (start_row, start_col):
            game_state['selected_piece'] = None
            game_state['valid_moves'] = []
            print("[LOG] handle_game_input: Piece deselected")
            return
        
        # Look for a valid move among the available ones.
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
            # Deselect if the move is invalid and no capturing is required.
            if not game_state.get('must_capture'):
                game_state['selected_piece'] = None
                game_state['valid_moves'] = []
                print("[LOG] handle_game_input: Invalid move - piece deselected")
    
    print("[LOG] Exiting handle_game_input()")

# Convert the pause menu to async so its loop yields control.
async def handle_pause_menu(screen):
    """Handle pause menu interaction asynchronously."""
    print("[LOG] Entering handle_pause_menu()")
    while True:
        button_positions = render_pause_menu(screen)
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
        # Yield to ensure the browser remains responsive.
        await asyncio.sleep(0)

# Update the game start functions to be async and await the game loop.
async def start_game():
    """Initialize and start a player vs player game asynchronously."""
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(WINDOW_TITLE)
    result = await handle_game_loop(screen, mode='pvp')
    print(f"[LOG] start_game returning: '{result}'")
    return result

async def start_ai_game():
    """Initialize and start a player vs AI game asynchronously."""
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(WINDOW_TITLE)
    result = await handle_game_loop(screen, mode='ai')
    print(f"[LOG] start_ai_game returning: '{result}'")
    return result