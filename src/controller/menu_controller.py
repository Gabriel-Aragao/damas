import asyncio  # For asynchronous delays
import pygame
from src.view.menu_view import render_menu, render_settings_menu, get_button_clicked
from src.controller.game_controller import start_game  # Now async version in game_controller
from src.controller.game_controller import start_ai_game  # Now async version

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
                        result = await handle_settings_menu(screen)
                        if result == "exit":
                            return "exit"
                    elif action == "exit":
                        return "exit"
        
        pygame.display.flip()
        # Yield control to keep the browser responsive.
        await asyncio.sleep(0)

# Convert the settings menu loop into async.
async def handle_settings_menu(screen):
    """Handle settings menu interaction asynchronously."""
    running = True
    while running:
        button_positions = render_settings_menu(screen)
        
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
        await asyncio.sleep(0)