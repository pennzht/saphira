class Expr:
    def __repr__ (self, showt = False):
        if showt:
            return self.directrepr () + ' : ' + repr (self.t)
        else:
            return self.directrepr ()

class Const (Expr):
    def __init__ (self, value, t = None):
        self.value = value
        self.t = t
    def directrepr (self):
        return self.value

class Variable (Expr):
    def __init__ (self, code, name, t = None):
        self.code = code
        self.name = name
        self.t = t
    def directrepr (self):
        return self.name + '#' + repr (self.code)

class Lambda (Expr):
    def __init__ (self, var, body, t = None):
        self.var = var
        self.body = body
        self.t = t
    def directrepr (self):
        return repr (self.var) + ' => ' + repr (self.body)

class Apply (Expr):
    def __init__ (self, rator, rand, t = None):
        self.rator = rator
        self.rand = rand
        self.t = t
    def directrepr (self):
        return '(' + repr (self.rator) + ' ' + repr (self.rand) + ')'

