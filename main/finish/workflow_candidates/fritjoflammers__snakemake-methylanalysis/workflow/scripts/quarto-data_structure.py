from snakemake.shell import shell

import os
import tempfile

from pathlib import Path
from shutil import copyfile

if not type(snakemake.input.rds) == str:
    input_files = map(lambda x: os.path.abspath(x), snakemake.input.rds)
    input_files_str = ",".join(input_files)
else:
    input_files = os.path.abspath(snakemake.input.rds)
    input_files_str = input_files

_notebook = "workflow/notebooks/data-structure.qmd"

if not snakemake.params.output_format == Path(snakemake.output[0]).suffix[1:]:
    raise ValueError(
        f"Output format {snakemake.params.output_format} does not match output file extension {Path(snakemake.output[0]).suffix[1:]}"
    )

wheatearcommons_repo_dir = os.path.abspath(snakemake.input.wheatearcommons_repo_dir)

snakemake.output.pca_object = os.path.abspath(snakemake.output.pca_object)

# run shell in temporary directory created with tempfile
with tempfile.TemporaryDirectory() as tmpdir:

    _notebook_tmp = Path(tmpdir, os.path.basename(_notebook)).absolute()
    _notebook_filename = Path(_notebook).name
    # replace suffix of notebook with output format
    _notebook_output = _notebook_tmp.with_suffix(f".{snakemake.params.output_format}")

    _exclusion_variants = os.path.abspath(snakemake.input.exclusion_variants_bedfile)
    _repeat_rds = os.path.abspath(snakemake.input.repeats_rds)
    copyfile(_notebook, _notebook_tmp)

    shell(
        "cd {tmpdir} &&     "
        "quarto render {_notebook_filename} "
        "--to {snakemake.params.output_format} "
        "-P input_files={input_files_str} "
        "-P exclusion_variants_bedfile={_exclusion_variants} "
        "-P genomicranges_repeats_rdsfile={_repeat_rds} "
        "-P output_pca_object_rds={snakemake.output.pca_object} "
        "-P wheatearcommons_repo_dir={wheatearcommons_repo_dir} "
    )

    copyfile(_notebook_output, snakemake.output[0])
