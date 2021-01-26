# HiCBin v1.0
Deconvoluting metagenomic assemblies via Hi-C connect network
(under construction)

## Getting started
### Systems requirements
- Docker
- 16GB memory recommended
- 64GB memory recommended if performing CheckM

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

## File contents
It is based on bin3C.
- mer.py: 解釋...

##  Typical workflow

###  Example data
The data is from ....
- scaffolds.fasta: 
- S_hic2scaf.bam: 

- We supply a simple script to run the whole process include metagenome deconvolution and result evaluation.
```bash 
# hicbin.sh <input assembled fasta> <input Hi-C bam file> <output path> <slm resolution default=25.0>
hicbin.sh /home/vol/data/scaffolds.fasta /home/vol/data/S_hic2scaf.bam /home/vol/output 25.0
```
- Or run by step-by-step.
1. generate contact map by bin3C mkmap
```bash 
/home/bin3C/bin3C.py mkmap -e MluCI -e Sau3AI <input assembled fasta> <input Hi-C bam file> <output path>
```
2. generate connect network by bin3C function
```bash
/home/bin3C/map2g.py -i <input contact map> -o <output path>
```
3. genome binning by SLM, slm resolution now set 25.0
```bash
java -jar /home/bin3C/external/ModularityOptimizer.jar <input connect network> <output path/result.txt> 1 25.0 3 10 10 9001882 1
```
4. fasta for checkm
```bash
/home/bin3C/SLM2seq.py <input slm result> <input contact map> <output path>
```
5. checkm and calcutlate the result from checkm report
```bash
checkm lineage_wf -t 8 <input fasta path>  <output path>
python3 /home/bin3C/ezcheck-full.py -f -i <input bin_stats_ext.tsv from chechm> -o <output path/ezcheck_result.csv>

```
