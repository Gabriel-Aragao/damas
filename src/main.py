import pygame
from config.settings import *
from controller.menu_controller import *
from controller.game_controller import handle_game_loop

def main():
    pygame.init()
    screen = pygame.display.set_mode((BOARD_SIZE * SQUARE_SIZE, BOARD_SIZE * SQUARE_SIZE))
    
    while True:
        selection = handle_main_menu(screen)
        
        if selection == "1v1":
            handle_game_loop(screen)
        elif selection == "ai":
            # Future AI mode
            pass
        elif selection == "exit":
            break

if __name__ == "__main__":
    main()