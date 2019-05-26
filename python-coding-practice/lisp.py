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
    def expectedArguments(self):
        return 2

class AtomicExpression:
    def __init__(self, repr):
        self.repr = repr
    def __str__(self):
        return 'AtomicExpression('+str(self.repr)+')'
    def eval(self, env):
        return self.repr.eval(env)

class Expression:    
    def __init__(self, oper, *exprs):
        self.oper = oper
        self.exprs = exprs
    def __str__(self):
        return 'Expression('+ str(self.oper) + str(self.exprs) +')'
    def eval(self, env):
        opt = self.oper.eval(env)
        evaledExprs = map(lambda x: x.eval(env), self.exprs)
        return functools.reduce(lambda a,b: opt(a,b), evaledExprs)

WhiteSpace = {' ', '\t'}
def skipWS(s, cursor):
    while cursor < len(s) and s[cursor] in WhiteSpace:
        cursor = cursor + 1
    return cursor

def operator(s, cursor):
    cursor = skipWS(s, cursor)
    if cursor < len(s) and s[cursor] in BuiltinOpts:
        return (Operator(s[cursor]), cursor+1)
    raise Exception('expect operator at', cursor)

def isNumeric(c):
    return '0' <= c and c <= '9'

def number(s, cursor):
    n = len(s)
    cursor = skipWS(s,cursor)
    start = cursor
    if cursor < n and s[cursor] == '-':
        cursor = cursor + 1
    if not cursor < n or not isNumeric(s[cursor]):
        raise Exception('expect numeric at', cursor)
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
    return (Number(s[start:cursor]), cursor)

def expression(s, cursor=0):
    cursor = skipWS(s, cursor)
    if s[cursor] == '(':
        opt = None
        (opt, cursor) = operator(s, cursor+1)
        (expr, cursor) = expression(s, cursor)
        exprs = [expr]
        cursor = skipWS(s, cursor)
        while cursor < len(s) and s[cursor] != ')':
            (expr, cursor) = expression(s, cursor)
            exprs.append(expr)
            cursor = skipWS(s, cursor)
        if cursor >= len(s) or s[cursor] != ')':
            raise Exception('expect ) at', cursor)
        else:
            return (Expression(opt, *exprs), cursor+1)
    else:
        (expr, cursor) = number(s, cursor)
        cursor = skipWS(s, cursor)
        return (expr, cursor)

commandMap = {
    'quit': lambda:exit()
}
def eval(cmd):
    if cmd[0] == ':':
        if cmd[1:] in commandMap:
            commandMap[cmd[1:]]()
    else:
        try:
            (expr, cursor) = expression(cmd)
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
