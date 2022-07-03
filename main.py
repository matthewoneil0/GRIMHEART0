import pygame
import sys
import time
from settings import *
from tile import Tile
from level import Level
from pygame import mixer


def main_menu():
    # background sound 
    mixer.init()
    mixer.music.load("music/TitleScreen.mp3")
    mixer.music.set_volume(0.2)
    mixer.music.play(-1)
    
    # Loading & resizing images
    bg = pygame.image.load("imgs/titlepage4.png").convert()
    bg = pygame.transform.scale(bg, (displayWidth, displayHeight))
    display.blit(bg, (0, 0))
    bg_rect = bg.get_rect()

    start_button = pygame.image.load('imgs/startButton.png')
    start_button = pygame.transform.scale(start_button, resized_sprite(start_button, 4))
    quit_button = pygame.image.load('imgs/quitButton.png')
    quit_button = pygame.transform.scale(quit_button, resized_sprite(quit_button, 4))

    # Drawing items onto background
    display.blit(start_button, (bg_rect.centerx-int(start_button.get_rect().width/2), bg_rect.centery))
    display.blit(quit_button,  (bg_rect.centerx-int(quit_button.get_rect().width/2), bg_rect.centery+70))

    start_coords = get_button_dims(start_button, 0)
    quit_coords = get_button_dims(quit_button, 70)

    while True: 
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                pygame.quit() 
            
            # update display
            display.blit(bg, (0, 0))
            display.blit(start_button, (bg_rect.centerx-int(start_button.get_rect().width/2), bg_rect.centery))
            display.blit(quit_button,  (bg_rect.centerx-int(quit_button.get_rect().width/2), bg_rect.centery+70))

            # get mouse position
            mouse = pygame.mouse.get_pos()

            # checks if a mouse is clicked
            if event.type == pygame.MOUSEBUTTONDOWN: 
                # start button
                if start_coords[0] <= mouse[0] <= start_coords[1] and start_coords[2] <= mouse[1] <= start_coords[3]:
                    mixer.music.fadeout(200)
                    time.sleep(0.2)
                    level1()
                elif quit_coords[0] <= mouse[0] <= quit_coords[1] and quit_coords[2] <= mouse[1] <= quit_coords[3]:
                    mixer.music.fadeout(200)
                    time.sleep(0.2)
                    pygame.quit()
                    sys.exit()

        # update display
        pygame.display.update() 


def pause_menu():
    paused = True
    # Load in pause screen buttons.
    unpause_button = pygame.image.load('imgs/unpauseButton.png')
    unpause_button = pygame.transform.scale(unpause_button, resized_sprite(unpause_button, 4))
    quit2main_button = pygame.image.load('imgs/quitToMenuButton.png')
    quit2main_button = pygame.transform.scale(quit2main_button, resized_sprite(quit2main_button, 4))
    keymap = pygame.image.load('imgs/keymap.png')
    keymap = pygame.transform.scale(keymap, resized_sprite(keymap, 4))

    # background sound 
    mixer.init()
    mixer.music.load("music/pause.mp3")
    mixer.music.set_volume(0.1)
    mixer.music.play(-1)

    while paused:
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                pygame.quit() 

            # Display pause buttons
            display.blit(unpause_button, (int(displayWidth/2)-int(unpause_button.get_rect().width/2),
                                          int(displayHeight/2-70)))
            display.blit(quit2main_button,  (int(displayWidth/2)-int(quit2main_button.get_rect().width/2),
                                             int(displayHeight/2)))
            display.blit(keymap,  (int(displayWidth/2)-int(keymap.get_rect().width/2),
                                             int(displayHeight/2+70)))

            unpause_dims = get_button_dims(unpause_button, -70)
            quit2main_dims = get_button_dims(quit2main_button, 0)

            # get mouse position
            mouse = pygame.mouse.get_pos()

            # checks if a mouse is clicked
            if event.type == pygame.MOUSEBUTTONDOWN: 
                # unpause button
                if unpause_dims[0] <= mouse[0] <= unpause_dims[1] and unpause_dims[2] <= mouse[1] <= unpause_dims[3]:
                    paused = False
                    mixer.music.stop()
                    mixer.music.unload()
                    mixer.music.load("music/level.mp3")
                    mixer.music.set_volume(0.2)
                    mixer.music.play(-1)

                # Bug (sorta) Need to change this to where it just exits the level function instead of going into the
                # main_menu function while inside the pause and level1 function
                elif quit2main_dims[0] <= mouse[0] <= quit2main_dims[1] and quit2main_dims[2] <= mouse[1] <= quit2main_dims[3]:
                    main_menu()

        # update display
        pygame.display.update() 


def level1():
    # Setting up level and background 
    level = Level(levelMap, display)
    bg = pygame.image.load("imgs/bg2.png"). convert()
    bg = pygame.transform.scale(bg, (displayWidth * 2, displayHeight))
    x_position = 0
    
    # background sound 
    mixer.init()
    mixer.music.load("music/level.mp3")
    mixer.music.set_volume(0.05)
    mixer.music.play(-1)
    
    # main loop
    playing = True
    while playing:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Insert scrolling background
        rel_x = int(x_position % bg.get_rect().width)
        display.blit(bg, (rel_x - int(bg.get_rect().width), 0))
        if rel_x < displayWidth:
            display.blit(bg, (rel_x, 0))
        key = pygame.key.get_pressed()
        if key[pygame.K_d]:
            x_position -= 0.25
        elif key[pygame.K_a]:
            x_position += 0.25
            
        elif key[pygame.K_ESCAPE]:
            mixer.music.pause()
            level.pause()
            pause_menu()
            mixer.music.unpause()

        level.run()
        pygame.display.update()
        clock.tick(60)
        if level.dead:
            # Christina feel free to replace my game over screen below
            game_over = pygame.image.load("imgs/deathscreen.png"). convert()
            game_over = pygame.transform.scale(game_over, (displayWidth, displayHeight))
            level.pause()
            mixer.music.stop()
            time.sleep(1)
            
            # background sound 
            mixer.init()
            mixer.music.load("music/death.mp3")
            mixer.music.set_volume(0.2)
            mixer.music.play(-1)
            
            # Display Game over screen that send back to main menu
            display.blit(game_over, (0, 0))
            pygame.display.update()
            time.sleep(14)
            main_menu()
        
        # put you win screen here
        if level.win:
            win_level = pygame.image.load("imgs/you_win.png"). convert()
            win_level = pygame.transform.scale(win_level, (displayWidth, displayHeight))
            level.pause()

            mixer.init()
            mixer.music.load("music/finale.mp3")
            mixer.music.set_volume(0.2)
            mixer.music.play(-1)

            display.blit(win_level, (0, 0))
            pygame.display.update()
            time.sleep(14)
            main_menu()

    mixer.music.fadeout(200)
    time.sleep(20)


# for resizing sprites by scale factor
def resized_sprite(sprite, scale):
    dimensions = list(sprite.get_size())
    length = len(dimensions)
    for i in range(length):
        dimensions[i] *= scale
    return tuple(dimensions)


# New function for getting button dimensions
def get_button_dims(button, offsety):
    X = (displayWidth/2)-int(button.get_rect().width/2)
    XX = X + button.get_rect().width
    Y = (displayHeight/2) + offsety
    YY = Y + button.get_rect().height
    return [X, XX, Y, YY]


pygame.init()
display = pygame.display.set_mode((displayWidth, displayHeight))
clock = pygame.time.Clock()

main_menu()
