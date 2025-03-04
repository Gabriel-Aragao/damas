import asyncio
import pygame
from src.config.settings import *
from src.controller.menu_controller import handle_main_menu
from src.controller.game_controller import handle_game_loop

async def main():
    pygame.init()
    # Set the display dimensions using the provided constants
    screen = pygame.display.set_mode((BOARD_SIZE * SQUARE_SIZE, BOARD_SIZE * SQUARE_SIZE))
    
    while True:
        # Yield control so the browser can update
        await asyncio.sleep(0)
        # Get menu selection
        selection = await handle_main_menu(screen)
        
        if selection == "1v1":
            # Player vs Player mode
            await handle_game_loop(screen, mode='pvp')
        elif selection == "ai":
            # Player vs AI mode
            await handle_game_loop(screen, mode='ai')
        elif selection == "exit":
            break
            
    # Quit pygame once the loop is exited
    pygame.quit()

asyncio.run(main())