import re

import Characters
from State import state
from Tokenizer import Tokenizer


class Interpreter(object):
    def __init__(self, text):
        self.tokens = Tokenizer(text).tokenize()

    def do_expr(self):
        return self.evaluate(self.tokens.pop(0))

    def evaluate(self, token):
        if re.fullmatch(r'[0-9]+', token):
            return int(token)
        elif token in Characters.operators:
            return state[token](*[self.do_expr() for _ in range(state[token].arity)])
        return str(token)


x = Interpreter('-*7-11 4/+1 2-4 3')
print(x.do_expr())