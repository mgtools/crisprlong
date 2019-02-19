#!/usr/bin/env python

import sys

def writemodule(clustid, lines, folder="./"):
	outfile = folder + "/module" + str(clustid) + ".list"
	print "write", outfile
	out = open(outfile, "w")
	for aline in lines:
		print >>out, aline	
	out.close()

inputfile, msize, folder = "", 10, "./"
for idx in range(len(sys.argv)):
	if sys.argv[idx] == '-i' and len(sys.argv) > idx + 1:
		inputfile = sys.argv[idx + 1]
	elif sys.argv[idx] == '-m' and len(sys.argv) > idx + 1:
		msize = int(sys.argv[idx + 1])
	elif sys.argv[idx] == '-f' and len(sys.argv) > idx + 1:
		folder = sys.argv[idx + 1]

if not inputfile:
	sys.exit("usage " + sys.argv[0] + " -i cluster-input <-m module-min-size> <-f folder>")

print "inputfile", inputfile
inf = open(inputfile, "r")

lines = []
clusterid = 0
for aline in inf: 
	if "#cluster " in aline:
		if lines:
			writemodule(clusterid, lines, folder)
		clusterid += 1
		lines = []
		subs = aline.split()
		if int(subs[3]) < msize:
			break
	elif aline[0] != '#':
		lines.append(aline.strip())
if lines:
	writemodule(clustid, lines, folder)
	clusterid += 1
inf.close()
