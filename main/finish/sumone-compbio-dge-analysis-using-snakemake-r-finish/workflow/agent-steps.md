# sumone-compbio-dge-analysis-using-snakemake-r-finish LLM Execution Spec

## Purpose

- Source repository: `sumone-compbio__DGE-Analysis-using-Snakemake-R`
- Source snakefile: `../workflow_candidates/sumone-compbio__DGE-Analysis-using-Snakemake-R/Snakefile`
- This generated finish workflow exposes the source workflow as stepwise checkpoints.
- Each step corresponds to one source rule or checkpoint discovered from the source Snakemake workflow.

## Operating Rules

- Execute steps in listed order.
- Treat the source workflow as the implementation source of truth.
- Do not mutate the source workflow structure during execution.
- Stop on failure and report the exact source rule that could not be reached.

## Step Order

1. `deseq2`
2. `volcano`
3. `gsea`
4. `all`
