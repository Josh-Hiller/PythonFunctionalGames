#############################################################################
# This version of Star Fish Collector was created on 7/24/2018              #
#by Josh Hiller, based off of code provided by Prof. Lee Stemkoski          #
#it illustrates the most basic concepts of creating a video game with pygame#
#############################################################################
import pygame
from pygame.locals import *
import random

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
def moveTo(sprite,x,y):
    moveByX=x-sprite["x"]
    moveByY=y-sprite["y"]
    moveSprite(sprite,moveByX,moveByY)

def testSpriteOverlap(sprite1, sprite2):
    noOverlap = (sprite1["right"] <= sprite2["left"]) or (sprite2["right"] <= sprite1["left"]) or (sprite1["bottom"] <= sprite2["top"]) or (sprite2["bottom"] <= sprite1["top"])
    return (not noOverlap)

#################################################    
#create our Sprites

background = makeSprite(0, 0, "background.png")
snake = makeSprite(0, 0, "snake.png")
apple = makeSprite(400, 300, "apple.png")
message = makeSprite(0, 0, "you-win.png")
lose=makeSprite(0,0,"lose.png")
vel={}
vel["x"]=snake["width"]
vel["y"]=0
##################################################
#Hide (initially) invisible sprites
message["visible"] = False
lose["visible"]=False

###################################################
# This function does all the importnt work in the game
def update():
    # Update based on user input
    if testKeyPressed(K_LEFT):
        vel["x"]= -snake["width"]
        vel["y"]=0
    if testKeyPressed(K_RIGHT):
        vel["x"]= snake["width"]
        vel["y"]=0
    if testKeyPressed(K_UP):
        vel["y"]= -snake["width"]
        vel["x"]=0
    if testKeyPressed(K_DOWN):
        vel["y"]= snake["width"]
        vel["x"]=0
    moveSprite(snake,vel["x"],vel["y"])

    #logic based on updated data, update sprite info
    # check if the turtle overlaps the starfish
    if testSpriteOverlap(snake, apple)==True:
        newX=random.randint(0,(800-apple["width"])/apple["width"])*apple["width"]
        newY=random.randint(0,(600-apple["height"])/apple["height"])*apple["height"]
        moveTo(apple,newX,newY)

    if snake["right"]>800 or snake["left"]<0 or snake["top"]<0 or snake["bottom"]>600:
        lose["visible"]=True
        

    # Update visibility on screen for each sprite
    drawSprite(background)
    drawSprite(snake)
    drawSprite(apple)
    drawSprite(message)
    drawSprite(lose)
    
#############################################################
# Game loop runs the game and spaces it out 
gameRunning=True

while gameRunning==True:
    #First we need statements regarding our user input
    for event in pygame.event.get():
        if event.type == pygame.locals.QUIT:
            gameRunning = False
        if event.type == pygame.KEYDOWN:
            keysPressed.append(event.key)
        if event.type == pygame.KEYUP:
            keysPressed.remove(event.key)
    #then we update our game data
    update()
    # we translate our data into images
    pygame.display.update()
    # pause program for enough time
    fpsClock.tick(15)
pygame.quit()

    
    
