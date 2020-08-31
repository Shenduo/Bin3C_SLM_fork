# HiCBin

1. Initial processing之後得到的bam files，使用bin3C的mkmap功能產生Hi-C contact map
>> bin/python2 ./bin3C.py mkmap -e MluCI -e Sau3AI assembly.fasta input.bam output_directory

2. 將產生的contact map透過bin3C的功能以及我寫的捷徑產生出Hi-C connect network
>> bin/python2 ./map2g.py

3. 將Hi-C connect network使用SLM做genome binning
>> java -jar ModularityOptimizer.jar Hi-C_connect_network.edges result.txt 1 25.0 3 10 10 9001882 1

4. SLM的clustering結果透過bin3C的功能以及捷徑產出各個bin的fasta
>> bin/python2 ./SLM2seq.py SLM_results.txt contact_map output_directory

5. 各個bin經過checkM評估genome品質後，計算checkM報告中各個rank的數量
>> python ezcheck-full.py -f -i input_file -o output_file
