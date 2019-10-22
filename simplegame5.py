#############################################################################
# This version of Snake was created on 7/24/2018                            #
# by Josh Hiller, based off of code for Star Fish Collector                 #
# provided by Prof. Lee Stemkoski of Adelphi University.                    #
# It illustrates loops, conditionals, funcations and variable types.        #
#############################################################################
import pygame, random
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
#General functions for any game

#Tests if a key is currently being pressed
def testKeyPressed(key):
    return key in keysPressed

# Create a Sprite using dictionary, this should contain all pertinent
# info regarding the sprite
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

#Function to move sprite by a specific number of pixels
def moveBy(sprite,movex,movey):
    sprite["x"]=sprite["x"]+movex
    x=sprite["x"]
    sprite["y"]=sprite["y"]+movey
    y=sprite["y"]

    sprite["rectangle"]=sprite["image"].get_rect(topleft=(x,y))
    sprite["left"]   = sprite["x"]
    sprite["right"]  = sprite["x"] + sprite["width"]
    sprite["top"]    = sprite["y"]
    sprite["bottom"] = sprite["y"] + sprite["height"]

# move sprite to a new location
def moveTo(sprite,x,y):
    moveX=x-sprite["x"]
    moveY=y-sprite["y"]
    moveBy(sprite,moveX,moveY)
    
#Tests for sprite overlap
def testSpriteOverlap(sprite1, sprite2):
    noOverlap = (sprite1["right"] <= sprite2["left"]) or (sprite2["right"] <= sprite1["left"]) or (sprite1["bottom"] <= sprite2["top"]) or (sprite2["bottom"] <= sprite1["top"])
    return (not noOverlap)
#################################################
# Game specific functions
#################################################

#Updates the location of all the visible snake components and the first invisible one
def updateChar(sprite):
    L=sprite["length"]+1
    for num in range(L,1,-1):
        moveTo(sprite[num],sprite[num-1]["x"],sprite[num-1]["y"])
        
# function to select a new position for the apple
def newAppleLocation():
    #this way we enter the while loop
    badCoordinates=True
    while badCoordinates==True:
        #We wish to exit the while loop if we ave picked a valid location
        badCoordinates=False
        #We test to see if the new apple is placed on top of a currently visible segment of the snake
        for num in range(1,snake["length"]+1):
            if testSpriteOverlap(snake[num], apple)==True:
                #if there is overlap we repeat the while loop
                badCoordinates=True
                newX=random.randint(0,(800-apple["width"])/apple["width"])*apple["width"]
                newY=random.randint(0,(600-apple["height"])/apple["height"])*apple["height"]
                moveTo(apple,newX,newY)

#################################################    
#Create our Sprites and game specific variables
#################################################
                
background = makeSprite(0, 0, "background.png")
snake = {"length":1}
for num in range(0,1200):
    snake[num]=makeSprite(0, 0, "snake.png")
    
apple = makeSprite(400, 300, "apple.png")
message = makeSprite(0, 0, "you-win.png")
lose=makeSprite(0,0,"lose.png")
vel={}
vel["x"]=snake[1]["width"]
vel["y"]=0
##################################################
#Hide (initially) invisible sprites
message["visible"] = False
lose["visible"]=False

###################################################
# This function does all the importnt work in the game
###################################################

def update():
    # Update snake head vepocity based on user input,
    if testKeyPressed(K_LEFT):
        vel["x"]= -snake[1]["width"]
        vel["y"]=0
    if testKeyPressed(K_RIGHT):
        vel["x"]= snake[1]["width"]
        vel["y"]=0
    if testKeyPressed(K_UP):
        vel["y"]= -snake[1]["width"]
        vel["x"]=0
    if testKeyPressed(K_DOWN):
        vel["y"]= snake[1]["width"]
        vel["x"]=0


    ###########################################################
    # logic based on updated data, update sprite info
    ###########################################################

    # updates the snake body position and then the head
    updateChar(snake)
    moveBy(snake[1],vel["x"],vel["y"])
    
    # check if the snake head has caught the apple,
    # if so we increase the visible segments of the snake by 1
    # and pick a new location for the apple
    if testSpriteOverlap(snake[1], apple)==True:
        snake["length"]+=1
        snake[snake["length"]]["visible"]=True
        newAppleLocation()

    # check lose condition (1) we hit the boarder of the screen
    if snake[1]["right"]>800 or snake[1]["left"]<0 or snake[1]["top"]<0 or snake[1]["bottom"]>600:
        lose["visible"]=True

    # check lose condition (2) the snake head hits a visible segment of the snake
    for num in range(2,snake["length"]+1):
        if testSpriteOverlap(snake[1],snake[num])==True:
            lose["visible"]=True
    
        
    #######################################################
    # Update visibility on screen for each sprite
    #######################################################
    drawSprite(background)

    # note that we only draw the visible snake segments
    for num in range(1,(snake["length"]+1)):
        drawSprite(snake[num])
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
    fpsClock.tick(10)
pygame.quit()

    
    
