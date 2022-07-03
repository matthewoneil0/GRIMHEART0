import pygame
from pygame import mixer
import time
import random

# Loading in sound effects for jumping and walking.
mixer.init()
effects = pygame.mixer.Channel(1)
jump_sound = pygame.mixer.Sound('music/jump3.wav')
jump_sound.set_volume(0.2)
hurt_sound = pygame.mixer.Sound('music/hurt.wav')
hurt_sound.set_volume(0.1)
steps = []
for j in range(0,5):
            step = pygame.mixer.Sound('music/steps'+str(j)+'.wav')
            step.set_volume(0.4)
            steps.append(step)

# Represents a player.
class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        # Player sprite variable(s)
        self.orientation = 'Right'
        self.num_walk_sprites = 6
        self.name = 'guy1'
        self.scale = 2
        self.walking_sound_index = 0
        self.walk_index = 0
        self.walk_count = 0
        self.walk_delay = 3
        # Attacking variables
        self.num_atk_sprites = 6
        self.is_attacking = False
        self.attack_index = 0
        self.attack_count = 0
        self.attack_delay = 2
        # Movement variables
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 10
        self.gravity = 0.8
        self.jump_speed = -16
        # health
        self.health_pool = 100
        self.hurt = False
        self.hurt_time = 0
        # timer
        self.start = 1
        self.stop = 1

        # Loading in & resizing idle, jump, fall, and hurt sprites.
        self.idle_right = pygame.image.load("imgs/playerSprites/"+self.name+"/idle1.png").convert_alpha()
        self.idle_right = pygame.transform.scale(self.idle_right, self.resize_sprite(self.idle_right))
        self.idle_left = pygame.transform.flip(self.idle_right, True, False)

        self.jump_right = pygame.image.load("imgs/playerSprites/"+self.name+"/jump1.png").convert_alpha()
        self.jump_right = pygame.transform.scale(self.jump_right, self.resize_sprite(self.jump_right))
        self.jump_left = pygame.transform.flip(self.jump_right, True, False)
        
        self.fall_right = pygame.image.load("imgs/playerSprites/"+self.name+"/fall1.png").convert_alpha()
        self.fall_right = pygame.transform.scale(self.fall_right, self.resize_sprite(self.fall_right))
        self.fall_left = pygame.transform.flip(self.fall_right, True, False)
        
        self.hurt_right = pygame.image.load("imgs/playerSprites/"+self.name+"/hurt1.png").convert_alpha()
        self.hurt_right = pygame.transform.scale(self.hurt_right, self.resize_sprite(self.hurt_right))
        self.hurt_left = pygame.transform.flip(self.hurt_right, True, False)

        # Using iteration to load & resize walking sprite lists.
        self.walk_right = []
        self.walk_left = []
        for j in range(1,(self.num_walk_sprites+1)):
            rightSprite = pygame.image.load('imgs/playerSprites/'+self.name+'/walk'+str(j)+'.png').convert_alpha()
            rightSprite = pygame.transform.scale(rightSprite, self.resize_sprite(rightSprite))
            leftSprite = pygame.transform.flip(rightSprite, True, False)
            self.walk_right.append(rightSprite)
            self.walk_left.append(leftSprite)
        
        # Using iteration to load & resize attacking sprite lists
        self.attack_right = []
        self.attack_left = []
        for j in range(1,(self.num_atk_sprites+1)):
            rightAtk = pygame.image.load('imgs/playerSprites/'+self.name+'/attack'+str(j)+'.png').convert_alpha()
            rightAtk = pygame.transform.scale(rightAtk, self.resize_sprite(rightAtk))
            leftAtk = pygame.transform.flip(rightAtk, True, False)
            self.attack_right.append(rightAtk)
            self.attack_left.append(leftAtk)

        # Start the player in the idle right orientation.
        self.image = self.idle_right
        self.rect = self.image.get_rect(topleft = pos)

    # Get user input
    def get_input(self):
        keys = pygame.key.get_pressed()
        #keys_down = pygame.KEYDOWN
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]: # move right
            self.direction.x = 1
            self.orientation  = 'Right'
        elif keys[pygame.K_a] or keys[pygame.K_LEFT]: # move left
            self.direction.x = -1
            self.orientation = 'Left'
        else:                                           # idle
            self.direction.x = 0
        if keys[pygame.K_SPACE] and self.direction.y == 0: # jump
            self.jump()
        
        if keys[pygame.K_m] and self.direction.y == 0:
            #print('melee')
            self.melee()
    
    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y
    
    def jump(self):
        self.direction.y = self.jump_speed
        jump_sound.play()
    
    def update(self):
        self.get_input()
        self.rect.x += self.direction.x * self.speed    
        self.animate()
    
    def add_health(self, add):
        self.health_pool += add
        if self.health_pool > 100:
            self.health_pool = 100
    
    def sub_health(self, sub):
        self.health_pool -= sub
        self.hurt = True
        hurt_sound.play()
    
    def get_health(self):
        return self.health_pool
    
    def melee(self):
        self.start += time.time()
        if self.start - self.stop > 0.5:
            self.is_attacking = True
            self.start = 0
            self.stop = 0
        self.stop += time.time()

    # Method to animate plus player sound effects in the update method
    def animate(self):
        # If not attacking, animate movement
        if self.is_attacking == False:
        # Jumping 
            if (self.orientation == 'Right' and (0.8 > self.direction.y < 0)):
                self.image = self.jump_right
            elif (self.orientation == 'Left' and (0.8 > self.direction.y < 0)):
                self.image = self.jump_left
            # Falling
            elif (self.orientation == 'Right' and (self.direction.y > 5)):
                self.image = self.fall_right
            elif (self.orientation == 'Left' and (self.direction.y > 5)):
                self.image = self.fall_left
            # Hurt/attacked
            elif self.orientation == 'Right' and self.hurt == True:
                self.image = self.hurt_right
                if self.hurt_time == 10:
                    self.hurt = False
                    self.hurt_time = 0
                else: 
                    self.hurt_time += 1
            elif self.orientation == 'Left' and self.hurt == True:
                self.image = self.hurt_left
                if self.hurt_time == 10:
                    self.hurt = False
                    self.hurt_time = 0
                else: 
                    self.hurt_time += 1
            # Idle 
            elif (self.orientation == 'Right' and self.direction.x == 0):
                self.image = self.idle_right
            elif (self.orientation == 'Left' and self.direction.x == 0):
                self.image = self.idle_left
            # Walking 
            elif (self.orientation == 'Right' and self.direction.x != 0 and self.direction.y == 0): 
                if self.walk_count == 0:
                    self.image = self.walk_right[self.walk_index]
                    self.walk_index += 1

                    # Sound effect every time the sprite changes
                    if self.walk_index in [1,4]:
                        steps[self.walking_sound_index].play()
                        self.walking_sound_index += 1
                self.walk_count += 1
            elif (self.orientation == 'Left' and self.direction.x != 0 and self.direction.y == 0):
                if self.walk_count == 0:
                    self.image = self.walk_left[self.walk_index]
                    self.walk_index += 1
                    
                    if self.walk_index in [1,4]:
                        steps[self.walking_sound_index].play()
                        self.walking_sound_index += 1
                self.walk_count += 1

            # reseting walking delay var and index to loop through sprite lists
            if self.walk_index >= self.num_walk_sprites:
                self.walk_index = 0
            if self.walk_count == self.walk_delay:
                self.walk_count = 0
            # loop the sound effect counter
            if self.walking_sound_index == 5:
                self.walking_sound_index = 0
        else:
            if (self.orientation == 'Right' and self.direction.y == 0): 
                
                if self.attack_count == 0:
                    self.image = self.attack_right[self.attack_index]
                    self.attack_index += 1
                self.attack_count += 1
            elif (self.orientation == 'Left' and self.direction.y == 0): 
                if self.attack_count == 0:
                    self.image = self.attack_left[self.attack_index]
                    self.attack_index += 1
                self.attack_count += 1

            # reseting walking delay var and index to loop through sprite lists
            if self.attack_index >= self.num_atk_sprites:
                self.attack_index = 0
                self.is_attacking = False
            if self.attack_count == self.attack_delay:
                self.attack_count = 0
            
            
        

    # for resizing sprites by scale factor
    def resize_sprite(self, sprite):
        dimensions = list(sprite.get_size())
        length = len(dimensions)
        for i in range(length):
            dimensions[i] *= self.scale
            dimensions[i] = int(dimensions[i])
        return tuple(dimensions)
