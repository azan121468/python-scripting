from z3 import *
from pprint import pprint

#ToDo: Add more conditions which check that in provided board no two values repeat in any row or column.
#In that case, print No Solution

# sudoku_board = [
# [9,0,0, 1,0,0, 0,4,0],
# [0,7,0, 6,0,0, 3,0,9],
# [0,0,0, 0,3,0, 0,5,0],

# [0,5,0, 0,0,1, 0,0,0],
# [0,0,0, 0,0,0, 0,0,4],
# [1,0,0, 0,2,0, 9,0,6],

# [5,0,0, 0,6,0, 2,0,1],
# [0,0,0, 0,0,0, 0,3,0],
# [0,0,8, 7,0,0, 0,0,0],
# ]

sudoku_board = [
[1,2,3, 0,0,0, 7,8,9],
[4,5,6, 0,0,0, 1,2,3],
[7,8,9, 0,0,0, 4,5,6],

[0,0,0, 0,0,0, 0,0,0],
[0,0,0, 0,0,0, 0,0,0],
[0,0,0, 0,0,0, 0,0,0],

[3,1,2, 0,0,0, 0,0,0],
[6,4,5, 0,0,0, 0,0,0],
[9,7,8, 0,0,0, 0,0,0],
]
zero_indices = [(i,j) for i in range(9) for j in range(9) if sudoku_board[i][j] == 0]
_vars = [BitVec(f'x{zero_indices[x][0]}{zero_indices[x][1]}', 6) for x in range(len(zero_indices))]
assert len(zero_indices) == len(_vars)
for (x, y), i in zip(zero_indices, _vars):
    sudoku_board[x][y] = i

s = Solver()

for row_num in range(9): # add row condition
    row = [sudoku_board[row_num][col_num] for col_num in range(9)]
    s.add(sum(row) == 45)

for col_num in range(9): # add column condition
    column = [sudoku_board[row_num][col_num] for row_num in range(9)]
    s.add(sum(column) == 45)
    
for row_num in range(9): # add condition that each element should be from 1 to 9
    for col_num in range(9):
        s.add(
            And(
                    sudoku_board[row_num][col_num] > 0,
                    sudoku_board[row_num][col_num] < 10
                )
        )

for row_num in range(9): # add condition that no element in row should be same
    row = [sudoku_board[row_num][col_num] for col_num in range(9)]
    s.add(Distinct(row))
    # for i in range(9):
        # for j in range(i, 9):
            # if i == j:
                # continue
            # s.add(row[i] != row[j])


for col_num in range(9): # add condition that no element in column should be same
    column = [sudoku_board[row_num][col_num] for row_num in range(9)]
    s.add(Distinct(column))
    # for i in range(9):
        # for j in range(i, 9):
            # if i == j:
                # continue
            # s.add(column[i] != column[j])

for block_row in range(3): # add condition that no element should repeat in 3*3 block. Generated by chatgpt.
    for block_col in range(3):
        block_values = [sudoku_board[row_num][col_num] for row_num in range(block_row * 3, (block_row + 1) * 3) for col_num in range(block_col * 3, (block_col + 1) * 3)]
        try:
            s.add(Distinct(block_values))
        except z3types.Z3Exception:
            pass


if s.check() == sat:
    print("Solution Found")
    model = s.model()
    print([model[i] for i in _vars])
    
    
    solved_board = sudoku_board
    for (i, j), symbolic_variable in zip(zero_indices, _vars):
        solved_board[i][j] = model[symbolic_variable]
    
    print("Complete sudoku board")
    pprint(solved_board)
else:
    print("Solution not found")