import pygame 

class Tile(pygame.sprite.Sprite):
    def __init__(self,size,x,y):
        super().__init__()
        self.image = pygame.Surface((size[0],size[1]))
        self.rect = self.image.get_rect(topleft = (x,y))

class StaticTile(Tile):
    def __init__(self, size, x, y, surface):
        super().__init__(size, x, y)
        self.image = surface

class AnimatedTile(Tile):
    def __init__(self, size, x, y, frame_num, path):
        super().__init__(size, x, y)
        self.spriteSheet = pygame.image.load(path).convert_alpha()
        self.frame_index = 0
        self.tile_width = size[0]
        self.tile_height = size[1]
        self.frame_num = frame_num
        self.image = self.spriteSheet.subsurface(self.tile_width,0,self.tile_width,self.tile_height)

    def animate(self):
        self.frame_index += 0.15
        if self.frame_index >= self.frame_num: self.frame_index = 0
        self.image = self.spriteSheet.subsurface(int(self.frame_index) * self.tile_width * 2, 0 , self.tile_width,self.tile_height)
    
    def update(self):
        self.animate()

    