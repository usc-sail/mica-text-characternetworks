#!/bin/bash 

for f in `ls ./data/out/*.tsv`; do
	<$f sed -n 1,2p | awk -F': ' '{print $2}' | paste - -
done;
	