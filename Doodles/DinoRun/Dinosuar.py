import pygame
from pygame.locals import *
import random

pygame.init()

def game_over(screen, images):

    game_over_image = images["game_over"]

    height = 34
    width = 30

    WHITE = (255,255,255)

    retry_button = game_over_image.subsurface((78, 34, 35, 30))

    retry = False
    
    while not(retry):

        screen.fill(WHITE)

        screen.blit(game_over_image, (250,100))

        mx, my = pygame.mouse.get_pos()

        b = screen.blit(retry_button, (328,134))

        for event in pygame.event.get():


            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                if b.collidepoint(mx, my):

                    main()
    
    


        pygame.display.flip()

def load_images():

    def load(img):

        img = pygame.image.load(f"./images/" + str(img)).convert_alpha()
        return img

    return {"Dino-still": load("dinosuar-still.png"),
            "Dino-left": load("dinosuar-left.png"),
            "Dino-right": load("dinosuar-right.png"),
            "Dino-crouch-right": load("dinosuar-crouch-right.png"),
            "Dino-crouch-left": load("dinosuar-crouch-left.png"),
            "floor": load("floor.png"),
            "game_over": load("game_over.png"),
            "cloud": load("cloud.png"),
            "Pterodactyl-wing-down": load("Pterodactyl-wing-down.png"),
            "Pterodactyl-wing-up": load("Pterodactyl-wing-up.png"),
            "cactus-big-1":load("cactus-big-1.png"),
            "cactus-big-2":load("cactus-big-2.png"),
            "cactus-mixed-4":load("cactus-mixed-4.png"),
            "cactus-small-1":load("cactus-small-1.png"),
            "cactus-small-2":load("cactus-small-2.png"),
            "cactus-small-3":load("cactus-small-3.png")}

class Dino():

    TICK = 0
    JUMP_SIZE = 12.6
    gravity = 0.6
    weight = 20
    index = 5
    current_rect = 0

    def __init__(self, images, cor):

        """
        Dino images
        """

        self.images = images
        self.dino_still = self.images["Dino-still"]
        self.dino_left = self.images["Dino-left"]
        self.dino_right = self.images["Dino-right"]
        self.dino_crouch_right = self.images["Dino-crouch-right"]
        self.dino_crouch_left = self.images["Dino-crouch-left"]
        self.dino_still_rect = pygame.Surface((40, 43)).get_rect()
        self.dino_crouch_rect = pygame.Surface((55, 26)).get_rect()
        """
        Dino rect

        """
 
        self.x, self.y = cor
        self._y = self.y
        Dino.current_rect = self.dino_still_rect
        Dino.current_rect.topleft= (self.x, self.y)
        self.isJump = True
        self.isCrouch = False
        self.jumpCount = Dino.JUMP_SIZE
        
    def walk(self, img1, img2):

        Dino.TICK += 0.25

        if Dino.TICK < 5:

                return img1

        else:

            if Dino.TICK >= 11:

                Dino.TICK = 0

            return img2      

    def animation(self, keys):

        self.dino_still_rect.topleft = self.x, self.y
        self.dino_crouch_rect.topleft = self.x, self.y + 20
        Dino.TICK += 1

        if keys[K_DOWN]:

            self.isCrouch = True
            animation = self.walk(self.dino_crouch_left, self.dino_crouch_right)
            Dino.current_rect = self.dino_crouch_rect
            return animation

        if self.isJump:
            
            Dino.current_rect = self.dino_still_rect
            return self.dino_still

        else:
            self.isCrouch = False
            animation = self.walk(self.dino_left, self.dino_right)
            Dino.current_rect = self.dino_still_rect
            return animation
    
    def jump(self, pressed_keys):

        if self.y <= self._y:
                
            if pressed_keys[K_DOWN]:

                self.y += Dino.weight

            if not(self.isJump):
        
                if pressed_keys[K_SPACE]:

                     self.isJump = True

            if self.isJump: 
               
                 if self.jumpCount >= -Dino.JUMP_SIZE:
        
                    neg = 1
                        
                    if self.jumpCount < 0:
                        neg = -neg

                    self.y -= (self.jumpCount ** 2) * 0.1 * neg
                    self.jumpCount -= Dino.gravity

                 else:

                    self.isJump = False
                    self.jumpCount = Dino.JUMP_SIZE

        if self.y >= self._y:
            self.y -= Dino.weight
            self.isJump = False
            self.jumpCount = Dino.JUMP_SIZE

    
    def touch(self, obs):

        touch =Dino.current_rect.colliderect(obs)
        return touch
        

class Background:

    WIDTH_OF_FLOOR = 829
    speed = 0
    time_of_day = 0
    day_length = 1000

    def __init__(self, images, cor, screen):

        self.screen = screen
        self.cloud_list = []
        self.floor_img = images["floor"]
        self.clouds = images["cloud"]
        self.floor_x, self.floor_y = cor
        self.color_sky = (255, 255, 255)

    def move(self, cactus):

        Background.speed = cactus.speed

        self.floor_x -= cactus.speed

        if self.floor_x < 0 - Background.WIDTH_OF_FLOOR:
            
            self.floor_x = 0
            
        return self.floor_img

    def gen_cloud(self):
        for cloud in range(3):

            cloud_x = random.randrange(700, 1500)
            cloud_y = random.randrange(0, 200)

            self.cloud_list.append([self.clouds, (cloud_x, cloud_y)])

            

    def move_clouds(self):
        for cloud in self.cloud_list:
            img = cloud[0]
            x, y = cloud[1]
            if x < -50:
                x = random.randrange(700, 1000)
                y = random.randrange(50, 205)

            air_resistance = Background.speed * 0.5
            x -= Background.speed - air_resistance
            cloud[1] = x,y

            self.screen.blit(img, (x ,y))

    def sky(self):

        Background.time_of_day += 1

        if Background.time_of_day <= Background.day_length:

            r,g,b = self.color_sky

            if r != 255:

                r += 1
                g += 1
                b += 1
                self.color_sky = r,g,b

        elif Background.time_of_day > Background.day_length and Background.time_of_day < Background.day_length * 2:

            r,g,b = self.color_sky

            if r != 0:

                r -= 1
                g -= 1
                b -= 1
                self.color_sky = r,g,b

        else:

            Background.time_of_day = 0

        return (self.color_sky)


class Cactus:

    split_idx = 10
    cactus_size = []
    cactus_list = []
    speed = 3
    difficulty = 0.01
    tick = 0


    def __init__(self, cor, images, screen):

        Cactus.cactus_list = []
        self.stop = False
        Cactus.speed = 2
        self.cactus_img = dict(list(images.items())[Cactus.split_idx:]) 
        Cactus.cactus_size = list(self.cactus_img.keys())
        self.x, self.y = cor
        self.screen = screen

    def increase_bird_chance(self):

        Cactus.tick += 1

    def increase_speed(self):
        
        self.speed += self.difficulty
        

    def cactus_gen(self):

        size = random.choice(Cactus.cactus_size)

        cactus = self.cactus_img[size]

        cactus_rect = cactus.get_rect()

        for cact in Cactus.cactus_size[3:]:

            if cact == size:

                Cactus.cactus_list.append([cactus, self.x, self.y + 10, cactus_rect])

                return Cactus.cactus_list
 
        Cactus.cactus_list.append([cactus, self.x, self.y, cactus_rect])

        return Cactus.cactus_list

    def draw(self, dino):

        self.increase_speed()

        for cactus_object in Cactus.cactus_list:

            index = Cactus.cactus_list.index(cactus_object)
            cactus_img = cactus_object[0]
            x = cactus_object[1]
            y = cactus_object[2]
            cactus_rect = cactus_object[3]
            cactus_rect.topleft = (x, y)

            touch = dino.touch(cactus_rect)

            if touch == True:

                return touch
            
            if x < -60:
                
                new_list = self.cactus_gen()
                s_list = []
                s_list.append(new_list[-1])
                Cactus.cactus_list = s_list
                x = 700
                self.increase_bird_chance()

                if Cactus.tick >= 2:
                    
                    self.stop = True
                    Cactus.tick = 0
                    return False


            x -= self.speed

            cactus_object[1] = x

            """
            check for touching the dinosuar

            """
    
            xy = x,y

            self.screen.blit(cactus_img, xy)

class Pterodactyl():

    splt_idx = 8
    splt_idx_end = 10
    to_next_sprite = 0

    def __init__(self,cor, images, screen):

        
        self.screen = screen
        self.sprite_height = random.randrange(0, 70, 10)
        self.current_sprite = None
        self.images = dict(list(images.items())[Pterodactyl.splt_idx:Pterodactyl.splt_idx_end])
        self.wing_down_rect = pygame.Surface((42, 30)).get_rect()
        self.wing_up_rect = pygame.Surface((42, 30)).get_rect()
        self.current_rect = (self.wing_up_rect)
        self.x, self.y = cor
        self._x = self.x

    def change_height(self):

        self.sprite_height = random.choice([10, 0])
            
    def draw(self, dino):

        Pterodactyl.to_next_sprite += 2

        if Pterodactyl.to_next_sprite < 50: 
        
            self.current_sprite = self.images["Pterodactyl-wing-up"]

            self.current_rect = self.wing_up_rect

        else:

            self.current_sprite = self.images["Pterodactyl-wing-down"]

            self.current_rect = self.wing_down_rect

            if Pterodactyl.to_next_sprite > 100:

                Pterodactyl.to_next_sprite = 0

        self.current_rect.topleft = self.x, self.y - self.sprite_height
        
        if dino.touch(self.current_rect):

            return True

        self.screen.blit(self.current_sprite, (self.x,self.y - self.sprite_height))

    def move(self, cactus):
        
        self.x -= cactus.speed * 1.5

        if self.x < -60:

            self.x = self._x

            self.current_rect.topleft = self.x, self.y

            cactus.stop = False
        
            self.sprite_height = random.randrange(0, 70, 10)

            return None
            
def main():

    #booleans

    quit_game = False

    #colors

    WHITE = (255,255,255)

    #screen

    WIDTH = 700

    HEIGHT = 300

    #clock

    clock = pygame.time.Clock()

    FPS = 60

    #dino

    d_cor = (50, 205)

    #Pterodactyl

    p_cor = (900, 205)

    # background

    f_cor = (20, 200)

    # cactus

    c_cor = (700, 193)

    # score

    score = 0

    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    pygame.display.set_caption("score")

    images = load_images()

    dino = Dino(images, d_cor)

    background = Background(images, f_cor, screen)
    background.gen_cloud()
    cactus = Cactus(c_cor, images, screen)
    pterodactyl = Pterodactyl(p_cor, images, screen)
    cactus.cactus_gen()
    while not quit_game:


        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                quit_game = True

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE:

                    pass

        #checks for key presses
        keys = pygame.key.get_pressed()
        dino.jump(keys)
        
        #fill screen white
        screen.fill(background.sky())        
        #blit images on screen
        score+= 1


        pygame.display.set_caption(f"SCORE:{score}")
        screen.blit(background.move(cactus), (background.floor_x, background.floor_y))
        background.move_clouds()
        screen.blit(dino.animation(keys), (dino.x, dino.y))

        if cactus.stop == False:

            quit_game = cactus.draw(dino)

        elif cactus.stop == True:

            pterodactyl.move(cactus)
            quit_game = pterodactyl.draw(dino)

        #update

        pygame.display.update()
        #frames per second
        clock.tick(FPS)

        if quit_game == True:

            return screen, images


screen, images = main()

game_over(screen, images)

pygame.quit()
        

        
