#!/usr/bin/env python

import sys
import subprocess
import os

if "check_output" not in dir( subprocess ): #old python doesn't support check_output
    def f(*popenargs, **kwargs):
        if 'stdout' in kwargs:
            raise ValueError('stdout argument not allowed, it will be overridden.')
        process = subprocess.Popen(stdout=subprocess.PIPE, *popenargs, **kwargs)
        output, unused_err = process.communicate()
        retcode = process.poll()
        if retcode:
            cmd = kwargs.get("args")
            if cmd is None:
                cmd = popenargs[0]
            raise subprocess.CalledProcessError(retcode, cmd)
        return output
    subprocess.check_output = f

def file_put_contents(filename, content):
        subprocess.check_output("echo \"" + content + "\" > " + filename, shell=True)

if len(sys.argv) < 2:
	sys.exit("usage " + sys.argv[0] + " list-file")

modulefile = sys.argv[1]

#YY 2020, June 15
dir0 = os.path.dirname(os.path.abspath(sys.argv[0]))
#cmd = "/u/yye/CRISPRpk/CRISPRcomp/spacer-toposort " + modulefile
cmd = dir0 + "/spacer-toposort " + modulefile
output = subprocess.check_output(cmd, shell=True)

subs = output.split()
old2new = {}
for idx in range(len(subs)):
	#print "key", int(subs[idx]) + 1, "value", idx + 1
	old2new[str(int(subs[idx]) + 1)] = idx + 1	

print old2new

inf = open(sys.argv[1], "r")
lines = inf.readlines()
inf.close()
out = open(sys.argv[1], "w")
for aline in lines:
	subs = aline.split()
	print >>out, subs[0] + " " + subs[1],
	for item in subs[2:-1]:
		if item in old2new:
			print >>out, old2new[item],
		else:
			print item, "not found in the map"
	print >>out, subs[-1]
out.close()

inf = open(sys.argv[2], "r")
lines = inf.readlines()
inf.close()
out = open(sys.argv[2], "w")
for aline in lines:
	subs = aline.split()
	print >>out, subs[0] + " " + subs[1],
	for item0 in subs[2:-1]:
		subs2 = item0.split("[")
		item = str(subs2[0])
		if item in old2new:
			print >>out, str(old2new[item]) + "[" + subs2[1],
		else:
			print item, "not found in the map"
	print >>out, subs[-1]
out.close()
