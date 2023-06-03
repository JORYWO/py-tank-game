import pygame
from math import cos, sin
from pygame.locals import *
from random import randint
from scripts.settings import NORMAL_ENEMY_COLOUR, TRACKER_ENEMY_COLOUR, get_angle

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.size = randint(30, 60)
        self.rect = pygame.Rect(pos[0], pos[1], self.size, self.size)
        self.start_tick = pygame.time.get_ticks()

        self.x, self.y = pos
        self.damage = self.size // 2

        self.spawned = False

    def update(self):
        self.damage = self.size // 2
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

    def draw(self, surf):
        milliseconds = pygame.time.get_ticks() - self.start_tick
        if milliseconds > 1000: 
            pygame.draw.ellipse(surf, self.colour, (self.rect.x, self.rect.y, self.size, self.size), 5)
            self.spawned = True
        else:  
            if (milliseconds // 100) % 2 == 0:  #blink effect
                pygame.draw.ellipse(surf, self.colour, (self.rect.x, self.rect.y, self.size, self.size), 5)


class NormalEnemy(Enemy):
    def __init__(self, pos):
        super().__init__(pos)
        self.vel_x, self.vel_y = ((-1) ** randint(0, 1)) * randint(2,5), ((-1) ** randint(0, 1)) * randint(2,5)
        self.colour = NORMAL_ENEMY_COLOUR

    def update(self):
        super().update()
        self.x += self.vel_x
        self.y += self.vel_y
        self.rect.x, self.rect.y = self.x, self.y

    def draw(self, surf):
        super().draw(surf)
        if self.spawned: self.update() #only move enemy after 1 second


'''Follows the player'''
class TrackerEnemy(Enemy):
    def __init__(self, pos):
        super().__init__(pos)
        self.vel_x , self.vel_y = 4, 4
        self.colour = TRACKER_ENEMY_COLOUR

    # find angle between player and self and adjust vel_x and vel_y
    def update(self, playerPos):
        super().update()
        angle = get_angle(playerPos, self.rect.center)
        dx, dy = cos(angle), sin(angle)
        self.x += dx * self.vel_x
        self.y += dy * self.vel_y
        self.rect.x, self.rect.y = self.x, self.y
    
    def draw(self, surf, playerPos):
        super().draw(surf)
        if self.spawned: self.update(playerPos) #only move enemy after 1 second


