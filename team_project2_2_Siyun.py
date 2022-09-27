import random

board = ['-', '-', '-',
         '-', '-', '-',
         '-', '-', '-']

counts = 0

able_puts = [i for i in range(9)]

while len(able_puts) != 0:
    able_puts = []
    for i, v in enumerate(board):
        if v == '-':
            able_puts.append(i)
    print(str(board[:3]) +"\n"+str(board[3:6]) +"\n"+str(board[6:]) +"\n"+"---------------")
    print('Type where you want to put:')
    put = input()

    try:
        put = int(put)
    except:
        print('Retype where you want to put')
        continue

    if put not in able_puts:
        print('Retype where you want to put')
        continue
    else:
        board[put] = 'O'
        able_puts = []
        for i, v in enumerate(board):
            if v == '-':
                able_puts.append(i)
        
        if len(able_puts) == 0:
            break
        
        board[random.choice(able_puts)] = 'X'

print(str(board[:3]) +"\n"+str(board[3:6]) +"\n"+str(board[6:]) +"\n"+"---------------")

if board[0] == 'O' and board[1] == 'O' and board[2] == 'O':
    print('Human wins')
elif board[3] == 'O' and board[4] == 'O' and board[5] == 'O':
    print('Human wins')
elif board[6] == 'O' and board[7] == 'O' and board[8] == 'O':
    print('Human wins')
elif board[0] == 'O' and board[3] == 'O' and board[6] == 'O':
    print('Human wins')
elif board[1] == 'O' and board[4] == 'O' and board[7] == 'O':
    print('Human wins')
elif board[2] == 'O' and board[5] == 'O' and board[8] == 'O':
    print('Human wins')
elif board[0] == 'O' and board[4] == 'O' and board[8] == 'O':
    print('Human wins')
elif board[2] == 'O' and board[4] == 'O' and board[6] == 'O':
    print('Human wins')
elif board[0] == 'X' and board[1] == 'X' and board[2] == 'X':
    print('Computer wins')
elif board[3] == 'X' and board[4] == 'X' and board[5] == 'X':
    print('Computer wins')
elif board[6] == 'X' and board[7] == 'X' and board[8] == 'X':
    print('Computer wins')
elif board[0] == 'X' and board[3] == 'X' and board[6] == 'X':
    print('Computer wins')
elif board[1] == 'X' and board[4] == 'X' and board[7] == 'X':
    print('Computer wins')
elif board[2] == 'X' and board[5] == 'X' and board[8] == 'X':
    print('Computer wins')
elif board[0] == 'X' and board[4] == 'X' and board[8] == 'X':
    print('Computer wins')
elif board[2] == 'X' and board[4] == 'X' and board[6] == 'X':
    print('Computer wins')
else:
    print('Draw!')