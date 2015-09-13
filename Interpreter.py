import re

import Characters
from State import state
from Tokenizer import Tokenizer


class Interpreter(object):
    def __init__(self, text):
        self.tokens = Tokenizer(text).tokenize()
        self.expr = []

    def next_expression(self):
        expr = [self.tokens.pop(0)]
        if expr[0] in Characters.operators:
            for _ in range(state[expr[0]].arity):
                expr += self.next_expression()
        return expr

    def evaluate(self):
        self.expr = self.next_expression()
        print('evaluating', ' '.join(self.expr))
        if re.fullmatch(r'[0-9]+', self.expr[0]):
            return int(self.expr[0])
        elif self.expr[0] in Characters.operators:
            return self.eval_token(self.expr.pop(0))
        return state[self.expr[0]]

    def eval_token(self, token):
        if re.fullmatch(r'[0-9]+', token):
            return int(token)
        elif token in Characters.operators:
            return state[token](*[self.eval_token(self.expr.pop(0)) for _ in range(state[token].arity)])
        return state[token]

    def has_token(self):
        return len(self.tokens) > 0

x = Interpreter('=x *2 5=y+1x y')
while x.has_token():
    print(x.evaluate())