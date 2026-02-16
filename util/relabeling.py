import string

fp = open("../ppdbs/ppdb-2.0-xxl-lexical.csv", "r")
fnew = open("../relabeled_ppdb/relabeled_ppdb_xxl_lexical.csv", "w")
while True:
    line = fp.readline()
    if not line:
        break
    pars_line = line.split(" ||| ")
    if len(pars_line) < 6:
        print(pars_line)
        break
    shorter = ""
    longer = ""

    if len(pars_line[1]) > len(pars_line[2]):
        shorter = pars_line[2]
        longer = pars_line[1]
    else:
        shorter = pars_line[1]
        longer = pars_line[2]

    # b and a / b or 0  # a / b
    # ratio = len(longer.translate(str.maketrans('', '', string.punctuation))) and len(shorter.translate(str.maketrans('', '', string.punctuation))) / len(longer.translate(str.maketrans('', '', string.punctuation))) or 0
    # TODO fix difference in ratio calculation which excludes punctuation
    ratio = len(longer) / len(shorter)

    fnew.write(pars_line[0] + " ||| " + longer + " ||| " + shorter + " ||| " + pars_line[4] + " ||| " + str(ratio) + " ||| " + pars_line[5])

fp.close()
fnew.close()
