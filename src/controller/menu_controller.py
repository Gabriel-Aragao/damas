import pygame
from view.menu_view import render_menu, render_settings_menu, get_button_clicked
from controller.game_controller import start_game

def handle_main_menu(screen):
    """Handle main menu interaction and navigation."""
    running = True
    while running:
        # Draw menu and get button positions
        button_positions = render_menu(screen)
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                action = get_button_clicked(button_positions, event.pos)
                if action:
                    if action == "pvp":
                        # Start player vs player game
                        result = start_game()
                        if result == "exit":
                            return "exit"
                    elif action == "ai":
                        # Start player vs AI game (future implementation)
                        pass
                    elif action == "settings":
                        # Open settings menu
                        result = handle_settings_menu(screen)
                        if result == "exit":
                            return "exit"
                    elif action == "exit":
                        return "exit"
        
        pygame.display.flip()
        
def handle_settings_menu(screen):
    """Handle settings menu interaction."""
    running = True
    while running:
        # Draw settings menu and get button positions
        button_positions = render_settings_menu(screen)
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                action = get_button_clicked(button_positions, event.pos)
                if action:
                    print(f'action: {action}')
                    if action == "force_capture":
                        toggle_setting('force_capture')
                    elif action == "multiple_jumps":
                        toggle_setting('multiple_jumps')
                    elif action == "kings_move_multiple":
                        toggle_setting('kings_move_multiple')
                    elif action == "back":
                        return None
        
        pygame.display.flip()

def toggle_setting_handler(setting_name):
    """Handle setting toggles."""
    if setting_name == 'SHOW_VALID_MOVES':
        toggle_setting("display", "show_valid_moves")
    elif setting_name == 'SHOW_LAST_MOVE':
        toggle_setting("display", "show_last_move")
    elif setting_name == 'DEBUG_MODE':
        toggle_setting("debug", "debug_mode")

def save_settings():
    """Save current settings."""
    save_config()

def load_settings():
    """Load settings from file."""
    load_config()

def start_menu():
    """Initialize and start the menu system."""
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(WINDOW_TITLE)
    
    # Load saved settings
    load_settings()
    
    # Start main menu loop
    result = handle_main_menu(screen)
    
    # Save settings before exit
    save_settings()
    
    return result

def handle_transition(screen, from_state, to_state):
    """Handle transitions between different menu states."""
    # Could implement fade effects or other transitions here
    pass