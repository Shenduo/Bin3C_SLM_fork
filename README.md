# HiCBin

## workflow

**Initial process**

Prepare bam file and fasta file.

**Run Docker**

We use Docker to build an environment for the process.
```bash 
git clone https://github.com/changlabtw/HiCBin.git
cd HiCBin

# build the image 
docker build -t HiCBin . --no-cache

# run docker container, use volume to get data from host machine
docker run -it -d -v <path of data from host>:/home/vol  --name HiCBin0 HiCBin

# get a bash shell in the container
docker exec -it HiCBin0 sh 

```
**Metagenome Deconvolution and Result evaluation**

We supply a simple script to run the whole process include checkm.
```bash 
# hicbin.sh <input assembled fasta> <input Hi-C bam file> <output path> <slm resolution default=25.0>
hicbin.sh /home/vol/data/scaffolds.fasta /home/vol/data/S_hic2scaf.bam /home/vol/output 25.0
```
Or run by steps.
generate contact map by bin3C mkmap
```bash 
/home/bin3C/bin3C.py mkmap -e MluCI -e Sau3AI <input assembled fasta> <input Hi-C bam file> <output path>
```
generate connect network by bin3C function
```bash
/home/bin3C/map2g.py -i <input contact map> -o <output path>
```
genome binning by SLM, slm resolution now set 25.0
```bash
java -jar /home/bin3C/external/ModularityOptimizer.jar <input connect network> <output path/result.txt> 1 25.0 3 10 10 9001882 1
```
fasta for checkm
```bash
/home/bin3C/SLM2seq.py <input slm result> <input contact map> <output path>
```
checkm and calcutlate the result from checkm report
```bash
checkm lineage_wf -t 8 <input fasta path>  <output path>
python3 /home/bin3C/ezcheck-full.py -f -i <input bin_stats_ext.tsv from chechm> -o <output path/ezcheck_result.csv>

```
