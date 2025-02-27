import asyncio  # For asynchronous delays
import pygame
from src.view.menu_view import render_menu, render_settings_menu, get_button_clicked
from src.controller.game_controller import start_game, start_ai_game
from src.config.settings_manager import set_ai_difficulty

# Convert the main menu loop into an async function.
async def handle_main_menu(screen):
    """Handle main menu interaction and navigation asynchronously."""
    running = True
    while running:
        # Draw menu and get button positions.
        button_positions = render_menu(screen)
        
        # Process events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                action = get_button_clicked(button_positions, event.pos)
                if action:
                    if action == "pvp":
                        # Await the async PvP game start.
                        result = await start_game()
                        if result == "exit":
                            return "exit"
                    elif action == "ai":
                        # Await the async AI game start.
                        result = await start_ai_game()
                        if result == "exit":
                            return "exit"
                    elif action == "settings":
                        # Await the async settings menu.
                        result = await handle_difficulty_menu(screen)
                        if result == "exit":
                            return "exit"
                    elif action == "exit":
                        return "exit"
        
        pygame.display.flip()
        # Yield control to keep the browser responsive.
        await asyncio.sleep(0)

# Difficulty menu handler
async def handle_difficulty_menu(screen):
    """Handle AI difficulty selection menu."""
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
                        # Extract difficulty level from the action string
                        difficulty = int(action.split('_')[1])
                        # Set the AI difficulty
                        set_ai_difficulty(difficulty)
                        print(f"[LOG] AI difficulty set to level {difficulty}")
                    elif action == "back":
                        return None
        
        pygame.display.flip()
        await asyncio.sleep(0)