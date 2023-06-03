import pygame, math

WINDOW_SIZE = (1280 , 720)  
MID_W, MID_H = WINDOW_SIZE[0] / 2, WINDOW_SIZE[1] / 2
FPS = 60
TILE_SIZE = 32
PLAYER_SIZE = 64

BLACK = (0, 0, 0) 
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 128, 0)
FONT = "data/fonts/Minecraft_font.ttf"
VEC = pygame.math.Vector2

PROJ_COLOUR = (20,20,60)
SPARK_COLOUR = (61, 22, 29)
DEATH_TEXT_COLOUR = (89, 9, 23)

NORMAL_ENEMY_COLOUR = (139, 64, 0)
TRACKER_ENEMY_COLOUR = (54, 2, 10)

#get angle between two points
def get_angle(coord1, coord2):
    angle = math.atan2(coord1[1] - coord2[1], coord1[0] - coord2[0]) #get angle of mouse in radians.
    return angle