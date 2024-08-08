from random import shuffle, randint
import pygame, time, sys

def main():
    board = generate_sudoku(20)
    pygame.init()
    screen = pygame.display.set_mode((450, 450))
    pygame.display.set_caption("sudoku")
    font = pygame.font.Font('freesansbold.ttf', 30)
    clock = pygame.time.Clock()

    while True:
        solve(board, screen, font)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        pygame.display.update()
        clock.tick(60)


#generate a valid sudoku with a certain number of squares filled in
def generate_sudoku(num_filled_squares: int) -> list[list[int]]:
    #exception handling for if user inputs more or less squares that what is possible
    if num_filled_squares > 81:
        num_filled_squares = 81
    elif num_filled_squares < 0:
        num_filled_squares = 0
    
    board = [[None for _ in range(9)] for _ in range(9)]
    fill_board(board)
    num_spaces = len(board) * len(board[0])
    visited_squares = set()
    num_spaces_to_delete = num_spaces - num_filled_squares

    while num_spaces_to_delete > 0:
        row = randint(0, 8)
        col = randint(0, 8)
        space = (row, col)

        if space in visited_squares:
            continue
        else:
            visited_squares.add(space)
            undo_move(board, space)
            num_spaces_to_delete -= 1
    return board

#fills an empty board in place
def fill_board(board):
    #get the next empty square. If there isn't one, that means the sudoku is complete
    space = get_empty_square(board)
    if not space:
        return board
    
    #get the valid moves for a square. If there aren't any, then we break out of this function to backtrack
    valid_moves = get_valid_moves(board, space)
    if not valid_moves:
        return False
    
    #shuffle the valid moves so we place a random number when generating a sudoku
    shuffle(valid_moves)
    for move in valid_moves:
        play_move(board, space, move)

        #recursively try to fill the board and undo moves if we fail to fill the board at some point
        result = fill_board(board)
        if result:
            return result
        
        undo_move(board, space)
         
#solves a sudoku board in place. display and font parameters for visual shenanigans, not important to algorithm
def solve(board: list[list[int]], display, font) -> bool:
    #get the next empty square. If there isn't one, that means the sudoku is solved
    space = get_empty_square(board)
    if not space:
        return True
    
    #get the valid moves for a square. If there aren't any, then we break out of this function to backtrack
    valid_moves = get_valid_moves(board, space)
    if not valid_moves:
        return False
    
    for move in valid_moves:
        play_move(board, space, move)

        #display shenanigans, not important to solve algorithm
        display.fill((255, 255, 255))
        width = 2
        for i in range(1, 9):
            if i % 3 == 0:
                width = 4
            else:
                width = 2
            pygame.draw.line(display, (0, 0, 0), (i*50, 0), (i*50, 450), width)
        for i in range(1, 9):
            if i % 3 == 0:
                width = 4
            else:
                width = 2
            pygame.draw.line(display, (0, 0, 0), (0, i*50), (450, i*50), width)
        
        for row in range(len(board)):
            for col in range(len(board[0])):
                if board[row][col]:
                    display.blit(font.render(str(board[row][col]), True, (0, 0, 0)), (col*50 + 13, row*50 + 17))
        display.blit(font.render(str(board[space[0]][space[1]]), True, (0, 0, 0)), (space[1]*50 + 13, space[0]*50 + 17))
        pygame.display.update()
        time.sleep(0.0001)

        #assign solve() to a variable so the previous iteration can access the win state
        result = solve(board, display, font)
        if result:
            return result
        
        undo_move(board, space)
    
    #if we get to this point of the code, then we've gone through every single possible way to fill the board, so the sudoku is unsolvable
    return False

#gets valid numbers for a given square
def get_valid_moves(board: list[list[int]], space: tuple[int, int]) -> list[int]:
    #given a sudoku board and a space on that board, return a list of all the valid numbers that could be in that spot
    row, col = space
    current_square = (row // 3, col // 3)

    col_values = [board[i][col] for i in range(len(board)) if board[i][col]]
    row_values = [spot for spot in board[row] if spot]
    square_values = []

    for i in range(current_square[0]*3, (current_square[0]*3 + 2) + 1):
        for j in range(current_square[1]*3, (current_square[1]*3 + 2) + 1):
            current_spot = board[i][j]
            if current_spot:
                square_values.append(current_spot)

    valid_moves = [i for i in range(1, 10)]
    valid_moves = [move for move in valid_moves if(move not in col_values and move not in row_values and move not in square_values)]
    return valid_moves

#gets the next empty square in a board
def get_empty_square(board: list[list[int]]) -> tuple[int, int]:
    #get the first available empty space in sudoku board
    for row in range(len(board)):
        for col in range(len(board[0])):
            if not board[row][col]:
                return (row, col)
    #if there is no empty square
    return False

#functions used to make and undo moves as part of the backtracking algorithm
def play_move(board: list[list[int]], space: tuple[int, int], num: int):
    row, col = space
    board[row][col] = num

def undo_move(board: list[list[int]], space: tuple[int, int]):
    row, col = space
    board[row][col] = None

if __name__ == '__main__':
    main()
