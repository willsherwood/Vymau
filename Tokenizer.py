import re
import Characters


class Tokenizer(object):
    def __init__(self, string):
        self.text = re.split(r'\s+', string)

    def tokenize(self):
        temp = []
        for i in self.text:
            x = re.split('([' + re.escape(Characters.operators) + '])', i)
            y = [re.split(r'(^[0-9]+)', t) for t in x]
            for t in y:
                for j in t:
                    if len(j) > 0:
                        temp += [j]
        self.text = temp
        print(self.text)
        return self.text