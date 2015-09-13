import re

from Operator import Operator
from State import state
from Tokenizer import Tokenizer


class Interpreter(object):
    def __init__(self, text):
        self.tokens = Tokenizer(text).tokenize()
        self.expr = []

    def next_expression(self):
        expr = [self.tokens.pop(0)]
        if type(state[expr[0]]) is Operator:
            for _ in range(state[expr[0]].arity):
                expr += self.next_expression()
        return expr

    def evaluate(self, new_expr=True):
        if new_expr:
            self.expr = self.next_expression()
        if len(self.expr) == 0:
            return None
        if re.fullmatch(r'while', self.expr[0]):
            A = self.next_expression()
            B = [self.next_expression()]
            while B[len(B)-1] != ['end']:
                B.append(self.next_expression())
                print(B)
            B = B[:-1]
            print(B)
            while True:
                self.expr = A[:]
                result = self.evaluate(new_expr=False)
                if not result:
                    return None
                for i in B:
                    self.expr = i[:]
                    self.evaluate(new_expr=False)
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


x = Interpreter("""
=x -=y +1=iters 0 1
while <iters 15
    p=t+x y
    =x y
    =y t
    =iters+1iters
end
""")

while x.has_token():
    x.evaluate(new_expr=True)