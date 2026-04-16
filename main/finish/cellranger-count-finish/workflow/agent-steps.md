# cellranger-count-finish LLM Execution Spec

## Purpose

- Source repository: `snakemake-workflows__cellranger-count`
- Source snakefile: `../workflow_candidates/snakemake-workflows__cellranger-count/workflow/Snakefile`
- This generated finish workflow exposes the source workflow as stepwise checkpoints.
- Each step corresponds to one source rule or checkpoint discovered from the source Snakemake workflow.

## Operating Rules

- Execute steps in listed order.
- Treat the source workflow as the implementation source of truth.
- Do not mutate the source workflow structure during execution.
- Stop on failure and report the exact source rule that could not be reached.

## Step Order

1. `follow_pedantic_cell_ranger_naming_scheme`
2. `create_cellranger_library_csv`
3. `cellranger_count`
4. `all`
