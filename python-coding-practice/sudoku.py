#!/usr/local/bin/python3
import math

def isOK(board,emptyValue='.'):
    def notOK(b,s):
        if b == emptyValue:
            return False
        if b in s:
            return True
        s.add(b)
        return False
    n = len(board)
    q = int(math.sqrt(n))
    complete = True
    for i in range(n):
        row = set()
        col = set()
        block = set()
        for j in range(n):
            if board[i][j] == emptyValue:
                complete = False
            if notOK(board[i][j],row) or \
               notOK(board[j][i],col) or \
               notOK(board[(i//q)*q+j//q][(i%q)*q+j%q],block):
                return (False,False)
    return (True,complete)

def solve_sudoku(board,emptyValue='.'):
    n = len(board)
    q = int(math.sqrt(n))
    def mapBoard(row,col,i):
        def bValue(r,c,i):
            if r == row and c == col:
                return i
            else:
                return board[r][c]
        return [ [bValue(r,c,i) for c in range(n)] for r in range(n)]
    (ok,complete) = isOK(board)
    if not ok:
        return (False,board)
    if complete:
        return (True,board)
    for row in range(n):
        for col in range(n):
            if board[row][col] == emptyValue:
                for i in range(1,n+1):
                    (complete,newBoard) = solve_sudoku(mapBoard(row,col,i))
                    if complete:
                        return (complete,newBoard)
                return (False,board)
    return (False,board)


def unit_tests():
    _ = '.'
    assert (True,False) == isOK([[_,_,_,_],
                                 [_,_,_,_],
                                 [_,_,_,_],
                                 [_,_,_,_]])
    assert (True,True) == isOK([[1,2,4,3],
                                [4,3,1,2],
                                [2,4,3,1],
                                [3,1,2,4]])
    assert (False,False) == isOK([[1,2,4,3],
                                  [4,3,1,2],
                                  [1,4,3,_],
                                  [3,1,2,4]])
    assert (False,False) == isOK([[1,2,4,3],
                                  [4,3,1,2],
                                  [2,4,3,4],
                                  [3,1,2,_]])
    assert (False,False) == isOK([[1,2,4,3],
                                  [4,1,_,2],
                                  [2,4,3,_],
                                  [3,_,_,_]])
    assert (False,False) == isOK([[1,2,4,3],
                                  [4,3,1,2],
                                  [2,4,3,1],
                                  [3,_,1,_]])
    assert (True,False) == isOK([[1,_,5,_,_,_,_,_,_],
                                 [_,2,_,_,_,_,_,_,_],
                                 [_,_,3,_,_,_,_,_,_],
                                 [_,_,_,4,_,_,_,_,_],
                                 [_,_,_,_,5,_,_,_,_],
                                 [_,_,_,1,_,6,_,_,_],
                                 [_,_,_,_,_,_,7,_,_],
                                 [_,_,_,_,_,_,_,8,_],
                                 [_,_,_,_,_,_,2,_,9]])

    assert (True,[[1,4,5,2,3,7,6,9,8],
                  [6,2,7,5,8,9,1,3,4],
                  [8,9,3,6,1,4,5,2,7],
                  [2,1,6,4,7,8,9,5,3],
                  [4,7,9,3,5,2,8,1,6],
                  [3,5,8,1,9,6,4,7,2],
                  [5,8,2,9,4,3,7,6,1],
                  [9,6,4,7,2,1,3,8,5],
                  [7,3,1,8,6,5,2,4,9]]) == \
         (solve_sudoku([[1,_,5,_,_,_,_,_,_],
                        [_,2,_,_,_,_,_,_,_],
                        [_,_,3,_,_,_,_,_,_],
                        [_,_,_,4,_,_,_,_,_],
                        [_,_,_,_,5,_,_,_,_],
                        [_,_,_,1,_,6,_,_,_],
                        [_,_,_,_,_,_,7,_,_],
                        [_,_,_,_,_,_,_,8,_],
                        [_,_,_,_,_,_,2,_,9]]))
    return "unit tests passed"
print(unit_tests())