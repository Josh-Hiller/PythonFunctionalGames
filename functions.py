import pygame
from pygame.locals import *

###########################################################
# variables and functions needed to run games

# sets up internal variables needed by pygame, shows window?
pygame.display.init()
# sets window title bar text
pygame.display.set_caption("Game Window")
# creates drawing area in window and sets its size ([width, height]) in pixels
displaySurface = pygame.display.set_mode([800, 600])
# list to keep track of which keys are currently being pressed
keysPressed = []
# creates a timer used to control how fast game loop runs
fpsClock = pygame.time.Clock()

##########################################################
#Helper functions

#Tests is a key is currently being pressed
def testKeyPressed(key):
    return key in keysPressed

# Create a Sprite using dictionary, this should contain all pertinent
#info regarding the sprite
def makeSprite(x,y,imageFileName):
    sprite={}

    #x,y coordinates of left corner
    sprite["x"]=x
    sprite["y"]=y
    
    sprite["image"]=pygame.image.load(imageFileName)
    sprite["width"]=sprite["image"].get_width()
    sprite["height"]=sprite["image"].get_height()

    #The total area being occupied by the sprite
    sprite["rectangle"]=sprite["image"].get_rect(topleft=(x,y))

    #To test if 2 sprites overlap
    sprite["left"]   = sprite["x"]
    sprite["right"]  = sprite["x"] + sprite["width"]
    sprite["top"]    = sprite["y"]
    sprite["bottom"] = sprite["y"] + sprite["height"]

    #determine if the sprite is visible
    sprite["visible"]=True

    return sprite

#draws sprites if they are visible 
def drawSprite(sprite):
    if sprite["visible"]:
        displaySurface.blit(sprite["image"],sprite["rectangle"])

#Function to move sprite
def moveSprite(sprite,movex,movey):
    sprite["x"]=sprite["x"]+movex
    x=sprite["x"]
    sprite["y"]=sprite["y"]+movey
    y=sprite["y"]

    sprite["rectangle"]=sprite["image"].get_rect(topleft=(x,y))
    sprite["left"]   = sprite["x"]
    sprite["right"]  = sprite["x"] + sprite["width"]
    sprite["top"]    = sprite["y"]
    sprite["bottom"] = sprite["y"] + sprite["height"]

#Tests for sprite overlap

def testSpriteOverlap(sprite1, sprite2):
    noOverlap = (sprite1["right"] <= sprite2["left"]) or (sprite2["right"] <= sprite1["left"]) or (sprite1["bottom"] <= sprite2["top"]) or (sprite2["bottom"] <= sprite1["top"])
    return (not noOverlap)

#################################################    
#create our Sprites
