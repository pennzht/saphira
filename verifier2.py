from sys import stdin
from treeparser2 import *
from pprinter2 import *
from type2 import *

class FileError (Exception):
    pass

parser = Parser ()

axiomfile = 'a1.axioms'

# read symbols, axioms, definitions

symbols = []
axioms = []
definitions = []

with open (axiomfile, 'r') as f:
    for expr in parser.parsestream (f):
        if expr[0] == 'symbol':
            [_, symname, symtype] = expr
            symbols.append ([symname, symtype])
        elif expr[0] == 'axiom':
            [_, axiname, vartypes, form1, form2] = expr
            axioms.append ([axiname, vartypes, form1, form2])
        elif expr[0] == 'define':
            [_, defname, defbody] = expr
            definitions.append ([defname, defbody])

pprinteach (symbols)

pprinteach (axioms)

pprinteach (definitions)

# interaction

interaction = Parser ()

statement = 'True'

