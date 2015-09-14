import re

from Operator import Operator
from State import state
import State
from Tokenizer import Tokenizer


class Interpreter(object):
    def __init__(self, text):
        self.tokens = Tokenizer(text).tokenize()
        self.expr = []

    def next_expression(self):
        expr = [self.tokens.pop(0)]
        if expr[0] == '{':
            c = self.tokens.pop(0)
            self.tokens.insert(0, '{'+c)
            state['{'+c] = State.brace(int(c))
            return self.next_expression()
        elif type(state[expr[0]]) is Operator:
            for _ in range(state[expr[0]].arity):
                expr += self.next_expression()
        return expr

    def evaluate(self, new_expr=True):
        if new_expr:
            self.expr = self.next_expression()
        if len(self.expr) == 0:
            return None
        if re.fullmatch(r'while', self.expr[0]):
            return self.process_while()
        if re.fullmatch(r'for', self.expr[0]):
            return self.process_for()
        elif re.fullmatch(r'[0-9]+', self.expr[0]):
            return int(self.expr[0])
        elif type(state[self.expr[0]]) is Operator:
            return self.eval_token(self.expr.pop(0))
        return self.expr[0]

    def eval_token(self, token):
        if re.fullmatch(r'[0-9]+', token):
            return int(token)
        elif type(state[token]) is Operator:
            return state[token](*[self.eval_token(self.expr.pop(0)) for _ in range(state[token].arity)])
        return token

    def has_token(self):
        return len(self.tokens) > 0

    def process_while(self):
        a = self.next_expression()
        b = self.next_expression()
        while True:
            self.expr = a[:]
            result = self.evaluate(new_expr=False)
            if not result:
                return None
            self.expr = b[:]
            self.evaluate(new_expr=False)

    def process_for(self):
        preset = self.next_expression()
        boolean = self.next_expression()
        increment = self.next_expression()
        body = self.next_expression()
        self.expr = preset[:]
        self.evaluate(new_expr=False)
        while True:
            self.expr = boolean[:]
            result = self.evaluate(new_expr=False)
            if not result:
                return None
            self.expr = body[:]
            self.evaluate(new_expr=False)
            self.expr = increment[:]
            self.evaluate(new_expr=False)

x = Interpreter("""
for =x-=y+1=i 0 1<i 100=i+1i {3
    p=t+x y
    =x y=y t
""")

#for =x-=y+1=iters 0 1<iters 100=iters+1iters{2p=t+x y =x y =y t

while x.has_token():
    x.evaluate(new_expr=True)