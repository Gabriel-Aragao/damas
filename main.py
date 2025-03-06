import asyncio
import pygame
from src.config.settings import *
from src.controller.menu_controller import handle_main_menu
from src.controller.game_controller import handle_game_loop

async def main():
    pygame.init()
    # Define as dimensões da tela usando as constantes fornecidas
    screen = pygame.display.set_mode((BOARD_SIZE * SQUARE_SIZE, BOARD_SIZE * SQUARE_SIZE))
    
    running = True
    while running:
        # Cede o controle para que o navegador possa atualizar
        await asyncio.sleep(0)
        # Obtém a seleção do menu
        selection = await handle_main_menu(screen)
        
        if selection == "1v1":
            # Modo Jogador contra Jogador
            await handle_game_loop(screen, mode='pvp')
        elif selection == "ai":
            # Modo Jogador contra IA
            await handle_game_loop(screen, mode='ai')
        elif selection == "exit":
            running = False
            
    # Encerra o pygame quando o loop for finalizado
    pygame.quit()

asyncio.run(main())