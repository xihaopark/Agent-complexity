# cite-seq-alevin-fry-seurat-finish LLM Execution Spec

## Purpose

- Source repository: `snakemake-workflows__cite-seq-alevin-fry-seurat`
- Source snakefile: `../workflow_candidates/snakemake-workflows__cite-seq-alevin-fry-seurat/workflow/Snakefile`
- This generated finish workflow exposes the source workflow as stepwise checkpoints.
- Each step corresponds to one source rule or checkpoint discovered from the source Snakemake workflow.

## Operating Rules

- Execute steps in listed order.
- Treat the source workflow as the implementation source of truth.
- Do not mutate the source workflow structure during execution.
- Stop on failure and report the exact source rule that could not be reached.

## Step Order

1. `get_sra`
2. `get_genome`
3. `get_annotation`
4. `get_geneid2name`
5. `build_splici_transcriptome`
6. `spoof_t2g`
7. `salmon_index`
8. `salmon_alevin`
9. `alevin_fry_preprocess`
10. `alevin_fry_quant`
11. `seurat`
12. `plot_initial_hto_counts`
13. `filter_normalize_demux`
14. `plot_counts_hto_filtered`
15. `filter_negatives`
16. `plot_umap_singlets_doublets`
17. `filter_to_singlets`
18. `all`
