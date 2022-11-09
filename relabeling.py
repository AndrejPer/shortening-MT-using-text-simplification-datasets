fp = open("mock.csv")
alllines = fp.readlines()
dict = dict()
for line in alllines:
    i = 0
    print(line)
    pars_line = line.split("|||")
    dict[0] = {"tag": pars_line[0], "left": pars_line[1]}
    print(pars_line)
