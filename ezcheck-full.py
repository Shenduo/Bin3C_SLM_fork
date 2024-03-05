#!/usr/bin/env python
# coding: utf-8

"""This script is used to analyze the CheckM bin_stats output tables.
It produces a reformatted report, an analysis summary of four rank categories, 
and a visualizaiton of their distribution"""

from ast import literal_eval
import sys
import argparse
import os
import pandas as pd
import matplotlib.pyplot as plt


# argument
parser = argparse.ArgumentParser()
parser.add_argument(
    "-i",
    "--input",
    dest="path",
    help="Input CheckM summary table. Must be .tsv or .csv",
)
parser.add_argument(
    "-f",
    "--FullTree",
    action="store_true",
    help="Full Tree CheckM summary table or not.",
)
parser.add_argument(
    "-o",
    "--output",
    default="",
    help="Store Full Tree CheckM summary table as normal format, and output to the target path.",
)
parser.add_argument(
    "--visualize", action="store_true", help="Generate and save visualizations."
)
parser.add_argument(
    "-b",
    "--include-biological-genome-stats",
    action="store_true",
    help="Include biological genome statistics from the CheckM report in the output",
)
parser.add_argument(
    "--min-genome-size",
    type=int,
    default=0,
    help="Minimum genome size (in bp) to include in the analysis. Default is 0 (include all)",
)
args = parser.parse_args()


filepath = args.path.split(".")
if (filepath[-1] != "tsv") and (filepath[-1] != "csv"):
    print(type(filepath[-1]))
    print("Summary table format must be .tsv or .csv")
    sys.exit(0)
elif args.FullTree:

    # read bin_stats_ext.tsv file from Checkm result, and sort it by the cluster number
    df_f = pd.read_csv(args.path, sep="\t", header=None)
    df_f = df_f.sort_values(by=[0])
    df_f = df_f.reset_index(drop=True)
    # create a dataframe 'df' with sorted bin name
    d = {"Bin Name": df_f[0].values}
    df = pd.DataFrame(data=d)
    # get the needed values in the second column of 'df_f',
    # and reconstruct them to a len(row)*12 array
    needcol = [
        "marker lineage",
        "# genomes",
        "# markers",
        "# marker sets",
        "0",
        "1",
        "2",
        "3",
        "4",
        "5+",
        "Completeness",
        "Contamination",
    ]
    if args.include_biological_genome_stats:
        needcol += [
            "GC",
            "GC std",
            "Genome size",
            "# ambiguous bases",
            "# scaffolds",
            "# contigs",
            "Longest scaffold",
            "Longest contig",
            "N50 (scaffolds)",
            "N50 (contigs)",
            "Mean scaffold length",
            "Mean contig length",
            "Coding density",
            "Translation table",
            "# predicted genes",
        ]
    list_tep = []
    for i in range(len(df_f)):
        dic = literal_eval(df_f[1][i])
        row = list(map(dic.get, needcol))
        list_tep.append(row)
    # combine the array to 'df' dataframe
    df_tep = pd.DataFrame(list_tep, columns=needcol)
    df = pd.concat([df, df_tep], axis=1)
elif filepath[-1] == "tsv":
    df = pd.read_csv(args.path, sep="\t")
else:
    df = pd.read_csv(args.path)

# Filter the df based on the minimum genome size argument
if args.min_genome_size > 0:
    df = df[df["Genome size"] > args.min_genome_size]


# Near Completeness>=90, Contamination<=5
mask1 = df["Completeness"] >= 90
mask2 = df["Contamination"] <= 5
df.loc[(mask1 & mask2), "Rank"] = "near"

# Substantial 90>Completeness>=70, 5<Contamination<=10
mask1 = df["Completeness"] >= 70
mask2 = df["Completeness"] < 90
mask3 = df["Contamination"] > 5
mask4 = df["Contamination"] <= 10
df.loc[((mask1 & mask2 & mask4) | (mask1 & mask3 & mask4)), "Rank"] = "substantial"

# Moderate 70>Completeness>=50, 10<Contamination<=15
mask1 = df["Completeness"] >= 50
mask2 = df["Completeness"] < 70
mask3 = df["Contamination"] > 10
mask4 = df["Contamination"] <= 15
df.loc[((mask1 & mask2 & mask4) | (mask1 & mask3 & mask4)), "Rank"] = "moderate"

# Partial Completeness<50, Contamination>15 (remaining bins)
mask1 = df["Completeness"] < 50
mask2 = df["Contamination"] > 15
df.loc[(mask1 | mask2), "Rank"] = "partial"

# if output path exist save 'df' dataframe
if args.output:
    outpath, outfile = os.path.split(args.output)
    if not os.path.isdir(outpath):
        os.mkdir(outpath)
    df.to_csv(args.output, index=False)


# Rank counts
total_count = len(df)
near_count = len(df[df["Rank"] == "near"])
sub_count = len(df[df["Rank"] == "substantial"])
mod_count = len(df[df["Rank"] == "moderate"])
par_count = len(df[df["Rank"] == "partial"])

# output rank counts
print("Total:", total_count)
print("Near:", near_count)
print("Substantial:", sub_count)
print("Moderate:", mod_count)
print("Partial:", par_count)

# Create dict containing rank counts for csv summary
rank_summary = {
    "Rank": ["Total", "Near", "Substantial", "Moderate", "Partial"],
    "Count": [total_count, near_count, sub_count, mod_count, par_count],
}

# convert dict to df
rank_summary_df = pd.DataFrame(rank_summary)

# save rank_summary to csv
if args.output:
    summary_outpath = os.path.splitext(args.output)[0] + "_rank_summary.csv"
    rank_summary_df.to_csv(summary_outpath, index=False)


# VISUALIZATION


def plot_rank_distribution(df_plot):
    """Plot the distribution of rank categories in a horizontal bar stacked bar chart"""

    colors = {
        "near": (0.449368, 0.813768, 0.335384, 1.0),
        "substantial": (0.120638, 0.625828, 0.533488, 1.0),
        "moderate": (0.188923, 0.41091, 0.556326, 1.0),
        "partial": (0.281412, 0.155834, 0.469201, 1.0),
    }

    plt.figure(figsize=(8, 1))

    # loop through rows in formatted_df and plot each bin's rank with respective color
    for plot_i, plot_row in df_plot.iterrows():
        rank = plot_row["Rank"]
        color = colors[rank]
        plt.barh(
            y=0,
            width=1,
            left=plot_i,
            color=color,
            align="edge",
            linewidth=0.15,
            edgecolor="black",
        )

    # plot invisible bars for each color for legend
    for label, color in colors.items():
        plt.bar(0, 0, color=color, label=label)

    plt.legend(ncol=4, loc="upper center", bbox_to_anchor=(0.5, -0.05))
    plt.subplots_adjust(bottom=0.4)
    plt.axis("off")

    # if -o was provided save plot to file
    if args.output:
        plot_outpath = os.path.splitext(args.output)[0] + "_rank_distribution.png"
        plt.savefig(plot_outpath, dpi=300)

    plt.show()


if args.visualize:
    plot_rank_distribution(df)
