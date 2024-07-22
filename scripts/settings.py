import pygame, math

pygame.mixer.init()

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

PROJ_COLOUR = (20, 20, 60)
BOSS_PROJ_COLOUR = (127, 14, 14)
SPARK_COLOUR = (61, 22, 29)
DEATH_TEXT_COLOUR = (89, 9, 23)
VICTORY_TEXT_COLOUR = (215, 202, 26)

NORMAL_ENEMY_COLOUR = (139, 64, 0)
TRACKER_ENEMY_COLOUR = (54, 2, 10)

menu_select_sound = pygame.mixer.Sound("data/sounds/menuSelect.wav")
menu_select_sound.set_volume(0.5)

#get angle between two points
def get_angle(coord1, coord2):
    angle = math.atan2(coord1[1] - coord2[1], coord1[0] - coord2[0]) #get angle of mouse in radians.
    return angle

#play the menu select sound on click
def play_menu_select_sound(delay=0):
    pygame.mixer.Sound.play(menu_select_sound)
    pygame.time.delay(int(delay * 1000))

#draw text onto the selected surfact
def draw_text(surface, text, size, x, y, colour):
    font = pygame.font.Font(FONT, size)
    text_surface = font.render(text, True, colour)
    text_rect = text_surface.get_rect()
    text_rect.center = (x,y)
    surface.blit(text_surface,text_rect)