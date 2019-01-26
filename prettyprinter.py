infixOperators = ['|-', '->']

def pp (tree):
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
                return '[' + ', '.join ([pp (x) for x in tree]) + ']'
