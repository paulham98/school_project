import queue

# 상태를 나타내는 클래스, f(n) 값을 저장한다. 
class State:
  def __init__(self, board, goal, moves=0):
    self.board = board
    self.moves = moves
    self.goal = goal

  # i1과 i2를 교환하여서 새로운 상태를 반환한다. 
  def get_new_board(self, i1, i2, moves):
    new_board = self.board[:]
    new_board[i1], new_board[i2] = new_board[i2], new_board[i1]
    return State(new_board, self.goal, moves)

  # 자식 노드를 확장하여서 리스트에 저장하여서 반환한다. 
  def expand(self, moves):
    result = []
    i = self.board.index(0)		# 숫자 0(빈칸)의 위치를 찾는다. 
    if not i in [0, 1, 2] :		# UP 연산자 
      result.append(self.get_new_board(i, i-3, moves))
    if not i in [0, 3, 6] :		# LEFT 연산자 
      result.append(self.get_new_board(i, i-1, moves))
    if not i in [2, 5, 8]:		# DOWN 연산자 
      result.append(self.get_new_board(i, i+1, moves))
    if not i in [6, 7, 8]:		# RIGHT 연산자 
      result.append(self.get_new_board(i, i+3, moves))
    return result

  # f(n)을 계산하여 반환한다. 
  def f(self):
    return self.h()+self.g()

  # 휴리스틱 함수 값인 h(n)을 계산하여 반환한다. 
  # 현재 제 위치에 있지 않은 타일의 개수를 리스트 함축으로 계산한다. 
  def bfs_board(self,current_index,current):
    cur_row = 0;cur_col=0;
    cur_row= current_index//3
    cur_col = current_index%3
    goal_index = self.goal.index(current)
    col = goal_index%3
    row = goal_index//3
    row = abs(row-cur_row)
    col = abs(col-cur_col)
    if row>=2:
      row+=2
    if col>=2:
      col+=2
    return row+col;
  
  def h(self):
    # find = set()
    result = []
    for i in range(9):
      if self.board[i] != self.goal[i]:
        result.append(2.5)
      # else:
        # result.append(-2.5) 
        # 더줄어들지만  
      result.append(self.bfs_board(i,self.board[i]))
    return sum(result)
    # return sum([1 if self.board[i] != self.goal[i] else 0 for i in range(9)])

  # 시작 노드로부터의 경로를 반환한다. 
  def g(self):
    return self.moves

  def __eq__(self, other):
    return self.board == other.board
 
  # 상태와 상태를 비교하기 위하여 less than 연산자를 정의한다. 
  def __lt__(self, other):
    return self.f() < other.f()

  def __gt__(self, other):
    return self.f() > other.f()

  # 객체를 출력할 때 사용한다. 
  def __str__(self):
    return "------------------ f(n)=" + str(self.f()) +"\n"+\
    "------------------ h(n)=" + str(self.h()) +"\n"+\
    "------------------ g(n)=" + str(self.g()) +"\n"+\
    str(self.board[:3]) +"\n"+\
    str(self.board[3:6]) +"\n"+\
    str(self.board[6:]) +"\n"+\
    "------------------"

if __name__ == '__main__':
  # 초기 상태
  puzzle = [1, 2, 3, 
            4, 8, 6, 
            0, 5, 7]

  # 목표 상태
  goal = [1, 2, 3, 
          4, 5, 6, 
          7, 8, 0]

  # open 리스트는 우선순위 큐로 생성한다. 
  open_queue = queue.PriorityQueue()
  open_queue.put(State(puzzle, goal))

  closed_queue = [ ]
  moves = 0
  while not open_queue.empty():

  #  디버깅을 위한 코드
    # print("START OF OPENQ")
    # for elem in open_queue.queue:
    #       print(elem)
    # print("END OF OPENQ")
    current = open_queue.get()
    if current.board == goal:
        print(current)
        print("탐색 성공")
        print("open queue 길이=", open_queue.qsize())
        print("closed queue 길이=", len(closed_queue))
        break
    moves = current.moves+1
    for state in current.expand(moves):
      if state not in closed_queue and state not in open_queue.queue :
        open_queue.put(state)
    closed_queue.append(current)
  else:
    print ('탐색 실패')
