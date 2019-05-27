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

BuiltinOpts = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv
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
        evaledExprs = map(lambda x: x.eval(env), self.exprs[1:])
        return functools.reduce(lambda a,b: opt(a,b), evaledExprs)

class QExpression:    
    def __init__(self, *exprs):
        self.exprs = exprs
    def eval(self, env):
        opt = self.oper.eval(env)
        return map(lambda x: x.eval(env), self.exprs)

WhiteSpace = {' ', '\t'}
def skipWS(s, cursor):
    while cursor < len(s) and s[cursor] in WhiteSpace:
        cursor = cursor + 1
    return cursor

def operator(s, cursor):
    cursor = skipWS(s, cursor)
    if cursor < len(s) and s[cursor] in BuiltinOpts:
        return (Operator(s[cursor]), cursor+1)
    else:
        return (None, cursor)

def isNumeric(c):
    return '0' <= c and c <= '9'

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
def expressionWithParan(s, cursor, openParan, closeParan):
    cursor = skipWS(s, cursor)
    if s[cursor] == openParan:
        exprs = []
        (expr, cursor) = expression(s, cursor+1)
        if expr:
            exprs.append(expr)
        cursor = skipWS(s, cursor)
        while cursor < len(s) and s[cursor] != ')':
            (expr, cursor) = expression(s, cursor)
            exprs.append(expr)
            cursor = skipWS(s, cursor)
        if cursor >= len(s) or s[cursor] != closeParan:
            raise Exception('expect '+closeParan+' at', cursor)
        else:
            return (Expression(exprs), cursor+1)
    else:
        return (None, cursor)

def sExpression(s, cursor):
    return expressionWithParan(s, cursor, '(',  ')')

def qExpression(s, cursor):
    return expressionWithParan(s, cursor, '{',  '}')

def expression(s, cursor=0):
    (expr,cursor) = sExpression(s,cursor)
    if expr:
        return (expr,skipWS(s, cursor))

    (expr, cursor) = number(s, cursor)
    if expr:
        return (expr, skipWS(s, cursor))

    (expr, cursor) = operator(s, cursor)
    if expr:
        return (expr, skipWS(s, cursor))

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
    return Expression(exprs)


commandMap = {
    'quit': lambda:exit()
}
def eval(cmd):
    if len(cmd) == 0:
        return

    if cmd[0] == ':':
        if cmd[1:] in commandMap:
            commandMap[cmd[1:]]()
    else:
        try:
            expr = lisp(cmd)
            if expr:
                result = expr.eval({})
            if result:
                print(result)
        except Exception as err:
            print(err)


def repl():
    while True:
        eval(input("lisp>").rstrip())


if len(sys.argv) > 1:
    eval(sys.argv[1])
else:
    repl()
