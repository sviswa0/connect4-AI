import numpy as np
from scipy.signal import convolve2d
import sys
import pygame
import math
BLUE = (0, 0, 200)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
PURPLE = (148, 43, 226)
SQUARE_SIZE = 100 #num pixels
RADIUS = int(SQUARE_SIZE / 2 - 5)
def make_board():
    return np.zeros((6,7))

def find_row(board, col, id):

    for i in reversed(range(np.shape(board)[0])):
        if board[i, col] == 0:
            board[i, col] = id
            return

def is_valid_move(board, col):
    return board[0][col] == 0
    
def make_move(board, col, id):

    if is_valid_move(board, col): 
        #board[]
        find_row(board, col, id)
        return True
    return False

def check_win(board, id, detection_kernels):
    #convert everything besides your moves to 0
    check = np.where(board != id, 0, board)
    
    for kernel in detection_kernels:
        if (convolve2d(check == id, kernel, mode="valid") == 4).any():
            return True
    return False

def draw_board(board):
    for r in range(np.shape(board)[1]):
        for c in range(np.shape(board)[0]):
            pygame.draw.rect(screen, BLUE, (r * SQUARE_SIZE, c * SQUARE_SIZE + SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            
            if board[c, r] == 0:
                pygame.draw.circle(screen, BLACK, (int(r*SQUARE_SIZE+SQUARE_SIZE/2), int(c*SQUARE_SIZE+SQUARE_SIZE+SQUARE_SIZE/2)), RADIUS)
            elif board[c, r] == 1:
                pygame.draw.circle(screen, RED, (int(r*SQUARE_SIZE+SQUARE_SIZE/2), int(c*SQUARE_SIZE+SQUARE_SIZE+SQUARE_SIZE/2)), RADIUS)
            else:
                pygame.draw.circle(screen, PURPLE, (int(r*SQUARE_SIZE+SQUARE_SIZE/2), int(c*SQUARE_SIZE+SQUARE_SIZE+SQUARE_SIZE/2)), RADIUS)   
    pygame.display.update()

horizontal_kernel = np.array([[ 1, 1, 1, 1]])
vertical_kernel = np.transpose(horizontal_kernel)
diag1_kernel = np.eye(4, dtype=np.uint8)
diag2_kernel = np.fliplr(diag1_kernel)


detection_kernels = [horizontal_kernel, vertical_kernel, diag1_kernel, diag2_kernel]
board = make_board()

p1Turn = True
gameOver = False


width = 7 * SQUARE_SIZE
height = (6 + 1) * SQUARE_SIZE
size = (width, height)
pygame.init()
screen = pygame.display.set_mode(size)

draw_board(board)
pygame.display.update()
while not gameOver:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))
            x = event.pos[0]
            color = RED if p1Turn else PURPLE
            pygame.draw.circle(screen, color, (x, RADIUS), RADIUS)
            pygame.display.update()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x = event.pos[0]
            y = event.pos[1]

            col = x // SQUARE_SIZE #maybe floor
            x = event.pos[0]
            y = event.pos[1]

            col = x // SQUARE_SIZE #maybe floor
            pass
            if p1Turn:
                #col = int(input("What column would you like to move in P1? "))
                #make move
                make_move(board, col, 1)

            else:
                #col = int(input("What column would you like to move in P2? "))
                make_move(board, col, 2)
            
            print(board)
            draw_board(board)
            if p1Turn: turn = 1
            else: turn = 2

            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))
            #x = event.pos[0]
            p1Turn = not p1Turn
            color = RED if p1Turn else PURPLE
            pygame.draw.circle(screen, color, (x, RADIUS), RADIUS)


            if check_win(board, turn, detection_kernels):
                pygame.draw.rect(screen, BLACK, (0,0, width, SQUARE_SIZE))
                #custom_font = pygame.font.SysFont("Ariel", 75)
                custom_font = pygame.font.SysFont("Ariel", 75)
                win = "Player " + str(turn) + " wins!"
                color = RED if not p1Turn else PURPLE
                label = custom_font.render(win, 1, color)
                screen.blit(label, (50, 10))
                #draw_board(board)
                gameOver = True
                pygame.display.update()
                pygame.time.wait(2000)
            else:
                pygame.display.update()
            


       


