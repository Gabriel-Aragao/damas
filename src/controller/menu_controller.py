import asyncio  # Para atrasos assíncronos
import pygame
from src.view.menu_view import render_menu, render_settings_menu, get_button_clicked
from src.controller.game_controller import start_game, start_ai_game
from src.config.settings_manager import set_ai_difficulty

# Converte o loop do menu principal em uma função assíncrona.
async def handle_main_menu(screen):
    """Manipula a interação e navegação do menu principal de forma assíncrona."""
    running = True
    while running:
        # Desenha o menu e obtém as posições dos botões.
        button_positions = render_menu(screen)
        
        # Processa eventos.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                action = get_button_clicked(button_positions, event.pos)
                if action:
                    if action == "pvp":
                        # Aguarda o início do jogo PvP assíncrono.
                        result = await start_game()
                        if result == "exit":
                            return "exit"
                    elif action == "ai":
                        # Aguarda o início do jogo contra IA assíncrono.
                        result = await start_ai_game()
                        if result == "exit":
                            return "exit"
                    elif action == "settings":
                        # Aguarda o menu de configurações assíncrono.
                        result = await handle_difficulty_menu(screen)
                        if result == "exit":
                            return "exit"
                    elif action == "exit":
                        return "exit"
        
        pygame.display.flip()
        # Cede o controle para manter o navegador responsivo.
        await asyncio.sleep(0)

# Manipulador do menu de dificuldade
async def handle_difficulty_menu(screen):
    """Manipula o menu de seleção de dificuldade da IA."""
    running = True
    while running:
        button_positions = render_settings_menu(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                action = get_button_clicked(button_positions, event.pos)
                if action:
                    if action.startswith('difficulty_'):
                        # Extrai o nível de dificuldade da string de ação
                        difficulty = int(action.split('_')[1])
                        # Define a dificuldade da IA
                        set_ai_difficulty(difficulty)
                        print(f"[LOG] Dificuldade da IA definida para nível {difficulty}")
                    elif action == "back":
                        return None
        
        pygame.display.flip()
        await asyncio.sleep(0)