import sys

import pandas as pd

from snakemake.shell import shell

log_fh = open(snakemake.log[0], "w")

log_fh = sys.stdout = sys.stderr


def subset_df_for_samples(df, samples):
    # check if samples are in metadata and raise error if not, print missing samples
    missing_samples = set(samples) - set(df["sample"])
    if missing_samples:
        raise ValueError(f"Samples not found in metadata: {missing_samples}")

    # subset for samples
    df = df[df["sample"].isin(samples)]

    # reorder metadata according to samples
    df = df.set_index("sample").loc[samples].reset_index()

    return df


# INPUT
samples_file = snakemake.input.samples_file

# build dictionary based on input attributes starting with "covariate_"
covariate_files = dict(
    (k, v[0]) for k, v in snakemake.input.items() if k.startswith("covariate_")
)

# READ SAMPLES
samples = pd.read_csv(samples_file, sep="\s", header=None, engine="python")[0].tolist()

# and rename samples if necessary
if "rename_samples" in snakemake.params.keys():
    rename_samples = snakemake.params.rename_samples
    print(rename_samples)
    samples = [rename_samples.get(sample, sample) for sample in samples]


# READ COVARIATE
covariate_dfs = map(lambda x: pd.read_csv(x, sep="\t"), covariate_files.values())
covariate_dfs_subset = map(lambda x: subset_df_for_samples(x, samples), covariate_dfs)

# join covariate dataframes by sample column
df_variables = pd.concat(covariate_dfs_subset, axis=1)

print("columns in metadata:")
print(df_variables.columns)


df_variables["intercept"] = 1  # add intercept column

# drop all sample columns
df_variables = df_variables.drop(columns=["sample"])

# move intercept to first column
# get a list of columns without intercept
other_colnames = df_variables.columns.tolist()
other_colnames.remove("intercept")
# and reorder columns
df_variables = df_variables[["intercept"] + other_colnames]

# replace missing values with "NA"
df_variables = df_variables.fillna("NA")

# is variable == age, specify as 3 if a "+" is present, else specfiy as 2, keep NA if is NA
if "age" in df_variables.columns:
    df_variables["age"] = df_variables[-pd.isna(df_variables["age"])].age.apply(
        lambda x: 3 if "+" in x else 2 if "2" in x else "NA"
    )
    df_variables.loc[pd.isna(df_variables["age"]), "age"] = "NA"

df_variables.to_csv(
    snakemake.output.variables_file, sep="\t", index=False, header=False
)

# save predictor columns to file
with open(snakemake.output.variables_columns_file, "w") as f:
    f.write("\n".join(df_variables.columns.tolist()))


log_fh.close()
