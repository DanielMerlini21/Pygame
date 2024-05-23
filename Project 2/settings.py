TITLE = "Jumpy!"
WIDTH =480
HEIGHT = 600
FPS = 60
FONT_NAME = "arial"
HS_FILE = "highscore.txt"

#player property
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
PLAYER_GRAVITY = 0.5
PLAYER_JUMP = 20
SPRITESHEET = "spritesheet_jumper.png"

# Game properties
BOOST_POWER = 60
POW_SPAWN_PCT = 7
MOB_FREQ = 5000
PLAYER_LAYER = 2
PLATFORM_LAYER = 1
POW_LAYER = 1
MOB_LAYER = 2

# starting platforms
PLATFORM_LIST = [(0, HEIGHT - 60),
                 (WIDTH / 2 - 50, HEIGHT * 3 /5),
                 (125, HEIGHT - 350),
                 (350, 200),
                 (175, 100)]

#define clours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED =(255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BGCOLOR = (127, 255, 212)


