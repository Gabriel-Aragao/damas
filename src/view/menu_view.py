import os
import pygame
from src.config.settings import *
from src.config.constants import *

def load_background():
    """Load and scale the background image."""
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, 'assets', 'menu_bg.png')
        bg_image = pygame.image.load(image_path)
        return pygame.transform.scale(bg_image, (WINDOW_WIDTH, WINDOW_HEIGHT))
    except Exception as e:
        print(f"Error loading background: {e}")
        return None

def render_menu(screen):
    """Render the main menu."""
    # Load and draw background
    bg_image = load_background()
    if bg_image:
        screen.blit(bg_image, (0, 0))
    else:
        screen.fill(COLORS['BOARD_DARK'])
    
    # Rest of the menu code remains the same...
    buttons = {
        'pvp': create_button('Player vs Player'),
        'ai': create_button('Player vs AI'),
        'exit': create_button('Exit')
    }
    
    button_spacing = 70
    total_height = len(buttons) * button_spacing
    start_y = (WINDOW_HEIGHT - total_height) // 2
    
    mouse_pos = pygame.mouse.get_pos()
    button_positions = {}
    
    for i, (key, button) in enumerate(buttons.items()):
        x = (WINDOW_WIDTH - button['rect'].width) // 2
        y = start_y + (i * button_spacing)
        button_positions[key] = (x, y)
        
        button_rect = pygame.Rect(x, y, button['rect'].width, button['rect'].height)
        is_hovered = button_rect.collidepoint(mouse_pos)
        
        draw_button(screen, button, (x, y), is_hovered)
    
    pygame.display.flip()
    return button_positions

def create_button(text, font_size=36, width=300, height=50):
    """Create a button surface with text."""
    font = pygame.font.SysFont('Arial', font_size)
    button_surface = pygame.Surface((width, height))
    text_surface = font.render(text, True, COLORS['BOARD_LIGHT'])
    text_rect = text_surface.get_rect(center=(width/2, height/2))
    
    return {
        'surface': button_surface,
        'text': text_surface,
        'text_rect': text_rect,
        'rect': button_surface.get_rect()
    }

def draw_button(screen, button, position, is_hovered=False):
    """Draw a button on the screen."""
    x, y = position
    button['rect'].topleft = (x, y)
    
    # Button background
    color = COLORS['HIGHLIGHT'] if is_hovered else (*COLORS['BOARD_DARK'], 200)
    pygame.draw.rect(screen, color, button['rect'], border_radius=10)
    
    # Button border
    pygame.draw.rect(screen, COLORS['BOARD_LIGHT'], button['rect'], 2, border_radius=10)
    
    # Center text on button
    text_x = x + (button['rect'].width - button['text'].get_width()) // 2
    text_y = y + (button['rect'].height - button['text'].get_height()) // 2
    screen.blit(button['text'], (text_x, text_y))

def render_settings_menu(screen):
    pass

def render_pause_menu(screen):
    """Render the pause menu overlay."""
    # Create semi-transparent overlay
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))
    screen.blit(overlay, (0, 0))
    
    # Create buttons
    buttons = {
        'resume': create_button('Resume'),
        'menu': create_button('Main Menu'),
        'exit': create_button('Exit Game')
    }
    
    # Position buttons
    button_spacing = 70
    total_height = len(buttons) * button_spacing
    start_y = (WINDOW_HEIGHT - total_height) // 2
    
    # Draw buttons
    mouse_pos = pygame.mouse.get_pos()
    button_positions = {}
    
    for i, (key, button) in enumerate(buttons.items()):
        x = (WINDOW_WIDTH - button['rect'].width) // 2
        y = start_y + (i * button_spacing)
        button_positions[key] = (x, y)
        
        button_rect = pygame.Rect(x, y, button['rect'].width, button['rect'].height)
        is_hovered = button_rect.collidepoint(mouse_pos)
        
        draw_button(screen, button, (x, y), is_hovered)
    
    pygame.display.flip()
    return button_positions

def get_button_clicked(button_positions, mouse_pos):
    """Return which button was clicked, if any."""
    for key, (x, y) in button_positions.items():
        button_rect = pygame.Rect(x, y, 300, 50)  # Using standard button size
        if button_rect.collidepoint(mouse_pos):
            return key
    return None
