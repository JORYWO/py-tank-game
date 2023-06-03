import pygame, math
from scripts.settings import PROJ_COLOUR, BLACK

class Projectile():
    def __init__(self, pos, angle):
        self.size = 10
        self.rect = pygame.Rect(pos[0], pos[1], self.size, self.size)
        self.x , self.y = pos

        self.dx = math.cos(angle)
        self.dy = math.sin(angle)
        self.vel_x, self.vel_y = 7, 7
        self.light_effect = 8
        self.increment_up = True

        self.collision_num = 0
        self.damage = 5 

    def update(self):
        self.x += self.dx * self.vel_x
        self.y += self.dy * self.vel_y
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        if self.increment_up and self.light_effect <= 8: self.light_effect += 0.2
        else: self.increment_up = False

        if not self.increment_up and self.light_effect >= 0: self.light_effect -= 0.2
        else: self.increment_up = True

    def draw(self, surf):
        self.update()
        pygame.draw.ellipse(surf, PROJ_COLOUR, (self.rect.x,self.rect.y,self.size,self.size))
        shadowRadius = self.size + int(self.light_effect)
        surf.blit(self.circle_lighting(shadowRadius, PROJ_COLOUR),
            (int(self.rect.centerx - shadowRadius), int(self.rect.centery - shadowRadius)), special_flags=pygame.BLEND_RGBA_ADD)

    # provides lighting for the projectile
    def circle_lighting(self, radius, colour):
        surf = pygame.Surface((radius * 2, radius * 2))
        pygame.draw.circle(surf, colour, (radius, radius), radius)
        surf.set_colorkey(BLACK)
        return surf


    
