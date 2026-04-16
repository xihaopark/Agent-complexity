# chandanbfx-scrna-seq-seurat-workflow-finish LLM Execution Spec

## Purpose

- Source repository: `chandanbfx__scRNA-seq-Seurat-Workflow`
- Source snakefile: `../workflow_candidates/chandanbfx__scRNA-seq-Seurat-Workflow/Snakefile`
- This generated finish workflow exposes the source workflow as stepwise checkpoints.
- Each step corresponds to one source rule or checkpoint discovered from the source Snakemake workflow.

## Operating Rules

- Execute steps in listed order.
- Treat the source workflow as the implementation source of truth.
- Do not mutate the source workflow structure during execution.
- Stop on failure and report the exact source rule that could not be reached.

## Step Order

1. `create_seurat_object`
2. `qc`
3. `normalization`
4. `batch_correction`
5. `dimreduction`
6. `clustering`
7. `marker_genes`
8. `annotation`
9. `generate_summary`
10. `all`
