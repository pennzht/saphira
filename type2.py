class Value:
    def __init__ (self, value, t):
        self.value = value
        self.t = t

class Lambda:
    def __init__ (self, bind, value, t):
        self.bind = bind
        self.value = value
        self.t = t

class Apply:
    def __init__ (self, rator, rand, t):
        self.rator = rator
        self.rand = rand
        self.t = t

class Basictype:
    def __init__ (self, label):
        self.label = label
    def __eq__ (self, other):
        return self.label == other.label

