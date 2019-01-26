import sys
import treeparser
from prettyprinter import pp
import test1.simple

def verify (axioms, tree):
    proven = dict ()
    for sentence in tree:
        if not (len (sentence) == 3 and
                type (sentence[0]) is not list and
                type (sentence[2]) is list and
                len (sentence[2]) >= 1):
            print ('syntax error: {}.'.format (pp (sentence)))
            return False
        [index, conc, caller] = sentence
        callname = caller[0]
        hypos_indices = caller[1:]
        hypos = []
        for hypo_index in hypos_indices:
            if hypo_index in proven:
                hypos.append (proven[hypo_index])
            else:
                print ('error: hypothesis {} not found before {}'.format (hypo_index, pp (sentence)))
                return False
        if callname in axioms:
            if axioms[callname] (conc, hypos):
                proven[index] = conc
            else:
                print ('error: {} not provable via {}'.format (pp (sentence), callname))
                return False
        else:
            print ('error: axiom {} does not exist.'.format (callname))
            return False
    return True

def main():
    infilename = sys.argv[-1]
    infile = open (infilename, 'r')
    code = infile.read ()
    infile.close ()
    tree = treeparser.code_to_tree (code) [0]
    judgment = verify (test1.simple.axioms, tree)
    if judgment:
        print ('{} successfully verified.'.format (infilename))
    else:
        print ('{} has an error.'.format (infilename))

main ()
