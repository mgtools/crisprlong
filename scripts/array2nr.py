#!/usr/bin/env python

import sys

if len(sys.argv) < 3:
	sys.exit("usage " + sys.argv[0] + " array-input array-nr-output")

infile, outfile = sys.argv[1], sys.argv[2]

arrayid, arraylist = [], []
inf = open(infile, "r")
for aline in inf:
	subs = aline.strip().split()
	if len(subs) < 2:
		continue
	arrayid.append(subs[0])
	arraylist.append(subs[1:])
inf.close()

tot = len(arrayid)
rep = [-1] * tot
for i in range(tot):
	if rep[i] == 0:
		continue
	rep[i] = 1
	for j in range(i + 1, tot):
		same = True
		if len(arraylist[j]) == len(arraylist[i]):
			for k in range(len(arraylist[i])):
				if arraylist[i][k] != arraylist[j][k]:
					same = False
		else:
			same = False
		if same:
			rep[j] = 0
			rep[i] += 1
out = open(outfile, "w")
for i in range(tot):
	if rep[i] == 0:
		continue
	showid = arrayid[i]
	if "-rev" in showid:
		showid = showid[:-4]
	if showid[-1] == 'R':
		showid = showid[:-1]
	if rep[i] > 1:
		showid = showid + "(" + str(rep[i]) + ") "
	print>>out, showid, " ".join(arraylist[i])
out.close()

print "non-redundant collection of arrays saved in", outfile
