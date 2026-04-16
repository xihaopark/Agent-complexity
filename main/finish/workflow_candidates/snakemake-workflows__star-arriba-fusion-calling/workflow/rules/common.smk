# import basic packages
import pandas as pd
from snakemake.utils import validate


# read sample sheet
samples = (
    pd.read_csv(config["samples"], sep="\t", dtype={"sample_name": str})
    .set_index("sample_name", drop=False)
    .sort_index()
)

units = (
    pd.read_csv(
        config["units"],
        sep="\t",
        dtype={"sample_name": str, "unit_name": str},
        comment="#",
    )
    .set_index(["sample_name", "unit_name"], drop=False)
    .sort_index()
)

validate(units, schema="../schemas/units.schema.yaml")

# validate sample sheet and config file

validate(samples, schema="../schemas/samples.schema.yaml")
validate(config, schema="../schemas/config.schema.yaml")


# construct genome name

datatype_genome = "dna"
species = config["ref"]["species"]
build = config["ref"]["build"]
release = config["ref"]["release"]
genome_name = f"genome.{datatype_genome}.{species}.{build}.{release}"

# define final output of workflow


def final_output(wildcards):
    final_output = expand(
        [
            "<results>/arriba_fusions/{sample}/{sample}.tsv",
            "<results>/arriba_fusions/{sample}/{sample}.fusion_plots.pdf",
        ],
        sample=samples["sample_name"],
    )
    return final_output


# helper functions


def extract_unique_sample_column_value(sample, col_name):
    result = samples.loc[samples["sample_name"] == sample, col_name].drop_duplicates()
    if type(result) is not str:
        if len(result) > 1:
            ValueError(
                "If a sample is specified multiple times in a samples.tsv"
                "sheet, all columns except 'group' must contain identical"
                "entries across the occurrences (rows).\n"
                f"Here we have sample '{sample}' with multiple entries for"
                f"the '{col_name}' column, namely:\n"
                f"{result}\n"
            )
        else:
            result = result.squeeze()
    return result


def get_star_read_group(wildcards):
    """Denote sample name and platform in read group."""
    platform = extract_unique_sample_column_value(wildcards.sample, "platform")
    return r"--outSAMattrRGline ID:{sample} SM:{sample} PL:{platform}".format(
        sample=wildcards.sample, platform=platform
    )


def is_paired_end(sample):
    sample_units = units.loc[sample]
    fq2_null = sample_units["fq2"].isnull()
    if "sra" in sample_units.columns:
        sra_null = sample_units["sra"].isnull()
    else:
        sra_null = True
    paired = ~fq2_null | ~sra_null
    all_paired = paired.all()
    all_single = (~paired).all()
    assert (
        all_single or all_paired
    ), "invalid units for sample {}, must be all paired end or all single end".format(
        sample
    )
    return all_paired


# input functions


def get_optional_arriba_inputs(wildcards):
    optional_arriba_inputs = dict()
    # optional arriba known fusions file
    custom_known_fusions = config["params"]["arriba"].get("custom_known_fusions", "")
    if custom_known_fusions:
        optional_arriba_inputs["custom_known_fusions"] = custom_known_fusions
    # optional arriba blacklist file
    custom_blacklist = config["params"]["arriba"].get("custom_blacklist", "")
    if custom_blacklist:
        optional_arriba_inputs["custom_blacklist"] = custom_blacklist
    # optional file with known structural variants, specified via sv_file
    # column in sample_sheet TSV file
    if "sv_file" in samples.columns:
        sv_file = samples.at[wildcards.sample, "sv_file"]
        if sv_file:
            optional_arriba_inputs["sv_file"] = sv_file
    return optional_arriba_inputs


def get_star_reads_input(wildcards, r2=False):
    match (bool(is_paired_end(wildcards.sample)), r2):
        case (True, False):
            return units.loc[wildcards.sample, "fq1"]
        case (True, True):
            return units.loc[wildcards.sample, "fq2"]
        case (False, False):
            return units.loc[wildcards.sample, "fq1"]
        case (False, True):
            return []
