from treeparser import code_to_sexp
from prettyprinter import pp_sexp

claim = None

f = open ('natdeduct.axioms', 'r')
axioms_text = f.read ()
f.close ()

axioms = code_to_sexp (axioms_text)
print (pp_sexp (axioms))

while True:
    print (pp_sexp (claim))
    print ()
    command = input ('> ')
    if ' '.join (command.split ()) == '#!quit':
        break
    try:
        sexp = code_to_sexp (command)
        if sexp[0] == 'claim':
            claim = sexp[1][0]
        elif sexp[0] == 'apply':
            rule = sexp[1][0]
            params = sexp[1][1]
            # todo
    except:
        print ('Input incorrect.')
        print ()
