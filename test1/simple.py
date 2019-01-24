def is_valid_sequent (expr):
    return (type (expr) is list and
            len (expr) == 3 and
            expr[0] == "|-" and
            type (expr[1]) is list)

def assumption (conc, hypos):
    return (len (hypos) == 0 and
            is_valid_sequent (conc) and
            conc[2] in conc[1])

def mp (conc, hypos):
    return (len (hypos) == 2 and
            is_valid_sequent (hypos[0]) and
            is_valid_sequent (hypos[1]) and
            is_valid_sequent (conc) and
            conc[1] == hypos[0][1] == hypos[1][1] and
            hypos[0][2] == ["->", hypos[1][2], conc[2]])

def intro (conc, hypos):
    return (len (hypos) == 1 and
            is_valid_sequent (hypos[0]) and
            is_valid_sequent (conc) and
            len (conc[1]) + 1 == len (hypos[0][1]) and
            hypos[0][1][:-1] == conc[1] and
            conc[2] == ["->", hypos[0][1][-1], hypos[0][2]])

def efq (conc, hypos):
    # Ex Falso Quodlibet.
    return (len (hypos) == 0 and
            is_valid_sequent (conc) and
            len(conc[2]) == 3 and
            conc[2][1] == "false")

axioms = {
    "assumption" : assumption,
    "mp" : mp,
    "intro" : intro,
    "efq" : efq
}

