import pygame
from scripts.settings import FONT, WHITE, BLACK, RED, GREEN

class Ui:
    def __init__(self, surf):
        self.display_surf = surf
        self.font = pygame.font.Font(FONT, 28)
        self.small_font = pygame.font.Font(FONT, 11)

        #FPS
        self.fps_text = self.font.render("FPS:", False, WHITE)
        self.fps_rect = self.fps_text.get_rect(topleft = (40, 12))       

        #Score
        self.score_text = self.font.render("Score:", False, WHITE)
        self.score_rect = self.score_text.get_rect(topleft = (40, 37))

    def draw_healthbar(self, pos, full_health, current_health):
        ratio = (full_health - current_health) / full_health
        green_bar = pygame.Rect(pos[0], pos[1], int(50 - (50 * ratio)), 10)
        red_bar = pygame.Rect(pos[0], pos[1], 50, 10)
        bar_outline = pygame.Rect(pos[0] - 2, pos[1] - 2, 52, 12)
        pygame.draw.rect(self.display_surf, RED, red_bar)
        pygame.draw.rect(self.display_surf, GREEN, green_bar)
        self.display_surf.blit(self.small_font.render(str(current_health), False, WHITE), (pos[0], pos[1]))
        pygame.draw.rect(self.display_surf, BLACK, bar_outline, 2)

    def show_fps(self, fps):
        self.display_surf.blit(self.fps_text, self.fps_rect)
        current_fps = self.font.render(str(fps), False, WHITE)
        current_fps_rect = current_fps.get_rect(midleft = (self.fps_rect.right + 35, self.fps_rect.centery))
        self.display_surf.blit(current_fps, current_fps_rect)
        
    def show_score(self, score):
        self.display_surf.blit(self.score_text, self.score_rect)
        current_score = self.font.render(str(score), False, WHITE)
        current_store_rect = current_score.get_rect(midleft = (self.score_rect.right + 12, self.score_rect.centery))
        self.display_surf.blit(current_score, current_store_rect)
