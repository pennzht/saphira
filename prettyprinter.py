infixOperators = ['|-', '->']

def pp_tree (tree):
    if type (tree) is int:
        return str (tree)
    elif type (tree) is str:
        return tree
    elif type (tree) is list:
        if len (tree) == 0:
            return '[]'
        else:
            head = tree[0]
            if head in infixOperators and len (tree) == 3:
                return '(' + pp (tree[1]) + ' ' + head + ' ' + pp (tree[2]) + ')'
            else:
                return '[' + ' '.join ([pp (x) for x in tree]) + ']'

def pp_sexp (sexp):
    if type (sexp) is not tuple and sexp is not None:
        if type (sexp) is int:
            return str (sexp)
        else:
            return sexp
    else:
        collection = []
        focus = sexp
        while type (focus) is tuple:
            collection.append (pp_sexp (focus[0]))
            focus = focus[1]
        if focus is not None:
            collection.append ('.')
            collection.append (pp_sexp (focus))
        return '[' + ' '.join (collection) + ']'
