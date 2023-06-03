import pygame, math
from pygame.locals import *
from scripts.projectile import Projectile
from scripts.settings import VEC, PLAYER_SIZE, get_angle

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.max_frames = 0
        self.frame_index = 0
        self.animation_speed = 0.15
        self.health = 100
        self.score = 0
        self.pos = pos
        self.alive = True

        #spritesheets
        self.animation = pygame.image.load("data/sprites/playerMove.png").convert_alpha()
        self.turret_sheet = pygame.image.load("data/sprites/playerTurret.png").convert_alpha()
        self.image = self.animation.subsurface(0, 0 , PLAYER_SIZE, PLAYER_SIZE)
        self.rect = self.image.get_rect(center = pos)

        #playerState
        self.facing_right ,self.facing_left, self.facing_down = False, False, False
        self.facing_up = True

        #shoot mechanic
        self.projectiles = []
        self.cooldown = 0
        self.shooting = False
        self.turret_index = 0

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index > self.max_frames:
            self.frame_index = 0

        image = self.animation.subsurface(int(self.frame_index) * PLAYER_SIZE, 0 , PLAYER_SIZE, PLAYER_SIZE)
        turret = self.turret_sheet.subsurface(int(self.turret_index) * PLAYER_SIZE, 0 , PLAYER_SIZE, PLAYER_SIZE)
        if self.facing_up:
            self.image = image.copy()
        elif self.facing_down:
            self.image = pygame.transform.flip(image, True, True)
        elif self.facing_right:
            self.image = pygame.transform.rotate(image, -90)
        elif self.facing_left:
            self.image = pygame.transform.rotate(image, 90)

        if self.shooting:
            self.turret_index += 0.3
        if self.turret_index >= self.turret_sheet.get_width() / PLAYER_SIZE:
            self.turret_index = 0
            self.shooting = False

        #rotate turret with mouse
        self.turret = pygame.transform.rotate(turret, 270 - get_angle(pygame.mouse.get_pos(), self.rect.center) * (180/math.pi))
        self.image.blit(self.turret, (32 - int(self.turret.get_width() / 2), 32 - int(self.turret.get_height() / 2)))

    #user input
    def user_input(self):
        self.acc = VEC(0,0)
        keys = pygame.key.get_pressed()

        #can only move in 1 direction
        if keys[pygame.K_d]:
            self.acc.x = 1
            self.facing_right = True
            self.facing_left, self.facing_up, self.facing_down = False, False, False
        elif keys[pygame.K_a]:
            self.acc.x = -1
            self.facing_left = True
            self.facing_right, self.facing_up, self.facing_down = False, False, False
        elif keys[pygame.K_w]:
            self.acc.y = -1
            self.facing_up = True
            self.facing_right, self.facing_left, self.facing_down  = False, False, False
        elif keys[pygame.K_s]:
            self.acc.y = 1
            self.facing_down = True
            self.facing_right, self.facing_left, self.facing_up = False, False, False
        if not any(pygame.key.get_pressed()):
            self.acc = VEC(0,0)

        if pygame.mouse.get_pressed()[0] and self.cooldown > 8:
            self.shoot()
            self.cooldown = 0
        if not pygame.mouse.get_pressed()[0]: self.speed = 6

    def shoot(self):
        self.shooting = True
        self.speed = 3 #slow down player when they are shooting
        self.projectiles.append(Projectile((self.rect.centerx, self.rect.centery),  
            get_angle(pygame.mouse.get_pos(), self.rect.center)))

    def get_state(self):
        if abs(self.acc.x) > 0 or abs(self.acc.y) > 0: self.max_frames = 6
        else: self.max_frames = 0 #so playerMove doesn't animate

    def update(self):
        if self.health <= 0: self.alive = False
        self.cooldown += 1
        self.user_input()
        self.get_state()
        self.animate()