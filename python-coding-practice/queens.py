#!/usr/local/bin/python3
# The following program's performance is really really bad
Directions = [  [ 0,-1], [ 0, 1], [-1, 0], [ 1, 0],
                [-1,-1], [ 1, 1], [-1, 1], [ 1, -1]]
def isOK(indexes, size):
    for row in range(size):
        for col in range(size):
            index = int(row * size + col)
            if index in indexes:
                for direction in Directions:
                    r = row + direction[0]
                    c = col + direction[1]
                    while 0 <= r and r < size and 0 <= c and c < size:
                        i = int(r*size+c)
                        if i in indexes:
                            return False
                        r = r + direction[0];
                        c = c + direction[1];
    return True

def maxQueens(boardSize, queens):
    assert boardSize >= 1
    maxQ = 0
    qSet = set()
    for i in range(int(boardSize*boardSize)):
        if not i in queens:
            queenSet = set(queens)
            queenSet.add(i)
            if isOK(queenSet, boardSize):
                (mq, qs) = maxQueens(boardSize, queenSet)
                if maxQ < mq:
                    maxQ = mq
                    qSet = qs
                "pegeon holes principle"
                if maxQ == boardSize:
                    return (maxQ, qSet)
    if maxQ > len(queens):
        return (maxQ, qSet)
    else:
        return (len(queens), queens)

def run():
    for i in range(8):
        boardSize = i + 1
        queens = maxQueens(boardSize, {})
        print(queens)
    return "done"

print(run())
