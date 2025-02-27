import asyncio
import pygame
from src.config.settings import *
from src.controller.menu_controller import handle_main_menu  # now async version
from src.controller.game_controller import handle_game_loop       # now async version

async def main():
    pygame.init()
    # Set the display dimensions using the provided constants
    screen = pygame.display.set_mode((BOARD_SIZE * SQUARE_SIZE, BOARD_SIZE * SQUARE_SIZE))
    
    while True:
        # Yield control so the browser can update
        await asyncio.sleep(0)
        # Use await when calling your async menu loop
        selection = await handle_main_menu(screen)
        
        if selection == "1v1":
            await handle_game_loop(screen)  # call async version
        elif selection == "ai":
            # Future AI mode -- placeholder for additional functionality.
            pass
        elif selection == "exit":
            break
            
    # Quit pygame once the loop is exited
    pygame.quit()

asyncio.run(main())