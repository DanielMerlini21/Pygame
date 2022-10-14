import pygame
import time
from random import *

pygame.init()
height = 600
width =800
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("OldSnake")

img = pygame.image.load("snake.png")
appleImg = pygame.image.load("apple.png")
bodyImg = pygame.image.load("BODY.png")
icon = pygame.image.load("apple.png")
pygame.display.set_icon(icon)
direction = "right" 

green = (0,255,0)
red = (255,0,0)
blue = (0,0,255)
white = (255,255,255)
black =(0,0,0)
purple = (128,0,128)

apple_x = round(randrange(0,width / 2 - 50)/10.0)*10.0
apple_y = round(randrange(0,height / 2 - 50)/10.0)*10.0

pos_x = height / 2
pos_y = width / 2

lead_x = 10
lead_y = 0

speed = 20

x_or_y = "x"
FPS = 15

AppleThickness = 50
block_size = 10

snakeLength = 1
snakeBody = [[pos_x,pos_y]]

clock = pygame.time.Clock()

def score(score,size):
    font = pygame.font.Font('freesansbold.ttf',size)
    text = font.render("Score is :" + str(score),True,black)
    screen.blit(text,[0,0])
    
def game_intro():
    intro = True
    while intro:
        screen.fill(white)
        message_to_screen("welcome",purple,-100,size = 80)
        message_to_screen("Snake",purple,-30,size = 20)
        message_to_screen("-You should eat apple to get points",black,40,20)
        message_to_screen("-Do not hit the walls",black,60,20)
        message_to_screen("-Dont hit your own body",black,80,20)
        clock.tick(FPS)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    intro = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

def inside(x,y):
    return 0 < x < 800 - 20 and 0 < y < 600 - 20

def square(color,pos_x,pos_y,width,height):
    pygame.draw.rect(screen,color,[pos_x,pos_y,width,height])

def message_to_screen(text,color,y_displace = 0,size = 20):
    font = pygame.font.Font('freesansbold.ttf',size)
    text = font.render(text, True,color)
    textRect = text.get_rect()  
    textRect.center = (width / 2, height / 2 + y_displace) 
    screen.blit(text, textRect)

def gameLoop():
    global pos_x,pos_y,lead_x,lead_y,x_or_y,apple_x,apple_y,snakeBody,snakeLength,direction
    gameExit = False
    gameOver = False
    while not gameExit:
        while gameOver == True:
            screen.fill(white)
            message_to_screen("Game Over", red,0,50)
            message_to_screen("press space to play again", black,50)
            pygame.display.update() 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                            pos_x = height / 2
                            pos_y = width / 2
                            snakeBody = [[pos_x,pos_y]]
                            gameOver = False
                            gameLoop()
                    if event.key == pygame.K_q:
                            pygame.quit()
                            quit()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    lead_y = -speed
                    x_or_y = "y"
                    direction = "up"
                elif event.key == pygame.K_DOWN:
                    lead_y = speed
                    x_or_y = "y"
                    direction = "down"
                elif event.key == pygame.K_LEFT:
                    lead_x = -speed
                    x_or_y = "x"
                    direction = "left"
                elif event.key == pygame.K_RIGHT:
                    lead_x = speed
                    x_or_y = "x"
                    direction = "right"
                    
        x = snakeBody[-1][0]
        y = snakeBody[-1][1]
        head = [x,y]
        
        if not inside(pos_x,pos_y):
            gameOver = True

    
        if x_or_y == "x":
            pos_x += lead_x
            head[0] += lead_x
            
        if x_or_y == "y":
            pos_y += lead_y
            head[1] += lead_y

        for xy in snakeBody:
            if xy[0] == head[0] and xy[1] == head[1]:
                gameOver = True
                
        snakeBody.append(head)
        
        touch = False
        
        if pos_x > apple_x and pos_x < apple_x + AppleThickness and pos_y > apple_y and pos_y < apple_y + AppleThickness:

            apple_x = round(randrange(0,width - 50)/10.0)*10.0
            apple_y = round(randrange(0,height - 50)/10.0)*10.0
            touch = True

        elif pos_x + block_size > apple_x and pos_x + block_size < apple_x + AppleThickness and pos_y + block_size > apple_y and pos_y + block_size < apple_y + AppleThickness:

            apple_x = round(randrange(0,width - 50)/10.0)*10.0
            apple_y = round(randrange(0,height - 50)/10.0)*10.0
            touch = True

        if touch == False:
            snakeBody.pop(0)

        clock.tick(FPS)
        screen.fill(white)

        screen.blit(appleImg,(apple_x,apple_y))
        score(len(snakeBody)-1,20)
        
        if direction == "right":
                Snakehead = pygame.transform.rotate(img,270)
        if direction == "left":
                Snakehead = pygame.transform.rotate(img,90)
        if direction == "up":
                Snakehead = img
        if direction == "down":
                Snakehead = pygame.transform.rotate(img,180)
        screen.blit(Snakehead,(snakeBody[-1][0],snakeBody[-1][1]))
        for xy in snakeBody[:-1]:
            screen.blit(bodyImg,(xy[0],xy[1]))
            
        pygame.display.update()


game_intro()
gameLoop()

pygame.quit()
quit()
    

    
                
