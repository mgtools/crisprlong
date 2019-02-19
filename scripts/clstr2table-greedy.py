#!/usr/bin/env python

import sys

if len(sys.argv) < 4:
	sys.exit("usage: " + sys.argv[0] + " seq-len-file clstr-input table-output")

seqlenfile, infile, outfile = sys.argv[1], sys.argv[2], sys.argv[3]

array2spacer = []
arraylist = []

inf = open(infile, "r")
clustnum = 0
for aline in inf:
	if aline[0] == '>':
		clustnum += 1
inf.close()
		
inf = open(infile, "r")
clustid = 0 
for aline in inf:
	if aline[0] == '>':
		clustid += 1
	else:
		subs = aline.split(">")
		subs2 = subs[1].split(":")
		arrayid = subs2[0] + ":" + subs2[1]
		if arrayid not in arraylist:
			arrayidx = len(arraylist)
			arraylist.append(arrayid)
			tmp = [0] * clustnum
			array2spacer.append(tmp)
		else:
			arrayidx = arraylist.index(arrayid)
		array2spacer[arrayidx][clustid - 1] = 1

inf.close()
totarray = len(arraylist)

spacernum = [0] * len(arraylist)
valid = 0
minspacer = 3
for i in range(len(array2spacer)):
	spacernum[i] = sum(array2spacer[i])
	if spacernum[i] >= minspacer:
		valid += 1
print "total array", len(array2spacer), "arrays with at least 3 spacers", valid
tosort = []
for idx in range(totarray):
	tosort.append([idx, spacernum[idx]])
tmp = sorted(tosort, key=lambda tosort: tosort[1], reverse=True)
array2spacer_s = []
arraylist_s = []
arrayseq = []
spacernum = []
for idx0 in range(totarray):
	idx = tmp[idx0][0]
	arraylist_s.append(arraylist[idx]) 
	subs = arraylist[idx].split(":")
	arrayseq.append(subs[0]) #strip off :c1 :c2 etc
	array2spacer_s.append(array2spacer[idx][:])
	spacernum.append(sum(array2spacer[idx]))
print "get seq len.."
seqlen = [0] * len(arraylist_s)
inf = open(seqlenfile, "r")
for aline in inf:
	subs = aline.strip().split()
	if subs[1] in arrayseq:
		seqlen[arrayseq.index(subs[1])] = subs[0]
	#if subs[1] == "SRR2822456.455839":
	#	print "subs[1]", subs[1], "subs[0]", subs[0]
inf.close()

last = 0
included = [False] * totarray
clustertmp = []
while last < totarray:
	for i in range(last, totarray):
		if not included[i]:
			break
	if i >= totarray:
		break
	beg = i
	allspacer = array2spacer_s[beg][:]
	included[beg] = True
	allspacer_num = sum(allspacer)
	print arraylist_s[beg], spacernum[beg]
	mem = [beg,]
	spacer = [sum(allspacer),]
	shared = [spacernum[beg],]
	for j in range(beg + 1, totarray):
		if included[j] == True:
			continue
		com = 0
		short = min(allspacer_num, spacernum[j])
		for k in range(clustnum):
			if (array2spacer_s[j][k] == 1) and (allspacer[k] == 1):
				com += 1
		if com > 0:
			included[j] = True
			mem.append(j)
			shared.append(com)
			for k in range(clustnum):
				if array2spacer_s[j][k] == 1:
					allspacer[k] = 1
			spacer.append(sum(allspacer))
			#print >>out, arraylist_s[j], spacernum[j], sum(allspacer), com, " ".join(str(v) for v in array2spacer_s[j])
	tmp = []
	for m in range(len(mem)):
		a = mem[m]
		tmp.append(arraylist_s[a] + " " + str(seqlen[a]) + " " + str(spacernum[m]) + " " + str(spacer[m]) + " " + str(shared[m]))
	clustertmp.append([len(mem), tmp])
		
	last = beg + 1

clustertmp_sort = sorted(clustertmp, key=lambda tosort: tosort[0], reverse=True)

out = open(outfile, "w")
print >>out, "#cluster-line cluster-id num-of-array-included"
print >>out, "#array-line seq-id seq-len spacer-in-this-seq total-spacer-so-far spacer-shared" 
valid = 0
for idx in range(len(clustertmp_sort)):
	tmp = clustertmp_sort[idx][1][-1]
	subs = tmp.split()	
	if int(subs[-2]) < 5: #less than 5 different spacers
		continue
	valid += 1
	print >>out, "#cluster ", valid, "arrays", clustertmp_sort[idx][0] 
	for m in clustertmp_sort[idx][1]:
		print >>out, m
out.close()

print "table file created"
