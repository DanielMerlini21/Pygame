import random

import pygame

"""
x = [ 'w', 'e', 's', 's', 's', 'z','z', 's']
print([i for i, n in enumerate(x) if n == 's'][0])

for i,n in enumerate(x):
    if n == "s":
        print(i)
        
"""

"""
BOARD_POS = (10, 10)
board = []

def get_square_under_mouse(board):
    mouse_pos = pygame.Vector2(pygame.mouse.get_pos()) - BOARD_POS
    x, y = [int(v // TILESIZE) for v in mouse_pos]
    try: 
        if x >= 0 and y >= 0: return (board[y][x], x, y)
    except IndexError: pass
    return None, None, None
    
if x != None:
    rect = (BOARD_POS[0] + x * TILESIZE, BOARD_POS[1] + y * TILESIZE, TILESIZE, TILESIZE)
    pygame.draw.rect(screen, (255, 0, 0, 50), rect, 2)
"""
"""
from itertools import product

print(product())

def knight_moves(position):
    x, y = position
    li = []
    moves = list(product([x-1, x+1],[y-2, y+2])) + list(product([x-2,x+2],[y-1,y+1]))
    print(f"a {x-1, x+1} b {y-2, y + 2} a1 {x - 2 , x + 2} b1 {y - 1, y + 1}")
    print(f"product1 {list(product([x-1, x+1],[y-2, y+2]))} product2 {list(product([x-2,x+2],[y-1,y+1]))}")
    for x, y in moves:
        if 0 <= x < 8 and 0 <= y < 8:
            li.append([x, y])
    return li

print(knight_moves((2, 2)))
#print(11//5)
#print((1,2)[0])
"""
"""
a = [2, 3, 4]


def func(t):
    t1 = t.copy()
    t1.append(4)
    return t1

s = func(a)

print(s, a)

a = "Bking"
print(a[1::])
"""

#l = [1,2,3,4,5,6,7,8,9]

#print(l[::-1])

#print([1,2] + [2,3])

#a = [1, 2, 3,2 ,4 ,5 ,6 ,7 ,8]
#print(a[2:4])

#a = [" ", " "]
#b = [" ", " "]

#for i in range(5, -10, -1):
#    print(i)

#print(len(["1", "2"]))


"""
    start_y1 = pos[1] - pos[0]
    if start_y1 < 0:
        start_y1 = 0
    start_x1 = pos[0] - pos[1]
    if start_x1 < 0:
        start_x1 = 0
    start_x1_copy = start_x1
    counter1 = 0
    for y in range(start_y1, 100):
        try:
            print(f"y1 : {y} ")
            diagonal1.append(board[y][start_x1])
            if start_x == pos[0]:
                index_x1 = counter
            start_x1 += 1
            counter1 += 1
            if start_x1 > 7:
                break
        except IndexError:
            break
"""
#a = []
#for x in a:
#    print("whats up")
"""
a = []
a[0]
if a[0] < 1 < a[-1]:
    print("WHAT")
"""

#a = []
#b = [[4, 6]]
#d = b
#c = d
#print(c)
#a,b = c
#
#x = [[1,2], [2,3], [3,4]]
#d = [[1,2],[2,3]]#
#y = x + d
#print(y)

#li = [1, 2, 3, 4]
#li[0] = "YES"

#print(li)

#print(random.choice(li))
print(5%7)

