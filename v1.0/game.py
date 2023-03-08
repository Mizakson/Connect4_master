"""
Connect 4 Game V1.0
This is a simple connect 4 game made using python, pygame and numpy.

"""
# import modules
import numpy as np
import pygame
import sys
import math

# define colors
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# define board size
ROW_COUNT = 6
COLUMN_COUNT = 7

# define game functions

# create board
def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board

# drop piece
def drop_piece(board, row, col, piece):
    board[row][col] = piece

# check if location is valid
def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0

# get next open row
def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

# print board
def print_board(board):
    print(np.flip(board, 0))

# check if there is a winning move
def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][c + 3] == piece:
                return True

    # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][c] == piece:
                return True

    # Check positively sloped diaganols
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][c + 3] == piece:
                return True

    # Check negatively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece:
                return True

# draw board
def draw_board(board):
    # draw board
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    
    # draw pieces
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()

# main game loop object
board = create_board()
print_board(board)
game_over = False
turn = 0

# initialize pygame
pygame.init()

# define screen size
SQUARESIZE = 100

# define width and height of the board
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE

# define size of the screen
size = (width, height)

# define radius of the circle
RADIUS = int(SQUARESIZE / 2 - 5)

# define screen
screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

# define font
myfont = pygame.font.SysFont("monospace", 75)

# main game loop
while not game_over:

    # check for events
    for event in pygame.event.get():
        # check if the user wants to quit
        if event.type == pygame.QUIT:
            sys.exit()

        # check if the user wants to play
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)
            else:
                pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE / 2)), RADIUS)
        pygame.display.update()

        # check if the user wants to drop a piece
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            # print(event.pos)
            # Ask for Player 1 Input
            if turn == 0:
                posx = event.pos[0]
                col = int(math.floor(posx / SQUARESIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 1)

                    if winning_move(board, 1):
                        label = myfont.render("Player 1 wins!!", 1, RED)
                        screen.blit(label, (40, 10))
                        game_over = True

            # # Ask for Player 2 Input
            else:
                posx = event.pos[0]
                col = int(math.floor(posx / SQUARESIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 2)

                    if winning_move(board, 2):
                        label = myfont.render("Player 2 wins!!", 1, YELLOW)
                        screen.blit(label, (40, 10))
                        game_over = True

            print_board(board)
            draw_board(board)
            
            # change turn
            turn += 1
            turn = turn % 2

            # check if game is over
            if game_over:
                pygame.time.wait(3000)
