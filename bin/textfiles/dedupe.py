outfilename = "playersdeduped.csv"
infilename = "players.csv"

lines_seen = set() # holds lines already seen
outfile = open(outfilename, "w",encoding="utf-8")
for line in open(infilename, "r",encoding="utf-8"):
    if line not in lines_seen: # not a duplicate
        outfile.write(line)
        lines_seen.add(line)
outfile.close()