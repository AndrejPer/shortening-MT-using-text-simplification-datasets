print("start")
fp = open("mock", "r")
fnew = open("relabeled_ppdb_small.csv", "w")
while True:
    line = fp.readline()
    if not line:
        break
    pars_line = line.split(" ||| ")
    if(len(pars_line) < 6):
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

    print(len(pars_line))
    fnew.write(pars_line[0] + " ||| " + longer + " ||| " + shorter + " ||| " + pars_line[4] + " ||| " + str(len(shorter) / len(longer)) + " ||| " + pars_line[5])

#print(ratios)
print("end")
fp.close()
fnew.close()
