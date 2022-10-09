#  use a bitboard as the board
#  https://towardsdatascience.com/dissecting-stockfish-part-1-in-depth-look-at-a-chess-engine-7fddd1d83579

# imports the modules
import random

import pygame
import os
import copy
from itertools import product

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
TILE_SIZE = 100
COLOR_KEY = RED

# screen - constants:
WIDTH = 800
HEIGHT = 800
FPS = 60
WIDTH_IN_TILES = int(WIDTH / TILE_SIZE)
HEIGHT_IN_TILES = int(HEIGHT / TILE_SIZE)
BOARD_POS = (0, 0)

# pieces and values
values = {"King": 900, "Queen": 9, "Rook": 5, "Bishop": 3, "Knight": 3, "Pawn": 1}

# variables
white_move = "W"
board_pieces_names = [["BRook", "BKnight", "BBishop", "BQueen", "BKing", "BBishop", "BKnight", "BRook"],
                      ["BPawn", "BPawn", "BPawn", "BPawn", "BPawn", "BPawn", "BPawn", "BPawn"],
                      [" ", " ", " ", " ", " ", " ", " ", " "],
                      [" ", " ", " ", " ", " ", " ", " ", " "],
                      [" ", " ", " ", " ", " ", " ", " ", " "],
                      [" ", " ", " ", " ", " ", " ", " ", " "],
                      ["WPawn", "WPawn", "WPawn", "WPawn", "WPawn", "WPawn", "WPawn", "WPawn"],
                      ["WRook", "WKnight", "WBishop", "WQueen", "WKing", "WBishop", "WKnight", "WRook"]]

# initialises screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))


# Functions
def tiles_to_pixels(tiles_cor, offset=(0, 0)):  # gets the coordinates of tiles into pixels
    offset_x, offset_y = offset  # tuple unpacking offset into x and y
    row, collum = tiles_cor  # tuple unpacking tiles into row and collum
    center = (offset_x + row * TILE_SIZE + TILE_SIZE / 2,
              offset_y + collum * TILE_SIZE + TILE_SIZE / 2)  # times them so you get the center of the tile
    return center  # returns center so it can be used


def all_possible_moves(board, board1, color):
    all_cor = []
    all_cap = []
    for row in board:
        for piece in row:
            if piece != " ":
                if piece.NAME[0] == color:
                    cor, cap = where_piece_can_move(piece, piece.pos, board1)  # need to be able to use board class
                    all_cor = all_cor + cor
                    all_cap = all_cap + cap

    # for cor in all_cor:
    #    tile = board1[cor[1]][cor[0]]
    #    if tile != " ":
    #        all_cor[all_cor.index(cor)] == [cor[0], cor[1], board1[cor[1]][cor[0]]]
    return all_cor


def all_color_pieces(color, board):
    same_color_pieces = []
    row_counter = 0
    tile_counter = 0
    for row in board:
        for tile in row:
            if tile != " ":
                if tile.NAME[0] == color:
                    same_color_pieces.append([tile, [tile_counter, row_counter]])
            tile_counter = tile_counter % (WIDTH_IN_TILES - 1)
            tile_counter += 1
        row_counter += 1
    return same_color_pieces


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


def move_diagonal(lis, start_x, start_y, index_x, direction="right to left", index=0):
    free_spaces = []
    free_spaces_real = []
    captured = []
    can_take = True
    for tile in lis:
        if direction == "left to right":
            x = start_x + index
            y = start_y + index
        if direction == "right to left":
            x = start_x - index
            y = start_y + index
            free_spaces_real.append([x, y])
        if tile == " ":
            free_spaces_real.append([x, y])
            free_spaces.append([index, start_y])
        else:
            try:
                if free_spaces[0][0] <= index_x <= free_spaces[-1][0]:
                    if white_move == tile[0]:
                        captured.append([x, y])
                        break
                else:
                    raise IndexError
            except IndexError:
                free_spaces_real = []
                free_spaces = []  # set again if piece not inside
                captured = []
                can_take = True
            print(f"white mooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooove {white_move}")
            if can_take and white_move == tile[0]:
                captured.append([x, y])
                can_take = False
        index += 1
    if [index_x, start_y] in free_spaces or len(free_spaces_real) == 0:
        free_spaces_real = free_spaces_real + captured
        return free_spaces_real, captured


def move_vertical_horizontal(lis, x, y, direction="horizontal", index=0):
    free_spaces = []  # create list
    captured = []
    can_take = True
    for tile in lis:  # loops through
        # print(f"tile {tile } lis {lis} index {index} x,y{x,y}")
        if tile == " ":  # if empty add x and y
            free_spaces.append([index, y])
        else:  # if piece and not empty
            try:
                if free_spaces[0][0] <= x <= free_spaces[-1][0]:  # check if its inside
                    if white_move == tile[0]:
                        captured.append([index, y])
                    break
                else:
                    raise IndexError
            except IndexError:
                captured = []
                free_spaces = []  # set again if piece not inside
                can_take = True
            if can_take and white_move == tile[0]:
                captured.append([index, y])
                can_take = False
        index += 1  # add 1 to index
    free_spaces = free_spaces + captured
    #  free_spaces.insert(0, [free_spaces[0][0] - 1, free_spaces[0][1]])
    #  free_spaces.append([free_spaces[-1][0] + 1, free_spaces[-1][1]])
    if not free_spaces:
        return free_spaces
    if [x, y] in free_spaces:  # check if value in free spaces
        if direction == "vertical":  # flip
            free2 = []
            for cor in free_spaces:
                cor = cor[::-1]
                free2.append(cor)
            free_spaces = free2
        start = len(free_spaces) - len(captured)
        return free_spaces, free_spaces[start::]  # return


def where_piece_can_move(piece, pos, board):
    collum = []
    row = board[pos[1]]
    diagonal = []
    diagonal1 = []
    index_x = 0
    index_x1 = 0
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
    # create diagonal
    start_y1 = pos[1] - pos[0]
    if start_y1 < 0:
        start_y1 = 0
    start_x1 = pos[0] - pos[1]
    if start_x1 < 0:
        start_x1 = 0
    start_x_copy1 = start_x1
    counter1 = 0
    for y in range(start_y1, 100):
        try:
            diagonal1.append(board[y][start_x1])
            if start_x1 == pos[0]:
                index_x1 = counter1
            start_x1 += 1
            counter1 += 1
            if start_x1 > 7:
                break
        except IndexError:
            break
    if piece.NAME[1::] == "Rook":
        y, cap = move_vertical_horizontal(row, pos[0], pos[1])
        x, cap1 = move_vertical_horizontal(collum, pos[1], pos[0], "vertical")
        return x + y, cap + cap1
    elif piece.NAME[1::] == "Queen":
        # move up and down and diagonal
        y, cap = move_vertical_horizontal(row, pos[0], pos[1])
        x, cap1 = move_vertical_horizontal(collum, pos[1], pos[0], "vertical")
        d1, cap2 = move_diagonal(diagonal, start_x_copy, start_y, index_x)
        d2, cap3 = move_diagonal(diagonal1, start_x_copy1, start_y1, index_x1, "left to right")
        return x + y + d1 + d2, cap + cap1 + cap2 + cap3
    elif piece.NAME[1::] == "King":
        row = row[max(0, pos[0] - 1):min(7, pos[0] + 2)]
        collum = collum[max(0, pos[1] - 1):min(8, pos[1] + 2)]
        diagonal = diagonal[max(0, index_x - 1):min(7, index_x + 2)]
        diagonal1 = diagonal1[(max(0, index_x1 - 1)):min(7, index_x1 + 2)]
        # move up and down
        y, cap = move_vertical_horizontal(row, pos[0], pos[1], "horizontal",
                                          max(0, pos[0] - 1))  # starts at the minus pos
        x, cap1 = move_vertical_horizontal(collum, pos[1], pos[0], "vertical",
                                           max(0, pos[1] - 1))  # starts at the minus pos
        # move diagonal
        d1, cap3 = move_diagonal(diagonal, start_x_copy, start_y, index_x, "right to left", max(0, index_x - 1))
        d2, cap4 = move_diagonal(diagonal1, start_x_copy1, start_y1, index_x1, "left to right", max(0, index_x1 - 1))
        return d1 + d2 + x + y, cap + cap1 + cap3 + cap4

    elif piece.NAME[1::] == "Bishop":
        # move diagonal
        d1, cap1 = move_diagonal(diagonal, start_x_copy, start_y, index_x)
        d2, cap2 = move_diagonal(diagonal1, start_x_copy1, start_y1, index_x1, "left to right")
        return d1 + d2, cap1 + cap2
    elif piece.NAME == "WPawn":
        # move up and down
        if pos[1] >= 6:
            collum = collum[pos[1] - 2:pos[1] + 1]  # go a bit back so add 1
            offset = 2
        else:
            collum = collum[pos[1] - 1:pos[1] + 1]  # go a bit back
            offset = 1
        # set diagonal
        diagonal = diagonal[max(0, index_x - 1):index_x + 1]
        diagonal1 = diagonal1[max(0, index_x1 - 1):index_x1 + 1]
        x, cap = move_vertical_horizontal(collum, pos[1], pos[0], "vertical", pos[1] - offset)  # starts back
        d1, cap2 = move_diagonal(diagonal, start_x_copy, start_y, index_x, "right to left", max(0, index_x - 1))
        d2, cap3 = move_diagonal(diagonal1, start_x_copy1, start_y1, index_x1, "left to right", max(0, index_x1 - 1))
        return x + cap2 + cap3, cap2 + cap3
    elif piece.NAME == "BPawn":
        # move up and down
        if pos[1] <= 1:
            collum = collum[pos[1]:pos[1] + 3]  # go a forwards
        else:
            collum = collum[pos[1]:pos[1] + 2]  # go a forwards
        # set diagonal
        diagonal = diagonal[index_x:index_x + 2]
        diagonal1 = diagonal1[index_x1:index_x1 + 2]
        x, cap = move_vertical_horizontal(collum, pos[1], pos[0], "vertical", pos[1])  # starts back
        d1, cap2 = move_diagonal(diagonal, start_x_copy, start_y, index_x, "right to left", index_x)
        d2, cap3 = move_diagonal(diagonal1, start_x_copy1, start_y1, index_x1, "left to right", index_x1)
        return x + cap2 + cap3, cap2 + cap3
    elif piece.NAME[1::] == "Knight":
        # knight all positions
        x, y = pos
        li = []
        capture = []
        moves = list(product([x - 1, x + 1], [y - 2, y + 2])) + list(product([x - 2, x + 2], [y - 1, y + 1]))
        for x, y in moves:
            if 0 <= x < 8 and 0 <= y < 8:
                li.append([x, y])

        for tile in li:
            pie = board[tile[1]][tile[0]]
            if pie != " ":
                if pie[0] == white_move:
                    capture.append(tile)
                else:
                    li.remove(tile)
        return li, capture


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
        self.pos = None
        try:
            self.value = values[name[1::]]
        except KeyError:
            self.value = 0

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
    global white_move
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
    coordinate_captured = []
    evalutation = 0

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
                flag = True
                for cor in coordinate_captured:
                    if coordinate == cor:
                        pygame.draw.circle(screen, GRAY, tiles_to_pixels((cor[0], cor[1])), TILE_SIZE / 2,
                                           int(TILE_SIZE / 10))
                        flag = False
                if flag:
                    pygame.draw.circle(screen, GRAY, tiles_to_pixels((coordinate[0], coordinate[1])), TILE_SIZE / 8)

            # draw yellow square
            selected_piece.rect.center = pygame.mouse.get_pos()
            screen.blit(selected_piece.image, (selected_piece.rect.left, selected_piece.rect.top))

        # keep running at the at the right speed
        clock.tick(FPS)
        # process input (events)
        # print(white_move)
        if white_move == "W":
            for event in pygame.event.get():
                # check for closing the window
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    selected_piece = board_pieces_class[y][x]
                    if piece != " " and hold is False and selected_piece.NAME[0] == white_move:
                        hold = True
                        old_x = x
                        old_y = y
                        board_pieces_names[y][x] = " "
                        coordinates, coordinate_captured = where_piece_can_move(selected_piece, (old_x, old_y)
                                                                                , board_pieces_names)
                        try:
                            coordinates.remove([old_x, old_y])
                        except ValueError:
                            print("Knight")
                if event.type == pygame.MOUSEBUTTONUP:
                    if hold is True:
                        if [x, y] in coordinates:
                            if white_move == "W":
                                white_move = "B"
                            board_pieces_names[y][x] = selected_piece.NAME
                            new_x = x
                            new_y = y
                            hold = False
                        else:
                            hold = False
                            board_pieces_names[old_y][old_x] = selected_piece.NAME
                            new_x = old_x
                            new_y = old_y
        if white_move == "B":  # board, board1, color
            # cor = all_possible_moves(board_pieces_class, board_pieces_names, white_move)
            # move = random.randrange(0, len(cor))
            all_pieces_same_color = all_color_pieces(white_move, board_pieces_class)
            pie = random.choice(all_pieces_same_color)
            print(f" x, y{pie[1][0], pie[1][1]}")
            board_pieces_names[pie[1][1]][pie[1][0]] = " "
            coordinates_bot, coordinate_captured_bot = where_piece_can_move(pie[0], (pie[1][0], pie[1][1])
                                                                    , board_pieces_names)
            try:\
                coordinates_bot.remove([pie[1][0], pie[1][1]])
            except ValueError:
                print("Knight")
            print(f"coordinates_bot {coordinates_bot} captured {coordinate_captured_bot}")
            coordinates_bot = [x for x in coordinates_bot if x not in coordinate_captured_bot]
            print(f"coordinates_bot {coordinates_bot}")
            move = random.choice(coordinates_bot)
            board_pieces_names[move[1]][move[0]] = pie[0].NAME
            white_move = "W"
        # updating
        pygame.display.update()


# check meaning
if __name__ == "__main__":
    main()
