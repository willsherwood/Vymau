from Operator import Operator


class State(dict):
    def __getitem__(self, key):
        try:
            return super().__getitem__(key)
        except KeyError:
            return key

state = State()

def add(x, y):
    return x + y
def sub(x, y):
    return x - y
def div(x, y):
    return x // y
def times(x, y):
    return x * y
def equal(x, y):
    state[x] = y
    return y
def less_than(x, y):
    return x < y
def greater_than(x, y):
    return x > y
def ternary(x, y, z):
    return y if x else z

state['+'] = Operator(2, add)
state['-'] = Operator(2, sub)
state['*'] = Operator(2, times)
state['/'] = Operator(2, div)

state['='] = Operator(2, equal)
state['<'] = Operator(2, less_than)
state['>'] = Operator(2, greater_than)
state['?'] = Operator(3, ternary)

