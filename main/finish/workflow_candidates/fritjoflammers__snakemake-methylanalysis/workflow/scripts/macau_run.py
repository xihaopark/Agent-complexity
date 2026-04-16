from snakemake.shell import shell

from pathlib import Path

output_dir = Path(snakemake.output.output_file).parent
output_fname = Path(snakemake.output.output_file).name
output_prefix = output_fname.split(".")[0]

# set defaults
args_covariates = ""
sampling_iterations = ""


if "covariate_file" in snakemake.input.keys():
    args_covariates = f"-c {snakemake.input.covariate_file} "

if "sampling_iterations" in snakemake.params.keys():
    sampling_iterations = f"-s {snakemake.params.sampling_iterations} "

shell(
    "{snakemake.params.macau_binary} "
    "-g {snakemake.input.mcounts_file} "
    "-t {snakemake.input.total_counts_file} "
    "-p {snakemake.input.predictor_file} "
    "{args_covariates} "
    "-k {snakemake.input.relatedness_matrix} "
    "{sampling_iterations} "
    "-bmm "
    "-outdir {output_dir} "
    "-o {output_prefix}.{snakemake.wildcards.chr}"
)
