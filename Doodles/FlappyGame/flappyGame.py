import pygame
from pygame.locals import *
from random import *
import time

pygame.init()

def font_screen(score):
    
    font = pygame.font.SysFont('Tahoma', 60, True, False)

    score = str(score)

    text = font.render(score, True, (255, 255, 255))

    return text
    
class Bird:

    COUNT = 0

    DEGREES = 45
    def __init__(self,x,y,images):

        self.images = images

        self.x = x

        self.y = y

        self.jumpCount = 5

        self.isJump = False

    def rotate(self):

        def rotate_img(image,degrees):

            img = pygame.transform.rotate(image,degrees)
            return img
        
        return {"bird-middle":rotate_img(self.images["bird-standerd"], Bird.DEGREES),
                "bird-up":rotate_img(self.images["bird-up"], Bird.DEGREES),
                "bird-down":rotate_img(self.images["bird-down"], Bird.DEGREES)}
    
    def jump(self,keys):
        if not(self.isJump): 
            if keys[pygame.K_SPACE]:
                self.isJump = True
        else:
            if self.jumpCount >= -20:
                self.y -= (self.jumpCount * abs(self.jumpCount)) * 0.5
                self.jumpCount -= 0.5
                if Bird.DEGREES > -90:
                    Bird.DEGREES -= 5
                if keys[pygame.K_SPACE]:
                    Bird.DEGREES = 45
                    self.jumpCount = 5
            else: 
                self.jumpCount = 5
                Bird.DEGREES = 45
                self.isJump = False
                    
    def touch(self,hy):

        if self.y > hy - 50:

            pygame.quit()
                    

    @property
    def animation(self):
        newImages = self.rotate()
        Bird.COUNT += 250

        if Bird.COUNT <= 250 :

            return newImages["bird-up"]

        if Bird.COUNT <= 500:

            return newImages["bird-middle"]

        if Bird.COUNT <= 750:

            return newImages["bird-down"]

        if Bird.COUNT > 750:

            Bird.COUNT = 0
            return newImages["bird-middle"]


def load_images():

    def load_img(name):
        img = pygame.image.load(name)
        return img

    return {"bird-up":load_img("Flappy_up.png"),
            "bird-down":load_img("Flappy_down.png"),
            "bird-standerd":load_img("Flappy_normal.png"),
            "ground":load_img("Ground.png"),
            "background":load_img("background.png"),
            "pipe-down":load_img("pipe.png"),
            "pipe-top":load_img("top.png"),
            "pipe-top2":load_img("top2.png")}


class Pipes:

    GAP = 2

    MAX_BLOCKS = 7
            
    HEIGHT = 400

    STEP = 100

    START = 0

    BLOCK_LIST = []

    BOTTOM_BLOCK_LIST = []

    SPEED = 10

    bottom_y = 800
    
    def __init__(self,x,y):

            self.x = x

            self.y = y

    def create_pipes(self):

            Pipes.BLOCK_LIST = []
            Pipes.BOTTOM_BLOCK_LIST = []

            self.y = randrange(Pipes.START,Pipes.HEIGHT,Pipes.STEP)

            BLOCKS = int(self.y / Pipes.STEP) + 1

            BOTTOM_BLOCKS = abs((BLOCKS + Pipes.GAP) - Pipes.MAX_BLOCKS)

            bottom_y = abs((self.y + (Pipes.GAP * 100)) + 100)

            for block in range(BLOCKS):

                Pipes.BLOCK_LIST.append((self.x,self.y))

                self.y -= 100

            for block in range(BOTTOM_BLOCKS):

                Pipes.BOTTOM_BLOCK_LIST.append((self.x,bottom_y))

                bottom_y += 100
                
    def move(self):
            newlist = []

            for cor in Pipes.BLOCK_LIST:
            
                x,y = cor
            
                x -= Pipes.SPEED

                newlist.append((x,y))
            
            Pipes.BLOCK_LIST = newlist

            newlist = []

            for cor in Pipes.BOTTOM_BLOCK_LIST:

                x,y = cor

                x -= Pipes.SPEED

                newlist.append((x,y))

            Pipes.BOTTOM_BLOCK_LIST = newlist

    def touch(self,x,y):
        height = Pipes.BOTTOM_BLOCK_LIST[0][1]
        width = Pipes.BOTTOM_BLOCK_LIST[0][0]

        height2 = Pipes.BLOCK_LIST[0][1]
        width2 =  Pipes.BLOCK_LIST[0][0]

        length = 60

        if height - 25 < y and width - 10 < x + 40 < width + length:
            pygame.quit()

        if height2 + 100 > y and width2 -10 < x+ 40 < width2 + length:
            pygame.quit()

    def speed(self):
        Pipes.SPEED += 2

class Background:
    LENGTH = 400
    SPEED = 10
    def __init__(self,x,y,images):

        self.x = x

        self.y = y

        self.ground = images["ground"]
        
    @property
    def move_Ground(self):

        self.x  -= Background.SPEED

    @property    
    def check_Ground(self):

        if self.x == -Background.LENGTH:

            self.x = 0

    def speed(self):

        Background.SPEED += 1

def mainLoop():
    
    clock = pygame.time.Clock()

    FPS = 30

    x = 200

    y =  400

    px = 1000

    py = 0

    bx = 0

    by = 700
            
    images = load_images()

    HEIGHT = 800

    WIDTH = 1000

    window = pygame.display.set_mode((WIDTH,HEIGHT))

    gameOn = True

    background = Background(bx, by, images)

    pipes = Pipes(px, py)

    flappy = Bird(x,y,images)

    pipes.create_pipes()

    score = 0

    text = font_screen(score)

    while gameOn:

        for event in pygame.event.get():

            if event == QUIT:

                gameOn = False

        keys =  pygame.key.get_pressed()

        animation = flappy.animation

        background.move_Ground

        background.check_Ground

        flappy.jump(keys)

        pipes.move()

        window.blit(images["background"],(0,0))

        window.blit(animation,(flappy.x,flappy.y))

        window.blit(images["ground"],(background.x,background.y))

        for cor in pipes.BOTTOM_BLOCK_LIST:

            x,y = cor
        
            window.blit(images["pipe-down"], cor)

        for cor in pipes.BLOCK_LIST:

            x,y = cor

            window.blit(images["pipe-down"],(cor))

            if  x < - 50:
                
                pipes.__init__(px,py)

                pipes.create_pipes()

        top_x = pipes.BLOCK_LIST[0][0]
        top_y = pipes.BLOCK_LIST[0][1]

        if flappy.x == top_x:

            score += 1

            # background.speed()

            # pipes.speed()

            text = font_screen(score)

        top_x -= 3
        top_y += 55
        
        window.blit(images["pipe-top2"], (top_x,top_y))

        top_y += (pipes.GAP * 100) + 45 

        if top_y <  (pipes.MAX_BLOCKS * 100): 

            window.blit(images["pipe-top"], (top_x,top_y))

        window.blit(text,(WIDTH / 2,0))

        clock.tick(FPS)

        pygame.display.update()

        pipes.touch(flappy.x,flappy.y)
        
        flappy.touch(background.y)

mainLoop()

pygame.quit()

        
