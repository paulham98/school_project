class State:
    def __init__(self, board, goal, moves=0, heuristic=0):
        self.board = board
        self.moves = moves
        self.goal = goal

        self.heuristic = 0
        for i, p in enumerate(board):
            if p != goal[i]:
                self.heuristic += 1
        
        self.cost = self.heuristic + self.moves

    def get_new_board(self, i1, i2):
        new_board = self.board[:]
        new_board[i1], new_board[i2] = new_board[i2], new_board[i1]
        return State(new_board, self.goal, self.moves, self.heuristic)

    def expand(self):
        self.moves += 1
        result = []
        i = self.board.index(0)
        # up
        if not i in [0, 1, 2] :
            result.append(self.get_new_board(i, i-3))
        # left
        if not i in [0, 3, 6] :
            result.append(self.get_new_board(i, i-1))
        # right
        if not i in [2, 5, 8]:
            result.append(self.get_new_board(i, i+1))
        # down
        if not i in [6, 7, 8]:
            result.append(self.get_new_board(i, i+3))
        return result

    def __eq__(self, other):
        return self.board == other.board

puzzle = [2, 8, 3, 
          1, 6, 4, 
          7, 0, 5]

goal = [1, 2, 3, 
        8, 0, 4, 
        7, 6, 5]

open_queue = []
open_queue.append(State(puzzle, goal))
closed_queue = []

while len(open_queue) != 0:
    current = open_queue.pop(0)
    # print(current.board)
    if current.board == goal:
        print("success")
        break
    closed_queue.append(current)
    states = current.expand()
    costs = [s.cost for s in states]
    for state in states:
        if (state in closed_queue) or (state in open_queue):
            continue
        else:
            if min(costs) == state.cost:
                open_queue.append(state)
                print(state.board, state.moves, state.heuristic, state.cost)