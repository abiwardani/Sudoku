board = [
[9,0,0,0,0,0,0,0,0],
[0,0,0,1,0,7,0,0,0],
[0,0,0,0,0,0,6,4,9],
[0,9,6,8,0,0,5,0,0],
[0,0,8,7,0,0,0,1,0],
[0,2,0,0,0,4,0,8,0],
[0,0,0,0,4,0,1,0,0],
[7,0,5,9,8,0,3,0,0],
[3,4,0,0,0,0,0,0,0]]

import sudoku.sudoku as sd

play = sd.Board(board)

play.solve()