from snakemake.shell import shell

import pandas as pd
import numpy as np

log_fh = open(snakemake.log[0], "w")

# input
relatedness_file = snakemake.input.matrix_file
samples_file = snakemake.input.samples_file

# params
samples_list = snakemake.params.samples_list
excluded_samples = snakemake.params.excluded_samples

# output
relatedness_subset_file = snakemake.output.relatedness_matrix
samples_subset_file = snakemake.output.samples_file_subset


# load data
relatedness = np.loadtxt(relatedness_file, skiprows=0)
samples = pd.read_csv(samples_file, sep="\s", header=None, engine="python")

# set colnames for samples
samples.columns = ["unknown", "sample", "unknown2", "unknown3", "unknown4", "unknown6"]

# remove excluded samples
samples = samples[~samples["sample"].isin(excluded_samples)]

# Get the indices of the samples in the relatedness matrix
indices = samples[samples["sample"].isin(samples_list)].index
n_samples = len(samples_list)

print("Total numbers of samples: {}".format(n_samples), file=log_fh)

try:
    if len(indices) != len(samples_list):
        _missing_samples = set(samples_list) - set(samples["sample"])
        raise ValueError(
            f"Not all {n_samples} samples are found in the relatedness matrix: {_missing_samples}"
        )
except ValueError as e:
    print(e, file=log_fh)
    print(
        "Trying to find samples that are present in the relatedness matrix", file=log_fh
    )
    # subset to the samples that are found

    common_samples = set(samples_list).intersection(set(samples["sample"]))

    samples_list = samples[samples["sample"].isin(common_samples)]["sample"].tolist()
    indices = samples[samples["sample"].isin(samples_list)].index
    print("Number of samples found: {}".format(len(indices)), file=log_fh)


# Get the relatedness matrix for selected indices
relatedness_subset = relatedness[indices][:, indices]

# Save the relatedness matrix with regular digits
np.savetxt(relatedness_subset_file, relatedness_subset, fmt="%1.12f")

# Save the samples file with selected samples
samples_subset = samples.loc[indices]["sample"]
samples_subset.to_csv(samples_subset_file, sep="\t", index=False, header=False)

log_fh.close()
