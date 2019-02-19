#!/bin/bash

script=$(basename $(readlink -nf $0))
dir=$(dirname $(readlink -nf $0))
if [[ ! $@ =~ ^\-.+ ]]
then
   echo "Usage: $script -c clstr-file -s spacer-file"; exit 1;
fi
m=10
while [[ "$#" > 0 ]]; do case $1 in
  -c|--clstr) c="$2"; shift;;
  -s|--spacer) s="$2"; shift;;
  -h|--help) echo "Usage: $script -c clstr-file -s spacer-file"; exit 1;;
  *) echo "Unknown parameter passed: $1"; exit 1;;
esac; shift; done

if [ -d "module" ]; then
   echo "module folder found -- nice"
else
   echo "module folder not found -- run array2group.sh first"
   exit
fi

for i0 in `find module -name "*.list" -type f`; do
	b=$(basename $i0 .list)
	i="module/$b"
        ${dir}/extractall-orit.py $i.list ${c} $i.all.ini
        ${dir}/extractall-sort.py $i.all.ini $i.all.ini.ori

        #redo cd-hit-est for the spacers in this module only (otherwise, in some cases, a spacer cluster may split into multiple)
        ${dir}/spacerseq.py $i.all.ini.ori ${s} $i-spacer.fna
        ${dir}/../third/cd-hit-est -i $i-spacer.fna -c 0.9 -o $i-spacer-cdhit0.9.fna -d 0

        #redo extractall-orit, using this clustering file
        ${dir}/extractall-orit.py $i.list $i-spacer-cdhit0.9.fna.clstr $i.all
        ${dir}/extractall-sort.py $i.all $i.all.ori

        #cp $i.all.ori $i.all.ori.old
        #${dir}/extractall-flip.py $i.all.ori.old ../../SRR2822456-long-sel-ort.info $i.all $i.all.ori
        ${dir}/spacerseq.py $i.all.ori ${s} $i-spacer s
        ${dir}/spacergraph.py $i.all $i.dot
        ${dir}/array2nr.py $i.all $i-nr.all
        dot -Tpdf -o $i.pdf $i.dot
done
