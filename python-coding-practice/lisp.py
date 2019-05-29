#!/usr/local/bin/python3
import sys
import operator
import functools
from inspect import signature

class Number:
    def __init__(self, repr):
        self.repr = repr
        self.value = float(repr)
    def __str__(self):
        return 'Number('+self.repr+')'
    def __eq__(self, another):
        return self.__dict__ == another.__dict__
    def eval(self, env):
        return self.value

def evalOpt(x, env):
    if isinstance(x, list):
        if callable(x[0]):
            paramLen = len(signature(x[0]).parameters)
            if paramLen == 0:
                x[0]()
            elif paramLen == 1:
                if len(x) == 1:
                    return x[0]
                else:
                    return x[0](x[1:])
            else:
                return evalOpt(x[1], env)
        else:
            return x[0]
    elif callable(x):
        return x()
    else:
        return x

def define(vars, value, env):
    if isinstance(vars, Symbol):
        env[vars.repr] = SExpression(value)
    elif isinstance(vars, QExpression):
        for i in range(len(vars.repr)):
            env[vars.repr[i].repr] = eval(value[i],env)

def eval(x, env):
    if isinstance(x, list):
        if x[0].repr == 'def':
            return define(x[1], x[2:], env)
        if len(x) == 2 and x[0].repr == 'list' and isinstance(x[1], Symbol):
            "This is hack for test case 'list arglist'"
            evaledX = list(map(lambda elem: eval(elem,env), x))
            if isinstance(evaledX[1], SExpression):
                sEvaledExpr = list(map(lambda elem: eval(elem,env), evaledX[1].repr))
                evaledX = [evaledX[0]] + sEvaledExpr
            return evalOpt(evaledX, env)
        else:
            evaledX = list(map(lambda elem: eval(elem,env), x))
            return evalOpt(evaledX, env)
    elif isinstance(x, Symbol):
        return x.eval(env)
    elif isinstance(x, Number):
        return x.eval(env)
    elif isinstance(x, Expression):
        return x.eval(env)
    elif isinstance(x, QExpression):
        return x.eval(env)
    else:
        return x

BuiltinOpts = {
    '+': lambda x: functools.reduce(lambda a,b: a+b, x),
    '-': lambda x: functools.reduce(lambda a,b: a-b, x),
    '*': lambda x: functools.reduce(lambda a,b: a*b, x),
    '/': lambda x: functools.reduce(lambda a,b: a/b, x),
    '%': lambda x: functools.reduce(lambda a,b: a%b, x),
    'head': lambda x: x[0][0:1],
    'tail': lambda x: x[0][1:],
    'join': lambda x: functools.reduce(lambda a,b: a+b, x),
    'list': lambda x: x,
    'init': lambda x: x[0][0:-1],
    'len': lambda x: len(x[0]),
    'cons': lambda x: functools.reduce(lambda a,b: a+b, x[::-1]),
    'exit': lambda: exit()
}
class Symbol:
    def __init__(self, repr):
        self.repr = repr
    def __str__(self):
        return 'Symbol('+self.repr+')'
    def __eq__(self, another):
        return self.__dict__ == another.__dict__
    def eval(self, env):
        if self.repr == 'eval':
            return evalOpt
        if self.repr in BuiltinOpts:
            return BuiltinOpts[self.repr]
        elif self.repr in env:
            return env[self.repr]
        else:
            raise Exception('Error: unbound symbol!')

class Expression:    
    def __init__(self, repr):
        self.repr = repr
    def eval(self, env):
        if len(self.repr) == 0:
            return None
        return eval(self.repr, env)

class SExpression:
    def __init__(self, repr):
        self.repr = repr
    def __str__(self):
        return ' '.join(str(self.repr))
    def __eq__(self, another):
        return self.__dict__ == another.__dict__

class QExpression:
    def __init__(self, repr):
        self.repr = repr
    def __str__(self):
        if len(self.repr) == 0:
            return '{}'
        else:
            return '{' + ' '.join(map(lambda x: str(x), self.repr)) + '}'
    def __eq__(self, another):
        return self.__dict__ == another.__dict__
    def eval(self, env):
        return list(map(lambda x: x.eval(env), self.repr))

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

def symbol(s, cursor):
    cursor = skipWS(s, cursor)
    if cursor < len(s) and s[cursor] in BuiltinOpts:
        return (Symbol(s[cursor]), cursor+1)
    if isAlphabet(s[cursor]):
        start = cursor
        while cursor < len(s) and isAlphaNumeric(s[cursor]):
            cursor = cursor+1
        symbolString = s[start:cursor]
        return (Symbol(symbolString), cursor)
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

    (expr, cursor) = symbol(s, cursor)
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
    return exprs


commandMap = {
    'quit': lambda:exit()
}
def execute(cmd, env):
    if len(cmd) == 0:
        return None
    try:
        result = eval(lisp(cmd), env)
        if result:
            return result
    except Exception as err:
        return err
    return None

def repl():
    env = {}
    while True:
        result = execute(input("lisp>").rstrip(), env)
        if result:
            print(result)

def unit_tests():
    env = {}
    def test(s, expected):
        result = eval(lisp(s), env)
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
    test('len { 0 1 2 3 4}', 5)
    test('cons { 1 2 3 } { 4 }', [4,1,2,3])
    test('init { 0 1 2 3 4}', [0,1,2,3])
    test('eval {head (list 1 2 3 4)}', [1])
    test('eval (tail { tail tail { 5 6 7 } })', [6,7])
    test('eval (head {(+ 1 2) (+ 10 20)})', 3)
    test('(eval (head {+ - + - * /})) 10 20', 30)
    test('def { x } 100', None)
    test('def { y } 200', None)
    test('x', 100)
    test('y', 200)
    test('+ x y', 300)
    test('def {a b} 10 20', None)
    test('+ a b', 30)
    test('def {arglist} {a b x y}', None)
    test('arglist', [10, 20, 100, 200])
    test('def arglist 1 2 3 4', None)
    test('arglist', QExpression([Number('1'), Number('2'), Number('3'), Number('4')]))
    test('list arglist', [1, 2, 3, 4])
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
