import os
import pygame
from src.config.settings import *

def load_background():
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, 'assets', 'menu_bg.jpeg')
        bg_image = pygame.image.load(image_path)
        return pygame.transform.scale(bg_image, (WINDOW_WIDTH, WINDOW_HEIGHT))
    except Exception as e:
        print(f"Erro ao carregar o fundo: {e}")
        return None

def render_menu(screen):
    bg_image = load_background()
    if bg_image:
        screen.blit(bg_image, (0, 0))
    else:
        screen.fill(COLORS['BOARD_DARK'])
    
    buttons = {
        'pvp': create_button('2 Jogadores'),
        'ai': create_button('1 jogador'),
        'settings': create_button('Configurações'),
        'exit': create_button('Sair')
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
    x, y = position
    button['rect'].topleft = (x, y)
    
    bg_surface = pygame.Surface((button['rect'].width, button['rect'].height), pygame.SRCALPHA)
    
    if is_hovered:
        bg_color = COLORS['HIGHLIGHT']
    else:
        bg_color = COLORS['BUTTON']
    
    pygame.draw.rect(bg_surface, bg_color, bg_surface.get_rect(), border_radius=10)
    screen.blit(bg_surface, button['rect'].topleft)
    
    pygame.draw.rect(screen, COLORS['BOARD_LIGHT'], button['rect'], 2, border_radius=10)
    
    text_x = x + (button['rect'].width - button['text'].get_width()) // 2
    text_y = y + (button['rect'].height - button['text'].get_height()) // 2
    screen.blit(button['text'], (text_x, text_y))

def render_settings_menu(screen):
    """Renderiza o menu de configurações com opções de dificuldade."""
    from src.config.settings_manager import get_ai_difficulty
    

    bg_image = load_background()
    if bg_image:
        screen.blit(bg_image, (0, 0))
    else:
        screen.fill(COLORS['BOARD_DARK'])
    

    font = pygame.font.SysFont('Arial', 38)
    title_text = font.render('Dificuldade', True, COLORS['BOARD_LIGHT'])
    title_x = (WINDOW_WIDTH - title_text.get_width()) // 2
    screen.blit(title_text, (title_x, 80))
    

    current_difficulty = get_ai_difficulty()
    

    buttons = {}
    for i in range(1, 6):
        label = f"Nível {i}" + (" (Atual)" if i == current_difficulty else "")
        buttons[f'difficulty_{i}'] = create_button(label)
    
    buttons['back'] = create_button('Menu Principal')
    

    button_spacing = 70
    total_height = len(buttons) * button_spacing
    start_y = (WINDOW_HEIGHT - total_height) // 2 + 30  # Deslocamento para o título
    

    mouse_pos = pygame.mouse.get_pos()
    button_positions = {}
    hovered_difficulty = None
    
    for i, (key, button) in enumerate(buttons.items()):
        x = (WINDOW_WIDTH - button['rect'].width) // 2
        y = start_y + (i * button_spacing)
        button_positions[key] = (x, y)
        
        button_rect = pygame.Rect(x, y, button['rect'].width, button['rect'].height)
        is_hovered = button_rect.collidepoint(mouse_pos)
        

        if is_hovered and 'difficulty_' in key:
            hovered_difficulty = int(key.split('_')[1])
        

        if key == f'difficulty_{current_difficulty}':
            highlight_color = COLORS['SELECTED']
            pygame.draw.rect(screen, highlight_color, button_rect, border_radius=10)
        
        draw_button(screen, button, (x, y), is_hovered)
    

    selected_difficulty = hovered_difficulty if hovered_difficulty else current_difficulty
    
    explanations = {
        1: "Nível 1: Fácil (avalia 1 movimento à frente)",
        2: "Nível 2: Casual (avalia 2 movimentos à frente)",
        3: "Nível 3: Moderado (avalia 3 movimentos à frente)",
        4: "Nível 4: Desafiador (avalia 4 movimentos à frente)",
        5: "Nível 5: Difícil (avalia 5 movimentos à frente)"
    }
    

    font_small = pygame.font.SysFont('Arial', 18)
    text_surface = font_small.render(explanations[selected_difficulty], True, COLORS['BOARD_LIGHT'])
    text_x = (WINDOW_WIDTH - text_surface.get_width()) // 2
    text_y = start_y + (len(buttons) * button_spacing) + 20
    screen.blit(text_surface, (text_x, text_y))
    
    pygame.display.flip()
    return button_positions

def render_pause_menu(screen):
    bg_image = load_background()
    if bg_image:
        screen.blit(bg_image, (0, 0))
    else:
        screen.fill(COLORS['BOARD_DARK'])
    
    buttons = {
        'resume': create_button('Continuar'),
        'menu': create_button('Menu Principal'),
        'exit': create_button('Sair do Jogo')
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

def get_button_clicked(button_positions, mouse_pos):
    for key, (x, y) in button_positions.items():
        button_rect = pygame.Rect(x, y, 300, 50)
        if button_rect.collidepoint(mouse_pos):
            return key
    return None
