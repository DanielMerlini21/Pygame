import pygame
import random

WIDTH = 600
HEIGHT = 600
FPS = 60

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255,255,0)

#variables
damage = 5
damage_to_p1 = 0
damage_to_p2 = 0

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SpaceBattle")
clock = pygame.time.Clock()

#loading images
player_img = pygame.image.load("./assets/images/playerShip1_orange.png").convert()
lazer_img = pygame.image.load("./assets/images/laserBlue01.png").convert()
explosion_dict = {"large": [],"small": [], "med": []}
meteor_img_list = []
player_img2 =pygame.image.load("./assets/images/playerShip1_green.png").convert()
background = pygame.image.load("./assets/images/background.png").convert()
background = pygame.transform.scale(background, (WIDTH,HEIGHT))

for i in range(1, 4):
    image = pygame.image.load(f"./assets/images/meteor/meteorGrey_{i}.png").convert()
    image.set_colorkey(BLACK)
    meteor_img_list.append(image)

for i in range(9):
    image = pygame.image.load(f"./assets/images/Expl_anim/regularExplosion0{i}.png").convert()
    image = pygame.transform.scale(image, (20,20))
    explosion_dict["small"].append(image)
    image = pygame.transform.scale(image, (40,40))
    explosion_dict["med"].append(image)
    image = pygame.transform.scale(image, (60,60))
    explosion_dict["large"].append(image)

def draw_text(surf, text, size, x, y):
    
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def spawnexpl(size, pos):
    
    x, y = pos
    expl = Explosion(x, y, size)
    all_sprites.add(expl)

def spawnmob():

    mob = Mob()
    all_sprites.add(mob)
    meteor_sprites.add(mob)

def draw_bar(surf, x, y, damage):
    
    if damage >= 100:
        damage = 100
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = BAR_LENGTH - damage
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)


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
            
class Vec2d():

    def __init__(self):
        self.x = 10
        self.y = 10

    def add(self, num1, num2):
        x1, y1 = num1
        x2, y2, = num2

        return x1 + x2, y1 + y2

class Mob(pygame.sprite.Sprite):

    def __init__(self):
         pygame.sprite.Sprite.__init__(self)
         self.image = random.choice(meteor_img_list)
         self.rect = self.image.get_rect()
         self.radius = int(self.rect.width / 2)
         self.rect.center = random.randrange(WIDTH, WIDTH + self.rect.width), random.randrange(100, HEIGHT - 50)
         self.speedxy = (random.randrange(-5, -2), random.randrange(-3, 3))
         self.vec2d = Vec2d()
         self.degrees = 0

    def update(self):
         self.rect.center = self.vec2d.add(self.rect.center, self.speedxy)
         if self.rect.left < 0- self.rect.width or self.rect.bottom > HEIGHT + self.rect.height or self.rect.top < 0 - self.rect.height:
             self.image = random.choice(meteor_img_list)
             self.rect = self.image.get_rect()  
             self.radius = int(self.rect.width / 2)
             self.rect.center = random.randrange(WIDTH, WIDTH + self.rect.width), random.randrange(-10, HEIGHT - 50)
             self.speedxy = (random.randrange(-5, -2), random.randrange(0, 3))

class Bullet(pygame.sprite.Sprite):

    def __init__(self, xy, face):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.speed_dir = {"UP": [(0, -self.speed), 0], "LEFT": [(-self.speed, 0), 90], "RIGHT": [(self.speed, 0), 270], "DOWN": [(0, self.speed), 180]}
        self.x, self.y = xy
        self.image = pygame.transform.rotate(lazer_img, self.speed_dir[face][1])
        self.rect = self.image.get_rect()
        self.rect.center = self.x, self.y
        self.speed = self.speed_dir[face][0]
        self.vec2d = Vec2d()

    def update(self):
        self.rect.center = self.vec2d.add(self.speed, self.rect.center)
        if self.rect.centerx > WIDTH or  self.rect.centerx  < 0 or self.rect.centery  < 0 or self.rect.centery  > HEIGHT:
            self.kill()


class Player(pygame.sprite.Sprite):

    bullet_position = {"LEFT":(-40,0), "RIGHT": (40,0),
                       "DOWN": (0,40), "UP": (0,-40)}

    def __init__(self):
         pygame.sprite.Sprite.__init__(self)
         self.orig_image = pygame.transform.scale(player_img, (39,30))
         self.image = self.orig_image
         self.image.set_colorkey(BLACK)
         self.rect = self.image.get_rect()
         self.rect.center = WIDTH/2, HEIGHT - self.rect.height
         self.radius = 13
         pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
         self.speed = 5
         self.face = "UP"
         self.speedxy = (0,0)
         self.vec2d = Vec2d()
         self.last_shoot = pygame.time.get_ticks()
         self.delay = 200
         self.degrees = 0
    
    def shoot(self, key_state):
        if key_state[pygame.K_SPACE]:
             tick = pygame.time.get_ticks()
             if tick - self.last_shoot > self.delay:
                 self.last_shoot = pygame.time.get_ticks()
                 pos = self.vec2d.add(self.rect.center, Player.bullet_position[self.face])
                 bullet = Bullet(pos, self.face)
                 all_sprites.add(bullet)
                 bullets_p1_sprites.add(bullet)

    def border(self):
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        elif self.rect.left  < 0:
            self.rect.left = 0
        elif self.rect.top  < 0:
            self.rect.top = 0
        elif self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            
    def update(self):
        self.speedxy = (0,0)
        key_state = pygame.key.get_pressed()
        if key_state[pygame.K_UP]:
             self.speedxy = self.vec2d.add(self.speedxy, (0, -self.speed))
             self.face = "UP"
             self.degrees = 0
        if key_state[pygame.K_DOWN]:
             self.speedxy = self.vec2d.add(self.speedxy, (0, self.speed))
             self.face = "DOWN"
             self.degrees = 180
        if key_state[pygame.K_LEFT]:
             self.speedxy = self.vec2d.add(self.speedxy, (-self.speed, 0))
             self.face = "LEFT"
             self.degrees = 90
        if key_state[pygame.K_RIGHT]:
             self.speedxy = self.vec2d.add(self.speedxy, (self.speed, 0))
             self.face = "RIGHT"
             self.degrees = 270
        self.image = pygame.transform.rotate(self.orig_image, self.degrees)
        self.shoot(key_state)
        self.rect.center = self.vec2d.add(self.speedxy, self.rect.center)
        self.border()
             
class Player2(pygame.sprite.Sprite):

    bullet_position = {"LEFT":(-40,0), "RIGHT": (40,0),
                       "DOWN": (0,40), "UP": (0,-40)}

    def __init__(self):
         pygame.sprite.Sprite.__init__(self)
         self.orig_image = pygame.transform.scale(player_img2 , (39,30))
         self.image = self.orig_image
         self.image.set_colorkey(BLACK)
         self.rect = self.image.get_rect()
         self.rect.center = WIDTH/2, HEIGHT - self.rect.height
         self.radius = 13
         self.speed = 5
         self.face = "UP"
         self.speedxy = (0,0)
         self.vec2d = Vec2d()
         self.last_shoot = pygame.time.get_ticks()
         self.delay = 200
         self.degrees = 0
    
    def shoot(self, key_state):
        if key_state[pygame.K_q]:
             tick = pygame.time.get_ticks()
             if tick - self.last_shoot > self.delay:
                 self.last_shoot = pygame.time.get_ticks()
                 pos = self.vec2d.add(self.rect.center, Player.bullet_position[self.face])
                 bullet = Bullet(pos, self.face)
                 all_sprites.add(bullet)
                 bullets_p2_sprites.add(bullet)

    def border(self):
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        elif self.rect.left  < 0:
            self.rect.left = 0
        elif self.rect.top  < 0:
            self.rect.top = 0
        elif self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            
    def update(self):
        self.speedxy = (0,0)
        key_state = pygame.key.get_pressed()
        if key_state[pygame.K_w]:
             self.speedxy = self.vec2d.add(self.speedxy, (0, -self.speed))
             self.face = "UP"
             self.degrees = 0
        if key_state[pygame.K_s]:
             self.speedxy = self.vec2d.add(self.speedxy, (0, self.speed))
             self.face = "DOWN"
             self.degrees = 180
        if key_state[pygame.K_a]:
             self.speedxy = self.vec2d.add(self.speedxy, (-self.speed, 0))
             self.face = "LEFT"
             self.degrees = 90
        if key_state[pygame.K_d]:
             self.speedxy = self.vec2d.add(self.speedxy, (self.speed, 0))
             self.face = "RIGHT"
             self.degrees = 270
        self.image = pygame.transform.rotate(self.orig_image, self.degrees)
        self.shoot(key_state)
        self.rect.center = self.vec2d.add(self.speedxy, self.rect.center)
        self.border()

#declare_sprite_group
all_sprites = pygame.sprite.Group()
bullets_p1_sprites = pygame.sprite.Group()
bullets_p2_sprites = pygame.sprite.Group()
meteor_sprites = pygame.sprite.Group() 
#declare_classes
player = Player()
player2 = Player2()

for i in range(4):
    spawnmob()
#add_to_sprite Group
all_sprites.add(player)
all_sprites.add(player2)
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
    #__check for collision p1__#
    #### bullet:meteor ####
    hits = pygame.sprite.groupcollide(bullets_p1_sprites, meteor_sprites, True, True)
    for hit in hits:
        spawnmob()
        spawnexpl("med", hit.rect.topleft)
        
    #### player:meteor ####
    hits = pygame.sprite.spritecollide(player, meteor_sprites, True, pygame.sprite.collide_circle)
    for hit in hits:
        damage_to_p1 += damage
        spawnmob()
        spawnexpl("small", hit.rect.center)
        if damage_to_p1 >= 100:
            running = False
    ### player:bullets ###
    hits = pygame.sprite.spritecollide(player, bullets_p2_sprites, True)
    for hit in hits:    
        damage_to_p1 += damage
        spawnexpl("small", hit.rect.center)
        if damage_to_p1 >= 100:
            running = False

    #__check for collision between bullets__#
    hits = pygame.sprite.groupcollide(bullets_p1_sprites, bullets_p2_sprites, True, True)
    for hit in hits:
        spawnexpl("med", hit.rect.center)
            
    #__check for collision p2__#
    #### bullet:meteor ####
    hits = pygame.sprite.groupcollide(bullets_p2_sprites, meteor_sprites, True, True)
    for hit in hits:
        spawnmob()  
        spawnexpl("med", hit.rect.topleft)
        
    #### player:meteor ####
    hits = pygame.sprite.spritecollide(player2, meteor_sprites, True, pygame.sprite.collide_circle)
    for hit in hits:
        damage_to_p2 += damage
        spawnmob()
        spawnexpl("small", hit.rect.center)
        if damage_to_p2 >= 100:
            running = False
            
    ### player:bullets ###
    hits = pygame.sprite.spritecollide(player2, bullets_p1_sprites, True)
    for hit in hits:
        damage_to_p2 += damage
        spawnexpl("small", hit.rect.center)
        if damage_to_p2 >= 100:
            running = False
 
    
    # Update
    all_sprites.update()

    # Draw / render
    screen.blit(background, (0,0))
    all_sprites.draw(screen)
    #__player1_draw__#
    draw_bar(screen, 50, 20, damage_to_p1)
     #__player1_draw__#
    draw_bar(screen, WIDTH - 150, 20, damage_to_p2)
    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()
