piece_positions = ["R", "N", "B", "Q", "K", "B", "B", "B",
                  "P", "P", "P", "P", "P", "P", "P", "P",
                  " ", " ", " ", " ", " ", " ", " ", " ",
                  " ", " ", " ", " ", " ", " ", " ", " ",
                  " ", " ", " ", " ", " ", " ", " ", " ",
                  " ", " ", " ", " ", " ", " ", " ", " ",
                  "p", "p", "p", "p", "p", "p", "p", "p",
                  "r", "n", "b", "q", "k", "b", "n", "r"]

king_binaryshift = [9, 8, 7, 1, -9, -8, -7, -1]

def bitboards(chess_board, piece_name):
    # creates bitboards required
    # binary 1 2 4 8 16 32 64... (2)^n
    # this makes it efficient because word sizes are 64 bit in 64 bit cpu wiki
    a, w, b, p = (0,) * 4 # create bit board variables
    bitboards = {} # store all bitboards
    for index, tile in enumerate(chess_board):
        if tile != " ":
            a += 2**(index) # getting binary value
            if tile == piece_name:
                p += 2**(index)
            if tile.islower() == True:
                b += 2**(index)
            else:
                w += 2**(index)
    
    # adding to dictionary
    bitboards["all pieces"] = a
    bitboards["white pieces"] = b
    bitboards["black pieces"] = w
    bitboards[str(piece_name)] = p
    return bitboards

def print_bitboard(bitboard):
    board = '{:064b}'.format(bitboard) # :064b used to remove b0
    board = str(board).zfill(64)
    for i in range(7, -1, -1): # goes opposite little endian encoding (smaller to larger)
        print(board[8*i+7] + " " + board[8*i+6] + " " + board[8*i+5] + " " + 
              board[8*i+4] + " " + board[8*i+3] + " " + board[8*i+2] + " " + 
              board[8*i+1] + " " + board[8*i+0])

def where_piece_can_move(chess_board, piece_name):
    # check where piece can move
    bitboards_dict = bitboards(chess_board, piece_name) # returns all the bitboards required
    print_bitboard(bitboards_dict["k"])
    # goes through each piece
    if piece_name == "k":
        # binary shift : **2 moves right **1/2 moves left 1 space
        # rose compass
        for shift in king_binaryshift:
                            
where_piece_can_move(piece_positions, "k")
            
