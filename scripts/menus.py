import pygame, sys, webbrowser
from scripts.settings import MID_W, WINDOW_SIZE, WHITE, BLACK, DEATH_TEXT_COLOUR, MID_W, MID_H, play_menu_select_sound, draw_text


class Menu():
    def __init__(self, game):
        self.game = game
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = - 120

    def draw_cursor(self):
        draw_text(self.game.display, ">>", 20, self.cursor_rect.x, self.cursor_rect.y, WHITE)

    def blit_screen(self):
        self.game.display.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()


class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

        self.bossesx, self.bossesy = MID_W, MID_H + 10
        self.bosses_rect = pygame.Rect(MID_W - 105, MID_H - 10, 210, 39)

        self.endlessx, self.endlessy = MID_W, MID_H + 50
        self.endless_rect = pygame.Rect(MID_W - 105, MID_H + 30, 210, 39)

        self.creditsx, self.creditsy = MID_W, MID_H + 90
        self.credits_rect = pygame.Rect(MID_W - 105, MID_H + 71, 210, 39)

        self.exitx, self.exity = MID_W, MID_H + 130
        self.exit_rect = pygame.Rect(MID_W - 105, MID_H + 110, 210, 39)

        
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(BLACK)
            draw_text(self.game.display, 'Bullet Bounce', 70, WINDOW_SIZE[0] / 2, WINDOW_SIZE[1] / 2 - 250, WHITE)
            draw_text(self.game.display, "Stage", int(30 * self.boss_scale), self.bossesx, self.bossesy, WHITE)
            draw_text(self.game.display, "Endless", int(30 * self.endless_scale), self.endlessx, self.endlessy, WHITE)
            draw_text(self.game.display, "Credits", int(30 * self.credits_scale), self.creditsx, self.creditsy, WHITE)
            draw_text(self.game.display, "Exit", int(30 * self.exit_scale), self.exitx, self.exity, WHITE)
            self.draw_cursor()
            self.blit_screen()

    #updates the cursor with mouse position
    def move_cursor(self):
        if self.bosses_rect.collidepoint((self.game.mx,self.game.my)):
            self.cursor_rect.midtop = (self.bossesx + self.offset, self.bossesy)
            self.boss_scale = 1.2
            self.endless_scale = self.exit_scale = self.credits_scale = 1
        elif self.endless_rect.collidepoint((self.game.mx,self.game.my)):
            self.cursor_rect.midtop = (self.endlessx + self.offset, self.endlessy)
            self.endless_scale = 1.2
            self.boss_scale = self.exit_scale = self.credits_scale = 1
        elif self.credits_rect.collidepoint((self.game.mx,self.game.my)):
            self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
            self.credits_scale = 1.2
            self.boss_scale = self.endless_scale = self.exit_scale = 1
        elif self.exit_rect.collidepoint((self.game.mx,self.game.my)):
            self.cursor_rect.midtop = (self.exitx + self.offset, self.exity)
            self.exit_scale = 1.2
            self.boss_scale = self.endless_scale = self.credits_scale = 1
        else:
            self.cursor_rect.midtop = (0,0)
            self.boss_scale = self.endless_scale = self.exit_scale = self.credits_scale = 1

    def check_input(self):
        self.move_cursor()
        if self.game.click:
            if self.bosses_rect.collidepoint((self.game.mx,self.game.my)):
                play_menu_select_sound()
                self.game.playing = True
                self.game.setup("boss1")
            elif self.endless_rect.collidepoint((self.game.mx,self.game.my)):
                play_menu_select_sound()
                self.game.playing = True
                self.game.setup()
            elif self.credits_rect.collidepoint((self.game.mx,self.game.my)):
                play_menu_select_sound()
                self.game.curr_menu = self.game.credits
            elif self.exit_rect.collidepoint((self.game.mx,self.game.my)):
                play_menu_select_sound(0.5)
                pygame.quit()
                sys.exit()
        elif self.game.BACK_KEY:
            play_menu_select_sound(0.5)
            pygame.quit()
            sys.exit()
        self.run_display = False


class PauseMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

        self.resumex, self.resumey = MID_W, MID_H
        self.resume_rect = pygame.Rect(MID_W - 105, MID_H - 20, 210, 39)

        self.back_to_menux, self.back_to_menuy = MID_W, MID_H + 40
        self.back_to_menu_rect = pygame.Rect(MID_W - 105, MID_H + 29, 210, 69)

        self.exitx, self.exity = MID_W, MID_H + 110
        self.exit_rect = pygame.Rect(MID_W - 105, MID_H + 97, 210, 39)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(BLACK)
            draw_text(self.game.display, 'Paused', 70, WINDOW_SIZE[0] / 2, WINDOW_SIZE[1] / 2 - 250, WHITE)
            draw_text(self.game.display, "Resume", int(30 * self.resume_scale), self.resumex, self.resumey, WHITE)
            draw_text(self.game.display, "Back to", int(30 * self.back_scale), self.back_to_menux, self.back_to_menuy, WHITE)
            draw_text(self.game.display, "Menu", int(30 * self.back_scale), self.back_to_menux, self.back_to_menuy + 30, WHITE)
            draw_text(self.game.display, "Exit", int(30 * self.exit_scale), self.exitx, self.exity, WHITE)
            self.draw_cursor()
            self.blit_screen()

    #updates the cursor with mouse position
    def move_cursor(self):
        if self.resume_rect.collidepoint((self.game.mx,self.game.my)):
            self.cursor_rect.midtop = (self.resumex + self.offset, self.resumey)
            self.resume_scale = 1.2
            self.exit_scale = self.back_scale = 1
        elif self.back_to_menu_rect.collidepoint((self.game.mx,self.game.my)):
            self.cursor_rect.midtop = (self.back_to_menux + self.offset, self.back_to_menuy + 12)
            self.back_scale = 1.2
            self.resume_scale = self.exit_scale = 1
        elif self.exit_rect.collidepoint((self.game.mx,self.game.my)):
            self.cursor_rect.midtop = (self.exitx + self.offset, self.exity)
            self.exit_scale = 1.2
            self.resume_scale = self.back_scale = 1
        else:
            self.cursor_rect.midtop = (0,0)
            self.resume_scale = self.back_scale = self.exit_scale = 1

    def check_input(self):
        self.move_cursor()
        if self.game.click:
            if self.resume_rect.collidepoint((self.game.mx,self.game.my)):
                play_menu_select_sound()
                self.game.playing = True
            elif self.back_to_menu_rect.collidepoint((self.game.mx,self.game.my)):
                play_menu_select_sound()
                self.game.curr_menu = self.game.main_menu
            elif self.exit_rect.collidepoint((self.game.mx,self.game.my)):
                play_menu_select_sound(0.5)
                pygame.quit()
                sys.exit()
        elif self.game.BACK_KEY:
            play_menu_select_sound(0.5)
            pygame.quit()
            sys.exit()
        self.run_display = False

class CreditsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game) 

        self.fontx, self.fonty = MID_W, MID_H - 50
        self.font_rect = pygame.Rect(MID_W - 70, MID_H - 70, 140, 45)

        self.codex, self.codey = MID_W, MID_H
        self.code = pygame.Rect(MID_W - 70, MID_H - 25, 140, 78)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            if self.game.BACK_KEY:
                play_menu_select_sound()
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            self.game.display.fill(BLACK)
            draw_text(self.game.display, 'Credits', 50, WINDOW_SIZE[0] / 2, WINDOW_SIZE[1] / 2 - 175, WHITE)
            draw_text(self.game.display, 'Font', int(30 * self.font_scale), self.fontx, self.fonty, WHITE)
            draw_text(self.game.display, 'Code', int(30 * self.sound_scale), self.codex, self.codey, WHITE)
            draw_text(self.game.display, 'Tutorials', int(30 * self.sound_scale), self.codex, self.codey + 30, WHITE)
            self.draw_cursor()
            self.blit_screen()

    #updates the text size with mouse position
    def move_cursor(self):
        if self.font_rect.collidepoint((self.game.mx,self.game.my)):
            self.cursor_rect.midtop = (self.fontx + self.offset, self.fonty)
            self.font_scale = 1.2
            self.sound_scale = 1
        elif self.code.collidepoint((self.game.mx,self.game.my)):
            self.cursor_rect.midtop = (self.codex + self.offset, self.codey + 12)
            self.sound_scale = 1.2
            self.font_scale = 1
        else: 
            self.cursor_rect.midtop = (0,0)
            self.font_scale = self.sound_scale = 1

    def check_input(self):
        self.move_cursor()
        if self.game.click:
            if self.font_rect.collidepoint((self.game.mx,self.game.my)):
                play_menu_select_sound()
                webbrowser.open("https://www.dafont.com/minecraft.font", new = 2)
            elif self.code.collidepoint((self.game.mx,self.game.my)):
                play_menu_select_sound()
                webbrowser.open("https://www.youtube.com/watch?v=wNMRq_uoWM0", new = 2)
                webbrowser.open("https://www.youtube.com/watch?v=a5JWrd7Y_14", new = 2)


class EndScreen(Menu):
    def __init__(self, game):
        Menu.__init__(self, game) 

    def display_menu(self, header, stats, command):
        self.run_display = True
        self.ellipses_num = 0
        while self.run_display:
            self.game.check_events()
            self.check_input()
            if self.ellipses_num <= 4: self.ellipses_num += 0.005
            else: self.ellipses_num = 0

            self.game.display.fill(BLACK)
            draw_text(self.game.display, header, 70, WINDOW_SIZE[0] / 2, WINDOW_SIZE[1] / 2 - 225, DEATH_TEXT_COLOUR)
            draw_text(self.game.display, stats, 40, WINDOW_SIZE[0] / 2, WINDOW_SIZE[1] / 2 - 100, WHITE)
            draw_text(self.game.display, f"Click again to go to the {command} or press Escape to quit", 20, WINDOW_SIZE[0] / 2, WINDOW_SIZE[1] / 2 + 230, WHITE)
            draw_text(self.game.display, int(self.ellipses_num) * '. ', 20, WINDOW_SIZE[0] / 2 + 305, WINDOW_SIZE[1] / 2 + 230, WHITE)
            self.blit_screen()

    def check_input(self):
        if self.game.click:
            play_menu_select_sound()
            self.game.curr_menu = self.game.main_menu #set the last screen to main menu so when user presses esc they return to main menu
            self.game.playing = False
            self.run_display = False
        if self.game.BACK_KEY:
            play_menu_select_sound(0.5)
            pygame.quit()
            sys.exit()


class DeathScreen(EndScreen):
    def __init__(self, game):
        EndScreen.__init__(self, game)

    def display_menu(self, final_score):
        return super().display_menu("YOU DIED", f"Score: {str(final_score)}", "main menu")

class VictoryScreen(EndScreen):
    def __init__(self, game):
        EndScreen.__init__(self, game)

    def display_menu(self, completed_time=0):
        return super().display_menu("VICTORY", f"Time: {str(completed_time)}s", "next boss")

    