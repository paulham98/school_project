
class AI_TIC_TAC_TOE:
    def __init__(self,player:bool=True):
        self.board = [' ' for x in range(9)]
        # self.player= player
        self.AI = True
        self.HUM = False
        self.AI_check = 'X'
        self.HUM_check = 'O'
        self.get_win = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]

    def find_Null(self,board:list):
        result= [x for x,index in enumerate(board) if index==' ']
        return result

    def is_finished(self,board:list):
        return self.is_win(board,self.AI_check) or self.is_win(board,self.HUM_check)
    
    def is_win(self,board:list,checker:str):
        for (x,y,z) in self.get_win:
            if board[x]==board[y]==board[z]:
                if board[x]==checker:
                    return True
        return False
    
    def evaluate(self,board:list):
        if self.is_win(board,self.AI_check):
            score= 1
        elif self.is_win(board,self.HUM_check):
            score=-1
        else:
            score = 0
        return score
    
    def is_valid(self,x:int):
        return x in self.find_Null(self.board) and self.board[x]==' '
    
    def place(self,x,player):
        if self.is_valid(x):
            self.board[x] = player
            return True
        return False
    
    def input_board(self):
        num = -2
        while num not in self.find_Null(self.board):
            num = int(input("put where? :"))
            num -=1
            if num <= -1 or num >= 9:
                print("Invalid input")
                num = -1
            elif not self.is_valid(num):
                print("It checked!")
        return num
    
    def draw(self):
        print(" ", self.board[0], '|', self.board[1], '|', self.board[2], "   1 | 2 | 3")
        print("----|---|----")
        print(" ", self.board[3], '|', self.board[4], '|', self.board[5],"   4 | 5 | 6")
        print("----|---|----")
        print(" ", self.board[6], '|', self.board[7], '|', self.board[8],"   7 | 8 | 9")
        print("\n")
    def finish(self):
        if self.is_win(self.board,self.AI_check):
            print("Winner AI")
        elif self.is_win(self.board,self.HUM_check):
            print("Winner HUMAN")
        else:
            print("No body can win")

    def minimax(self,board,depth:int, max:bool):
        position =-1
        if depth == 0 or not self.find_Null(board) or self.is_finished(board):
            return -1, self.evaluate(board)
        if max==self.AI:
            value = float('-inf')
            for empty_index in self.find_Null(board):
                copy_board = board.copy()
                copy_board[empty_index]=self.AI_check
                _,score = self.minimax(copy_board,depth-1,self.HUM)
                if score > value:
                    value = score
                    position = empty_index
                if score ==1:
                    break
        else:
            value = float('inf')
            for empty_index in self.find_Null(board):
                copy_board = board.copy()
                copy_board[empty_index]=self.HUM_check
                _,score = self.minimax(copy_board,depth-1,self.AI)
                if score < value:
                    value = score
                    position = empty_index
                if score == -1:
                    break
        return position,value

    def start(self):
        player = True
        if player == self.HUM:
            print("\n_ _ _   789\n_ _ _   456\n _ _ _   123")
        while a.find_Null(self.board) and not a.is_finished(self.board):
            # print(a.find_Null(self.board))
            if player == self.AI:
                pos, _ = self.minimax(self.board,9,self.AI)
                self.place(pos,self.AI_check)
                # while AI_turn:
                #     AI_turn =self.place(pos,self.AI_check)
                player = self.HUM
            else:
                pos = self.input_board()
                self.place(pos,self.HUM_check)
                print("HUM")
                player=  self.AI
            self.draw()
        self.finish()

a = AI_TIC_TAC_TOE()
a.start()
    

