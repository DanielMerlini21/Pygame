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

#print(11//5)
#print((1,2)[0])
"""
#a = [2, 3, 4]


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

a = []
a[0]
if a[0] < 1 < a[-1]:
    print("WHAT")