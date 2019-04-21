'''
Parses an []-expression into lambda-expression waiting to be typed
'''

from type2 import *

class SyntaxError (Exception):
    pass

def curry (expr):
    if type (expr) is str:
        return expr
    elif type (expr) is list and len (expr) >= 2 and expr[0] == '=>':
        [head, *variables, body] = expr
        if variables == []:
            return curry (body)
        else:
            [firstvar, *restvars] = variables
            return ['=>', firstvar, curry (['=>', *restvars, body])]
    elif type (expr) is list and len (expr) >= 1:
        [*function, operand] = expr
        if function == []:
            return curry (operand)
        else:
            return [curry (function), curry (operand)]
    else:
        raise SyntaxError (expr)

def restructure (expr):
    if type (expr) is str and expr != '=>':
        # expr is a value
        return Value (expr, Blank ())
    elif type (expr) is list and expr[0] == '=>':
        # expr is a lambda
        [head, var, body] = expr
        if type (var) is str:
            return Lambda (restructure (var), restructure (body), Blank ())
        else:
            raise SyntaxError (expr)
    elif type (expr) is list:
        # expr is an application
        [function, operand] = expr
        return Apply (restructure (function), restructure (operand), Blank ())
    else:
        raise SyntaxError (expr)

def numbervariables (parsed, start, vartable):
    if exprtype (parsed) is Value:
        [head, val, vtype] = parsed
        if val in vartable and vartable[val]:
            newexpr = Value (Variable (val, vartable[val][-1]), vtype)
        else:
            newexpr = parsed
        return newexpr, start
    elif exprtype (parsed) is Lambda:
        [head, [head2, binder, body], ltype] = parsed
        [head3, var, vartype] = binder
        if var not in vartable:
            vartable[var] = []
        vartable[var].append (start)
        newbinder = Value (Variable (var, start), vartype)
        newbody, newstart = numbervariables (body, start + 1, vartable)
        newexpr = Lambda (newbinder, newbody, ltype)
        vartable[var].pop ()
        return newexpr, newstart
    elif exprtype (parsed) is Apply:
        [head, [head2, function, operand], atype] = parsed
        newfunction, start1 = numbervariables (function, start, vartable)
        newoperand, start2 = numbervariables (operand, start1, vartable)
        newexpr = Apply (newfunction, newoperand, atype)
        return newexpr, start2

def numberblanks (parsed, start):
    if exprtype (parsed) is Value:
        [head, val, vtype] = parsed
        vtype = Blank (start)
        newexpr = Value (val, vtype)
        newstart = start + 1
    elif exprtype (parsed) is Lambda:
        [head, [head2, binder, body], ltype] = parsed
        newbinder, start = numberblanks (binder, start)
        newbody, start = numberblanks (body, start)
        ltype = Blank (start)
        newexpr = Lambda (newbinder, newbody, ltype)
        newstart = start + 1
    elif exprtype (parsed) is Apply:
        [head, [head2, function, operand], atype] = parsed
        newfunction, start = numberblanks (function, start)
        newoperand, start = numberblanks (operand, start)
        atype = Blank (start)
        newexpr = Apply (newfunction, newoperand, atype)
        newstart = start + 1
    else:
        raise Exception (parsed)
    return newexpr, newstart

def exprparse (expr):
    expr = curry (expr)
    parsed = restructure (expr)
    parsed, _ = numbervariables (parsed, 0, {})
    parsed, _ = numberblanks (parsed, 0)
    return parsed

