print("start")
fp = open("../relabeled_ppdb_small.csv", "r")
fnew = open("../sorted_ppdb_small.csv", "w")
minLine = ""
minVal = float('inf')
lowerBound = float('-inf')
while True:
    # find the maximum ration and the line it appears at
    fp = open("../relabeled_ppdb_small.csv", "r") #open the file every time
    while True:
        line = fp.readline()
        #print(line)
        if not line:
            break

        pars_line = line.split(" ||| ")

        if lowerBound < float(pars_line[4]) < minVal:
            minVal = float(pars_line[4])
            minLine = line

    # checking if we should be done
    if minVal == lowerBound:
        print("we done here")
        break
    lowerBound = minVal
    minVal = float('inf')
    # we found the next biggest line, we now put it
    fnew.write(minLine)
    print(f"added {minLine}")

fp.close()
fnew.close()
