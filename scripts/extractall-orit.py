#!/usr/bin/env python

#input: cd-hit-est clustering file for all spacers to be considered
#ori-seq-file is only used to extract the subjects (in the order first appear in the sequence file)
#YY April 2, 2018

import sys

def processOneCluster(lines, arraylist):
	clusterid = lines[0][1:]
	spacerpos = [] * len(arraylist)
	spacerdir = [] * len(arraylist)
	spacerpos_f = [] * len(arraylist)
	for idx in range(len(arraylist)):
		spacerpos.append([])
		spacerpos_f.append([])
		spacerdir.append([])
	valid = False
	ref = ""
	for aline in lines[1:]:
		subs0 = aline.split()
		subs = aline.split(">")
		subs2 = subs[1].split("...")
		subs3 = subs2[0].split(":")
		seqid = subs3[0]
		arrayid = subs3[0] + ":" + subs3[1]
		pos = subs3[-1][1:]
		if subs0[-1][0] == '*': 
			ref = subs3[0] 
		if arrayid not in arraylist:
			continue	
		valid = True
		sidx = arraylist.index(arrayid)
		if subs0[-1][0] == '*': 
			spacerdir[sidx].append(True)
		else:
			spacerdir[sidx].append(subs0[-1][0] == '+')
		spacerpos[sidx].append(int(pos)) #spacer duplication, use an array
		spacerpos_f[sidx].append(subs2[0]) #spacer duplication, use an array, _f for full name + pos
	return valid, ref, clusterid, spacerpos, spacerpos_f, spacerdir

def resolveDuplication(hitlist, hitcount, hitpos):
	for sidx in range(len(hitlist)):
		totp = len(hitpos[sidx])
		poslist, duplist, duppos = [], [], []
		for p in range(0, totp):
			subs2 = hitpos[sidx][p].split(":")
			if len(subs2) == 1:
				poslist.append(int(hitpos[sidx][p]))
				hitpos[sidx][p] = int(hitpos[sidx][p])
			else:
				if hitpos[sidx][p] not in duplist:
					duplist.append(hitpos[sidx][p])
					duppos.append([])
				duppos[duplist.index(hitpos[sidx][p])].append(p)
		if len(duplist) == 0:
			continue	
		increase = 0
		for idx in range(1, len(poslist)):
			if poslist[idx] > poslist[idx - 1]:
				increase += 1
		decrease = len(poslist) - 1 - increase
		small2large = True
		if decrease > increase:
			small2large = False

		for d in range(len(duplist)):
			print "remove duplication", duplist[d]
			subs = duplist[d].split(":")
			seqpos = []
			for p in subs:
				seqpos.append(int(p))
			seqpos.sort()
			if not small2large:
				seqpos.reverse()
			for idx in range(len(duppos[d])):
				p = duppos[d][idx]
				hitpos[sidx][p] = seqpos[idx]
		print "after", hitpos[sidx]

if len(sys.argv) < 4:
	print sys.argv[0], "all-seq-id-file clustering-file outputfile"
	sys.exit()

subjects = []
allseqfile, clusterfile, outputfile = sys.argv[1], sys.argv[2], sys.argv[3]
infile = open(allseqfile, "r")

allseq, seqlen = [], []
arrayid = []
refseqidx = 0
for aline in infile:
	subs = aline.strip().split()
	subs2 = subs[0].split(":")
	thisid = subs2[0]
	#some sequences have more than one crispr array
	#print "arrayid", subs[0], "seqid", thisid
	if subs[0] not in arrayid:
		arrayid.append(subs[0])
	if thisid not in allseq:
		allseq.append(thisid)
		seqlen.append(int(subs[1]))
infile.close()
totseq = len(allseq)

print "total seq involved", totseq, "array", len(arrayid), "refseq", allseq[refseqidx], refseqidx
#print "spacerid", spacerid

infile = open(clusterfile, "r")
print "clusterfile", clusterfile
lines = []
clustid_list, spacerpos_list, spacerdir_list, spacerpos_f_list = [], [], [], []
spacerref_list = []
for aline in infile:
	aline = aline.strip()
	if aline[0] == '>':
		if len(lines) > 0:
			#valid, clustid, spacerpos, spacerpos_f = processOneCluster(lines, allseq)
			valid, ref, clustid, spacerpos, spacerpos_f, spacerdir = processOneCluster(lines, arrayid)
			if valid:
				#if ref not in allseq:
				#	sys.exit("ref " + ref + " cluster error " + lines[0])
				clustid_list.append(clustid)
				spacerpos_list.append(spacerpos)
				spacerdir_list.append(spacerdir)
				spacerpos_f_list.append(spacerpos_f)
				if ref in allseq:
					spacerref_list.append(allseq.index(ref))
				else:
					spacerref_list.append(-1)
		lines = [aline,]
		valid = 0
	else:
		lines.append(aline)
infile.close()
if len(lines) > 0:
	#valid, clustid, spacerpos, spacerpos_f = processOneCluster(lines, allseq)
	valid, ref, clustid, spacerpos, spacerpos_f, spacerdir = processOneCluster(lines, arrayid)
	if valid:
		clustid_list.append(clustid)
		spacerpos_list.append(spacerpos)
		spacerpos_f_list.append(spacerpos_f)
		spacerdir_list.append(spacerdir)
		if ref in allseq:
			spacerref_list.append(allseq.index(ref))
		else:
			spacerref_list.append(-1)

#infer the direction of spacers & arrays according to the spacers
ref_spacer_pos = []
spacer_old2new = [-1] * len(clustid_list)
#True -- forward True, reverse False
cluster_dir = [True] * len(clustid_list)
seq_dir = [True] * len(allseq)
#all spacers in the reference sequence will be indexed first, 1, 2, ...., considered + direction
print "total cluster", len(clustid_list)
print "first consider clusters contained in the reference sequence"
for spaceridx in range(len(clustid_list)):
	pos = spacerpos_list[spaceridx][refseqidx] 
	spacer = clustid_list[spaceridx]
	print "spacer", spacer, "pos", pos
	if len(pos) > 0:
		minpos = min(pos)
		ref_spacer_pos.append([spacer, minpos])
		#orient the cluster direction according to the spacer in the reference sequence
		sdir = spacerdir_list[spaceridx][refseqidx] 
		print "sdir", sdir, "#"
		if (True in sdir) and (False in sdir):
			#sys.exit("reverse found in duplicated spacer\n")
			print "WARNING: reverse found in duplicated spacer"
		cluster_dir[spaceridx] = sdir[0]
		print "cluster", clustid_list[spaceridx], cluster_dir[spaceridx]
sorted_by_pos = sorted(ref_spacer_pos, key=lambda tup: tup[1])
for idx in range(len(sorted_by_pos)):
	tmp = sorted_by_pos[idx]
	spacer_old2new[clustid_list.index(tmp[0])] = idx
	print "old", tmp[0], clustid_list.index(tmp[0]), "pos", tmp[1], "new", idx
refspaceronly = idx + 1
#other spacers follow
add = refspaceronly
for sidx in range(len(allseq)):
	remain_spacer = []
	included_spacer_f, included_spacer_r = 0, 0
	for cidx in range(len(clustid_list)):
		if len(spacerpos_list[cidx][sidx]) > 0:
			if (spacer_old2new[cidx] == -1):
				remain_spacer.append([clustid_list[cidx], min(spacerpos_list[cidx][sidx]), spacerdir_list[cidx][sidx][0]]) 	
			else: #spacer cluster already considered, used for determining the orientation of the sequence
				sdir = spacerdir_list[cidx][sidx]
				if cluster_dir[cidx] == sdir[0]:
					included_spacer_f += 1 
				else:
					included_spacer_r += 1 
	if included_spacer_f and not included_spacer_r:
		seq_dir[sidx] = True 
	elif included_spacer_r and not included_spacer_f:
		seq_dir[sidx] = False 
	else:
		#sys.exit("reverse encountered in " + allseq[sidx])	
		print "WARNING: reverse encountered in ", allseq[sidx]

	print "Now check sequence ", sidx, allseq[sidx], "included_spacer_f", included_spacer_f, "included_spacer_r", included_spacer_r, "dir", seq_dir[sidx]
				
	#print "remain_spacer", len(remain_spacer)
	if remain_spacer:
		if seq_dir[sidx]:
			sorted_by_pos = sorted(remain_spacer, key=lambda tup: tup[1])
		else:
			sorted_by_pos = sorted(remain_spacer, key=lambda tup: tup[1], reverse = True)
		for idx in range(len(sorted_by_pos)):
			tmp = sorted_by_pos[idx]
			spacer_old2new[clustid_list.index(tmp[0])] = add
			print "old spacer", tmp[0], "new spacer", add, "cluster", sorted_by_pos[idx][0]
			add += 1
			cidx = clustid_list.index(sorted_by_pos[idx][0])
			cluster_dir[cidx] = seq_dir[sidx] and sorted_by_pos[idx][2]
		
#output spacer information for the sequences
print "total seq", len(allseq)
out = open(outputfile, "w")
out2 = open(outputfile + ".ori", "w")
#print >>out, len(allseq)
#print >>out2, len(allseq)
for sidx in range(len(allseq)):
	print "check seq", allseq[sidx]
	aseq = allseq[sidx]
	this_spacer_pos = []
	minpos, maxpos = -1, -1
	for cidx in range(len(clustid_list)):
		if len(spacerpos_list[cidx][sidx]) > 0:
			for p0 in range(len(spacerpos_list[cidx][sidx])): #duplications
				p = spacerpos_list[cidx][sidx][p0]
				if (minpos == -1) or (p < minpos): 
					minpos = int(p)
				if (maxpos == -1) or (p > maxpos): 
					maxpos = int(p)
				this_spacer_pos.append([cidx, int(p), spacerpos_f_list[cidx][sidx][p0]])
	sorted_by_pos = sorted(this_spacer_pos, key=lambda tup: tup[1])
	this_refspacer = []
	this_spacer = []
	spacerplusrepeat = []
	for idx in range(len(sorted_by_pos)):
		cidx = sorted_by_pos[idx][0]
		nidx = spacer_old2new[cidx]
		this_spacer.append(nidx)
		if idx > 0:
			spacerplusrepeat.append(sorted_by_pos[idx][1] - sorted_by_pos[idx-1][1])
		if nidx < refspaceronly:
			this_refspacer.append(nidx)
	spacerplusrepeat_avelen = sum(spacerplusrepeat) / len(spacerplusrepeat)
	print "refspaceronly", refspaceronly
	print "this_refspacer", this_refspacer

	spacerlist = []
	spacerlist_f = []
	for cidx in range(len(sorted_by_pos)):
		oldspacer = sorted_by_pos[cidx][0]
		newspacer = spacer_old2new[oldspacer]
		#spacerlist.append(newspacer)
		spacerlist.append(newspacer + 1)
		spacerlist_f.append(sorted_by_pos[cidx][2])
	newid=aseq
	if not seq_dir[sidx]:
		spacerlist.reverse()	
		spacerlist_f.reverse()
		newid += "-rev"
	if len(spacerlist) < 1:
		continue
	print >>out, newid,
	print >>out2, newid,
	leftcomp, rightcomp = False, False
	if minpos >= spacerplusrepeat_avelen * 2: #repeat-spacer-repeat
		leftcomp = True
	if maxpos < seqlen[sidx] - spacerplusrepeat_avelen * 2.5: #spacer-repeat-spacer-repeat
		rightcomp = True

	if ((seq_dir[sidx]) and leftcomp) or (not seq_dir[sidx] and rightcomp):
		print >>out, "end",
		print >>out2, "end",
	else:
		print >>out, "unk",
		print >>out2, "unk",

	for idx in range(len(spacerlist)):
		print >>out, spacerlist[idx],
		print >>out2, str(spacerlist[idx]) + "[" + spacerlist_f[idx] + "]",

	if ((seq_dir[sidx]) and rightcomp) or (not seq_dir[sidx] and leftcomp):
		print >>out, "end",
		print >>out2, "end",
	else:
		print >>out, "unk",
		print >>out2, "unk",

	print >>out
	print >>out2


print "resuls saved to ", outputfile
