import pygame
import os
import time
import sys
import random
from Pieces import *
# Load pygame
pygame.init()
pygame.mixer.init()

select_color = pygame.Color(255, 247, 37)
rook_loc = (0*15, 0, 15, 15)
knight_loc = (1*15, 0, 15, 15)
bishop_loc = (2*15, 0, 15, 15)
queen_loc = (3*15, 0, 15, 15)
king_loc = (4*15, 0, 15, 15)
pawn_loc = (5*15, 0, 15, 15)
# Classes
# Display
WIDTH = 640
HEIGHT = 640
wn = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("chess (whites turn)")  # Set the initial caption
running = True
wh_bl = 0
current_player = "white"  # Variable to track the current player's turn

music = ["snd/1.mp3","snd/2.mp3","snd/3.mp3"]

pathdir = os.path.dirname(os.path.abspath(__file__))

    
sheetblack = SpriteSheet("pieces_black_1.png")
sheetwhite = SpriteSheet("pieces_white_1.png")

class squares:
    fields = []

    def __init__(self, x, y, colorblack, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.piece = None
        if colorblack:
            self.color = pygame.Color(93, 50, 49)  # Color for black squares
        else:
            self.color = pygame.Color(121, 72, 57, 255)  # Color for white squares
        self.originalcolor = self.color

    def draw(self):
        pygame.draw.rect(wn, self.color, (self.x * 80, self.y * 80, self.width, self.height))
        if self.piece is not None:
            wn.blit(self.piece.get_sprite(), (self.x * 80 + 5, self.y * 80 + 5))  # Offset the pawn sprite position

    def get_xy(self):
        return self.x, self.y

    def get_pos(self):
        return self.y * 8 + self.x

    def get_piece(self):
        return self.piece

    def set_piece(self, piece):
        self.piece = piece

    def set_color(self,color):
        self.oldcolor = self.color
        self.color = color

    def reset_color(self):
        self.color = self.originalcolor


# Draw squares
for y in range(8):
    for x in range(8):
        if wh_bl % 2 == 0:
            squares.fields.append(squares(x, y, False, 80, 80))  # Create black square
        else:
            squares.fields.append(squares(x, y, True, 80, 80))  # Create white square
        wh_bl = 1 - wh_bl
    wh_bl = 1 - wh_bl

# Draw pawns, knights, rooks, bishops, queens and kings
for i in range(64):
    #pawns
    xy = squares.fields[i].get_xy()
    if xy[1] == 1:
        squares.fields[i].set_piece(pieces.pawn("black", i))
    elif xy[1] == 6:
        squares.fields[i].set_piece(pieces.pawn("white", i))
    #knights
    if xy == (1,0) or xy == (6,0):
        squares.fields[i].set_piece(pieces.knight("black", i))
    elif xy == (1,7) or xy == (6,7):
        squares.fields[i].set_piece(pieces.knight("white", i))
    #rooks
    if xy == (0,0) or xy == (7,0):
        squares.fields[i].set_piece(pieces.rook("black", i))
    elif xy == (0,7) or xy == (7,7):
        squares.fields[i].set_piece(pieces.rook("white", i))
    #bishops
    if xy == (2,0) or xy == (5,0):
        squares.fields[i].set_piece(pieces.bishop("black", i))
    elif xy == (2,7) or xy == (5,7):
        squares.fields[i].set_piece(pieces.bishop("white", i))
    #queens
    if xy == (3,0):
        squares.fields[i].set_piece(pieces.queen("black", i))
    elif xy == (3,7):
        squares.fields[i].set_piece(pieces.queen("white", i))
    #kings
    if xy == (4,0):
        squares.fields[i].set_piece(pieces.king("black", i))
    elif xy == (4,7):
        squares.fields[i].set_piece(pieces.king("white", i))


storage = None
oldsquare = 0
square = 0
while running:
    for field in squares.fields:
        field.draw()
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mousepos = pygame.mouse.get_pos()
            buttons = pygame.mouse.get_pressed(num_buttons=5)

            # Left click
            if not buttons[0]:
                continue

            x = mousepos[0] // 80  # Calculate the column of the clicked square
            y = mousepos[1] // 80  # Calculate the row of the clicked square
            xy = (x, y)

            for square in range(64):
                xypos = squares.fields[square].get_xy()

                if xypos != xy:
                    continue

                clicked_piece = squares.fields[square].get_piece()

                if storage is None and clicked_piece is not None and clicked_piece.color == current_player:
                    # select
                    storage = clicked_piece
                    squares.fields[square].set_color(select_color)
                    oldsquare = square
                elif storage is not None:
                    if clicked_piece is None and square in storage.get_moves():
                        # move
                        storage.set_square(square)
                        squares.fields[oldsquare].set_piece(None)
                        storage = None
                        current_player = "black" if current_player == "white" else "white"
                        squares.fields[oldsquare].reset_color()
                    elif clicked_piece is not None and clicked_piece.color != current_player and square in storage.get_moves():
                        # attack
                        storage.set_square(square)
                        squares.fields[oldsquare].set_piece(None)
                        storage = None
                        current_player = "black" if current_player == "white" else "white"
                        squares.fields[oldsquare].reset_color()
                        pygame.mixer.music.load(os.path.join(pathdir, music[random.randint(0, 2)]))
                        pygame.mixer.music.play()
                    elif clicked_piece is not None and clicked_piece.color == current_player:
                        # select
                        storage = clicked_piece
                        squares.fields[oldsquare].reset_color()
                        squares.fields[square].set_color(select_color)
                        oldsquare = square
                    else:
                        # illegal move, reset selection
                        storage = None
                        squares.fields[oldsquare].reset_color()

    pygame.display.flip()

    caption = f'chess ({current_player}\'s turn)'

    white_king_found = False
    black_king_found = False

    for f in squares.fields:
        figure = f.get_piece()
        if isinstance(figure, pieces.king):
            if figure.color == "white":
                white_king_found = True
                if figure.is_in_check():
                    caption = "white is in check"
            else:
                black_king_found = True
                if figure.is_in_check():
                    caption = "black is in check"

    pygame.display.set_caption(caption)
                
    '''
        xy = squares.fields[i].get_xy()
        if figure != None:
            if xy[1] == 7 and figure.color == "black" and isinstance(figure, pieces.pawn):

                checking = True
                pygame.display.set_caption("waiting for input(1 = queen,2 = rook,p 3 = bishop, 4 = knight)")

                while checking:
                    keys = pygame.key.get_pressed()

                    if keys[pygame.K_1]:
                        square.set_piece(pieces.queen("black",squares.fields[i]))
                        checking = False
                    elif keys[pygame.K_2]:
                        square.set_piece(pieces.rook("black",squares.fields[i]))
                        checking = False
                    elif keys[pygame.K_3]:
                        square.set_piece(pieces.bishop("black",squares.fields[i]))
                        checking = False
                    elif keys[pygame.K_1]:
                        square.set_piece(pieces.knight("black",squares.fields[i]))
                        checking = False
    '''

    

    if not black_king_found:
        pygame.display.set_caption("white won! congrats to white! (game made by noschXL)")
        time.sleep(5)
        running = False

 
    if not white_king_found:
        pygame.display.set_caption("black won! congrats to black! (game made by noschXL)")  
        time.sleep(5)
        running = False


pygame.quit()
sys.exit()
