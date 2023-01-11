print("start")
fp = open("relabeled_ppdb_small.csv", "r")
fnew = open("sorted_ppdb_small.csv", "w")
maxLine = ""
maxVal = float('-inf')
upperBound = float('inf')
search = True
while search:
    # find the maximum ration and the line it appears at
    fp = open("relabeled_ppdb_small.csv", "r") #open the file every time
    while True:
        line = fp.readline()
        #print(line)
        if not line:
            break

        pars_line = line.split(" ||| ")

        if maxVal < float(pars_line[4]) < upperBound:
            maxVal = float(pars_line[4])
            maxLine = line

    # checking if we should be done
    if maxVal == upperBound:
        print("we done here")
        break
    upperBound = maxVal
    maxVal = float('-inf')
    # we found the next biggest line, we now put it
    fnew.write(maxLine)
    print(f"added {maxLine}")

fp.close()
fnew.close()
