from random import randint

def main():
    board = {f'{i};{j}': ' ' for i in range(10) for j in range(10)}
    visible_board = {f'{i};{j}': '*' for i in range(10) for j in range(10)}
    num_bombs = 10
    game_over = False
    dug_spots = set()

    #place bombs on the board
    while num_bombs > 0:
        row = randint(0, 9)
        col = randint(0, 9)

        if board[f'{row};{col}'] == '*':
            continue
        board[f'{row};{col}'] = '*'
        num_bombs -= 1
    
    #check surrounding bombs of each space
    for space in board:
        check_bombs(board, space)
    
    #game loop
    while not game_over:
        print_board(visible_board)

        #get valid player move, 1 is subtracted from input since the user inputs a value between 1-10 but our board uses 0 indexing
        row = int(input("Choose a row: ")) - 1
        col = int(input("Choose a column: ")) - 1
        player_move = f'{row};{col}'

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

def print_board(board: dict):
    #formatting for printing the board in a human readable manner
    print("\n  1 2 3 4 5 6 7 8 9 10\n--------------------")
    for i in range(10):
        row = f"{i+1}-"
        for j in range(10):
            row += board[f'{i};{j}'] + "|"
        print(row)

def get_surrounding_spaces(board: dict, pos: str) -> list[str]:
    surrounding_spaces = []
    offsets = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    pos_coordinates = (int(pos[0]), int(pos[-1]))

    for offset in offsets:
        check_loc = f'{pos_coordinates[0] + offset[0]};{pos_coordinates[1] + offset[1]}'
        if check_loc in board:
            surrounding_spaces.append(check_loc)
    return surrounding_spaces

def check_bombs(board: dict, pos: str):
    if board[pos] == '*':
        return
    surrounding_spaces = get_surrounding_spaces(board, pos)
    surrounding_bombs = 0

    for space in surrounding_spaces:
        if board[space] == '*':
            surrounding_bombs += 1
    board[pos] = str(surrounding_bombs)

def dig(visible_board: dict, board: dict, space: str, dug_spots: set) -> bool:
    if space in dug_spots:
        return
    if board[space] == '*':
        return True
    
    visible_board[space] = board[space]
    dug_spots.add(space)
    
    if board[space] == '0':
        check_spots = get_surrounding_spaces(board, space)

        for spot in check_spots:
            dig(visible_board, board, spot, dug_spots)
    

main()
