import pygame
from scripts.game import Game
from scripts.settings import WINDOW_SIZE

pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE, pygame.RESIZABLE,)

if __name__ == "__main__":
    game = Game(screen)
    
    #main game loop
    while game.running:
        if game.curr_menu == game.death_screen: 
            stats = game.final_score if game.is_endless else game.start_time
            game.curr_menu.display_menu(stats, game.is_endless)
        elif game.curr_menu == game.victory_screen: game.curr_menu.display_menu(game.start_time)
        else: game.curr_menu.display_menu()
        game.game_loop()