import sys

import pandas as pd

from snakemake.shell import shell

log_fh = open(snakemake.log[0], "w")

log_fh = sys.stdout = sys.stderr


FIELD_DELIM = snakemake.params.delim
TARGET_COLUMNS = snakemake.params.columns

# check that TARGET_COLUMNS is a list
if not isinstance(TARGET_COLUMNS, list):
    raise ValueError("TARGET_COLUMNS must be a list")

# print input parameters
print(f"FIELD_DELIM: {FIELD_DELIM}")
print(f"TARGET_COLUMNS: {TARGET_COLUMNS}")

df = pd.read_csv(snakemake.input[0], sep=FIELD_DELIM)

# sort alphabetically by sample, if exists
if "sample" in df.columns:
    print("Sorting by sample column.")
    df = df.sort_values("sample")

    # and rename samples if necessary
    if "rename_samples" in snakemake.params.keys():
        rename_samples = snakemake.params.rename_samples
        print(rename_samples)
        # rename samples in sample column, keep original name if not found in rename_samples
        df["sample"] = df["sample"].map(lambda x: rename_samples.get(x, x))
else:
    print("No sample column found in input file. Not sorted.")

# print first 5 rows of df
print(df.head())

# check if target columns are in df
missing_vars = set(TARGET_COLUMNS) - set(df.columns)
if missing_vars:
    raise ValueError(f"Predictors not found in metadata: {missing_vars}")


df = df[TARGET_COLUMNS]
# print first 5 rows of df
print(df.head())

# write to file
df.to_csv(snakemake.output[0], sep=FIELD_DELIM, index=False)

log_fh.close()
