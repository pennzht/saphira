def pformat (expr, *optional):
    if type (expr) is list:
        return '[' + ' '.join (pformat (elem, *optional) for elem in expr) + ']'
    elif type (expr) is str:
        return expr

def pprint (expr):
    print (pformat (expr))

def pprinteach (lst):
    for elem in lst:
        pprint (elem)

