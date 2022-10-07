# imports the modules

import pygame
import os
import copy

# game settings

# colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (48, 148, 13)
BEIGE = (211, 237, 172)
GRAY = (150, 150, 150)
RED = (255, 0, 0)
YELLOW = (235, 235, 80)

# constants
BOARD_POS = (0, 0)
TILE_SIZE = 50
COLOR_KEY = RED

# screen - constants:
WIDTH = 800
HEIGHT = 800
FPS = 60
WIDTH_IN_TILES = int(WIDTH / TILE_SIZE)
HEIGHT_IN_TILES = int(HEIGHT / TILE_SIZE)

# variables
board_pieces_names = [["BRook", "BKnight", "BBishop", "BQueen", "BKing", "BBishop", "BKnight", "BRook"],
                      ["BPawn", "BPawn", "BPawn", "BPawn", "BPawn", "BPawn", "BPawn", "BPawn"],
                      [" ", " ", " ", " ", " ", " ", " ", " "],
                      ["BRook", " ", "BRook", " ", "BRook", " ", " ", " "],
                      [" ", " ", " ", "BKing", "WBishop", " ", " ", " "],
                      [" ", " ", " ", " ", " ", " ", " ", " "],
                      ["WPawn", "WPawn", "WPawn", "WPawn", "WPawn", "WPawn", "WPawn", "WPawn"],
                      ["WRook", "WKnight", "WBishop", "WQueen", "WKing", "WBishop", "WKnight", "WPawn"]]

# initialises screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))


# Functions
def tiles_to_pixels(tiles_cor, offset=(0, 0)):  # gets the coordinates of tiles into pixels
    offset_x, offset_y = offset  # tuple unpacking offset into x and y
    row, collum = tiles_cor  # tuple unpacking tiles into row and collum
    center = (offset_x + row * TILE_SIZE + TILE_SIZE / 2,
              offset_y + collum * TILE_SIZE + TILE_SIZE / 2)  # times them so you get the center of the tile
    return center  # returns center so it can be used


def get_square_under_mouse(board):  # used to get square under mouse
    mouse_pos = pygame.Vector2(pygame.mouse.get_pos()) - pygame.Vector2(BOARD_POS)  # minus offset
    v, v1 = mouse_pos  # gets mouse position
    x = int(v // TILE_SIZE)  # finds how much it goes into TILE_SIZE and returns value for x
    y = int(v1 // TILE_SIZE)  # for y instead
    try:  # see if coordinates are too big
        if x >= 0 and y >= 0:  # make sure its positive because minus values would ruins things
            return board[y][x], x, y
    except IndexError:  # if too big then return None
        return None, None, None


def move_diagonal(lis, x, y, end_x):
    free_spaces = []
    free_spaces_real = []
    index = 0
    for tile in lis:
        if tile == " ":
            free_spaces_real.append([end_x - index, y + index])
            free_spaces.append([index, y])
        elif free_spaces:
            if free_spaces[0][0] <= x <= free_spaces[-1][0]:
                break
            else:
                free_spaces = []
                free_spaces_real = []
        index += 1
    if [x, y] in free_spaces:
        return free_spaces_real


def move_vertical_horizontal(lis, x, y, direction="horizontal", index=0):
    free_spaces = []  # create list
    print(lis)
    for tile in lis:  # loops through
        print(tile)
        if tile == " ":  # if empty add x and y
            free_spaces.append([index, y])
            print(free_spaces)
        elif free_spaces:  # if piece and not empty
            if free_spaces[0][0] <= x <= free_spaces[-1][0]:  # check if its inside
                break
            else:
                free_spaces = [] # set again if piece not inside
        index += 1  # add 1 to index
    print(f"free spaces {free_spaces}")
    if not free_spaces:
        return free_spaces
    if [x, y] in free_spaces:  # check if value in free spaces
        if direction == "vertical":  # flip
            free2 = []
            for cor in free_spaces:
                cor = cor[::-1]
                free2.append(cor)
            free_spaces = free2
        return free_spaces  # return


def where_piece_can_move(piece, pos, board):
    collum = []
    row = board[pos[1]]
    diagonal = []
    index_x = 0
    # create collum
    for y in range(0, 8):
        collum.append(board[y][pos[0]])
    # create diagonals
    start_y = pos[1] - (abs(pos[0] - 7))
    if start_y < 0:
        start_y = 0
    start_x = pos[0] + (abs(start_y - pos[1]))
    start_x_copy = start_x
    counter = 0
    for y in range(start_y, 100):
        try:
            diagonal.append(board[y][start_x])
            if start_x == pos[0]:
                index_x = counter
            start_x -= 1
            counter += 1
            if start_x < 0:
                break
        except IndexError:
            break

    if piece.NAME[1::] == "Rook":
        y = move_vertical_horizontal(row, pos[0], pos[1])
        x = move_vertical_horizontal(collum, pos[1], pos[0], "vertical")
        return x + y
    elif piece.NAME[1::] == "Queen":
        y = move_vertical_horizontal(row, pos[0], pos[1])
        x = move_vertical_horizontal(collum, pos[1], pos[0], "vertical")
        return x + y
    elif piece.NAME[1::] == "King":
        row = row[(pos[0] - 1):(pos[0] + 2)]
        collum = collum[(pos[1] - 1):(pos[1] + 2)]
        y = move_vertical_horizontal(row, pos[0], pos[1], "horizontal", pos[0] - 1)  # starts at the minus pos
        x = move_vertical_horizontal(collum, pos[1], pos[0], "vertical", pos[1] - 1)  # starts at the minus pos
        return x + y
    elif piece.NAME[1::] == "Bishop":
        d = move_diagonal(diagonal, index_x, start_y, start_x_copy)
        return d
    elif piece.NAME == "WPawn":
        # print(f"orig collum {collum} start {pos[1] - 2} end {pos[1]}")
        if pos[1] >= 6:
            collum = collum[pos[1] - 2:pos[1] + 1]  # go a bit back so add 1
            offset = 2
        else:
            collum = collum[pos[1] - 1:pos[1] + 1]  # go a bit back
            offset = 1
        x = move_vertical_horizontal(collum, pos[1], pos[0], "vertical", pos[1] - offset)  # starts back
        print(f"free spaces {x}")
        return x


# Classes
class SpriteSheet:  # cuts up sprite sheet and saves them
    def __init__(self):
        # assigns variables for cutting sprite sheet
        self.PADDING_X = 80
        self.PADDING_Y = 55
        self.MARGIN_X = 65
        self.MARGIN_Y = 72
        self.WIDTH = (1052 - (self.PADDING_X * 5 + self.MARGIN_X * 2)) / 6
        self.HEIGHT = (375 - (self.PADDING_Y + self.MARGIN_Y * 2)) / 2
        self.COLOR_KEY = COLOR_KEY
        self.sprite_sheet = "None"
        self.piece = Piece

    def load_images(self):
        # loads images
        x1 = self.MARGIN_X
        y1 = self.MARGIN_Y
        pieces_names = ["BKing", "BQueen", "BRook", "BBishop", "BKnight", "BPawn",
                        "WKing", "WQueen", "WRook", "WBishop", "WKnight", "WPawn"]
        pieces1 = []
        directory = os.getcwd()
        file_path = os.path.join(directory, "images", "chess pieces.png")
        done = "Null"
        self.sprite_sheet = pygame.image.load(file_path)
        for i in range(1, 13):
            image = pygame.Surface((self.WIDTH, self.HEIGHT)).convert_alpha()
            if i // 7 == 1:
                if done == "Null":
                    y1 += self.PADDING_Y + self.HEIGHT
                    x1 = self.MARGIN_X
                    done = True
            image.blit(self.sprite_sheet, (0, 0), (x1, y1, self.WIDTH, self.HEIGHT))
            image = pygame.transform.scale(image, (self.WIDTH * (TILE_SIZE / 100), self.HEIGHT * (TILE_SIZE / 100)))
            pieces1.append(self.piece(image, pieces_names[i - 1]))
            image.set_colorkey(self.COLOR_KEY)
            x1 += self.PADDING_X + self.WIDTH
        return pieces1


class Piece:  # Pieces class has attributes
    def __init__(self, image, name):
        self.image = image
        self.rect = image.get_rect()
        self.NAME = name
        self.x = 0
        self.y = 0
        self.id = 0
        self.pos = None

    def in_hit_box(self, x1, y1):
        pygame.draw.rect(screen, RED, (self.rect.left, self.rect.top, self.rect.width, self.rect.height))
        if self.rect.left < x1 < self.rect.right and self.rect.top < y1 < self.rect.bottom:
            return True

    def update(self):
        screen.blit(self.image, (self.rect.left, self.rect.top))


class ChessBoard:  # Class in control board
    def __init__(self):
        self.WIDTH_IN_TILES = int(WIDTH / TILE_SIZE)
        self.HEIGHT_IN_TILES = int(HEIGHT / TILE_SIZE)
        self.SIZE_OF_TILES = TILE_SIZE
        self.HEIGHT = self.HEIGHT_IN_TILES * self.SIZE_OF_TILES
        self.WIDTH = self.WIDTH_IN_TILES * self.SIZE_OF_TILES
        self.pos_x, self.pos_y = BOARD_POS
        self.piece = Piece

    def coordinates_of_tile(self, row1, collum):
        pos_x = self.pos_x + (row1 * self.SIZE_OF_TILES)
        pos_y = self.pos_y + (collum * self.SIZE_OF_TILES)
        return pos_x, pos_y

    def create_board(self):
        x1 = 0
        y1 = 0
        dark = False
        board_surf = pygame.Surface((self.WIDTH, self.HEIGHT))
        for tile_y in range(0, self.HEIGHT_IN_TILES):  # displaying board
            for tile_x in range(0, self.WIDTH_IN_TILES):
                pygame.draw.rect(board_surf, (GREEN if dark else BEIGE), (
                    x1 + (self.SIZE_OF_TILES * tile_x),
                    y1 + (self.SIZE_OF_TILES * tile_y),
                    self.SIZE_OF_TILES, self.SIZE_OF_TILES))
                dark = not dark
            dark = not dark
        return board_surf

    def update_board(self, board1, pieces1, screen1):
        offset_x, offset_y = BOARD_POS
        copy_board1 = copy.deepcopy(board1)
        for row1 in copy_board1:
            for entity in row1:
                for piece1 in pieces1:
                    if piece1.NAME == entity:
                        collum = row1.index(entity)
                        row2 = copy_board1.index(row1)
                        object_piece = self.piece(piece1.image, piece1.NAME)
                        object_piece.rect.center = (offset_x + collum * self.SIZE_OF_TILES + self.SIZE_OF_TILES / 2,
                                                    offset_y + row2 * self.SIZE_OF_TILES + self.SIZE_OF_TILES / 2)
                        screen1.blit(object_piece.image, object_piece.rect.topleft)
                        copy_board1[row2][collum] = object_piece
        return copy_board1


def main():  # main loop game
    # initialising pygame
    pygame.init()
    clock = pygame.time.Clock()
    # assigning variables
    running = True
    hold = False
    new_x = 100
    new_y = -100
    old_x = 0
    old_y = 0
    coordinates = [[0, 0]]

    # init classes
    chessboard = ChessBoard()
    sprite_sheet = SpriteSheet()
    selected_piece = Piece(pygame.Surface((0, 0)), "Start")

    # use methods
    pieces_list = sprite_sheet.load_images()
    board_surf = chessboard.create_board()
    # main loop
    while running:
        # Drawing
        piece, x, y = get_square_under_mouse(board_pieces_names)
        screen.blit(board_surf, BOARD_POS)

        if not hold:
            pygame.draw.rect(screen, YELLOW, (new_x * TILE_SIZE, new_y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

        board_pieces_class = chessboard.update_board(board_pieces_names, pieces_list, screen)

        if x is not None:
            rect = (BOARD_POS[0] + x * TILE_SIZE, BOARD_POS[1] + y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, WHITE, rect, 4)

        if hold:
            pygame.draw.rect(screen, YELLOW, (old_x * TILE_SIZE, old_y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            # draw dots
            for coordinate in coordinates:
                pygame.draw.circle(screen, GRAY, tiles_to_pixels((coordinate[0], coordinate[1])), TILE_SIZE / 8)
            # draw yellow square
            selected_piece.rect.center = pygame.mouse.get_pos()
            screen.blit(selected_piece.image, (selected_piece.rect.left, selected_piece.rect.top))

        # keep running at the at the right speed
        clock.tick(FPS)
        # process input (events)
        for event in pygame.event.get():
            # check for closing the window
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if piece != " " and hold is False:
                    hold = True
                    old_x = x
                    old_y = y
                    selected_piece = board_pieces_class[y][x]
                    board_pieces_names[y][x] = " "
                    coordinates = where_piece_can_move(selected_piece, (old_x, old_y), board_pieces_names)
            if event.type == pygame.MOUSEBUTTONUP:
                if hold is True:
                    board_pieces_names[y][x] = selected_piece.NAME
                    new_x = x
                    new_y = y
                    hold = False
        # updating
        pygame.display.update()


# check meaning
if __name__ == "__main__":
    main()
