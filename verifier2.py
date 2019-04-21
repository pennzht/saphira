from sys import stdin, stdout, stderr
from treeparser2 import *
from exprparser2 import *
from exprtyper2 import *
from pprinter2 import *
from type2 import *

class FileError (Exception):
    pass

parser = Parser ()

axiomfile = 'a1.axioms'

# read symbols, axioms, definitions

symbols = {}
axioms = {}
definitions = {}

with open (axiomfile, 'r') as f:
    for expr in parser.parsestream (f):
        if expr[0] == 'symbol':
            [_, symname, symtype] = expr
            symbols[symname] = symtype
        elif expr[0] == 'axiom':
            [_, axiname, vartypes, form1, form2] = expr
            axioms[axiname] = [vartypes, form1, form2]
        elif expr[0] == 'define':
            [_, defname, defbody] = expr
            definitions[defname] = defbody

pprinteach (symbols)

pprinteach (axioms)

pprinteach (definitions)

# interaction

interaction = Parser ()

for expr in interaction.parseinputstream ():
    try:
        parsed = exprparse (expr) 
        pprint (parsed)
        trytype (parsed, symbols)
        print ()
    except SyntaxError as e:
        print (f'Syntax error at {e}; please try again.')

