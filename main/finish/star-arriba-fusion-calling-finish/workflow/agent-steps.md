# star-arriba-fusion-calling-finish LLM Execution Spec

## Purpose

- Source repository: `snakemake-workflows__star-arriba-fusion-calling`
- Source snakefile: `../workflow_candidates/snakemake-workflows__star-arriba-fusion-calling/workflow/Snakefile`
- This generated finish workflow exposes the source workflow as stepwise checkpoints.
- Each step corresponds to one source rule or checkpoint discovered from the source Snakemake workflow.

## Operating Rules

- Execute steps in listed order.
- Treat the source workflow as the implementation source of truth.
- Do not mutate the source workflow structure during execution.
- Stop on failure and report the exact source rule that could not be reached.

## Step Order

1. `get_genome_fasta`
2. `get_genome_gtf`
3. `star_index`
4. `star_align`
5. `arriba`
6. `index_fusion_bams`
7. `draw_fusions`
8. `all`
