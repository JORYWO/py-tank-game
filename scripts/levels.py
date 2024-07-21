from os import remove
import pygame, math
from random import randint 
from csv import reader
from scripts.projectile import Projectile
from scripts.tiles import StaticTile, AnimatedTile
from scripts.player import Player
from scripts.enemy import NormalEnemy, TrackerEnemy
from scripts.bosses import Boss1
from scripts.ui import Ui
from scripts.sparks import Spark
from scripts.settings import WINDOW_SIZE, FPS, TILE_SIZE, PROJ_COLOUR, SPARK_COLOUR

display = pygame.Surface(WINDOW_SIZE) #surface for rendering onto and used for screen shake

class Level:
    def __init__(self, level_data, surface, mode):
        self.display_surface = surface
        self.mode = mode
        self.screen_shake_timer = 0
        self.ui = Ui(self.display_surface)
        self.collision_sound = pygame.mixer.Sound("data/sounds/playerCollision.wav")
        self.collision_sound.set_volume(0.5) 

        #player
        player_layout = import_csv_layout(level_data["player"])
        self.player = pygame.sprite.GroupSingle()
        self.player_setup(player_layout)

        #boss
        if self.mode != "endless":
            boss1 = Boss1()
            self.boss1 = pygame.sprite.GroupSingle()
            self.boss1.add(boss1)

        #background
        background_layout = import_csv_layout(level_data["background"])
        self.background_sprites = self.create_tile_group(background_layout, "background")

        #walls - collidable
        wall_layout = import_csv_layout(level_data["walls"])
        self.wall_sprites = self.create_tile_group(wall_layout, "walls")

        #torches - animated 
        torch_layout = import_csv_layout(level_data["torches"])
        self.torch_sprites = self.create_tile_group(torch_layout, "torches")

        #lanterns - animated
        lantern_layout = import_csv_layout(level_data["lanterns"])
        self.lantern_layout = self.create_tile_group(lantern_layout, "lanterns")

        self.frame = 0
        self.enemy_list = []
        self.num_of_enemies_spawned = 0
        self.sparks = []

    def create_tile_group(self,layout,type):
        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row): 
                if val != "-1":
                    x = col_index * TILE_SIZE
                    y = row_index * TILE_SIZE

                    if type == "background":
                        background_tile_list = import_cut_graphics("data/sprites/tileset.png")
                        tile_surface = background_tile_list[int(val)]
                        sprite = StaticTile([TILE_SIZE, TILE_SIZE], x, y, tile_surface)
                    if type == "walls":
                        wall_tile_list = import_cut_graphics("data/sprites/tileset.png")
                        tile_surface = wall_tile_list[int(val)]
                        sprite = StaticTile([TILE_SIZE, TILE_SIZE], x, y, tile_surface)
                    if type == "torches":
                        sprite = AnimatedTile([TILE_SIZE, TILE_SIZE], x, y, 5, "data/sprites/torch-sheet.png")
                    if type == "lanterns":
                        sprite = AnimatedTile([TILE_SIZE,TILE_SIZE * 2], x, y, 4, "data/sprites/lantern-sheet.png")
                    sprite_group.add(sprite)
        return sprite_group  

    def player_setup(self,layout):
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                if val == "0":
                    sprite = Player((x,y))
                    self.player.add(sprite)

    #player collision with the wall
    def player_collisions(self):
        player = self.player.sprite
        player.rect.x += int(player.acc.x * player.speed)
        player.rect.y += int(player.acc.y * player.speed)
        collidable_sprites = self.wall_sprites.sprites()
        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.rect):
                if player.acc.x < 0: player.rect.left = sprite.rect.right
                elif player.acc.x > 0: player.rect.right = sprite.rect.left
                elif player.acc.y < 0: player.rect.top = sprite.rect.bottom
                elif player.acc.y > 0: player.rect.bottom = sprite.rect.top

    #enemy and projectile collision with the wall
    def wall_collisions(self, elemList, remove_on_wall_collision=False):
        for i, element in sorted(enumerate(elemList), reverse=True):
            if element.rect.left <= TILE_SIZE or element.rect.right >= WINDOW_SIZE[0] - TILE_SIZE: 
                if remove_on_wall_collision: elemList.pop(i)
                element.vel_x *= -1 
                if type(element) is Projectile: element.collision_num += 1
            elif element.rect.top <= TILE_SIZE * 2 or element.rect.bottom >= WINDOW_SIZE[1] - TILE_SIZE / 2: 
                if remove_on_wall_collision: elemList.pop(i)
                element.vel_y *= -1
                if type(element) is Projectile: element.collision_num += 1
            if type(element) is TrackerEnemy: element.draw(self.display_surface, self.player.sprite.rect.center)
            else: element.draw(self.display_surface)

    #spawns different types of enemies every 2 seconds
    def spawn_enemies(self):
        self.frame += 1
        if self.frame > FPS * 2 and len(self.enemy_list) < 15: 
            if self.num_of_enemies_spawned % 5 != 4:
                self.enemy_list.append(NormalEnemy((randint(TILE_SIZE * 2, WINDOW_SIZE[0] - (TILE_SIZE * 2)) , randint(TILE_SIZE * 3, WINDOW_SIZE[1] - (TILE_SIZE * 2)))))
            else: #spawn tracker enemy every 5th enemy spawned
                self.enemy_list.append(TrackerEnemy((randint(TILE_SIZE * 2, WINDOW_SIZE[0] - (TILE_SIZE * 2)) , randint(TILE_SIZE * 3, WINDOW_SIZE[1] - (TILE_SIZE * 2)))))
            self.frame = 0
            self.num_of_enemies_spawned += 1

    #collision with projectile and enemy
    def proj_enemy_collisions(self):
        proj_list = self.player.sprite.projectiles
        new_proj_list = list(proj_list)
        for proj_index, proj in sorted(enumerate(proj_list), reverse=True):
            new_proj_list.pop(proj_index)

            for enemy_index, enemy in sorted(enumerate(self.enemy_list), reverse=True):
                if enemy.rect.colliderect(proj.rect) and enemy.spawned:
                    if enemy.size <= 25: 
                        self.player.sprite.score += enemy.size
                        for sparks in range(enemy.size):
                            self.sparks.append(Spark([proj.rect.centerx, proj.rect.centery], math.radians(randint(0, 360)), randint(5, 9), SPARK_COLOUR, 2))
                        self.enemy_list.pop(enemy_index)

                    else: 
                        self.player.sprite.score += 10
                        for sparks in range(7):
                            self.sparks.append(Spark([proj.rect.centerx, proj.rect.centery], math.radians(randint(0, 360)), randint(2, 5), SPARK_COLOUR, 2))
                        enemy.size -= 10
                    proj_list.pop(proj_index)

    #player projectiles can shoot other player projectiles
    def player_bullet_collisions_with_itself(self):
        proj_list = self.player.sprite.projectiles
        new_proj_list = list(proj_list)
        for proj_index, proj in sorted(enumerate(proj_list), reverse=True):
            new_proj_list.pop(proj_index)
            for next_proj_index, next_proj in sorted(enumerate(new_proj_list), reverse=True):
                if next_proj.rect.colliderect(proj.rect): 
                    for sparks in range(7):
                        self.sparks.append(Spark([proj.rect.centerx, proj.rect.centery], math.radians(randint(0, 360)), randint(3, 5), PROJ_COLOUR, 2))
                    proj_list.pop(proj_index)
                    proj_list.pop(next_proj_index)

    # player collision with any type of bullet
    def player_bullet_collisions(self, bullet_list):
        player = self.player.sprite
        for j, proj in sorted(enumerate(bullet_list), reverse=True):
            if proj.rect.colliderect(player.rect) and proj.collision_num:
                player.health -= proj.damage
                bullet_list.pop(j)
                self.screen_shake_timer = 12
                pygame.mixer.Sound.play(self.collision_sound)

    #collision with enemy and projectiles
    def player_hit_collisions(self):
        player = self.player.sprite
        for i, enemy in sorted(enumerate(self.enemy_list), reverse=True):
            if enemy.rect.colliderect(player.rect) and enemy.spawned:
                player.health -= enemy.damage
                self.screen_shake_timer = enemy.size // 1.5
                self.enemy_list.pop(i)
                pygame.mixer.Sound.play(self.collision_sound)

        # for j, proj in sorted(enumerate(player.projectiles), reverse=True):
        #     if proj.rect.colliderect(player.rect) and proj.collision_num:
        #         player.health -= proj.damage
        #         player.projectiles.pop(j)
        #         self.screen_shake_timer = 12
        #         pygame.mixer.Sound.play(self.collision_sound)

    def boss_bullet_collision(self):
        proj_list = self.player.sprite.projectiles
        boss = self.boss1.sprite
        for proj_index, proj in sorted(enumerate(proj_list), reverse=True):
            if boss.image_mask.overlap(proj.mask, (proj.x - boss.rect.x, proj.y - boss.rect.y)) and not boss.invulnerable:
                boss.health -= 1
                proj_list.pop(proj_index)

    # def boss_player_bullet_collision(self):
    #     boss_proj_list = self.boss1.sprite.projectiles
    #     new_proj_list = list(boss_proj_list )
    #     for proj_index, proj in sorted(enumerate(new_proj_list), reverse=True):
    #         if proj.rect.collide

    #draw and update sparks
    def update_sparks(self):
        for i, spark in sorted(enumerate(self.sparks), reverse=True):
            spark.update(1)
            spark.draw(display)
            if not spark.alive:
                self.sparks.pop(i)

    #shake screen for a duration
    def shake_screen(self):
        if self.screen_shake_timer > 0: self.screen_shake_timer -= 1

        render_offset = [0,0]
        if self.screen_shake_timer:
            render_offset[0], render_offset[1] = randint(0, 16) - 8, randint(0, 16) - 8 
        return render_offset


    def run(self, frames):
        offset = self.shake_screen()
        self.display_surface.blit(pygame.transform.scale(display, WINDOW_SIZE), offset)

        # draw the tiles
        self.background_sprites.draw(display)
        self.wall_sprites.draw(display)
        self.torch_sprites.update()
        self.torch_sprites.draw(display)
        self.lantern_layout.update()
        self.lantern_layout.draw(display)
            
        #sparks
        self.update_sparks()

        #enemies
        if self.mode == "endless":
            self.spawn_enemies()
            self.wall_collisions(self.enemy_list)
            self.proj_enemy_collisions()
        #boss
        else:
            self.boss1.update(self.player.sprite.rect.center)
            self.boss1.sprite.draw(display)
            self.wall_collisions(self.boss1.sprite.projectiles, True)
            self.boss_bullet_collision()

        #player 
        self.player.update()
        self.player_collisions()
        self.wall_collisions(self.player.sprite.projectiles)
        self.player_bullet_collisions_with_itself()
        self.player_hit_collisions()
        self.player_bullet_collisions(self.player.sprite.projectiles)
        if self.mode != "endless": self.player_bullet_collisions(self.boss1.sprite.projectiles)
        self.player.draw(display)

        #ui 
        self.ui.show_fps(frames)
        self.ui.show_score(self.player.sprite.score)
        self.ui.draw_healthbar((self.player.sprite.rect.centerx - 25, self.player.sprite.rect.bottom - 5), 100, self.player.sprite.health)

        return self.player.sprite.alive, self.player.sprite.score


'''HELPER FUNCTIONS'''
#create 2d array of values of tile ids
def import_csv_layout(path):
    terrain_map = []
    with open(path) as map:
        level = reader(map, delimiter=",")
        for row in level:
            terrain_map.append(list(row))
        return terrain_map

#cuts out each tile and places them in an array 
def import_cut_graphics(path):
    surface = pygame.image.load(path).convert_alpha()
    tile_num_x = int(surface.get_size()[0] / TILE_SIZE)
    tile_num_y = int(surface.get_size()[1] / TILE_SIZE)

    cut_tiles = []
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * TILE_SIZE
            y = row * TILE_SIZE
            new_surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
            new_surf.blit(surface, (0,0), pygame.Rect(x,y,TILE_SIZE,TILE_SIZE))
            cut_tiles.append(new_surf)
    return cut_tiles
