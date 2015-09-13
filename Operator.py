class Operator(object):
    def __init__(self, arity, method):
        self.arity = arity
        self.method = method

    def __call__(self, *args, **kwargs):
        return self.method(*args, **kwargs)

    def __repr__(self):
        return self.method.__repr__()