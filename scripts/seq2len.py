#!/usr/bin/env python

#This code reads in gene sequences from a file and outputs the gene lengths 
#Demo for I519 
#working with files of biological sequences in FASTA format
#reading & writing
#@YY

import sys
import math

class MySeqIO(object):
	def __init__(self, file):
		self.ReadFasta(file)

	def ReadFasta(self, file):
		try:
			infile = open(file, "r")
		except IOError:
			sys.exit("open file error\n")

		self.seqID = []
		self.seqSeq = []

		for aline in infile:
			aline = aline.strip()
			if len(aline) < 1:
				continue
			if aline[0] == '>':
				subs = aline[1:].split()
				self.seqID.append(subs[0])
				self.seqSeq.append("")
			else:
				self.seqSeq[-1] += aline
		infile.close()

		self.totSeq = len(self.seqID)
		self.seqLen = []
		for idx in range(self.totSeq):
			self.seqLen.append(len(self.seqSeq[idx]))

	def GetGeneLen(self):
		return self.seqLen

	def LenStatics(self):
		if self.totSeq < 2:
			return
		lenave = float(sum(self.seqLen)) / self.totSeq 
		lenstd = 0
		for idx in range(self.totSeq):
			lenstd += (self.seqLen[idx] - lenave) ** 2 
		lenstd = math.sqrt(lenstd / (self.totSeq - 1))
		print "average length", lenave, "standard deviation", lenstd, "min", min(self.seqLen), "max", max(self.seqLen)
		print "total length", sum(self.seqLen)

	def WriteLen(self, outfile):
		try:
			out = open(outfile, "w")
		except IOError:
			sys.exit("open file error\n")
		
		for idx in range(self.totSeq):
			print >>out, self.seqLen[idx], self.seqID[idx]

		out.close()
		
if __name__ == '__main__':
	if len(sys.argv) < 3:	
		print "usage: Seq2Len.py fasta-file outfile(length-file)"
		sys.exit()
	test = MySeqIO(sys.argv[1]) 
	test.WriteLen(sys.argv[2])
	test.LenStatics()
