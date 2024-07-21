import pygame
import random
from pygame.locals import *
from scripts.projectile import Projectile
from scripts.settings import WHITE, BOSS_PROJ_COLOUR, draw_text, get_angle

class Boss(pygame.sprite.Sprite):
  def __init__(self, pos, health):
    super().__init__()
    self.x, self.y = pos
    self.health = health
    self.projectiles = []
    self.frame_index = 0
    self.move_timer = 0
    self.animation_speed = 0.1
    self.invulnerable = True

  def is_alive(self):
    return self.health > 0

class Boss1(Boss):
  def __init__(self):
    super().__init__((250, 352), 150)
    self.idle = pygame.image.load("data/sprites/boss1/idle.png").convert_alpha()
    self.attack = pygame.image.load("data/sprites/boss1/attack.png").convert_alpha()
    self.skill = pygame.image.load("data/sprites/boss1/skill.png").convert_alpha()
    self.summon = pygame.image.load("data/sprites/boss1/summon.png").convert_alpha()
    self.death = pygame.image.load("data/sprites/boss1/death.png").convert_alpha()
    self.curr_state = "idle"
    self.state_dict = {
      # [spritePNG, maxFrameNumber]
      "idle": [self.idle, 4],
      "attack": [self.attack, 11],
      "skill": [self.skill, 10],
      "summon": [self.summon, 7],
      "death": [self.death, 19],
    }
    self.image = self.state_dict[self.curr_state][0].subsurface(0, 0, 192, 192)
    self.rect = self.image.get_rect(center = (self.x, self.y))
    self.time_in_state = 0
    self.flipped = False

    self.projectiles = []
    self.cooldown = 0

  def animate(self):
    self.frame_index += self.animation_speed
    if self.frame_index > self.state_dict[self.curr_state][1]: 
      self.frame_index = 0
      self.handle_state_transition()

    self.image = self.state_dict[self.curr_state][0].subsurface(int(self.frame_index) * 192, 0, 192, 192)
    if self.flipped: self.image = pygame.transform.flip(self.image, True, False)
    self.image_mask = pygame.mask.from_surface(self.image)
    self.mask_image = self.image_mask.to_surface()

  def handle_state_transition(self):
    if self.curr_state == "idle":
      print("idle")
      if self.time_in_state >= 2 * 60:
        self.invulnerable = False
        self.curr_state = "attack"
        self.time_in_state = 0
    elif self.curr_state == "attack":
      print("attack")
      if self.time_in_state >= 2 * 11:  # Attack animation runs twice
          self.curr_state = random.choices(["skill", "summon"], [0.5, 0.5])[0]
          self.time_in_state = 0
    elif self.curr_state in ["skill", "summon"]:
      print(self.curr_state)
      self.curr_state = random.choices(["attack", "skill", "summon"], [0.4, 0.3, 0.3])[0]
      self.time_in_state = 0

  def handle_shoot(self, player_pos):
    if self.curr_state == "attack":
      if self.time_in_state >= 3 and self.time_in_state <= 45 and self.cooldown > 5:
        offsets, angles = [-75, 0, 75], [0, -3.14]
        for offset in offsets:
            for angle in angles:
                self.projectiles.append(Projectile((self.rect.centerx, self.rect.centery + offset), angle, BOSS_PROJ_COLOUR))
        self.cooldown = 0
      elif self.time_in_state > 60 and self.time_in_state <= 110 and self.cooldown > 5:
        offsets, angles_set_1, angles_set_2 = [-40, 0, 40], [-0.4, 0, 0.4], [-2.74, -3.14, 2.74]
        for offset, angle in zip(offsets, angles_set_1):
          self.projectiles.append(Projectile((self.rect.centerx, self.rect.centery + offset), angle, BOSS_PROJ_COLOUR))
        for offset, angle in zip(offsets, angles_set_2):
          self.projectiles.append(Projectile((self.rect.centerx + 12, self.rect.centery + offset), angle, BOSS_PROJ_COLOUR))
        self.cooldown = 0
    elif self.curr_state == "skill":
      if self.cooldown > 1:
        self.projectiles.append(Projectile((self.rect.centerx, self.rect.centery), random.uniform(-3.14, 3.14), BOSS_PROJ_COLOUR, 20))
        self.cooldown = 0
    elif self.curr_state == "summon":
      if self.cooldown > 2:
        self.projectiles.append(Projectile((self.rect.centerx, self.rect.centery), get_angle(player_pos, self.rect.center), BOSS_PROJ_COLOUR, 15))
        self.cooldown = 0


  def move_boss(self):
    if self.move_timer <= 0:
      self.move_timer = random.randint(30, 90)  # Random duration between 0.5 and 1.5 seconds
      self.move_direction = random.choice(['left', 'right', 'up', 'down', 'idle'])
    else:
      self.move_timer -= 1
      if self.move_direction == 'left':
        self.x -= 2
        self.flipped = True
      elif self.move_direction == 'right':
        self.x += 2
        self.flipped = False
      elif self.move_direction == 'up':
        self.y -= 2
      elif self.move_direction == 'down':
        self.y += 2

      self.x = max(0, min(1200 - self.rect.width, self.x))
      self.y = max(0, min(650 - self.rect.height, self.y))

    self.rect.topleft = (self.x, self.y)

  def update(self, player_pos):
    if not self.is_alive():
      self.curr_state = "death"
    self.cooldown += 1
    self.time_in_state += 1
    self.move_boss()
    self.handle_shoot(player_pos)
    self.animate()

  def draw(self, surface):
    surface.blit(self.image, self.rect.topleft)
    draw_text(surface, str(self.health), 20, self.rect.centerx - 10 , self.rect.bottom - 20, WHITE)
    # pygame.draw.rect(surface, (255, 0, 0), self.rect, 2)
