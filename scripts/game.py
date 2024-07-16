import pygame
from pygame.locals import *
from scripts.levels import Level
from scripts.gameData import endless
from scripts.menus import *
from scripts.settings import FPS, BLACK, FONT, play_menu_select_sound

clock = pygame.time.Clock()

class Game:
    def __init__(self, screen):
        self.running, self.playing, self.player_alive = True, False, True
        self.UP_KEY, self.DOWN_KEY, self.click, self.BACK_KEY = False, False, False, False
        self.display = screen
        self.main_menu = MainMenu(self)
        self.credits = CreditsMenu(self)
        self.death_screen = DeathScreen(self)
        self.pause_menu = PauseMenu(self)
        self.curr_menu = self.main_menu

    def setup(self):
        self.level_name = endless
        self.level = Level(self.level_name, self.display)

    def game_loop(self):
        while self.playing and self.player_alive:
            self.check_events()
            if self.BACK_KEY:
                play_menu_select_sound()
                self.playing, self.player_alive = False, True
                self.curr_menu = self.pause_menu
            self.display.fill(BLACK)
            self.player_alive, self.final_score = self.level.run(int(clock.get_fps()))
            if not self.player_alive: self.curr_menu = self.death_screen # set to death screen if player is dead
            pygame.display.update()
            clock.tick(FPS)
            self.reset_keys()
        self.player_alive = True

    def check_events(self):
        self.mx, self.my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.curr_menu.run_display = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True
            if event.type == MOUSEBUTTONDOWN: 
                if event.button == 1:
                    self.click = True
                    
    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.click, self.BACK_KEY = False, False, False, False

    def draw_text(self, text, size, x, y, colour):
        font = pygame.font.Font(FONT, size)
        text_surface = font.render(text, True, colour)
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.display.blit(text_surface,text_rect)