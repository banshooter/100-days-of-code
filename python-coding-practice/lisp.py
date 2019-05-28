#!/usr/local/bin/python3
import sys
import operator
import functools

class Number:
    def __init__(self, repr):
        self.repr = repr
        self.value = float(repr)
    def __str__(self):
        return 'Number('+self.repr+')'
    def eval(self, env):
        return self.value

def evalOpt(x):
    if isinstance(x, list):
        if callable(x[0]):
            return x[0](x[1:])
        else:
            return x[0]
    elif callable(x):
        return x()
    else:
        return x

BuiltinOpts = {
    '+': lambda x: functools.reduce(lambda a,b: a+b, x),
    '-': lambda x: functools.reduce(lambda a,b: a-b, x),
    '*': lambda x: functools.reduce(lambda a,b: a*b, x),
    '/': lambda x: functools.reduce(lambda a,b: a/b, x),
    'head': lambda x: x[0][0:1],
    'tail': lambda x: x[0][1:],
    'join': lambda x: functools.reduce(lambda a,b: a+b, x),
    'list': lambda x: x,
    'eval': lambda x: evalOpt(x[0]),
}
class Operator:
    def __init__(self, repr):
        self.repr = repr
    def __str__(self):
        return 'Operator('+self.repr+')'
    def eval(self, env):
        return BuiltinOpts[self.repr]

class Expression:    
    def __init__(self, exprs):
        self.exprs = exprs
    def eval(self, env):
        if len(self.exprs) == 0:
            return None
        opt = self.exprs[0].eval(env)
        if len(self.exprs) == 1:
            return opt
        evaledExprs = list(map(lambda x: x.eval(env), self.exprs[1:]))
        return opt(evaledExprs)

class QExpression:    
    def __init__(self, exprs):
        self.exprs = exprs
    def eval(self, env):
        return list(map(lambda x: x.eval(env), self.exprs))

WhiteSpace = {' ', '\t'}
def skipWS(s, cursor):
    while cursor < len(s) and s[cursor] in WhiteSpace:
        cursor = cursor + 1
    return cursor

def isNumeric(c):
    return '0' <= c and c <= '9'

def isAlphabet(c):
    return ('a' <= c and c <= 'z') or \
           ('A' <= c and c <= 'Z') or \
           '_' == c

def isAlphaNumeric(c):
    return isNumeric(c) or isAlphabet(c)

def operator(s, cursor):
    cursor = skipWS(s, cursor)
    if cursor < len(s) and s[cursor] in BuiltinOpts:
        return (Operator(s[cursor]), cursor+1)
    if isAlphabet(s[cursor]):
        start = cursor
        while isAlphaNumeric(s[cursor]):
            cursor = cursor+1
        return (Operator(s[start:cursor]), cursor)
    else:
        return (None, cursor)

def number(s, cursor):
    n = len(s)
    cursor = skipWS(s,cursor)
    start = cursor
    if cursor < n and s[cursor] == '-':
        cursor = cursor + 1
    if cursor < n and isNumeric(s[cursor]):
        while cursor < n and isNumeric(s[cursor]):
            cursor = cursor + 1
        if cursor < n and s[cursor] == '.':
            cursor = cursor + 1
            while(cursor < n and isNumeric(s[cursor])):
                cursor = cursor + 1
        if cursor < n and s[cursor] == 'e':
            cursor = cursor + 1
            if cursor < n and s[cursor] == '-':
                cursor = cursor + 1
            if not cursor < n or not isNumeric(s[cursor]):
                raise Exception('expect numeric at', cursor)
            while cursor < n and isNumeric(s[cursor]):
                cursor = cursor + 1
    if start == cursor or (start == cursor-1 and s[start] == '-'):
        return (None, start)
    else:
        return (Number(s[start:cursor]), cursor)

"""
    sexpr  : '(' <expr>* ')' ;               \
    expr   : <number> | <symbol> | <sexpr> ; \
    lispy  : /^/ <expr>* /$/ ;               \
"""
def expressionWithParan(s, cursor, constructor, openParen, closeParen):
    cursor = skipWS(s, cursor)
    if s[cursor] == openParen:
        exprs = []
        (expr, cursor) = expression(s, cursor+1)
        if expr:
            exprs.append(expr)
        cursor = skipWS(s, cursor)
        while cursor < len(s) and s[cursor] != closeParen:
            (expr, cursor) = expression(s, cursor)
            exprs.append(expr)
            cursor = skipWS(s, cursor)
        if cursor >= len(s) or s[cursor] != closeParen:
            raise Exception('expect '+closeParen+' at', cursor)
        else:
            return (constructor(exprs), cursor+1)
    else:
        return (None, cursor)

def sExpression(s, cursor):
    return expressionWithParan(s, cursor, lambda x: Expression(x), '(',  ')')

def qExpression(s, cursor):
    return expressionWithParan(s, cursor, lambda x: QExpression(x), '{',  '}')

def expression(s, cursor=0):
    (expr,cursor) = sExpression(s,cursor)
    if expr:
        return (expr,skipWS(s, cursor))

    (expr,cursor) = qExpression(s,cursor)
    if expr:
        return (expr,skipWS(s, cursor))

    (expr, cursor) = number(s, cursor)
    if expr:
        return (expr, skipWS(s, cursor))

    (expr, cursor) = operator(s, cursor)
    if expr:
        return (expr, skipWS(s, cursor))
    if cursor < len(s):
        raise Exception('invalid expression at', cursor)
    return None

def lisp(s):
    exprs = []
    (expr, cursor) = expression(s, 0)
    if not expr:
        return None
    exprs = [expr]
    while cursor < len(s):
        (expr, cursor) = expression(s, cursor)
        if expr:
            exprs.append(expr)
        else:
            break
    if cursor < len(s):
        raise Exception('It\'s expected to end but it isn\'t at ', cursor)
    if len(exprs) > 0 and isinstance(exprs[0], Operator):
        return Expression(exprs)
    elif len(exprs) == 1:
        return exprs[0]
    else:
        return exprs


commandMap = {
    'quit': lambda:exit()
}
def eval(cmd):
    if len(cmd) == 0:
        return None

    if cmd[0] == ':':
        if cmd[1:] in commandMap:
            commandMap[cmd[1:]]()
    else:
        try:
            exprs = lisp(cmd)
            if exprs:
                for expr in exprs:
                    result = expr.eval({})
                    if result:
                        return result
        except Exception as err:
            return err
    return None

def repl():
    while True:
        result = eval(input("lisp>").rstrip())
        if result:
            print(result)

def unit_tests():
    def test(s, expected):
        result = lisp(s).eval({})
        if result != expected:
            print("actual ", result)
        assert expected == result
    test('+ 1 2', 3.0)
    test('+ 1 2 3.5', 6.5)
    test('+ 1 (* 2 3.5)', 8.0)
    test('(+ 1 (* 2 3.5))', 8.0)
    test('(* 1 (* 2 3.5))', 7.0)
    test('(/ (* 2 3.5) 1)', 7.0)
    test('{ 1 2 3 }', [1, 2, 3])
    test('head { 1 2 3 }', [1])
    test('tail { 1 2 3 }', [2,3])
    test('join { 1 2 3 } { 4 }', [1,2,3,4])
    test('list 1 2 3 ', [1,2,3])
    test('eval {head (list 1 2 3 4)}', [1])
    test('eval (tail { tail tail { 5 6 7 } })', [6,7])
    test('eval (head {(+ 1 2) (+ 10 20)})', 3)
    return "unit tests passed"


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "test":
            print(unit_tests())
        else:
            result = eval(sys.argv[1])
            if result:
                print(result)
    else:
        repl()
