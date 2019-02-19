#!/usr/bin/env python

import sys
import os

if len(sys.argv) < 5:
	sys.exit(sys.argv[0] + " spacer-ori-file array-dir-file new-all-file new-ori-file")

oldorifile, olddirfile, newallfile, neworifile = sys.argv[1:5]

inf = open(oldorifile, "r")
lines = inf.readlines()
tot = len(lines)
inf.close()

arraydir = {}
inf = open(olddirfile, "r")
for aline in inf:
	aline = aline.strip()
	subs = aline.split()
	arraydir[subs[0]] = subs[1]

rrev, rkeep, fkeep, frev = 0, 0, 0, 0
spacer = {}
for aline in lines:
	subs = aline.strip().split()
	seqid = subs[0]
	if "R-rev" in subs[0]:
		rrev += 1
	elif "-rev" in subs[0]:
		seqid = seqid[:-4]
		#print "old name", subs[0], "new", seqid, "dir", arraydir[seqid]
		if arraydir[seqid] == 'for':  #only consider "forward" with orientation (not the unk ones)
			frev += 1
	elif subs[0][-1] != 'R':
		if arraydir[seqid] == 'for':
			print "seqid", seqid, "dir", arraydir[seqid]
			fkeep += 1
	else:
		rkeep += 1
	for item in subs[2:-1]:
		subs2 = item.split("[")
		sid = subs2[0]
		if sid in spacer:
			spacer[sid] = spacer[sid] + 1
		else:
			spacer[sid] = 1
allspacer = spacer.keys()
totspacer = len(allspacer)

print "total spacer", totspacer

tag = "keep"
evidence = rkeep + fkeep 
if (rrev + frev) > (fkeep + rkeep): #needs to flip all arrays around
	tag = "flipped"
	evidence = rrev + frev
	out1 = open(newallfile, "w")
	out2 = open(neworifile, "w")
	for aline in lines:
		subs = aline.strip().split()
		if "-rev" in subs[0]:	
			newid = subs[0][:-4]
		else:
			newid = subs[0] + "-rev"
		print >>out1, newid, subs[-1],
		print >>out2, newid, subs[-1],
		for item in subs[-2:1:-1]:
			subs2 = item.split("[")
			sid = subs2[0]
			nid = totspacer - int(sid) + 1
			print >>out1, nid,	
			print >>out2, str(nid) + "[" + subs2[1],
		print >>out1, subs[1]
		print >>out2, subs[1]
	out1.close()
	out2.close()

print newallfile, "array", tot, "evidence", evidence, "forward-keep", fkeep, "forward-rev", frev, "reverse-keep", rkeep, "reverse-rev", rrev, "status", tag
