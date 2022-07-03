import pygame
import random

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, scale):
        super().__init__()
        self.num_walk_sprites = 4
        self.name = 'enemy1'
        self.walk_index = 0
        self.walk_count = 0
        self.walk_delay = 4
        self.scale = scale
        # 1.5 = normal scale
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = random.randrange(1, 5)
        self.gravity = 0.8
        self.jump_speed = -16
        self.orientation = 'Right'
        self.health_pool = 100
        self.change = 0
        self.hurt = False
        self.hurt_time = 0
        self.dead = False
        
        # Loading in & resizing idle sprites.
        self.idle_right = pygame.image.load("imgs/playerSprites/"+self.name+"/idle1.png").convert_alpha()
        self.idle_right = pygame.transform.scale(self.idle_right, self.resize_sprite(self.idle_right))
        self.idle_left = pygame.transform.flip(self.idle_right, True, False)        
        self.hurt_left = pygame.image.load('imgs/playerSprites/'+self.name+'/hurt.png').convert_alpha()
        self.hurt_left = pygame.transform.scale(self.hurt_left, self.resize_sprite(self.hurt_left))
        self.hurt_right = pygame.transform.flip(self.hurt_left, True, False)        
        
        # Using iteration to load & resize walking sprite lists.
        self.walk_right = []
        self.walk_left = []
        for j in range(1,(self.num_walk_sprites+1)):
            rightSprite = pygame.image.load('imgs/playerSprites/'+self.name+'/walk'+str(j)+'.png').convert_alpha()
            rightSprite = pygame.transform.scale(rightSprite, self.resize_sprite(rightSprite))
            leftSprite = pygame.transform.flip(rightSprite, True, False)
            self.walk_right.append(rightSprite)
            self.walk_left.append(leftSprite)
        
        self.image = self.idle_right
        self.rect = self.image.get_rect(topleft = pos)

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y
    
    def jump(self):
        self.direction.y = self.jump_speed
    
    def update(self, x_shift):
        if self.orientation == 'Right':
            self.direction.x = 1
            self.rect.x += self.direction.x * self.speed + x_shift
        elif self.orientation == 'Left':
            self.direction.x = -1
            self.rect.x -= self.direction.x * -1 * self.speed - x_shift
        else:
            self.direction.x = 0
            self.rect.x += x_shift
        self.change += 1
        self.change_direction()
        self.animate()
    
    def change_direction(self):
        if self.change >= random.randrange(40, 60):
            if self.orientation == 'Right':
                self.orientation = 'Left'
            elif self.orientation == 'Left':
                self.orientation = 'Right'
            self.change = 0
    
    def sub_health(self, sub):
        self.health_pool -= sub
        self.hurt = True
        if self.hurt == True:
            if self.orientation == 'Right':
                self.image = self.hurt_right
            elif self.orientation == 'Left':
                self.image = self.hurt_left
            if self.hurt_time == 10:
                self.hurt = False
                self.hurt_time = 0
            else:
                self.hurt_time += 1
        if self.health_pool == 0:
            self.dead == True
    
    def get_health(self):
        return self.health_pool
        
    def animate(self):
        # Death
        if self.dead == True:
            print("deady boi")
        # Idle
        elif (self.orientation == 'Left'):
            self.image = self.idle_right
        elif (self.orientation == 'Right'):
            self.image = self.idle_left
            
    # for resizing sprites by scale factor
    def resize_sprite(self, sprite):
        dimensions = list(sprite.get_size())
        length = len(dimensions)
        for i in range(length):
            dimensions[i] *= self.scale
            dimensions[i] = int(dimensions[i])
        return tuple(dimensions)