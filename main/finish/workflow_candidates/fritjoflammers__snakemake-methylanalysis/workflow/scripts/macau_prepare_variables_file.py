import sys

import pandas as pd

from snakemake.shell import shell

log_fh = open(snakemake.log[0], "w")

log_fh = sys.stdout = sys.stderr

samples_file = snakemake.input.samples_file
metadata_file = snakemake.input.metadata_file

variable_names = snakemake.params.variables


# check if is_covariates is in params
if "is_covariates" in snakemake.params.keys():
    is_covariates = snakemake.params.is_covariates
else:
    is_covariates = False

# output
variables_file = snakemake.output.variables_file
variables_columns_file = snakemake.output.variables_columns_file

# read files
samples = pd.read_csv(samples_file, sep="\s", header=None, engine="python")[0].tolist()
metadata = pd.read_table(metadata_file, sep="\t")

# rename samples in sample list after list of tuples in params
if "rename_samples" in snakemake.params.keys():
    rename_samples = snakemake.params.rename_samples
    print(rename_samples)
    samples = [rename_samples.get(sample, sample) for sample in samples]

# check if samples are in metadata and raise error if not, print missing samples
missing_samples = set(samples) - set(metadata["sample"])
if missing_samples:
    raise ValueError(f"Samples not found in metadata: {missing_samples}")

# subset for samples
metadata = metadata[metadata["sample"].isin(samples)]

# reorder metadata according to samples
metadata = metadata.set_index("sample").loc[samples].reset_index()

# check if predictors are columns in metadata and raise error if not, print missing predictors
missing_vars = set(variable_names) - set(metadata.columns)
if missing_vars:
    raise ValueError(f"Predictors not found in metadata: {missing_vars}")

# subset for predictors
if is_covariates:
    metadata["intercept"] = 1  # add intercept column
    metadata = metadata[
        ["intercept"] + variable_names
    ]  # move intercept column to first position
else:
    metadata = metadata[variable_names]
    # replace missing values with "NA"
    metadata = metadata.fillna("NA")


# specific metadata transformation

# is variable == age, specify as 3 if a "+" is present, else specfiy as 2, keep NA if is NA
if "age" in variable_names:
    metadata["age"] = metadata[-pd.isna(metadata["age"])].age.apply(
        lambda x: 3 if "+" in x else 2 if "2" in x else "NA"
    )
    metadata.loc[pd.isna(metadata["age"]), "age"] = "NA"

metadata.to_csv(variables_file, sep="\t", index=False, header=False)

# save predictor columns to file
with open(variables_columns_file, "w") as f:
    f.write("\n".join(variable_names))


log_fh.close()
