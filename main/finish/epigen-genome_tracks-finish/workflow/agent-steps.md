# epigen-genome_tracks-finish LLM Execution Spec

## Purpose

- Source repository: `epigen__genome_tracks`
- Source snakefile: `../workflow_candidates/epigen__genome_tracks/workflow/Snakefile`
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
3. `annot_export`
4. `gene_list_export`
5. `make_bed`
6. `split_sc_bam`
7. `merge_bams`
8. `coverage`
9. `ucsc_hub`
10. `plot_tracks`
11. `igv_report`
12. `all`
