#!/bin/bash 


echo "assembly=" ${1}
echo "bam file=" ${2}
inputfasta="${1}"
outputpath="${3}"
if [[ "${3}" != */ ]]
then outputpath="${3}"/
fi

if [[ (-e "${3}") && (-d "${3}") ]]
	then echo "output directory=" ${3} "exist"
else mkdir -p ${3}
	echo "output directory=" ${3}
fi

slmresolution=25.0
if [[ ("${4}" =~ ^[0-9]*\.[0-9]+$) || ("${4}" =~ ^[0-9]+$)  ]] ; then 
	slmresolution=${4}
fi

echo "slm resolution="$slmresolution

# generate contact map by bin3C mkmap
/home/bin3C/bin3C.py mkmap -e MluCI -e Sau3AI "$inputfasta" ${2} "$outputpath"contact_map

# generate connect network by bin3C function
/home/bin3C/map2g.py -i "$outputpath"contact_map/contact_map.p.gz -o "$outputpath"network

# genome binning by SLM, slm resolution now set 25.0
mkdir "$outputpath"slm/
java -jar /home/bin3C/external/ModularityOptimizer.jar "$outputpath"network/slm_graph_selfloop.edges "$outputpath"slm/result.txt 1 "${slmresolution}" 3 10 10 9001882 1

# generate fasta for checkm
/home/bin3C/SLM2seq.py "$outputpath"slm/result.txt "$outputpath"contact_map/contact_map.p.gz "$outputpath"for_checkm

# checkm 
mkdir "$outputpath"checkm_result/
checkm lineage_wf -t 8 "$outputpath"for_checkm/fasta/  "$outputpath"checkm_result

# calcutlate the result from checkm report
python3 /home/bin3C/ezcheck-full.py -f -i "$outputpath"checkm_result/storage/bin_stats_ext.tsv -o "$outputpath"checkm_result/ezcheckm_result.csv

