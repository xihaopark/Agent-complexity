from snakemake.shell import shell

import pandas as pd

import pyreadr


# Define a function to pivot data and save to file
def pivot_and_save(df, metric_type, output_file):
    # Filter data based on metric type
    filtered_df = df[df["metric"] == metric_type]

    # Pivot wide with one column per sample
    pivoted_df = filtered_df.pivot(index="site", columns="sample", values="value")

    # Remove the index name
    pivoted_df.index.name = None

    # Save to file
    pivoted_df.to_csv(output_file, sep="\t", header=True, index=True)


# input RDS tibble
methylation_file = snakemake.input.meth_data

# subsetted samples from the relatedness matrix
samples_file = snakemake.input.samples_file

# output
read_counts_file = snakemake.output.read_counts_file
total_counts_file = snakemake.output.total_counts_file

samples = pd.read_csv(samples_file, sep="\s", header=None, engine="python")[0].tolist()

# load data
df_meth = pyreadr.read_r(methylation_file)[None]

# create new column with site ID, consisting of chr:pos
df_meth["site"] = df_meth["chr"].astype(str) + "_" + df_meth["start"].astype(str)

# check if samples are in the data, if not, raise an error
# relatedness data was subsetted for samples in the methylation data before uniting the data
# after uniting we might have more dropouts
if not set(samples).issubset(set(df_meth["sample"])):
    raise ValueError("Not all samples are in the methylation data")

# subset the data to the samples of interest
df_meth = df_meth[df_meth["sample"].isin(samples)]


# Process and save read counts
pivot_and_save(df_meth, "numCs", read_counts_file)

# Process and save total counts
pivot_and_save(df_meth, "coverage", total_counts_file)
