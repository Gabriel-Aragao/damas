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
    
    # Add the settings button
    buttons = {
        'pvp': create_button('Player vs Player'),
        'ai': create_button('Player vs AI'),
        'settings': create_button('Settings'),
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
    
    # Button background - create a surface with alpha
    bg_surface = pygame.Surface((button['rect'].width, button['rect'].height), pygame.SRCALPHA)
    
    # Choose color based on hover state
    if is_hovered:
        bg_color = (255, 255, 0, 200)  # Yellow with transparency
    else:
        bg_color = (64, 64, 64, 200)  # Dark gray with transparency
    
    # Draw the background onto the alpha surface
    pygame.draw.rect(bg_surface, bg_color, bg_surface.get_rect(), border_radius=10)
    screen.blit(bg_surface, button['rect'].topleft)
    
    # Button border
    pygame.draw.rect(screen, COLORS['BOARD_LIGHT'], button['rect'], 2, border_radius=10)
    
    # Center text on button
    text_x = x + (button['rect'].width - button['text'].get_width()) // 2
    text_y = y + (button['rect'].height - button['text'].get_height()) // 2
    screen.blit(button['text'], (text_x, text_y))

def render_settings_menu(screen):
    """Render the settings menu with difficulty options."""
    from src.config.settings_manager import get_ai_difficulty
    
    # Create semi-transparent overlay
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))
    screen.blit(overlay, (0, 0))
    
    # Draw menu title
    font = pygame.font.SysFont('Arial', 48)
    title_text = font.render('AI Difficulty Settings', True, COLORS['BOARD_LIGHT'])
    title_x = (WINDOW_WIDTH - title_text.get_width()) // 2
    screen.blit(title_text, (title_x, 80))
    
    # Get current AI difficulty
    current_difficulty = get_ai_difficulty()
    
    # Create difficulty buttons
    buttons = {}
    for i in range(1, 6):
        label = f"Level {i}" + (" (Current)" if i == current_difficulty else "")
        buttons[f'difficulty_{i}'] = create_button(label)
    
    buttons['back'] = create_button('Back to Main Menu')
    
    # Position buttons
    button_spacing = 70
    total_height = len(buttons) * button_spacing
    start_y = (WINDOW_HEIGHT - total_height) // 2 + 30  # Offset for title
    
    # Draw buttons
    mouse_pos = pygame.mouse.get_pos()
    button_positions = {}
    
    for i, (key, button) in enumerate(buttons.items()):
        x = (WINDOW_WIDTH - button['rect'].width) // 2
        y = start_y + (i * button_spacing)
        button_positions[key] = (x, y)
        
        button_rect = pygame.Rect(x, y, button['rect'].width, button['rect'].height)
        is_hovered = button_rect.collidepoint(mouse_pos)
        
        # Highlight current difficulty
        if key == f'difficulty_{current_difficulty}':
            # Create a slightly different highlight color for current selection
            highlight_color = (255, 215, 0, 100)  # Gold with transparency
            pygame.draw.rect(screen, highlight_color, button_rect, border_radius=10)
        
        draw_button(screen, button, (x, y), is_hovered)
    
    # Add explanation text
    font_small = pygame.font.SysFont('Arial', 18)
    explanations = [
        "Level 1: Easy - AI looks 1 move ahead",
        "Level 2: Casual - AI looks 2 moves ahead",
        "Level 3: Moderate - AI looks 3 moves ahead",
        "Level 4: Challenging - AI looks 4 moves ahead",
        "Level 5: Difficult - AI looks 5 moves ahead"
    ]
    
    for i, text in enumerate(explanations):
        text_surface = font_small.render(text, True, COLORS['BOARD_LIGHT'])
        text_x = (WINDOW_WIDTH - text_surface.get_width()) // 2
        text_y = start_y + ((len(buttons) + i) * button_spacing) + 20
        screen.blit(text_surface, (text_x, text_y))
    
    pygame.display.flip()
    return button_positions

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
