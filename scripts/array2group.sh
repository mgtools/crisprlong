#!/bin/bash
script=$(basename $(readlink -nf $0))
dir=$(dirname $(readlink -nf $0))
if [[ ! $@ =~ ^\-.+ ]]
then
   echo "Usage: $script -s spacer-file -i fasta-file -o output-file -m min-arrays-per-group"; exit 1;
fi
m=10
while [[ "$#" > 0 ]]; do case $1 in
  -s|--spacer) s="$2"; shift;;
  -i|--input) i="$2"; shift;;
  -o|--output) o="$2"; shift;;
  -m|--min) m="$2"; shift;;
  -h|--help) echo "Usage: $script -s spacer-file -i fasta-file -o output-file -m min-arrays-per-group"; exit 1;;
  *) echo "Unknown parameter passed: $1"; exit 1;;
esac; shift; done

if [ -f "$s" ]; then
   echo "$s found -- nice"
else 
   echo "-s #$s# not given or the file is not found"
   exit
fi
if [ -f "$i" ]; then
   echo "$i found -- nice"
else 
   echo "-i not given or the file is not found"
   exit
fi
c=${s}-cdhit0.9.clstr
if [ -f ${c} ]; then
	echo "${c} exists; skip clustering step"
else
	${dir}/../third/cd-hit-est -i ${s} -d 0.9 -o ${s}-cdhit0.9 -M 8000
fi
${dir}/seq2len.py ${i} ${i}.len
echo ${dir}/clstr2table-greedy.py ${i}.len ${s}-cdhit0.9.clstr ${o} 
if [ -f ${o} ]; then
	echo "${o} exists; skip ${dir}/clstr2table-greedy.py"
else
	${dir}/clstr2table-greedy.py ${i}.len ${s}-cdhit0.9.clstr ${o} 
fi
if [ -d "module" ]; then
	echo "module exists"
else
	mkdir module
fi
echo ${dir}/table2module.py -i ${o} -m ${m} -f module
${dir}/table2module.py -i ${o} -m ${m} -f module
