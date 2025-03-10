import asyncio 
import pygame
from src.view.menu_view import render_menu, render_settings_menu, get_button_clicked
from src.controller.game_controller import start_game, start_ai_game
from src.config.settings_manager import set_ai_difficulty


async def handle_main_menu(screen):
    running = True
    while running:
        button_positions = render_menu(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                action = get_button_clicked(button_positions, event.pos)
                if action:
                    if action == "pvp":
                        result = await start_game()
                        if result == "exit":
                            return "exit"
                    elif action == "ai":
                        result = await start_ai_game()
                        if result == "exit":
                            return "exit"
                    elif action == "settings":
                        result = await handle_difficulty_menu(screen)
                        if result == "exit":
                            return "exit"
                    elif action == "exit":
                        return "exit"

        pygame.display.flip()
        await asyncio.sleep(0)


async def handle_difficulty_menu(screen):
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
                        difficulty = int(action.split('_')[1])
                        set_ai_difficulty(difficulty)
                    elif action == "back":
                        return None
        
        pygame.display.flip()
        await asyncio.sleep(0)