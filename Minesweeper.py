from random import randint

def main():
    #initialize game settings for the game
    board = [[' ' for _ in range(10)] for _ in range(10)]
    visible_board = [['*' for _ in range(10)] for _ in range(10)]
    num_bombs = 2
    game_over = False
    dug_spots = set()

    #place bombs on the board
    while num_bombs > 0:
        row = randint(0, 9)
        col = randint(0, 9)

        if board[row][col] == "*":
            continue
        board[row][col] = '*'
        num_bombs -= 1
    
    #check surrounding bombs of each space
    check_bombs(board)
    
    #game loop
    while not game_over:
        print_board(visible_board)

        #get valid player move
        row = int(input("Choose a row: ")) - 1
        col = int(input("Choose a column: ")) - 1
        player_move = (row, col)
        if player_move in dug_spots:
            print("\nThat space has already been dug, try again\n")
            continue
        
        #dig space and determine if it was a bomb
        if dig(visible_board, board, player_move, dug_spots) is True:
            game_over = True
        
        #if all spots have been dug
        if visible_board == board:
            break
    
    print_board(board)
    if game_over:
        print("You Lost")
    else:

        print("You Win")
    


    

    

def print_board(board):
    print("      1    2    3    4    5    6    7    8    9    10")
    for i in range(len(board)):
        print(f"{i+1}---{board[i]}", end='\n')

def check_bombs(board):
    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] == '*':
                continue
            surrounding_bombs = 0
            checked_spots = set()

            if (max(0, row-1), max(0, col-1)) in checked_spots:
                pass
            else:
                if board[max(0, row-1)][max(0, col-1)] == '*':
                    surrounding_bombs += 1
                checked_spots.add((max(0, row-1), max(0, col-1)))

            if (max(0, row-1), col) in checked_spots:
                pass
            else:
                if board[max(0, row-1)][col] == '*':
                    surrounding_bombs += 1
                checked_spots.add((max(0, row-1), col))
            
            if (max(0, row-1), min(9, col+1)) in checked_spots:
                pass
            else:
                if board[max(0, row-1)][min(9, col+1)] == '*':
                    surrounding_bombs += 1
                checked_spots.add((max(0, row-1), min(9, col+1)))
            
            if (row, max(0, col-1)) in checked_spots:
                pass
            else:
                if board[row][max(0, col-1)] == '*':
                    surrounding_bombs += 1
                checked_spots.add((row, max(0, col-1)))

            if (row, min(9, col+1)) in checked_spots:
                pass
            else:
                if board[row][min(9, col+1)] == '*':
                    surrounding_bombs += 1
                checked_spots.add((row, min(9, col+1)))
            
            if (min(9, row+1), max(0, col-1)) in checked_spots:
                pass
            else:
                if board[min(9, row+1)][max(0, col-1)] == '*':
                    surrounding_bombs += 1
                checked_spots.add((min(9, row+1), max(0, col-1)))
            
            if (min(9, row+1), col) in checked_spots:
                pass
            else:
                if board[min(9, row+1)][col] == '*':
                    surrounding_bombs += 1
                checked_spots.add((min(9, row+1), col))
            
            if (min(9, row+1), min(9, col+1)) in checked_spots:
                pass
            else:
                if board[min(9, row+1)][min(9, col+1)] == '*':
                    surrounding_bombs += 1
                checked_spots.add((min(9, row+1), min(9, col+1)))

            
            board[row][col] = str(surrounding_bombs)


def dig(visible_board, board, space, dug_spots):
    if space in dug_spots:
        pass
    else:
        checked_spots = set()
        dug_spots.add(space)
        row, col = space
        if board[row][col] == '*':
            return True
        
        visible_board[row][col] = board[row][col]
        if board[row][col] == '0':
            if (max(0, row-1), max(0, col-1)) in checked_spots:
                pass
            else:
                checked_spots.add((max(0, row-1), max(0, col-1)))

            if (max(0, row-1), col) in checked_spots:
                pass
            else:
                checked_spots.add((max(0, row-1), col))
            
            if (max(0, row-1), min(9, col+1)) in checked_spots:
                pass
            else:
                checked_spots.add((max(0, row-1), min(9, col+1)))
            
            if (row, max(0, col-1)) in checked_spots:
                pass
            else:
                checked_spots.add((row, max(0, col-1)))

            if (row, min(9, col+1)) in checked_spots:
                pass
            else:
                checked_spots.add((row, min(9, col+1)))
            
            if (min(9, row+1), max(0, col-1)) in checked_spots:
                pass
            else:
                checked_spots.add((min(9, row+1), max(0, col-1)))
            
            if (min(9, row+1), col) in checked_spots:
                pass
            else:
                checked_spots.add((min(9, row+1), col))
            
            if (min(9, row+1), min(9, col+1)) in checked_spots:
                pass
            else:
                checked_spots.add((min(9, row+1), min(9, col+1)))
            
            for spot in checked_spots:
                dig(visible_board, board, spot, dug_spots)


main()