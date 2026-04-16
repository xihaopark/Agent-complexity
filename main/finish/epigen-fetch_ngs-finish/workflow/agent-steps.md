# epigen-fetch_ngs-finish LLM Execution Spec

## Purpose

- Source repository: `epigen__fetch_ngs`
- Source snakefile: `../workflow_candidates/epigen__fetch_ngs/workflow/Snakefile`
- This generated finish workflow exposes the source workflow as stepwise checkpoints.
- Each step corresponds to one source rule or checkpoint discovered from the source Snakemake workflow.

## Operating Rules

- Execute steps in listed order.
- Treat the source workflow as the implementation source of truth.
- Do not mutate the source workflow structure during execution.
- Stop on failure and report the exact source rule that could not be reached.

## Step Order

1. `env_export`
2. `config_export`
3. `iseq_download`
4. `fastq_to_bam`
5. `fetch_file`
6. `merge_metadata`
7. `all`
