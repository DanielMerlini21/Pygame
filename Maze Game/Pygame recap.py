import pygame
pygame.init()
WIDTH = 500
HEIGHT = 500
WHITE = (255,255,255)
BLACK = (0,0,0)
screen = pygame.display.set_mode((WIDTH, HEIGHT))

a = {(1, 2) :(2, 3)}
print(a[(1,2)])
print(["dam", "son"].pop())


# build the grid
def build_grid(x, y, w): # 40, 0, 20                                                        # start a new row
        pygame.draw.line(screen, WHITE, [x, y], [x + w, y])           # top of cell
        pygame.draw.line(screen, WHITE, [x + w, y], [x + w, y + w])   # right of cell
        pygame.draw.line(screen, WHITE, [x + w, y + w], [x, y + w])   # bottom of cell
        pygame.draw.line(screen, WHITE, [x, y + w], [x, y])           # left of cell                                         # add cell to grid list


running = True
build_grid(20,20,20)
pygame.draw.rect(screen, (22,22,255), (21,21,19,19))
pygame.display.update()


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


pygame.display.flip()
pygame.quit()


for i in range(1,10):
    print(i)