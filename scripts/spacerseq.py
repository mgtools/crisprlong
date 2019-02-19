#!/usr/bin/env python

import sys
import os

def revcomp(seq):
	rev = ""
	pair = {"A":"T", "T":"A", "C":"G", "G":"C"}
	for b in seq:
		rev = pair[b] + rev
	return rev

dirn, base, outfile = "", "", ""
if len(sys.argv) < 4:
	sys.exit("usage " + sys.argv[0] + " array-input-file spacer-seq-input-file <outfile-dir outfile-base> <outfile>")
if len(sys.argv) >= 5:
	arrayfile, seqfile, dirn, base = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
	if not os.path.exists(dirn):
		os.mkdir(dirn)
else:
	arrayfile, seqfile, outfile = sys.argv[1], sys.argv[2], sys.argv[3]


inf = open(arrayfile, "r")
spacer_idx = []
spacer_mem, spacer_mem_rev = [], []
spacer_mem_seq = {}
for aline in inf:
	subs = aline.split()
	if len(subs) < 3:
		continue
	if "-rev" in subs[0]:
		reverse = True
	else:
		reverse = False
	for tmp in subs[2:-1]:
		subs2 = tmp.split("[")	
		sid, fid = subs2[0], subs2[1][:-1]
		if sid in spacer_idx:
			spacer_mem[spacer_idx.index(sid)].append(fid)
			spacer_mem_rev[spacer_idx.index(sid)].append(reverse)
		else:
			spacer_idx.append(sid)
			spacer_mem.append([fid,])
			spacer_mem_rev.append([reverse,])
		spacer_mem_seq[fid] = ""
inf.close()

inf = open(seqfile, "r")
for aline in inf:
	aline = aline.strip()
	if aline[0] == '>':
		if(aline[1:] in spacer_mem_seq):
			thisid = aline[1:]
		else:
			thisid = ""
	elif thisid:
		spacer_mem_seq[thisid] = spacer_mem_seq[thisid] + aline
inf.close()

if outfile: #all in one file
	out = open(outfile, "w")
	for i in range(len(spacer_idx)):
		s = spacer_idx[i]
		for j in range(len(spacer_mem[i])):
			mem = spacer_mem[i][j]
			seq = spacer_mem_seq[mem]
			thisid = mem
			#if spacer_mem_rev[i][j]:
			#	seq = revcomp(seq)
			#	thisid += " rev"
			#don't reverse - output the original sequences
			print >>out, ">" + thisid + "\n" + seq
	out.close()
else:
	for i in range(len(spacer_idx)):
		s = spacer_idx[i]
		outfile = dirn + "/" + base + str(s) + ".fna"
		out = open(outfile, "w")
		print "write ", outfile
		for j in range(len(spacer_mem[i])):
			mem = spacer_mem[i][j]
			seq = spacer_mem_seq[mem]
			thisid = mem
			if spacer_mem_rev[i][j]:
				seq = revcomp(seq)
				thisid += " rev"
			print >>out, ">" + thisid + "_s" + str(s) + "\n" + seq
		out.close()
