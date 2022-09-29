import random

if __name__ == '__main__':
    board = [' ', ' ', ' ', 
            ' ', ' ', ' ', 
            ' ', ' ', ' ']

    def print_board():
        print(" ", board[0], '|', board[1], '|', board[2])
        print("----|---|----")
        print(" ", board[3], '|', board[4], '|', board[5])
        print("----|---|----")
        print(" ", board[6], '|', board[7], '|', board[8])

    def is_valid(board,x,y):
        if(x > 2 or x < 0 or y > 2 or y < 0):
            print("wrong pos")
            return False
        elif(board[3*x + y] != " "):
            print("can't put here")
            return False
        return True

    def is_win(board, mark):
        for r in range(3):
            if(board[3*r] == mark and board[3*r + 1] == mark and board[3*r +2] == mark) or\
                (board[r] == mark and board[r + 3] == mark and board[r+6] == mark):
                return True
        if (board[0] == mark and board[4] == mark and board[8] == mark) or \
            (board[2] == mark and board[4] == mark and board[6] == mark):
            return True
        else:
            return False

    def is_full(board):
        full = True
        for mark in board:
            if mark == " ":
                full = False
                break
        return full

    def run_game():
        play = True
        turn = 0
        print_board()
        
        while play:
            if turn % 2 == 0: #human first
                x = int(input("enter pos x"))
                y = int(input("enter pos y"))
                if is_valid(board,x,y):
                    board[3*x + y] = "x"
                
                if is_win(board,"x"):
                    print("human win 'X'")
                    play = False
            
            else: #computer
                while(1):
                    x = random.randrange(0,3)
                    y = random.randrange(0,3)
                    print(x,y)
                    if is_valid(board,x,y):
                        board[3*x +y] = "O"
                        break;
                if is_win(board, "O"):
                    print("computer win 'O'")
                    play = False
                        
            if is_full(board):
                print("Draw")
                play = False
                
            print_board()
            turn += 1
                
    if __name__ == '__main__':
        run_game()