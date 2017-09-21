#!/usr/local/bin/bash

scripts_dir='../../ScriptParser/Data/utterances_with_charnames'
charinfo_dir='../../BiasUsingText/v2/Data/charandmovie_info/'
results_dir='../Results/character_network_jsonfiles'
for x in `ls $scripts_dir`; 
do 
#    y=${x%.xml}; 
#    charinfo_file=$charinfo_dir/$y\_xml.txt
    charinfo_file=$charinfo_dir/$x
    if [ -f $charinfo_file ];
    then
        echo $x
        ./create_character_networksjson_fromtxt.py $scripts_dir/$x > $results_dir/${x%.txt}.json
    fi
done
