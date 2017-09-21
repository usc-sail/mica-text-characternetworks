#!/usr/local/bin/bash

scripts_dir='../../ScriptParser/Data/utterances_with_charnames/'
charinfo_dir='../../BiasUsingText/v2/Data/charandmovie_info/'
results_dir='../Results/degree_central_graphs'
for x in `ls $scripts_dir`; 
do 
    y=${x%.xml}; 
    charinfo_file=$charinfo_dir/$y\_xml.txt
    if [ -f $charinfo_file ];
    then
        echo $y
        ./perform_bechdel_test.py $scripts_dir/$x > /tmp/tmpfile
        status=`head -n 1 /tmp/tmpfile`
        if [ $status == 'passed' ];
        then
            tail -n +2 /tmp/tmpfile | dot -Tpng -o $results_dir/bechdeltest_passed/$y
        elif [ $status == 'failed' ];
        then
            tail -n +2 /tmp/tmpfile | dot -Tpng -o $results_dir/bechdeltest_failed/$y
        fi
    fi
done
