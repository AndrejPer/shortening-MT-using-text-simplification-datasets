print("start")
fp = open("ppdb-2.0-s-all.csv", "r")
fnew = open("relabeled_ppdb_small.csv", "w")
while True:
    line = fp.readline()
    if not line:
        break
    pars_line = line.split(" ||| ")
    shorter = ""
    longer = ""

    if len(pars_line[1]) > len(pars_line[2]):
        shorter = pars_line[2]
        longer = pars_line[1]
    else:
        shorter = pars_line[1]
        longer = pars_line[2]

    print(pars_line[5])
    fnew.write(pars_line[0] + " ||| " + longer + " ||| " + shorter + " ||| " + pars_line[4] + " ||| " + str(len(shorter) / len(longer)) + " ||| " + pars_line[5])

#print(ratios)
print("end")
fp.close()
fnew.close()
