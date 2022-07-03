import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size, type):
        super().__init__()
        self.type = type
        # Creating tile from ground.png sprite
        base0 = pygame.image.load("imgs/tiles/LIGHT_1C.png").convert()
        box0 = pygame.image.load("imgs/tiles/LIGHT_1C.png").convert()
        sideL = pygame.image.load("imgs/tiles/TECH_4C.png").convert_alpha()
        sideR = pygame.image.load("imgs/tiles/TECH_4C.png").convert_alpha()
        sand = pygame.image.load("imgs/tiles/sand.png").convert_alpha()
        if type == 'base0':
            self.image = base0
        if type == 'box0':
            self.image = box0
        if type == 'sideL':
            self.image = sideL
        if type == 'sideR':
            self.image = sideR
        if type == 'sand':
            self.image = sand
        self.image = pygame.transform.scale(self.image, (size,size))
        self.rect = self.image.get_rect(topleft = pos)
    
    def update(self, xShift):
        self.rect.x += xShift