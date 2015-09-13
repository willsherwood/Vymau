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
        A = self.next_expression()
        B = [self.next_expression()]
        while B[len(B) - 1] != ['end']:
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

    def process_for(self):
        preset = self.next_expression()
        boolean = self.next_expression()
        increment = self.next_expression()
        body = [self.next_expression()]
        while body[len(body) - 1] != ['end']:
            body.append(self.next_expression())
        body = body[:-1]
        self.expr = preset[:]
        self.evaluate(new_expr=False)
        while True:
            self.expr = boolean[:]
            result = self.evaluate(new_expr=False)
            if not result:
                return None
            for i in body:
                self.expr = i[:]
                self.evaluate(new_expr=False)
            self.expr = increment[:]
            self.evaluate(new_expr=False)

x = Interpreter("""
for =x-=y+1=iters 0 1
    <iters 100=iters+1iters
    p=t+x y
    =x y =y t
end
""")

while x.has_token():
    x.evaluate(new_expr=True)