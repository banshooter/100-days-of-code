#!/usr/local/bin/python3
import sys
import operator

class Number:
    def __init__(self, repr):
        self.repr = repr
        self.value = float(repr)
    def __str__(self):
        return 'Number('+self.repr+')'
    def eval(self, env):
        return self.value

class Operator:
    builtinOpts = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv
    }
    def __init__(self, repr):
        self.repr = repr
    def __str__(self):
        return 'Operator('+self.repr+')'
    def eval(self, env):
        return builtinOpts[self.repr]
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
        return 'Expression('+ self.oper + self.exprs +')'
    def eval(self, env):
        opt = self.oper.eval(env)
        evaledExprs = map(lambda x: x.eval(env),exprs)
        return reduce(lambda a,b: opt(a,b), evaledExprs)

def expr(s):
    return s

commandMap = {
    'quit': lambda:exit()
}
def eval(cmd):
    if cmd[0] == ':':
        if cmd[1:] in commandMap:
            commandMap[cmd[1:]]()
    else:
        print(expr(cmd))

def repl():
    while True:
        eval(input("lisp>").rstrip())

if len(sys.argv) > 1:
    eval(sys.argv[1])
else:
    repl()
