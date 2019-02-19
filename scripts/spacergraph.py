#!/usr/bin/env python

import sys

class Graph:
	def __init__(self, nodelist, adjmatrix):
		self.nodelist = nodelist
		self.adjmatrix = adjmatrix
		self.num = len(self.nodelist)
		self.supernode = []

	#collapse graph -- collapse one-in-one-out nodes (spacers)
	def collapse(self):
		self.supernode = []
		notvisited = range(self.num) #notvisited -- store node indices not actual names 
		while(notvisited):
			tovisit = notvisited.pop(0)
			self.supernode.append([tovisit,])
			#forward
			#print "tovisit", tovisit
			outnodes = self.getOutNode(tovisit)
			#print "outNode", nodes
			while(len(outnodes) == 1):
				if outnodes[0] not in notvisited:
					break
				innodes = self.getInNode(outnodes[0])
				if len(innodes) > 1: 
					break
				#print "forward extension: last node", self.nodelist[self.supernode[-1][-1]], "this node", self.nodelist[outnodes[0]] 
				if int(self.nodelist[outnodes[0]]) != int(self.nodelist[self.supernode[-1][-1]]) + 1: #discontinue in numbering
					break
				self.supernode[-1].append(outnodes[0])
				del notvisited[notvisited.index(outnodes[0])]
				outnodes = self.getOutNode(outnodes[0])
				
			#backward	
			innodes = self.getInNode(tovisit)
			#print "inNode", nodes
			while(len(innodes) == 1):
				if innodes[0] not in notvisited:
					break
				outnodes = self.getOutNode(innodes[0])
				if len(outnodes) > 1:
					break
				#print "backward extension: last node", self.nodelist[self.supernode[-1][0]], "this node", self.nodelist[innodes[0]] 
				if int(self.nodelist[innodes[0]]) != int(self.nodelist[self.supernode[-1][0]]) - 1: #discontinue in numbering
					break
				self.supernode[-1].insert(0, innodes[0])
				del notvisited[notvisited.index(innodes[0])]
				innodes = self.getInNode(innodes[0])
			print "supernode", self.supernode[-1]
		self.supernodegraph()
		print "total supernodes", len(self.supernode)	

	def getpath(self, spacerlist):
		print "getpath.."
		spidxlist = [-1] * len(spacerlist)
		for sidx in range(len(spacerlist)):
			spacer = spacerlist[sidx]
			spidx = -1
			for s1idx in range(len(self.supernode)):
				s1 = self.supernode[s1idx]
				s1n = self.supernodename(s1idx)
				tmp = s1n.split("-")
				if (len(tmp) == 1) and (int(spacer) == int(tmp[0])):
					spidx = s1idx
					break
				elif (len(tmp) > 1) and (int(spacer) <= int(tmp[1])) and (int(spacer) >= int(tmp[0])):
					spidx = s1idx
					break
			if spidx == -1:
				print "spacer", spacer, "not found in spacergraph with supernodes"
				sys.exit("wrong spacergraph")	
			spidxlist[sidx] = spidx
		self.onpath = []
		for idx in range(len(self.supernode)):
			self.onpath.append([0] * len(self.supernode))
		for idx in range(len(spacerlist) - 1):
			self.onpath[spidxlist[idx]][spidxlist[idx + 1]] = 1


	def supernodelen(self, n):
		i = int(self.nodelist[self.supernode[n][0]])
		j = int(self.nodelist[self.supernode[n][-1]])
		return j - i + 1

	def supernodename(self, n):
		i = self.nodelist[self.supernode[n][0]]
		j = self.nodelist[self.supernode[n][-1]]
		#tmp = "g" + str(n) + "_" + str(len(self.supernode[n])) + "_" + i 	
		#tmp = "b" + str(n) + "_" + i 	
		tmp = i 	
		if j != i:
			tmp += "-" + j	
		return tmp

	def supernodegraph(self):
		self.supernode_edge = []
		self.supernode_edgeweighted = []
		self.supernode_edgeweighted_all = []
		for s1idx in range(len(self.supernode)):
			self.supernode_edge.append([0] * len(self.supernode))
			self.supernode_edgeweighted.append([0] * len(self.supernode))
			self.supernode_edgeweighted_all.append([0] * len(self.supernode))
			s1 = self.supernode[s1idx]
			s1n = self.supernodename(s1idx)
			for s2idx in range(len(self.supernode)):
				s2 = self.supernode[s2idx]
				s2n = self.supernodename(s2idx) 
				edge = 0 
				edgeweighted = 0
				edgeweighted_all = 0
				for n1 in s1:
					for n2 in s2:
						if self.adjmatrix[n1][n2] > 0:
							#self edge
							edgeweighted_all += self.adjmatrix[n1][n2]
							if s1idx != s2idx:
								edge += 1
								edgeweighted += self.adjmatrix[n1][n2]
		
				self.supernode_edge[s1idx][s2idx] = edge
				self.supernode_edgeweighted[s1idx][s2idx] = edgeweighted
				self.supernode_edgeweighted_all[s1idx][s2idx] = edgeweighted_all

	def writedot(self, outfile):
		out = open(outfile, "w")
		print >>out, "digraph SpacerGraph {"
		print >>out, 'rankdir="LR";'
		for s1idx in range(len(self.supernode)):
			s1 = self.supernode[s1idx]
			s1n = self.supernodename(s1idx)
			shownode = True
			color=""
			if self.supernodelen(s1idx) > 0:
				shownode = True
				innode = self.getInSupernode(s1idx)
				outnode = self.getOutSupernode(s1idx)
				#print "supernode", s1idx, s1, s1n, "innode", len(innode), "outnode", len(outnode)
				if (innode) and (not outnode):
					color = "yellow"
				elif (not innode) and (outnode):
					color = "skyblue"
			if shownode:
				if color:
					print >>out, '"' + s1n + '"' + "[style=filled, fillcolor=" + color + "]"
				else:
					print >>out, '"' + s1n + '"'
				#print >>out, '"' + s1n + '"'

		#assign weights to edges
		edgeweightlist = []
		for s1idx in range(len(self.supernode)):
			for s2idx in range(len(self.supernode)):
				if self.supernode_edge[s1idx][s2idx] > 0:
					edgeweightlist.append(self.supernode_edgeweighted[s1idx][s2idx])
		edgeweightlist.sort()
		totedge = len(edgeweightlist)
		if totedge >= 10:
			quarter = totedge / 4
			low, medium, high = edgeweightlist[quarter], edgeweightlist[2 * quarter], edgeweightlist[3 * quarter]
				
		for s1idx in range(len(self.supernode)):
			s1 = self.supernode[s1idx]
			s1n = self.supernodename(s1idx)
			for s2idx in range(len(self.supernode)):
				#allow self edge for supernode with only one spacer
				s2 = self.supernode[s2idx]
				s2n = self.supernodename(s2idx) 
				if (s1idx == s2idx) and (len(s1) > 1):
					continue
				edge = self.supernode_edge[s1idx][s2idx] 
				edgeweighted = self.supernode_edgeweighted_all[s1idx][s2idx]  #use edgeweighted_all
				if edgeweighted > 0:
					penweight = 1
					if totedge >= 10:
						if edgeweighted > high:
							penweight = 4	
						elif edgeweighted > medium:
							penweight = 3
						elif edgeweighted > low:
							penweight = 2
					if self.onpath[s1idx][s2idx]:
						print >>out, '"' + s1n + '"', "->", '"' + s2n + '"' + '[color=red, penwidth=' + str(penweight) + ']'
					else:
						print >>out, '"' + s1n + '"', "->", '"' + s2n + '"' + '[penwidth=' + str(penweight) + ']'
		print >>out, "}"
		out.close()
		print "graph saved to", outfile

	def getInNode(self, n):
		a = []
		for r in range(self.num):	
			if self.adjmatrix[r][n] > 0:
				a.append(r)		
		return a

	def getInSupernode(self, n):
		a = []
		for r in range(len(self.supernode)):	
			if self.supernode_edge[r][n] > 0:
				a.append(r)		
		return a

	def getOutNode(self, n):
		a = []
		for c in range(self.num):	
			if self.adjmatrix[n][c] > 0:
				a.append(c)
		return a

	def getOutSupernode(self, n):
		a = []
		for c in range(len(self.supernode)):	
			if self.supernode_edge[n][c] > 0:
				a.append(c)
		return a

def main():
	if len(sys.argv) < 3:
		sys.exit(sys.argv[0] + " inputfile outfile")
	inpfile, dotfile = sys.argv[1], sys.argv[2]
	inf = open(inpfile, "r")
	lines = inf.readlines()
	inf.close()
	seqs = []
	spacers = []
	for aline in lines:
		subs = aline.strip().split()	
		if len(subs) < 2:
			continue
		seqs.append(subs[0])
		for one in subs[2:-1]:
			if one not in spacers:
				spacers.append(one)
	tot = len(spacers)

	#build graph -- using adjacency matrix
	adjmatrix = []
	for idx in range(tot):
		tmp = [0] * tot
		adjmatrix.append(tmp)

	print "spacers", spacers
	for aline in lines:
		subs = aline.strip().split()
		pre = spacers.index(subs[2])
		for one in subs[3:-1]:
			curr = spacers.index(one)
			adjmatrix[pre][curr] += 1
			pre = curr

	spacergraph = Graph(spacers, adjmatrix)
	spacergraph.collapse()
	spacergraph.getpath(lines[0].split()[2:-1])
	spacergraph.writedot(dotfile)


main()
