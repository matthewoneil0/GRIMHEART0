from dis import dis
import pygame
import time
from tile import Tile
from settings import tileSize, displayWidth, displayHeight
from player import Player
from enemy import Enemy

class Level:
    def __init__(self, levelData, surface):
        self.displaySurface = surface
        self.setupLevel(levelData)
        # camera var
        self.worldShiftX = 0
        self.start = 1
        self.stop = 1
        self.dead = False
        self.player_health = 100
        self.win = False
        
        
    # create tile map from levelMap in settings
    def setupLevel(self, layout):
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.enemy = pygame.sprite.Group()
        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                x = col_index * tileSize
                y = row_index * tileSize
                # draw tile if X in levelMap
                if cell == 'P':
                    player = Player((x, y))
                    self.player.add(player)
                elif cell == 'E':
                    enemy = Enemy((x, y), 1.5)
                    self.enemy.add(enemy)
                elif cell == 'M':
                    boss = Enemy((x, y), 5)
                    boss.scale = 5
                    boss.health_pool = 1000
                    self.enemy.add(boss)
                elif cell != ' ':
                    cell = str(self.get_tile(cell))
                    tile = Tile((x, y), tileSize, cell)
                    self.tiles.add(tile)
        
        # Load in health bar images via for loop
        health_ranges = [100, 90, 80, 70, 60, 50, 40, 30, 20, 10, 0]
        self.health_bars = []
        for health in health_ranges:
            image = pygame.image.load("imgs/healthbar/health"+str(health)+".png")
            image = pygame.transform.scale(image, self.resized_sprite(image, 4))
            self.health_bars.append(image)
                    
    # Switch statement using a dictionary to keep track of tile types
    def get_tile(self, cell):
        switch={
            'X':'base0',
            'B':'box0',
            'L':'sideL',
            'R':'sideR',
            'S':'sand',
            
        }
        return switch.get(cell, "Invalid tile type.")
                
    
    # camera
    def scrollX(self):
        player = self.player.sprite
        playerX = player.rect.centerx
        directionX = player.direction.x
        # scroll left
        if playerX < displayWidth / 3 and directionX < 0:
            self.worldShiftX = 10
            player.speed = 0
        # scroll right
        elif playerX > displayWidth - displayWidth / 3 and directionX > 0:
            self.worldShiftX = -10
            player.speed = 0
        else:
            self.worldShiftX = 0
            player.speed = 5
    
    # horizontal collision
    def hzCollision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed
        for enemy in self.enemy.sprites():
            enemy.rect.x += enemy.direction.x * enemy.speed
        # collision detection
        for sprite in self.tiles.sprites():
            for enemy in self.enemy.sprites():
                # player
                if sprite.rect.colliderect(player.rect):
                    if player.direction.x < 0:
                        player.rect.left = sprite.rect.right
                    elif player.direction.x > 0:
                        player.rect.right = sprite.rect.left
                # enemy
                if sprite.rect.colliderect(enemy.rect):
                    if enemy.direction.x < 0:
                        enemy.rect.left = sprite.rect.right
                    elif enemy.direction.x > 0:
                        enemy.rect.right = sprite.rect.left
                # player collide w/ enemy
                if player.rect.colliderect(enemy.rect):
                    # player attack
                    if player.is_attacking == True:
                        enemy.sub_health(100)
                        if enemy.get_health() <= 0:
                            # if boss is defeated end game
                            if enemy.scale == 5:
                                self.enemy.remove(enemy)
                                self.win = True
                            else:
                                self.enemy.remove(enemy)
                        player.is_attacking = False
                    # enemy attack
                    else:
                        self.start += time.time()
                        if self.start - self.stop > 1:
                            player.sub_health(10)
                            self.start = 0
                            self.stop = 0
                        self.stop += time.time()
                        if player.get_health() <= 0:
                            self.death()
    
    # vertical collision
    def vrtCollision(self):
        player = self.player.sprite
        player.apply_gravity()
        for enemy in self.enemy.sprites():
            enemy.apply_gravity()
        # collision detection
        for sprite in self.tiles.sprites():
            for enemy in self.enemy.sprites():
                # player
                if sprite.rect.colliderect(player.rect):
                    if player.direction.y > 0:
                        player.rect.bottom = sprite.rect.top
                        player.direction.y = 0
                    elif player.direction.y < 0:
                        player.rect.top = sprite.rect.bottom
                        #player.direction.y = 0
                        player.direction.y = 0.1
                # enemy
                if sprite.rect.colliderect(enemy.rect):
                    if enemy.direction.y > 0:
                        enemy.rect.bottom = sprite.rect.top
                        enemy.direction.y = 0
                    elif enemy.direction.y < 0:
                        enemy.rect.top = sprite.rect.bottom
                        #enemy.direction.y = 0
                        enemy.direction.y = 0.1
                    # enemy w/ edge platform
                    if sprite.type == 'sideL':
                        enemy.orientation = 'Right'
                    elif sprite.type == 'sideR':
                        enemy.orientation = 'Left'

    # kill player if outside screen
    def offscreen_death(self):
        player = self.player.sprite
        playerY = player.rect.centery
        directionY = player.direction.y
        if (playerY > displayHeight and directionY > 0) or (playerY < (-1 * displayHeight) and directionY < 0):
            self.death()
    
    def death(self):
        self.dead = True
        
    def update_health(self):
        player = self.player.sprite
        self.player_health = player.get_health()
        if self.player_health == 100:
            self.health_bar = self.health_bars[0]
        elif self.player_health == 90:
            self.health_bar = self.health_bars[1]
        elif self.player_health == 80:
            self.health_bar = self.health_bars[2]
        elif self.player_health == 70:
            self.health_bar = self.health_bars[3]
        elif self.player_health == 60:
            self.health_bar = self.health_bars[4]
        elif self.player_health == 50:
            self.health_bar = self.health_bars[5]
        elif self.player_health == 40:
            self.health_bar = self.health_bars[6]
        elif self.player_health == 30:
            self.health_bar = self.health_bars[7]
        elif self.player_health == 20:
            self.health_bar = self.health_bars[8] 
        elif self.player_health == 10:
            self.health_bar = self.health_bars[9] 
        elif self.player_health == 0:
            self.health_bar = self.health_bars[10] 
    
    # draw tiles
    def run(self):
        # tiles
        self.tiles.update(self.worldShiftX)
        self.tiles.draw(self.displaySurface)
        # camera
        self.scrollX()
        # player
        self.player.update()
        self.enemy.update(self.worldShiftX)
        self.hzCollision()
        self.vrtCollision()
        self.offscreen_death()
        self.player.draw(self.displaySurface)
        self.enemy.draw(self.displaySurface)
        # health bar
        self.update_health()
        self.displaySurface.blit(self.health_bar, (10, 10))

    def pause(self):
        self.tiles.draw(self.displaySurface)
        self.player.draw(self.displaySurface)
        self.enemy.draw(self.displaySurface)
        self.displaySurface.blit(self.health_bar, (10, 10))
        
    # for resizing sprites by scale factor
    def resized_sprite(self, sprite, scale):
        dimensions = list(sprite.get_size())
        length = len(dimensions)
        for i in range(length):
            dimensions[i] *= scale
        return tuple(dimensions)