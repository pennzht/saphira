from treeparser2a import *
from pprinter2 import *
from sys import argv

functions = {}
axioms = {}
theorems = {}
    

def replace (expr, variables, values):
    replacements = {var : val for (var, val) in zip (variables, values)}
    return replacedict (expr, replacements)

def replacedict (expr, replacements):
    if type (expr) is list:
        return [replacedict (subexpr, replacements) for subexpr in expr]
    else:
        return expr if expr not in replacements else replacements[expr]

def evaluate (expr):
    global functions
    if type (expr) is not list:
        return expr
    elif expr[0] == 'quote':
        return expr[1]
    elif expr[0] == 'cons':
        return [evaluate (expr[1]), evaluate (expr[2])]
    elif expr[0] == 'first':
        return evaluate (expr[1][0])
    elif expr[0] == 'rest':
        return evaluate (expr[1][1:])
    elif expr[0] in ['both', 'all']:
        return all (evaluate (subexpr) for subexpr in expr[1:])
    elif expr[0] in ['either', 'any']:
        return any (evaluate (subexpr) for subexpr in expr[1:])
    elif expr[0] == '=':
        return evaluate (expr[1]) == evaluate (expr[2])
    elif expr[0] == 'not':
        return not evaluate (expr[1])
    elif expr[0] == 'list':  
        return [evaluate (subexpr) for subexpr in expr[1:]]
    elif expr[0] == 'cases':
        return evaluate_cases (expr)
    elif expr[0] == 'match':
        return evaluate_match (expr)
    elif expr[0] == 'in':
        return evaluate (expr[1]) in evaluate (expr[2])
    elif expr[0] in functions:
        return evaluate_function (expr)
    else:
        raise ValueError (expr)

def evaluate_cases (expr):
    if len (expr) <= 1:
        return False
    [_cases, cond1, ans1, *rest] = expr
    if evaluate (cond1):
        return evaluate (ans1)
    else:
        return evaluate_cases ([_cases, *rest])

def trymatch (value, pattern):
    if type (pattern) is str:
        return (True, {pattern: value})
    elif pattern[0] == 'quote':
        if value == pattern[1]:
            return (True, {})
        else:
            return (False, {})
    else:
        if type (value) is not list:
            return (False, {})
        elif len (value) != len (pattern):
            return (False, {})
        else:
            matches = {}
            for index in range (len (pattern)):
                (newhasmatch, newmatches) = trymatch (value[index], pattern[index])
                if not newhasmatch:
                    return (False, {})
                else:
                    for (a, b) in newmatches.items ():
                        matches[a] = b
            return (True, matches)

def evaluate_match (expr):
    [_match, value, pattern, transform] = expr
    (hasmatch, matches) = trymatch (evaluate (value), pattern)
    if hasmatch:
        return evaluate (replacedict (transform, {index: ['quote', word] for (index, word) in matches.items ()}))
    else:
        return False

def evaluate_function (expr):
    global functions
    [function_name, *args] = expr
    function = functions[function_name]
    return evaluate (replace (function[1], function[0], args))

def main ():
    
    parser = Parser ()

    global functions
    global axioms
    global theorems
    
    with open ('a3.axioms', 'r') as axiomsfile:
        for expr in parser.parsestream (axiomsfile):
            # pprint (expr)
            if expr[0] == 'def':
                [_def, [fn_name, *fn_arg_names], fn_body] = expr
                functions[fn_name] = [fn_arg_names, fn_body]
            elif expr[0] == 'axiom':
                [_axiom, axiom_name,
                 _blanks, blanks,
                 _require, requirements,
                 _from, sources,
                 _obtain, target] = expr
                axioms[axiom_name] = [blanks, requirements, sources, target]
    
    # verify
    filename = argv [1:] [0]
    
    parser = Parser ()
    
    
    with open (filename, 'r') as theoryfile:
        for expr in parser.parsestream (theoryfile):
            if expr[0] == 'prove':
                [_prove, theorem_name, my_target, [my_axiom_name, *my_blanks], my_sources] = expr
                # print (my_axiom_name)
                # print (my_blanks)
                # print (my_sources)
                # print (my_target)
    
                if my_axiom_name not in axioms:
                    print (f'Axiom {my_axiom_name} not found.')
                else:
                    axiom = axioms[my_axiom_name]
                    [blanks, requirements, sources, target] = axiom
                    if len (blanks) != len (my_blanks):
                        print (f'In {pformat(expr)}: {len (blanks)} blanks needed but {len (my_blanks)} provided.')
                    elif len (sources) != len (my_sources):
                        print (f'In {pformat(expr)}: {len (sources)} sources needed but {len (my_sources)} provided.')
                    elif replace ([sources, target], blanks, my_blanks) != [[theorems[s] for s in my_sources], my_target]:
                        print (f'Non-matching pattern in {pformat (expr)}.')
                    elif any (evaluate (replace (requirement, blanks, [['quote', r] for r in my_blanks])) != True for requirement in requirements):
                        print (f'Requirement not met in {pformat (expr)}.')
                        print ([replace (requirement, blanks, [['quote', r] for r in my_blanks]) for requirement in requirements])
                    else:
                        theorems[theorem_name] = my_target
                        print ('Success.')

if __name__ == '__main__':
    main ()