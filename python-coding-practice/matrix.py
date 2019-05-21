#!/usr/local/bin/python3
from enum import Enum

class Direction(Enum):
    clockWise = 1
    counterClockWise = 2

def rotate(m, direction):
    n = len(m)
    def swap(p1, p2):
        tmp = m[p1[0]][p1[1]]
        m[p1[0]][p1[1]] = m[p2[0]][p2[1]]
        m[p2[0]][p2[1]] = tmp
    def topLeft(r, i):
        return [r, r+i]
    def topRight(r, i):
        return [r+i, n-r-1]
    def bottomRight(r, i):
        return [n-r-1, n-r-1-i]
    def bottomLeft(r, i):
        return [n-r-1-i, r]
    for row in range(n//2):
        for col in range(n-2*row-1):
            if direction == Direction.clockWise:
                swap(topLeft(row,col), topRight(row,col))
                swap(topLeft(row,col), bottomRight(row,col))
                swap(topLeft(row,col), bottomLeft(row,col))
            elif direction == Direction.counterClockWise:
                swap(topLeft(row,col), bottomLeft(row,col))
                swap(topLeft(row,col), bottomRight(row,col))
                swap(topLeft(row,col), topRight(row,col))
    return m

def unit_tests():
    assert [[3,1],
            [4,2]] == rotate([[1,2],
                              [3,4]], Direction.clockWise)
    assert [[2,4],
            [1,3]] == rotate([[1,2],
                              [3,4]], Direction.counterClockWise)
    assert [[7,4,1],
            [8,5,2],
            [9,6,3]] == rotate([[1,2,3],
                                [4,5,6],
                                [7,8,9]], Direction.clockWise)
    assert [[3,6,9],
            [2,5,8],
            [1,4,7]] == rotate([[1,2,3],
                                [4,5,6],
                                [7,8,9]], Direction.counterClockWise)
    assert [['M','I','E','A'],
            ['N','J','F','B'],
            ['O','K','G','C'],
            ['P','L','H','D']] == rotate([['A','B','C','D'],
                                          ['E','F','G','H'],
                                          ['I','J','K','L'],
                                          ['M','N','O','P']], Direction.clockWise)
    assert [['D','H','L','P'],
            ['C','G','K','O'],
            ['B','F','J','N'],
            ['A','E','I','M']] == rotate([['A','B','C','D'],
                                          ['E','F','G','H'],
                                          ['I','J','K','L'],
                                          ['M','N','O','P']], Direction.counterClockWise)
    assert [['U','P','K','F','A'],
            ['V','Q','L','G','B'],
            ['W','R','M','H','C'],
            ['X','S','N','I','D'],
            ['Y','T','O','J','E']] == rotate([['A','B','C','D','E'],
                                              ['F','G','H','I','J'],
                                              ['K','L','M','N','O'],
                                              ['P','Q','R','S','T'],
                                              ['U','V','W','X','Y']], Direction.clockWise)
    assert [['E','J','O','T','Y'],
            ['D','I','N','S','X'],
            ['C','H','M','R','W'],
            ['B','G','L','Q','V'],
            ['A','F','K','P','U']] == rotate([['A','B','C','D','E'],
                                              ['F','G','H','I','J'],
                                              ['K','L','M','N','O'],
                                              ['P','Q','R','S','T'],
                                              ['U','V','W','X','Y']], Direction.counterClockWise)
    assert [['P','Q','R','S','T','A'],
            ['O','j','k','l','a','B'],
            ['N','i','4','1','b','C'],
            ['M','h','3','2','c','D'],
            ['L','g','f','e','d','E'],
            ['K','J','I','H','G','F']] == rotate([['A','B','C','D','E','F'],
                                                  ['T','a','b','c','d','G'],
                                                  ['S','l','1','2','e','H'],
                                                  ['R','k','4','3','f','I'],
                                                  ['Q','j','i','h','g','J'],
                                                  ['P','O','N','M','L','K']], Direction.clockWise)
    assert [['F','G','H','I','J','K'],
            ['E','d','e','f','g','L'],
            ['D','c','2','3','h','M'],
            ['C','b','1','4','i','N'],
            ['B','a','l','k','j','O'],
            ['A','T','S','R','Q','P']] == rotate([['A','B','C','D','E','F'],
                                                  ['T','a','b','c','d','G'],
                                                  ['S','l','1','2','e','H'],
                                                  ['R','k','4','3','f','I'],
                                                  ['Q','j','i','h','g','J'],
                                                  ['P','O','N','M','L','K']], Direction.counterClockWise)
    return "unit tests passed"

print(unit_tests())
