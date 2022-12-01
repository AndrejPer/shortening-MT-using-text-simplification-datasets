print("start")
fp = open("ppdb-2.0-s-all.csv", "r")
fnew = open("relabeled_ppdb_small.csv", "w")
all_lines = fp.readlines()
dictionary = dict()
ratios = []
for line in all_lines:
    i = 0
    #print(line)
    pars_line = line.split(" ||| ")
    shorter = ""
    longer = ""

    if len(pars_line[1]) > len(pars_line[2]):
        shorter = pars_line[2]
        longer = pars_line[1]
    else:
        shorter = pars_line[1]
        longer = pars_line[2]

    dictionary[i] = {"tag": pars_line[0], "longer": longer, "shorter": shorter, "alignment": pars_line[4],
                     "equivalence": pars_line[5].strip("\n"), "ratio": len(shorter) / len(longer)}
    print(longer)
    fnew.write(pars_line[0] + " ||| " + longer + " ||| " + shorter + " ||| " + pars_line[4] + " ||| " + str(len(shorter) / len(longer)) + " ||| " + pars_line[5])
    #ratios.append(dictionary[i]["ratio"])
    #print(dictionary[i])
    i = i + 1

#print(ratios)
print("end")
