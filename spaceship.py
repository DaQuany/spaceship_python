import pygame
from pygame.rect import *
import random

#########################################################
#restart when R button is pressed
def restart():
    global score, isGameOver
    for i in range(len(star)):
        rectStar[i].y = -1
    score = 0
    isGameOver = False

#processing the events according to the inputs(buttons)
def eventProcess(move):
    global isActive
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                isActive = False
            if event.key == pygame.K_LEFT:
                move.x = -1
            if event.key == pygame.K_RIGHT:
                move.x = 1
            if event.key == pygame.K_UP:
                move.y = -1
            if event.key == pygame.K_DOWN:
                move.y = 1
            if event.key == pygame.K_r:
                restart()

#########################################################
#moving the player according to the input
def movePlayer(player, current, move, isGameOver):
    global SCREEN_WIDTH, SCREEN_HEIGHT
    if not isGameOver:
        current.x += move.x
        current.y += move.y
#### limit
    if current.y > SCREEN_HEIGHT - current.height:
        current.y = SCREEN_HEIGHT - current.height
    if current.x > SCREEN_WIDTH-current.width:
        current.x = SCREEN_WIDTH - current.width
    if current.y < 0:
        current.y = 0
    if current.x < 0:
        current.x = 0
    SCREEN.blit(player, current)
#########################################################
def timeUpdate50ms():
    global time500ms
    time500ms += 1
    if time500ms > 5:
        time500ms = 0
        return True
    return False

#making stars in random x values from the top of the game screen
def makeStar(rec):
    if timeUpdate50ms():
        idex = random.randint(0, len(star)-1)
        if rec[idex].y == -1:
            rec[idex].x = random.randint(0, SCREEN_WIDTH)
            rec[idex].y = 0

#dropping the stars
def moveStar(star, current, isGameOver):
    global SCREEN_HEIGHT
    for i in range(len(star)):    
        if current[i].y == -1:
            continue
        if not isGameOver:
            current[i].y += 1
        if current[i].y > SCREEN_HEIGHT:
            current[i].y = -1
        SCREEN.blit(star[i], current[i])
#########################################################
#checking if the player has crashed to a star by checking it's width and height and star's x and y values
def CheckCollision(player, star):
    global isGameOver, score
    if isGameOver:
        return
    for rec in star:
        if rec.top < player.bottom \
                and player.top < rec.bottom \
                and rec.left < (player.right-8) \
                and (player.left+8) < rec.right:
            isGameOver = True
            break
    score += 1
#########################################################
def timeUpdate4sec(isGameOver):
    global time4Sec, time4SecToggle
    if not isGameOver:
        return False
    time4Sec += 1
    if time4Sec > 40:
        time4Sec = 0
        time4SecToggle = (~time4SecToggle)
    return time4SecToggle


#displaying the text messages on the screen
def setText(isupdate=False):
    global score
    myFont = pygame.font.SysFont("arial", 20, True, False)

    SCREEN.blit(myFont.render(
        f'score : {score}', True, 'green'), (10, 10, 0, 0))

    if isupdate:
        SCREEN.blit(myFont.render(
            f'Game Over!!', True, 'red'), (150, 300, 0, 0))
        SCREEN.blit(myFont.render(
            f'press R - Restart', True, 'red'), (140, 320, 0, 0))
#########################################################
#########################################################


##variables
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
score = 0
isActive = True
isGameOver = False
move = Rect(0, 0, 0, 0)
time500ms = 0
time4Sec = 0
time4SecToggle = False
#########################################################
#screen
pygame.init()
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("space!!")
#########################################################
##3. player
player = pygame.image.load("Player.png")
player = pygame.transform.scale(player, (20, 30))
rectPlayer = player.get_rect()
rectPlayer.centerx = (SCREEN_WIDTH / 2)
rectPlayer.centery = (SCREEN_HEIGHT / 2)
#########################################################
#meteors
star = [pygame.image.load("star.png") for i in range(20)]
rectStar = [None for i in range(len(star))]
for i in range(len(star)):
    star[i] = pygame.transform.scale(star[i], (20, 20))
    rectStar[i] = star[i].get_rect()
    rectStar[i].y = -1
#########################################################
#time
clock = pygame.time.Clock()

while isActive:
#showing the blank screen
    SCREEN.fill((0, 0, 0))
#event processing with keyboard inputs
    eventProcess(move)    
#moving the player
    movePlayer(player, rectPlayer,move,isGameOver)
#creating and moving the stars
    makeStar(rectStar)
    moveStar(star, rectStar,isGameOver)
#collision check
    CheckCollision(rectPlayer, rectStar)
#according to the events happening, displaying the texts on the screen
    setText(timeUpdate4sec(isGameOver))    
#updating with time
    pygame.display.flip()
    clock.tick(100) 