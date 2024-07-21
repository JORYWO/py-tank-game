import pygame
from scripts.game import Game
from scripts.settings import WINDOW_SIZE

pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE, pygame.RESIZABLE,)

if __name__ == "__main__":
    game = Game(screen)
    
    #main game loop
    while game.running:
        if game.curr_menu == game.death_screen: game.curr_menu.display_menu(game.final_score)
        elif game.curr_menu == game.victory_screen: game.curr_menu.display_menu()
        else: game.curr_menu.display_menu()
        game.game_loop()