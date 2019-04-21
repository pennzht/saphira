def Value (val, vtype):
    return [':', val, vtype]

def Lambda (binder, body, ltype):
    return [':', ['lambda', binder, body], ltype]

def Apply (function, operand, atype):
    return [':', ['apply', function, operand], atype]

def exprtype (expr):
    if len (expr) == 3:
        [head, value, exprtype] = expr
        if head == ':' and type (value) in [str, Variable]:
            return Value
        elif head == ':' and type (value) is list and len (value) == 3 and value[0] == 'lambda':
            return Lambda
        elif head == ':' and type (value) is list and len (value) == 3 and value[0] == 'apply':
            return Apply
        else:
            return None
    else:
        return None

def functiontype (domain, codomain):
    return ['->', domain, codomain]

class Blank:
    def __init__ (self, number=None):
        self.number = number
    def __eq__ (self, other):
        return self.number == other.number
    def __repr__ (self):
        return f'_{self.number}'

class Variable:
    def __init__ (self, name=None, number=None):
        self.name = name
        self.number = number
    def __eq__ (self, other):
        return self.number == other.number
    def __repr__ (self):
        return f'{self.name}#{self.number}'

