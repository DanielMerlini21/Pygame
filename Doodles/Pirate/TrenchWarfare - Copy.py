import pygame
import random

WIDTH = 500
HEIGHT = 600
FPS = 60



# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

#define variables
health_lost_p1 = 0
health_lost_p2 = 0
last_tick = pygame.time.get_ticks()
font_name = pygame.font.match_font("arial")
last_tick_p2 = last_tick

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Trench Warfare")
clock = pygame.time.Clock()

#loading images
fence_img = pygame.image.load("./images/fence.png").convert()
tank = pygame.image.load("./images/tank.png").convert()
mystery_box = pygame.image.load("./images/mystery_box.png").convert() 
cannon_ball = pygame.image.load("./images/cannon_ball.png").convert()
pavement =  pygame.image.load("./images/pavement.png").convert()
explosion_dict = {"large": [],"small": [], "med": []}
smoke_dict = {"p1": [],"p2": []}

for i in range(9):
    image = pygame.image.load(f"./images/Expl_anim/regularExplosion0{i}.png").convert()
    image = pygame.transform.scale(image, (100,100))
    explosion_dict["small"].append(image)
    image = pygame.transform.scale(image, (40,40))
    explosion_dict["med"].append(image)
    image = pygame.transform.scale(image, (60,60))
    explosion_dict["large"].append(image)

for i in range(6):
    image = pygame.image.load(f"./images/smoke_animation/smoke0{i}.png").convert_alpha()
    image.set_colorkey(WHITE)
    image = pygame.transform.scale(image, (60,60))
    smoke_dict["p1"].append(image)
    image = pygame.transform.rotate(image, 180)
    smoke_dict["p2"].append(image)

def spawn_box():
    powerup = PowerUp()
    all_sprites.add(powerup)
    powerup_group.add(powerup)

def shop(player, screen, last_tick, HEIGHT, text, keys):
    tick = pygame.time.get_ticks()
    next_tick = 500
                    
    bar(screen,20, HEIGHT - 200,-100 + player.upgrade_speed)
    bar(screen,20, HEIGHT- 150,-100 + player.upgrade_bullet_speed)
    bar(screen,20, HEIGHT - 100,-100 + player.upgrade_delay)
    draw_text(screen, str(player.coins), 30, 20, text)

    if tick - last_tick > next_tick:

        last_tick = tick
    
        key_state = pygame.key.get_pressed()
        if key_state[keys[0]]:
       #     if player.upgrade_speed < 100:
                if player.coins >= 2:
                
                    player.upgrade_speed += 10
                    player.coins -= 2
                    player.speed += 2
                            
        if key_state[keys[1]]:

          #  if player.upgrade_bullet_speed < 100:
                if player.coins >= 3:

                    player.upgrade_bullet_speed += 10
                    player.coins -= 3
                    player.bullet_speed += 2

        if key_state[keys[2]]:

       #     if player.upgrade_delay < 100:

                if player.coins >= 4:

                    player.upgrade_delay += 10
                    player.coins -= 4
                    player.delay -= 100

        return last_tick

    return last_tick

def draw_text(surf, text, size, x, y):
    
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect) 

def bar(surf, x, y, health_lost):
    if health_lost < -100:
        health_lost = -100
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = BAR_LENGTH + health_lost
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

def create_wall(y, size, img, wall_sprites):
    for i in range(0, 600, size):
        square = Square(i, y, size, img)
        all_sprites.add(square)
        wall_sprites.add(square)

class Vector2D():

    def __init__(self):
        self.x = 10

    def add(self, tup, other, xy = "x"):
        x, y = tup
        if xy == "x":
            return x + other, y
        elif xy == "y":
            return x, y + other  

class Square(pygame.sprite.Sprite):

    def __init__(self, x, y, size, image = 0):
        pygame.sprite.Sprite.__init__(self)
        if image == 0:
            self.image = pygame.Surface((size,size))
            self.image.fill(RED)
        else:
            self.image = image
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.topleft = self.x, self.y

    def return_rect(self):
        return self.rect

    def return_image(self):
        return self.image

class Explosion(pygame.sprite.Sprite):

    def __init__(self, x, y, size = "small"):
        pygame.sprite.Sprite.__init__(self)
        self.expl_list = explosion_dict[size]
        self.image = self.expl_list[0]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.center = self.x, self.y
        self.last_update = pygame.time.get_ticks()
        self.delay = 100
        self.index = 0

    def update(self):
        tick = pygame.time.get_ticks()
        if self.index == 8:
            self.kill()
            
        if tick - self.last_update > self.delay:
            self.last_update = pygame.time.get_ticks()
            self.index += 1
            self.image = self.expl_list[self.index]
            self.image.set_colorkey(BLACK)

class Smoke_anim(pygame.sprite.Sprite):
    def __init__(self, x, y,player):
        pygame.sprite.Sprite.__init__(self)
        self.smoke_list = smoke_dict[player]
        self.image = self.smoke_list[0]
        self.rect = self.image.get_rect()
        self.x = x - 10
        self.y = y
        if player == "p1":
            self.y= self.y + 15
            self.rect.bottomleft = self.x, self.y
        if player == "p2":
            self.rect.topleft = self.x, self.y
        self.last_update = pygame.time.get_ticks()
        self.delay = 20
        self.index = -1

    def update(self):
        tick = pygame.time.get_ticks()

        if tick - self.last_update > self.delay:
            self.index += 1
            if self.index <= 5:
                self.last_update = pygame.time.get_ticks()
                self.image = self.smoke_list[self.index]
                self.image.set_colorkey(BLACK)
            else:
                self.kill()
    
class PowerUp(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.square = Square(random.randrange(100, WIDTH - 100), random.randrange(150, HEIGHT - 150), 10, mystery_box)
        self.radius = 9
        self.rect = self.square.return_rect()
        self.image = self.square.return_image()
        
class Bullet(pygame.sprite.Sprite): 

    def __init__(self, xy, speed = 10, player = "p1"):

        pygame.sprite.Sprite.__init__(self)
        self.image = cannon_ball
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.x, self.y = xy
        self.rect.topleft = self.x, self.y
        self.speed = speed
        
    def update(self):
        self.y -= self.speed
        self.rect.topleft = self.x, self.y
        if self.rect.top < 0 - 10:
            self.kill()
        elif self.rect.bottom > HEIGHT:
            self.kill()

class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = tank
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.topleft = WIDTH / 2, HEIGHT - 55
        self.speedx = 0
        self.speed = 20
        self.vector2d = Vector2D()
        self.last_shoot = pygame.time.get_ticks()
        self.delay = 200
        self.coins = 0
        self.bullet_speed = 8
        self.upgrade_speed = 0
        self.upgrade_delay = 0
        self.upgrade_bullet_speed = 0
                 

    def add_coins(self):
        self.coins += 1
        
    def update(self):
        self.speedx = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.speedx = -self.speed
        elif keys[pygame.K_RIGHT]:
            self.speedx = self.speed
        self.rect.topleft = self.vector2d.add(self.rect.topleft, self.speedx)
        if keys[pygame.K_UP]:
            new_time = pygame.time.get_ticks()
        
            if new_time - self.last_shoot > self.delay:

                self.last_shoot = pygame.time.get_ticks()
                bullet = Bullet(self.vector2d.add(self.rect.topleft, -20, "y"), self.bullet_speed * 0.8, "p1")
                all_sprites.add(bullet)
                bullets_sprites_p1.add(bullet)
                all_bullets_sprites.add(bullet)
        #stops player from moving off screen
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

class Player2(pygame.sprite.Sprite):

    def __init__(self):
        
        pygame.sprite.Sprite.__init__(self)
        self.tank = pygame.transform.rotate(tank,180)
        self.image = self.tank
        self.rect = self.image.get_rect()
        self.rect.topleft = WIDTH / 2, 0 + 15
        self.speedx = 0
        self.speed = 10
        self.vector2d = Vector2D()
        self.last_shoot = pygame.time.get_ticks()
        self.delay = 200
        self.coins = 0
        self.bullet_speed = 8
        self.upgrade_speed = 0
        self.upgrade_delay = 0
        self.upgrade_bullet_speed = 0
                 

    def add_coins(self):
        self.coins += 1

    def update(self):
        self.speedx = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.speedx = -self.speed
        elif keys[pygame.K_d]:
            self.speedx = self.speed
        self.rect.topleft = self.vector2d.add(self.rect.topleft, self.speedx)
        if keys[pygame.K_w]:
            new_time = pygame.time.get_ticks()
        
            if new_time - self.last_shoot > self.delay:

                self.last_shoot = pygame.time.get_ticks()
                bullet = Bullet(self.vector2d.add(self.rect.topleft, 50, "y"), -self.speed * 0.8, "p2")
                all_sprites.add(bullet)
                bullets_sprites_p2.add(bullet)
                all_bullets_sprites.add(bullet)
        #stops player from moving off screen
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:

            self.rect.left = 0

#declaring sprites
all_sprites = pygame.sprite.Group()
bullets_sprites_p1 = pygame.sprite.Group()
bullets_sprites_p2 = pygame.sprite.Group()
all_bullets_sprites = pygame.sprite.Group()
wall_sprites_p1 = pygame.sprite.Group()
wall_sprites_p2 =pygame.sprite.Group()
powerup_group = pygame.sprite.Group()
#construct wall

create_wall(80, 30, fence_img, wall_sprites_p2)
create_wall(HEIGHT - 105, 30, fence_img, wall_sprites_p1)   
#setting players
player = Player()
player2 = Player2()
#setting PowerUp
for i in range(9):
    spawn_box()
#setting classes
#adding to sprite groups
all_sprites.add(player2)
all_sprites.add(player)
    
# Game loop
running = True
while running:
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False

    # Update
    all_sprites.update()

    #check for collision
    hits = pygame.sprite.groupcollide(wall_sprites_p1, bullets_sprites_p2, True, True)
    for hit in hits:
        x, y = hit.rect.center
        expl = Explosion(x, y, "med")
        all_sprites.add(expl)
        
    hits = pygame.sprite.groupcollide(wall_sprites_p2, bullets_sprites_p1, True, True)
    for hit in hits:
        x, y = hit.rect.center
        expl = Explosion(x, y, "med")
        all_sprites.add(expl)
        
    hits = pygame.sprite.spritecollide(player, bullets_sprites_p2, True)

    for hit in hits:
        #takes life off from player_1
        x, y= hit.rect.center
        expl = Explosion(x, y)
        all_sprites.add(expl)
        health_lost_p1 -= 0.5 
        if health_lost_p1 < -100:
            running = False
            x, y= hit.rect.center
            expl = Explosion(x, y)
            all_sprites.add(expl)

    hits = pygame.sprite.spritecollide(player2, bullets_sprites_p1, True)

    for hit in hits:
        #takes life off from player_2
        health_lost_p2 -= 0.5
        x, y= hit.rect.center
        expl = Explosion(x, y)
        all_sprites.add(expl)
        if health_lost_p2 < -100:
            running = False

    hits = pygame.sprite.groupcollide(powerup_group, bullets_sprites_p2, True, True)
    #check for player2
    for hit in hits:
        x, y= hit.rect.center
        expl = Explosion(x, y, "small")
        all_sprites.add(expl)
        spawn_box()
        player2.add_coins()
    
    hits = pygame.sprite.groupcollide(powerup_group, bullets_sprites_p1, True, True)
    #check for player1
    for hit in hits:
        x, y= hit.rect.center
        expl = Explosion(x, y, "small")
        all_sprites.add(expl)
        spawn_box()
        player.add_coins()

    #check collision between bullets
    hits = pygame.sprite.groupcollide(bullets_sprites_p2, bullets_sprites_p1, True, True)
    for hit in hits:
        x, y = hit.rect.center
        expl = Explosion(x, y, "large")
        all_sprites.add(expl)

    # Draw / render
    screen.fill(BLACK)
    screen.blit(pavement, (0,HEIGHT - 100))
    screen.blit(pavement, (0, 0))
    bar(screen, 20, 10, health_lost_p2)
    bar(screen, 20, HEIGHT - 20, health_lost_p1)
    all_sprites.draw(screen)
    #draw shop
    last_tick = shop(player, screen, last_tick, HEIGHT, 515, [pygame.K_b,pygame.K_n,pygame.K_m])
    last_tick_p2 = shop(player2, screen, last_tick_p2, 320, 75, [pygame.K_1,pygame.K_2,pygame.K_3])
    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()
