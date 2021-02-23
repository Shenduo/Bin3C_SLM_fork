# HiCBin v0.1
Deconvoluting metagenomic assemblies via Hi-C connect network

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
HiCBin is based on [bin3C](https://github.com/cerebis/bin3C) with addtional homemade functions to perform specific clustering and evaluation.
- mzd/cluster.py: replace the original cluster.py of bin3C with two additional functions, getGraph() and getSLMresult()
  + getGraph(): convert the seq_map to an undirected Networkx Graph using `to_Graph()` in original cluster.py of bin3C, and generate the edge file by `write_edgelist` function from Networkx package. 
  + getSLMresult(): combining  `_read_table()` and part of `cluster_map()` function in original cluster.py of bin3C to get the sequence indices of every cluster.
- map2g.py: get an edge file from a contact map file using getGraph() in mzd/cluster.py
- SLM2seq.py: generate the sequence fasta of each bin using getSLMresult() in mzd/cluster.py
- ezcheck-full.py: evaluate the ranks (near, substantial, moderate) of the checkM result file, bin_stats_ext.tsv

Docker
- Dockerfile: for building docker image.
- requirements.txt/requirementspy3.txt: for installing required python packages during building docker image.

Tool
- hicbin.sh: a wrap-up script to run the whole process of HicBin include CheckM.

##  Quick start

###  Example data
The original dataset derives from a human fecal sample and contains a shotgun read-set ([SRR6131123](https://trace.ncbi.nlm.nih.gov/Traces/sra/?run=SRR6131123)), and two separated Hi-C read-sets produced using two restriction enzymes MluCI ([SRR6131122](https://trace.ncbi.nlm.nih.gov/Traces/sra/?run=SRR6131122)) and Sau3AI ([SRR6131123](https://trace.ncbi.nlm.nih.gov/Traces/sra/?run=SRR6131123)). The following example data is generated after initial process. 
- scaffolds.fasta: shotgun reads are cleaned up by BBDuk in BBTools, and assembled using metaSPAdes.
- [merged_scaf.bam](https://drive.google.com/file/d/14mWTpNUT7_PELF3cCjoXYTXNSHuxbXXx/view?usp=sharing): merged from two bam files mapped by MluCI and Sau3AI Hi-Cs.  

[data download](https://drive.google.com/drive/folders/141ZTekBQ3VVy4VbDMcrz32cOqus2N0lo?usp=sharing)

###  Example usage
There are two ways to run HiCBin: one command or step-by-step.
- We supply a simple script to run the whole process include metagenome deconvolution and result evaluation.
```bash 
# hicbin.sh <input:assembled fasta> <input:Hi-C bam file> <output:path> <slm resolution=25.0>
hicbin.sh /home/vol/data/scaffolds.fasta /home/vol/data/merged_scaf.bam /home/vol/output 25.0
```
- Step-by-step.
  1. generate contact map
  ```bash 
  /home/bin3C/bin3C.py mkmap -e MluCI -e Sau3AI <input:assembled fasta> <input:Hi-C bam file> <output:path>
  ```
  2. generate connect network
  ```bash
  /home/bin3C/map2g.py -i <input:contact map> -o <output:path>
  ```
  3. genome binning
  ```bash
  java -jar /home/bin3C/external/ModularityOptimizer.jar <input:connect network> <output:path/result.txt> 1 25.0 3 10 10 9001882 1
  ```
  4. get fasta seqs based on binning
  ```bash
  /home/bin3C/SLM2seq.py <input:slm result> <input:contact map> <output:path>
  ```
  5. perform checkm and evaluate performance
  ```bash
  checkm lineage_wf -t 8 <input:fasta path>  <output:path>
  python3 /home/bin3C/ezcheck-full.py -f -i <input:bin_stats_ext.tsv from chechm> -o <output:path/ezcheck_result.csv>
  ```

