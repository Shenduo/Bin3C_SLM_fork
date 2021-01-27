# HiCBin v1.0
Deconvoluting metagenomic assemblies via Hi-C connect network
(under construction)

## Installation
### Systems requirements
- Docker
- 16GB memory recommended
- 40GB memory recommended if performing CheckM

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
- map2g.py: using the functions in cluster.py of bin3C to convert seq_map to a undirected Networkx Graph.
- mzd/cluster.py: we revised the original cluster.py of bin3C, adding getGraph() and getSLMresult() function for callings from map2g.py and SLM2seq.py. 
- SLM2seq.py: using the functions in cluster.py of bin3C to get fasta of each bin.
- ezcheck-full.py: generate a easy check file from CheckM result bin_stats_ext.tsv and calculate the ranks(near, substantial, moderate).
- Dockerfile: for building docker image.
- requirements.txt/ requirementspy3.txt: for installing required python packages.
- hicbin.sh: a simple script to run the whole process of HicBin include CheckM.



##  Quick start

###  Example data
The example data is generated after initial process(read cleanup, shotgun assembly, Hi-C read mapping). The original dataset derives from a human fecal sample and contains a shotgun read-set, and two separated Hi-C read-sets produced using two restriction enzymes MluCI and Sau3AI. It can be downloaded from the NCBI Sequence Read Archive under the accession numbers: SRR6131123(shotgun), SRR6131122 (Hi-C, MluCI) and SRR6131124 (Hi-C, Sau3AI).
- scaffolds.fasta: from shotgun cleaned up by BBDuk from BBTools, and assembled using metaSPAdes.
- merged_scaf.bam: merged from two bam files mapped by Hi-C read-sets using MluCI and Sau3AI.  

[data download](https://drive.google.com/drive/folders/141ZTekBQ3VVy4VbDMcrz32cOqus2N0lo?usp=sharing)

###  Example usage
There are two ways to run HiCBin: one command or step-by-step.
- We supply a simple script to run the whole process include metagenome deconvolution and result evaluation.
```bash 
# hicbin.sh <input assembled fasta> <input Hi-C bam file> <output path> <slm resolution default=25.0>
hicbin.sh /home/vol/data/scaffolds.fasta /home/vol/data/merged_scaf.bam /home/vol/output 25.0
```
- Step-by-step.
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
