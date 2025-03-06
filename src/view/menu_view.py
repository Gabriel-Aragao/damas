import os
import pygame
from src.config.settings import *
from src.config.constants import *

def load_background():
    """Carrega e redimensiona a imagem de fundo."""
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, 'assets', 'menu_bg.png')
        bg_image = pygame.image.load(image_path)
        return pygame.transform.scale(bg_image, (WINDOW_WIDTH, WINDOW_HEIGHT))
    except Exception as e:
        print(f"Erro ao carregar o fundo: {e}")
        return None

def render_menu(screen):
    """Renderiza o menu principal."""
    # Carrega e desenha o fundo
    bg_image = load_background()
    if bg_image:
        screen.blit(bg_image, (0, 0))
    else:
        screen.fill(COLORS['BOARD_DARK'])
    
    # Adiciona o botão de configurações
    buttons = {
        'pvp': create_button('Jogador vs Jogador'),
        'ai': create_button('Jogador vs IA'),
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
    """Cria uma superfície de botão com texto."""
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
    """Desenha um botão na tela."""
    x, y = position
    button['rect'].topleft = (x, y)
    
    # Fundo do botão - cria uma superfície com transparência
    bg_surface = pygame.Surface((button['rect'].width, button['rect'].height), pygame.SRCALPHA)
    
    # Escolhe a cor com base no estado de hover
    if is_hovered:
        bg_color = (255, 255, 0, 200)  # Amarelo com transparência
    else:
        bg_color = (64, 64, 64, 200)  # Cinza escuro com transparência
    
    # Desenha o fundo na superfície com transparência
    pygame.draw.rect(bg_surface, bg_color, bg_surface.get_rect(), border_radius=10)
    screen.blit(bg_surface, button['rect'].topleft)
    
    # Borda do botão
    pygame.draw.rect(screen, COLORS['BOARD_LIGHT'], button['rect'], 2, border_radius=10)
    
    # Centraliza o texto no botão
    text_x = x + (button['rect'].width - button['text'].get_width()) // 2
    text_y = y + (button['rect'].height - button['text'].get_height()) // 2
    screen.blit(button['text'], (text_x, text_y))

def render_settings_menu(screen):
    """Renderiza o menu de configurações com opções de dificuldade."""
    from src.config.settings_manager import get_ai_difficulty
    
    # Cria sobreposição semi-transparente
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))
    screen.blit(overlay, (0, 0))
    
    # Desenha o título do menu
    font = pygame.font.SysFont('Arial', 48)
    title_text = font.render('Configurações de Dificuldade da IA', True, COLORS['BOARD_LIGHT'])
    title_x = (WINDOW_WIDTH - title_text.get_width()) // 2
    screen.blit(title_text, (title_x, 80))
    
    # Obtém a dificuldade atual da IA
    current_difficulty = get_ai_difficulty()
    
    # Cria botões de dificuldade
    buttons = {}
    for i in range(1, 6):
        label = f"Nível {i}" + (" (Atual)" if i == current_difficulty else "")
        buttons[f'difficulty_{i}'] = create_button(label)
    
    buttons['back'] = create_button('Menu Principal')
    
    # Posiciona os botões
    button_spacing = 70
    total_height = len(buttons) * button_spacing
    start_y = (WINDOW_HEIGHT - total_height) // 2 + 30  # Deslocamento para o título
    
    # Desenha os botões
    mouse_pos = pygame.mouse.get_pos()
    button_positions = {}
    
    for i, (key, button) in enumerate(buttons.items()):
        x = (WINDOW_WIDTH - button['rect'].width) // 2
        y = start_y + (i * button_spacing)
        button_positions[key] = (x, y)
        
        button_rect = pygame.Rect(x, y, button['rect'].width, button['rect'].height)
        is_hovered = button_rect.collidepoint(mouse_pos)
        
        # Destaca a dificuldade atual
        if key == f'difficulty_{current_difficulty}':
            # Cria uma cor de destaque ligeiramente diferente para a seleção atual
            highlight_color = (255, 215, 0, 100)  # Dourado com transparência
            pygame.draw.rect(screen, highlight_color, button_rect, border_radius=10)
        
        draw_button(screen, button, (x, y), is_hovered)
    
    # Adiciona texto explicativo
    font_small = pygame.font.SysFont('Arial', 18)
    explanations = [
        "Nível 1: Fácil - IA prevê 1 movimento à frente",
        "Nível 2: Casual - IA prevê 2 movimentos à frente",
        "Nível 3: Moderado - IA prevê 3 movimentos à frente",
        "Nível 4: Desafiador - IA prevê 4 movimentos à frente",
        "Nível 5: Difícil - IA prevê 5 movimentos à frente"
    ]
    
    for i, text in enumerate(explanations):
        text_surface = font_small.render(text, True, COLORS['BOARD_LIGHT'])
        text_x = (WINDOW_WIDTH - text_surface.get_width()) // 2
        text_y = start_y + ((len(buttons) + i) * button_spacing) + 20
        screen.blit(text_surface, (text_x, text_y))
    
    pygame.display.flip()
    return button_positions

def render_pause_menu(screen):
    """Renderiza a sobreposição do menu de pausa."""
    # Cria sobreposição semi-transparente
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))
    screen.blit(overlay, (0, 0))
    
    # Cria botões
    buttons = {
        'resume': create_button('Continuar'),
        'menu': create_button('Menu Principal'),
        'exit': create_button('Sair do Jogo')
    }
    
    # Posiciona botões
    button_spacing = 70
    total_height = len(buttons) * button_spacing
    start_y = (WINDOW_HEIGHT - total_height) // 2
    
    # Desenha botões
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
    """Retorna qual botão foi clicado, se houver."""
    for key, (x, y) in button_positions.items():
        button_rect = pygame.Rect(x, y, 300, 50)  # Usando tamanho padrão de botão
        if button_rect.collidepoint(mouse_pos):
            return key
    return None
