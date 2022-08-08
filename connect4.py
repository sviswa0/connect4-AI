import numpy as np
from scipy.signal import convolve2d
import pygame

def make_board():
    return np.zeros((6,7))

def find_row(board, col, id):

    for i in reversed(range(np.shape(board)[0])):
        if board[i, col] == 0:
            board[i, col] = id
            return


def make_move(board, col, id):

    if board[0][col] == 0: 
        #board[]
        find_row(board, col, id)

def check_win(board, id, detection_kernels):
    #convert everything besides your moves to 0
    check = np.where(board != id, 0, board)
    
    for kernel in detection_kernels:
        if (convolve2d(check == id, kernel, mode="valid") == 4).any():
            return True
    return False
        
        
horizontal_kernel = np.array([[ 1, 1, 1, 1]])
vertical_kernel = np.transpose(horizontal_kernel)
diag1_kernel = np.eye(4, dtype=np.uint8)
diag2_kernel = np.fliplr(diag1_kernel)


detection_kernels = [horizontal_kernel, vertical_kernel, diag1_kernel, diag2_kernel]
board = make_board()

p1Turn = True
gameOver = False

SQUARE_SIZE = 100 #num pixels
width = 7 * SQUARE_SIZE
height = (6 + 1) * SQUARE_SIZE
size = (width, height)

screen = pygame.display.set_mode(size)
while not gameOver:

    if p1Turn:
        col = int(input("What column would you like to move in P1? "))
        #make move
        make_move(board, col, 1)

    else:
        col = int(input("What column would you like to move in P2? "))
        make_move(board, col, 2)
    
    print(board)

    if p1Turn: turn = 1
    else: turn = 2

    if check_win(board, turn, detection_kernels):
        print("Player", turn, "wins!")
        break

    p1Turn = not p1Turn


       


