# dwheelerau-snakemake-rnaseq-counts-finish LLM Execution Spec

## Purpose

- Source repository: `dwheelerau__snakemake-rnaseq-counts`
- Source snakefile: `../workflow_candidates/dwheelerau__snakemake-rnaseq-counts/Snakefile`
- This generated finish workflow exposes the source workflow as stepwise checkpoints.
- Each step corresponds to one source rule or checkpoint discovered from the source Snakemake workflow.

## Operating Rules

- Execute steps in listed order.
- Treat the source workflow as the implementation source of truth.
- Do not mutate the source workflow structure during execution.
- Stop on failure and report the exact source rule that could not be reached.

## Step Order

1. `project_setup`
2. `make_index`
3. `qc_trim`
4. `aln`
5. `sam_to_bam`
6. `do_counts`
7. `log_count_result`
8. `make_latex_tables`
9. `clean`
10. `all`
