''' Typing an expression.
'''

from type2 import *
from pprinter2 import *

class Untypable (Exception):
    pass

class Nonuniquetype (Exception):
    pass

def join (*gens):
    for gen in gens:
        yield from gen

def typerequirements (parsed, symbols):
    # parsed, symbols -> gen [lhs, rhs]
    if exprtype (parsed) is Value:
        [head, val, vtype] = parsed
        if type (val) is str:
            if val in symbols:
                yield [vtype, symbols[val]]
            else:
                raise Untypable ()
        elif type (val) is Variable:
            if val.name in symbols:
                raise Untypable ()
            else:
                pass
    elif exprtype (parsed) is Lambda:
        [head, [head2, binder, body], ltype] = parsed
        [head3, var, vtype] = binder
        [head4, structbody, bodytype] = body
        yield [ltype, functiontype (vtype, bodytype)]
        yield from typerequirements (binder, symbols)
        yield from typerequirements (body, symbols)
    elif exprtype (parsed) is Apply:
        [head, [head2, function, operand], atype] = parsed
        [head3, f, ftype] = function
        [head4, o, otype] = operand
        yield [ftype, functiontype (otype, atype)]
        yield from typerequirements (function, symbols)
        yield from typerequirements (operand, symbols)

def enumvars (parsed):
    if exprtype (parsed) is Value:
        [head, val, vtype] = parsed
        if type (val) is Variable:
            yield parsed
    elif exprtype (parsed) is Lambda:
        [head, [head2, binder, body], ltype] = parsed
        yield from enumvars (binder)
        yield from enumvars (body)
    elif exprtype (parsed) is Apply:
        [head, [head2, function, operand], atype] = parsed
        yield from enumvars (function)
        yield from enumvars (operand)

def varrequirements (parsed):
    types = {}
    for varwithtype in enumvars (parsed):
        [head, var, vtype] = varwithtype
        if var.number not in types:
            types[var.number] = vtype
        else:
            yield [types[var.number], vtype]

def unificationtermtype (side):
    if type (side) is Blank:
        return 0
    elif type (side) is str:
        return 1
    elif type (side) is list:
        return 2
    else:
        raise ValueError ('Not a valid unification term.')
            
def substitute

def substituteall

def unify (requirements):
    # unification algorithm
    substitutions = []
    while requirements:
        lastcond = requirements.pop ()
        lastcond.sort (key = unificationtermtype)
        [lhs, rhs] = lastcond
        [ttlhs, ttrhs] = [unificationtermtype (lhs), unificationtermtype (rhs)]
        if ttlhs == 0:
            if lhs == rhs:
                pass
            elif occurs (lhs, rhs):
                return None
            else:
                substitutions.append ([lhs, rhs])
                requirements = substituteall (lhs, rhs, requirements)
        elif ttlhs == 1:
            if lhs == rhs:
                pass
            else:
                return None
        elif ttlhs == 2:
            if ttrhs != 2 or len (lhs) != len (rhs):
                return None
            else:
                for index in range (len (lhs)):
                    requirements.append ([lhs[index], rhs[index]])
    return substitutions

def trytype (parsed, symbols):
    requirements = list (join (typerequirements (parsed, symbols), varrequirements (parsed)))
    print (':::')
    pprinteach (requirements)
    print ('...')
    return
    assignments = unify (requirements)
    if isfullassignment (assignments):
        return substituteunification (parsed, assignments)
    elif assignments is None:
        raise Untypable ()
    else:
        raise Nonuniquetype ()

