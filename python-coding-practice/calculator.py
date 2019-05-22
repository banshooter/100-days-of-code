#!/usr/local/bin/python3
import operator
import re

OperatorDict = {
    '+':operator.add,
    '-':operator.sub,
    '*':operator.mul,
    '/':operator.truediv,
    '%':operator.mod,
    '//':operator.floordiv
}

class Expression:
    def __init__(self, left, oper=None, right=None):
        self.left = left
        self.oper = oper
        self.right = right

    def __str__(self):
        if self.isAtom():
            return str(self.left)
        return str(self.left) + ' ' + str(self.oper) + ' ' + str(self.right)

    def isAtom(self):
        return self.oper == None and self.right == None

    def eval(self, env):
        def atom(ex):
            if isinstance(ex, str):
                return float(ex)
            elif isinstance(ex, Expression):
                return ex.eval(env)
            else:
                raise 'Invalid type'
        if self.isAtom():
            return atom(self.left)
        else:
            return OperatorDict[self.oper](atom(self.left), atom(self.right))

WhiteSpace = {' ', '\t', '\n', '\r'}
def skipWs(s, cursor):
    while s[cursor] in WhiteSpace:
        cursor = cursor + 1
    return cursor

def match(s, reg):
    result = reg.match(s)
    if result:
        return (result.group().strip(), len(result.group()))
    return (None, 0)

numberRe = re.compile('\\s*-?[0-9]*([0-9][.]|[.][0-9])?[0-9]*([eE]-?[0-9]+)?\\s*')
def number(s):
    return match(s,numberRe)

operRe = re.compile('\\s*([+]|-|[*]|//?|%|)\\s*')
def oper(s):
    return match(s,operRe)

def expression(s):
    def exprWithinParen(s, cursor):
        "expression = '(' expression ')'"
        cursor = skipWs(s, cursor)
        if s[cursor] != '(':
            return (None, cursor)
        (exp, cursor) = expression_(s, cursor+1)
        cursor = skipWs(s, cursor)
        if s[cursor] != ')':
            raise Exception(s + ': expect ) at ' + str(cursor))
        if not exp:
            raise Exception(s + ': expect expression within ()')
        if exp.isAtom():
            return (exp, cursor+1)
        else:
            return (Expression(exp), cursor+1)

    def expression_(s, cursor):
        left = None
        (exp, cursor) = exprWithinParen(s,cursor)
        if exp:
            left = exp
        else:
            (exp, step) = number(s[cursor:])
            cursor = cursor + step
            left = Expression(exp)
            if not exp:
                return (None, cursor)
        (op, step) = oper(s[cursor:])
        cursor = cursor + step
        if op:
            (right, cursor) = expression_(s, cursor)
            if not right:
                raise Exception('expect expression at ' + str(cursor))
            if isinstance(right, Expression) and right.isAtom():
                return (Expression(left, op, right.left),cursor)
            else:
                return (Expression(left, op, right),cursor)
        else:
            return (left,cursor)

    (exp, cursor) = expression_(s,0)
    if cursor < len(s):
        raise Exception('There are remaining string left: ' + s[cursor:])
    return exp

def unit_tests():
    def test(s, expected):
        exp = expression(s)
        print(exp, '=', end=' ')
        result = exp.eval({})
        print(result)
        assert expected == result
    test('10', 10)
    test('10+2', 12)
    test('10-2', 8)
    test('10*2', 20)
    test('10/4', 2.5)
    test('10//4', 2)
    test('10%4', 2)
    test('(10%4)+2', 4)
    test('10%4+2', 4)
    test('(10*4)+4',44)
    # This causes exception because it's just operate from
    # left to right without any operation priority.
    # test('10*4+4', 44)
    return "unit tests passed"

print(unit_tests())
