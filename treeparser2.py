class UnbalancedBracketError (Exception):
    pass

class ParseError (Exception):
    pass

def follow (*gens):
    for gen in gens:
        yield from gen

def gentokens (line):
    token = ''
    for char in follow (line, ['\n']):
        if char in ['[', ']']:
            if token:
                yield token
            token = ''
            yield char
        elif char in [' ', '\n', '\t']:
            if token:
                yield token
            token = ''
        else:
            token = token + char

class Parser:
    def __init__ (self):
        self.stack = [[]]
        self.exprcount = 0
        self.uncommitted = []
    def hasnextexpr (self):
        if self.exprcount == len (self.stack[0]):
            return False
        else:
            return True
    def nextexpr (self):
        if self.hasnextexpr ():
            ans = self.stack[0][self.exprcount]
            self.exprcount += 1
            return ans
        else:
            raise StopIteration ()
    def stackdepth (self):
        return len (self.stack) - 1
    def prompt (self, cutoff = 16, tab = '  '):
        indent = self.stackdepth ()
        indentshow = str (indent)
        if len (indentshow) > 2:
            indentshow = '++'
        else:
            indentshow = ' '*(2 - len (indentshow)) + indentshow
        tabs = min (cutoff, indent)
        return indentshow + ' ? ' + tab * tabs
    def parseline (self, line):
        try:
            for token in gentokens (line):
                if token == '#:' :
                    break
                self.parsetoken (token)
            self.commit ()
        except ParseError:
            self.rollback ()
            raise ParseError ()
    def parsetoken (self, token):
        if token == '[':
            self.stack.append ([])
            self.uncommitted.append (token)
        elif token == ']':
            if len (self.stack) > 1:
                last = self.stack.pop ()
                self.stack[-1].append (last)
                self.uncommitted.append (token)
            else:
                raise ParseError ()
        else:
            self.stack[-1].append (token)
            self.uncommitted.append (token)
    def parsestream (self, stream):
        # generator line -> generator expr
        for line in stream:
            try:
                self.parseline (line)
                if self.hasnextexpr ():
                    yield self.nextexpr ()
            except ParseError:
                print ('!!!! Parse error; please retry.')
    def commit (self):
        self.uncommitted = []
    def rollback (self):
        while self.uncommitted:
            token = self.uncommitted.pop ()
            # undo token
            if token == '[':
                self.stack.pop ()
            elif token == ']':
                last = self.stack[-1].pop ()
                self.stack.append (last)
            else:
                self.stack[-1].pop ()
    def sealed (self):
        return len (self.stack) == 1

