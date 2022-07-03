import random
# X - base tile
# B - box tile
# L - left side tile
# R - right side tile
# P - player
# this can be randomized - func to gen map?
with open("LevelDes.txt") as file:
    levelMap = [line.rstrip('\n') for line in file]

file.close()

tileSize = 32
displayWidth = 1200
displayHeight = 640
#displayHeight = len(levelMap) * tileSize *2