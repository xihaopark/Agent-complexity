# RNA-seq STAR DESeq2 finish workflow

This workflow is already split into explicit Snakemake step files under `steps/`.

Run order:

1. `trimming`
2. `alignment`
3. `rseqc_qc`
4. `multiqc_report`
5. `count_matrix`
6. `differential_expression`
7. `pca_plot`

Each step uses:

- `config_basic/config.yaml`
- local reads under `ngs-test-data/reads/`
- local references under `resources/`

The step runner should execute the specific snakefile for that step and keep the working directory inside this workflow folder.

Execution requirements:

- Do not call bare `snakemake`.
- Do not create a workflow-specific Snakemake environment.
- Always use the shared conda environment named `snakemake`.
- Always import `os`, `sys`, `tempfile`, `subprocess`, and `shutil` when generating a Python runner script.
- Always set the working directory to this workflow folder: `/lab_workspace/projects/Agent-complexity/main/finish/rna-seq-star-deseq2-finish`
- Execute Snakemake via `conda run -n snakemake python -m snakemake`.
- For the current step, use:
  `conda, "run", "-n", "snakemake", "python", "-m", "snakemake", "--snakefile", "steps/<step>.smk", "--configfile", "config_basic/config.yaml", "--cores", "1", "--directory", "."`
- Run one step at a time in the exact order listed above.
