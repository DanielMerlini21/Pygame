import pygame
import math

WIDTH = 800
HEIGHT = 800
FPS = 30

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)


class Chess:
    def __init__(self, width_in_tiles, height_in_tiles, size_of_tiles, pos_x=0, pos_y=0):
        self.width_in_tiles = width_in_tiles
        self.height_in_tiles = height_in_tiles
        self.size_of_tiles = size_of_tiles
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.hyp_of_tile = math.sqrt(size_of_tiles ** 2 + size_of_tiles ** 2)
        self.board = []

    def coordinates_of_tile(self, row, collum):
        pos_x = self.pos_x + (row * self.size_of_tiles)
        pos_y = self.pos_y + (collum * self.size_of_tiles)
        return pos_x, pos_y

    def create_board(self):
        x = 0
        y = 0
        counter = 0
        for tile_y in range(0, self.height_in_tiles):  # displaying board
            self.board.append([])
            counter += 1
            for tile_x in range(0, self.width_in_tiles):
                self.board[tile_y].append(" ")
                counter += 1
                if counter % 2 == 0:
                    pygame.draw.rect(screen, WHITE, (
                    x + (self.size_of_tiles * tile_x), y, self.size_of_tiles, self.size_of_tiles))
                else:
                    pygame.draw.rect(screen, BLACK, (
                    x + (self.size_of_tiles * tile_x), y, self.size_of_tiles, self.size_of_tiles))
            y += self.size_of_tiles
        pygame.display.update()
        return self.board

    def move_to(self, row, collum, image, piece):
        self.board[row][collum] = piece
    #    width, height = image.get_size()
        width = 40
        height = 50
        dist1 = (self.size_of_tiles - width)/2
        dist2 = (self.size_of_tiles - height)/2
        x = dist1
        y = dist2
        pygame.draw.rect(screen, RED, (x, y, width, height))
        pygame.display.update()



chess = Chess(8, 8, 100)
board = chess.create_board()
chess.move_to(0, 0, None, "rook")
print(chess.board)

running = True
while running:
    # keep running at the at the right speed
    clock.tick(FPS)
    # process input (events)
    for event in pygame.event.get():
        # check for closing the window
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
