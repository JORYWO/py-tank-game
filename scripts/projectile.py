import pygame, math
from scripts.settings import BLACK

class Projectile():
    def __init__(self, pos, angle, colour, size = 10, collision_num=1):
        self.size = size
        self.rect = pygame.Rect(pos[0], pos[1], self.size, self.size)
        self.x , self.y = pos
        self.colour = colour

        self.dx = math.cos(angle)
        self.dy = math.sin(angle)
        self.vel_x, self.vel_y = 7, 7
        self.light_effect = 8
        self.increment_up = True

        self.collision_num = collision_num
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
        surface = pygame.Surface((self.size, self.size))
        self.mask = pygame.mask.from_surface(surface)

    def draw(self, surf):
        self.update()
        pygame.draw.ellipse(surf, self.colour, (self.rect.x,self.rect.y,self.size,self.size))
        shadowRadius = self.size + int(self.light_effect)
        # surf.blit(self.mask.to_surface(), self.rect.topleft)
        surf.blit(self.circle_lighting(shadowRadius, self.colour),
            (int(self.rect.centerx - shadowRadius), int(self.rect.centery - shadowRadius)), special_flags=pygame.BLEND_RGBA_ADD)

    # provides lighting for the projectile
    def circle_lighting(self, radius, colour):
        surf = pygame.Surface((radius * 2, radius * 2))
        pygame.draw.circle(surf, colour, (radius, radius), radius)
        surf.set_colorkey(BLACK)
        return surf


    
