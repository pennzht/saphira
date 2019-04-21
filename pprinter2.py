def pformat (expr, *optional):
    if type (expr) is list:
        return '[' + ' '.join (pformat (elem, *optional) for elem in expr) + ']'
    elif type (expr) is str:
        return expr
    else:
        return repr (expr)

def pprint (expr):
    print (pformat (expr))

def pprinteach (lst):
    if type (lst) is list:
        for elem in lst:
            pprint (elem)
    elif type (lst) is dict:
        for elem in lst:
            print (pformat (elem), '--->', pformat (lst[elem]))