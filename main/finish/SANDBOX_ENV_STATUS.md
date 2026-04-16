# Sandbox Environment Status

- 更新时间: 2026-04-16T06:17:28.585388+00:00
- 宿主 snakemake 环境就绪: True
- special env 成功数: 0
- Snakemake prewarm 成功 workflow 数: 0

## Special Envs

| Env | Ready | Detail |
|---|---|---|

## Workflow Readiness

| Workflow | Ready | Command envs | Snakemake prewarm | Detail |
|---|---|---|---|---|
| `akinyi-onyango-rna_seq_pipeline-finish` | True | - | False | no command envs; snakemake prewarm input-gated; prewarm_input_gated: command failed (1): /root/miniconda3/bin/conda run -n snakemake python -m snakemake -s /lab_workspace/projects/Agent-complexity/main/finish/workflow_candidates/Akinyi-Onyango__rna_seq_pipeline/Snakefile --directory /lab_workspace/projects/Agent-complexity/main/finish/workflow_candidates/Akinyi-Onyango__rna_seq_pipeline --cores 1 --use-conda --conda-create-envs-only --scheduler greedy all
Building DAG of jobs...
MissingInputException in rule quality_filtering in file "/lab_workspace/projects/Agent-complexity/main/finish/workflow_candidates/Akinyi-Onyango__rna_seq_pipeline/Snakefile", line 36:
Missing input files for rule quality_filtering:
    output: data/trimmed/sample_0_trimmed.fastq.gz
    wildcards: sample=sample_0
    affected files:
        data/raw/sample_0.fastq.gz
ERROR conda.cli.main_run:execute(142): `conda run python -m snakemake -s /lab_workspace/projects/Agent-complexity/main/finish/workflow_candidates/Akinyi-Onyango__rna_seq_pipeline/Snakefile --directory /lab_workspace/projects/Agent-complexity/main/finish/workflow_candidates/Akinyi-Onyango__rna_seq_pipeline --cores 1 --use-conda --conda-create-envs-only --scheduler greedy all` failed. (See above for error) |
