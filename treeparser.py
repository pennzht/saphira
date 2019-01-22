class UnbalancedBracketError (Exception):
    pass

def code_to_tokens (code):
    tokens = []
    token = ''
    for ch in '\n' + code + '\n':
        if ch in [' ', '\t', '\n']:
            if token != '':
                tokens.append(token)
                token = ''
        elif ch in ['[', ']']:
            if token != '':
                tokens.append(token)
            tokens.append(ch)
            token = ''
        else:
            token += ch
    return tokens

def tokens_to_raw_tree (tokens):
    stack = [[]]
    for token in tokens:
        if token == '[':
            stack.append ([])
        elif token == ']':
            if len (stack) > 1:
                stack[-2].append (stack[-1])
                stack.pop ()
            else:
                raise UnbalancedBracketError ('Too many closing brackets.')
        else:
            stack[-1].append (token)
    if len (stack) == 1:
        return stack[0]
    else:
        raise UnbalancedBracketError ('Too many opening brackets.')

def raw_tree_to_tree (raw_tree):
    if type (raw_tree) is str:
        try:
            value = int (raw_tree)
        except:
            value = raw_tree
        finally:
            return value
    elif type (raw_tree) is list:
        return [raw_tree_to_tree (elem) for elem in raw_tree]

def code_to_tree (code):
    return raw_tree_to_tree (tokens_to_raw_tree (code_to_tokens (code)))

