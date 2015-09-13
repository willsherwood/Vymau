from Operator import Operator


class State(dict):
    def __getitem__(self, key):
        try:
            return super().__getitem__(key)
        except KeyError:
            return key

state = State()


def from_state(op):
    return lambda *args: op(*[state[y] for y in args])


@from_state
def add(x, y):
    return x + y
@from_state
def sub(x, y):
    return x - y
@from_state
def div(x, y):
    return x // y
@from_state
def times(x, y):
    return x * y
def equal(x, y):
    state[x] = state[y]
    return state[y]
@from_state
def less_than(x, y):
    return x < y
@from_state
def greater_than(x, y):
    return x > y
@from_state
def ternary(x, y, z):
    return y if x else z
@from_state
def _print(x):
    print(x)
    return x

state['+'] = Operator(2, add)
state['-'] = Operator(2, sub)
state['*'] = Operator(2, times)
state['/'] = Operator(2, div)

state['='] = Operator(2, equal)
state['<'] = Operator(2, less_than)
state['>'] = Operator(2, greater_than)
state['?'] = Operator(3, ternary)
state['p'] = Operator(1, _print)
state['while'] = Operator(0, None)
