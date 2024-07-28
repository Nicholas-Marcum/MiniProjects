from random import randint

def main():
    #initialize game settings for the game

    #Two boards are created to handle 2 different things. The actual board is used to handle all the behind the scenes game logic of generating a board.
    #The visible board is the board that the player interacts with when the program is ran.
    board = [[' ' for _ in range(10)] for _ in range(10)]
    visible_board = [['*' for _ in range(10)] for _ in range(10)]
    num_bombs = 10
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

        #get valid player move, 1 is subtracted from input since the user inputs a value between 1-10 but our board uses 0 indexing
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
    #formatting for printing the board in a human readable manner
    print("      1    2    3    4    5    6    7    8    9    10")
    for i in range(len(board)):
        print(f"{i+1}---{board[i]}", end='\n')

# WHAT THE FUCK
def check_bombs(board):
    #iterate through 2D list so we visit every space
    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] == '*':
                continue
            surrounding_bombs = 0
            checked_spots = set()

            #This code sucks. Essentially, we check to see if a spot is in checked spots, if it's not, then we check if it's a bomb and increment surrounding_bombs
            #accordingly and add that spot to checked spots. The reasoning behind all the min() and max() functions is that when checking an edge space, if we try
            #to check the previous or next row/col, we will accidentally index outside the length of the board list
            if (max(0, row-1), max(0, col-1)) in checked_spots: #topleft
                pass
            else:
                if board[max(0, row-1)][max(0, col-1)] == '*':
                    surrounding_bombs += 1
                checked_spots.add((max(0, row-1), max(0, col-1)))

            if (max(0, row-1), col) in checked_spots: #top middle
                pass
            else:
                if board[max(0, row-1)][col] == '*':
                    surrounding_bombs += 1
                checked_spots.add((max(0, row-1), col))
            
            if (max(0, row-1), min(9, col+1)) in checked_spots: #topright
                pass
            else:
                if board[max(0, row-1)][min(9, col+1)] == '*':
                    surrounding_bombs += 1
                checked_spots.add((max(0, row-1), min(9, col+1)))
            
            if (row, max(0, col-1)) in checked_spots: #middleleft
                pass
            else:
                if board[row][max(0, col-1)] == '*':
                    surrounding_bombs += 1
                checked_spots.add((row, max(0, col-1)))

            if (row, min(9, col+1)) in checked_spots: #middleright, we don't check middle middle because that is the spot we are currently on
                pass
            else:
                if board[row][min(9, col+1)] == '*':
                    surrounding_bombs += 1
                checked_spots.add((row, min(9, col+1)))
            
            if (min(9, row+1), max(0, col-1)) in checked_spots: #downleft
                pass
            else:
                if board[min(9, row+1)][max(0, col-1)] == '*':
                    surrounding_bombs += 1
                checked_spots.add((min(9, row+1), max(0, col-1)))
            
            if (min(9, row+1), col) in checked_spots: #down middle
                pass
            else:
                if board[min(9, row+1)][col] == '*':
                    surrounding_bombs += 1
                checked_spots.add((min(9, row+1), col))
            
            if (min(9, row+1), min(9, col+1)) in checked_spots: #down right
                pass
            else:
                if board[min(9, row+1)][min(9, col+1)] == '*':
                    surrounding_bombs += 1
                checked_spots.add((min(9, row+1), min(9, col+1)))

            
            board[row][col] = str(surrounding_bombs)


def dig(visible_board, board, space, dug_spots):
    #We don't want to dig a spot thats already been dug, otherwise this would exceed the max recursion depth in the dig() function
    if space in dug_spots:
        pass
    else:
        checked_spots = set()
        dug_spots.add(space)

        #turn user input into usable row, col indexing for our 2d board list
        row, col = space
        
        #game state is handled with this if statement
        if board[row][col] == '*':
            return True

        #The space on the visible board is revealed whenever the dig function is called on that space
        visible_board[row][col] = board[row][col]

        #This part of the code is very similar to the check_bombs() function. If the space the player has chosen has a value of 0, that means that no bombs surround it.
        #In minesweeper, whenever you dig a spot that is 0 all the surrounding spots are automatically revealed for you. To do this, we first get all the surrounding
        #spots of the space and add it to the checked_spots set. Then the dig() function must be called on each one of those spots to reveal it and check if it's 0
        #again so that it continues to reveal each spot until you have an "island" of 0's surrounded by 1's, 2's, etc.
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

            #this is the recursive part of the dig() function
            for spot in checked_spots:
                dig(visible_board, board, spot, dug_spots)


main()
