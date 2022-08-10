import numpy as np
from scipy.signal import convolve2d
import sys
import pygame
import math
import random

BLUE = (0, 0, 200)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
PURPLE = (148, 43, 226)
SQUARE_SIZE = 100 #num pixels
RADIUS = int(SQUARE_SIZE / 2 - 5)
ROWS = 6
COLS = 7
horizontal_kernel = np.array([[ 1, 1, 1, 1]])
vertical_kernel = np.transpose(horizontal_kernel)
diag1_kernel = np.eye(4, dtype=np.uint8)
diag2_kernel = np.fliplr(diag1_kernel)


detection_kernels = [horizontal_kernel, vertical_kernel, diag1_kernel, diag2_kernel]

def make_board():
    return np.zeros((6,7))

def find_open_row(board, col):
    for i in reversed(range(np.shape(board)[0])):
        if board[i, col] == 0:
            return i


def find_row(board, col, id):

    for i in reversed(range(np.shape(board)[0])):
        if board[i, col] == 0:
            board[i, col] = id
            return

def is_valid_move(board, col):
    return board[0][col] == 0

def get_valid_locations(board):
	valid_locations = []
	for col in range(7):
		if is_valid_move(board, col):
			valid_locations.append(col)
	return valid_locations
    
def make_move(board, col, id):

    if is_valid_move(board, col): 
        #board[]
        find_row(board, col, id)
        return True
    return False

def make_move_min(board, r, c, id):
    board[r][c] = id

def check_win(board, id, detection_kernels):
    #convert everything besides your moves to 0
    check = np.where(board != id, 0, board)
    
    for kernel in detection_kernels:
        if (convolve2d(check == id, kernel, mode="valid") == 4).any():
            return True
    return False

def evaluate_window(window, piece):
	score = 0
	opp_piece = 1
	if piece == 1:
		opp_piece = 2

	#if window.count(piece) == 4:
		#score += 100
	if window.count(piece) == 3 and window.count(0) == 1:
		score += 5
	elif window.count(piece) == 2 and window.count(0) == 2:
		score += 2

	if window.count(opp_piece) == 3 and window.count(0) == 1:
		score -= 4

	return score

def score_position(board, piece):
	score = 0

	## Score center column
	center_array = [int(i) for i in list(board[:, COLS//2])]
	center_count = center_array.count(piece)
	score += center_count * 3

	## Score Horizontal
	for r in range(ROWS):
		row_array = [int(i) for i in list(board[r,:])]
		for c in range(COLS-3):
			window = row_array[c:c+4]
			score += evaluate_window(window, piece)

	## Score Vertical
	for c in range(COLS):
		col_array = [int(i) for i in list(board[:,c])]
		for r in range(ROWS-3):
			window = col_array[r:r+4]
			score += evaluate_window(window, piece)

	## Score posiive sloped diagonal
	for r in range(ROWS-3):
		for c in range(COLS-3):
			window = [board[r+i][c+i] for i in range(4)]
			score += evaluate_window(window, piece)

	for r in range(ROWS-3):
		for c in range(COLS-3):
			window = [board[r+3-i][c+i] for i in range(4)]
			score += evaluate_window(window, piece)

	return score

def minimax(board, depth, alpha, beta, maxPlayer):
    valid_locations = get_valid_locations(board)
   
    if check_win(board, 1, detection_kernels):
        return (None, -10000000000)
    elif check_win(board, 2, detection_kernels):
        return (None, 10000000000)
    elif np.count_nonzero(board==0) == 0:
        return (None, 0)
    elif depth == 0:
        return (None, score_position(board, 2))
    

    if maxPlayer:
        val = -math.inf
        column = random.choice(valid_locations)
        for c in valid_locations:
            r = find_open_row(board, c)
            b_copy = board.copy()
            make_move_min(b_copy, r, c, 2)
            new_score = minimax(b_copy, depth - 1, alpha, beta, False)[1]

            if new_score > val:
                val = new_score
                column = c
            alpha = max(val, alpha)

            if alpha >= beta: break
        return column, val
    else:
        val = math.inf
        column = random.choice(valid_locations)
        for c in valid_locations:
            r = find_open_row(board, c)
            b_copy = board.copy()
            make_move_min(b_copy, r, c, 1)
            new_score = minimax(b_copy, depth - 1, alpha, beta, True)[1]

            if new_score < val:
                val = new_score
                column = c
            beta = min(val, beta)

            if alpha >= beta: break
            
        return column, val



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

p1Turn = False if random.randint(0, 1) == 0 else True

turns = 0
while not gameOver:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))
            x = event.pos[0]
            if p1Turn:
                
                color = RED #if p1Turn else PURPLE
                pygame.draw.circle(screen, color, (x, RADIUS), RADIUS)
            pygame.display.update()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x = event.pos[0]
            y = event.pos[1]

            col = x // SQUARE_SIZE #maybe floor
            if p1Turn and not gameOver:
                #col = int(input("What column would you like to move in P1? "))
                #make move
                make_move(board, col, 1)

            
            
                print(board)
                draw_board(board)
                if p1Turn: turn = 1
                else: turn = 2

                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))
                #x = event.pos[0]
                p1Turn = not p1Turn
                color = RED
                pygame.draw.circle(screen, color, (x, RADIUS), RADIUS)


                if check_win(board, turn, detection_kernels) or turns == 21:
                    pygame.draw.rect(screen, BLACK, (0,0, width, SQUARE_SIZE))
                    #custom_font = pygame.font.SysFont("Ariel", 75)
                    custom_font = pygame.font.SysFont("Ariel", 75)
                    win = "Player 1 wins!" if turns != 21 else "Tie game!"
                    color = RED
                    label = custom_font.render(win, 1, color)
                    screen.blit(label, (50, 10))
                    #draw_board(board)
                    gameOver = True
                    pygame.display.update()
                    pygame.time.wait(5000)
            else:
                pygame.display.update()
    if not p1Turn and not gameOver:
        #col = random.randint(0, 6)
        
        #pygame.time.wait(200)
        #while not make_move(board, col, 2):
        #    col = random.randint(0, 6)
        #    pygame.time.wait(200)

        col, minimax_score = minimax(board, 6, -math.inf, math.inf, True)
        make_move(board, col, 2)
        turns += 1
        print(board)
        draw_board(board)
        turn = 2

        #pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))
        #x = event.pos[0]
        p1Turn = not p1Turn
        color = PURPLE
        #pygame.draw.circle(screen, color, (x, RADIUS), RADIUS)


        if check_win(board, turn, detection_kernels) or turns == 21:
            pygame.draw.rect(screen, BLACK, (0,0, width, SQUARE_SIZE))
            #custom_font = pygame.font.SysFont("Ariel", 75)
            custom_font = pygame.font.SysFont("Ariel", 75)
            win = "Player 2 wins!" if turns != 21 else "Tie game!"
            color = PURPLE
            label = custom_font.render(win, 1, color)
            screen.blit(label, (50, 10))
            #draw_board(board)
            gameOver = True
            pygame.display.update()
            pygame.time.wait(5000)
        else:
            pygame.display.update()

            