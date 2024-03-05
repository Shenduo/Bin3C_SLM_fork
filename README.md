# Bin3C_SLM v0.1 (`ezcheck-full_visual` Branch)

This repository is a fork of [Bin3C_SLM](https://github.com/changlabtw/Bin3C_SLM), designed for deconvoluting metagenomic assemblies via Hi-C connect networks. This specific branch, `ezcheck-full_visual`, introduces new functionality to the `ezcheck-full.py` script, specifically adding visualization and data output features for analyzing quality rankings derived from CheckM results. These additions aim to provide users with new ways to interpret and understand their data, complementing the existing capabilities of Bin3C_SLM.

## Added Functionality to ezcheck-full.py

### New Features:

- **CSV Summary Output**: Support for saving a summary of the quality rank distribution to a CSV file.
- **Visualization Capability**: A new feature allowing users to graphically represent the distribution of quality ranks.
- **Extended Quality Ranks**: Introduction of an additional rank category, "partial" to the existing quality ranks.

## Original Features, Installation and Requirements

For detailed information on the core functionalities of Bin3C_SLM, please refer to the [original repository](https://github.com/changlabtw/Bin3C_SLM). The installation process and system requirements are consistent with the original Bin3C_SLM. Note any additional usage details for the new features in this branch here.

## Usage

The updated `ezcheck-full.py` script now produces three distinct output files, adding new functionality for the analysis of CheckM quality rankings and introducing visualization capabilities.

### Running the Script

Execute the `ezcheck-full.py` script using the following command in the terminal, specifying the input file and the output path where the script will save the generated files. Replace `<input_file>` with the path to your `bin_stats_ext.tsv` file from CheckM, and `<output_path>` with the desired directory and filename prefix for the output files.


```bash
`# To run the script, use the following command format: 
python3 ezcheck-full.py -f -i <input_file> -o <output_path/outfile.csv>
# Example: python3 /home/bin3C/ezcheck-full.py -f -i /data/bin_stats_ext.tsv -o /results/ezcheck_result.csv`
```

### Output Files

the script generates the following files in the specified output directory:

1. **CheckM Report CSV** (`<output_path>.csv`): Contains the detailed CheckM report for each bin, including the newly introduced "partial" quality rank
    
2. **Rank Summary CSV** (`<output_path>_rank_summary.csv`): Lists the count of bins classified into each quality rank category: Near, Substantial, Moderate, and Partial, providing a quick overview of the quality distribution
    
3. **Rank Distribution Visualization** (`<output_path>_rank_distribution.png`): Visualizes the distribution of quality ranks across all bins

![Rank Distribution Visualization](./Images/ezcheckm_result_rank_distribution.png)

## Acknowledgments

This project builds upon the original Bin3C_SLM tool developed by [changlabtw](https://github.com/changlabtw). I express my gratitude for their foundational work and the to the authors of [bin3C](https://github.com/cerebis/bin3C).
