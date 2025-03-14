import asyncio
import pygame
from src.config.settings import *
from src.controller.menu_controller import handle_main_menu
from src.controller.game_controller import handle_game_loop

async def main():
    pygame.init()
    screen = pygame.display.set_mode((BOARD_SIZE * SQUARE_SIZE, BOARD_SIZE * SQUARE_SIZE))
    
    running = True
    while running:
        await asyncio.sleep(0)
    
        selection = await handle_main_menu(screen)
        
        if selection == "1v1":
            await handle_game_loop(screen, mode='pvp')
        elif selection == "ai":
            await handle_game_loop(screen, mode='ai')
        elif selection == "exit":
            running = False
            
    pygame.quit()

asyncio.run(main())