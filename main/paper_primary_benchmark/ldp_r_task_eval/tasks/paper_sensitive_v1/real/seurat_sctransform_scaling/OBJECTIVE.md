# Paper-sensitive R-task: seurat_sctransform_scaling

**Design intent:** the **Seurat v3/v4/5** paper argues for **SCTransform** as a replacement for `NormalizeData` + `ScaleData` in many settings. The agent might default to the old pattern.

**Conceptual source:** `epigen-scrnaseq_processing_seurat-finish`.

## Your goal

You are given an **RDS** or **MTX + barcodes** minimal dataset in `input/` (see `input/README.md`).

- Load in **Seurat**.
- You **must** use **`SCTransform`** (not `LogNormalize` pipeline) to normalize / stabilize variance, at least for the RNA assay.
- Identify **at least 5 variable features**; export the **top 20** by `variance` or SCT metric as:
  - `output/hvg_top.tsv` with columns: `feature,rank,metric_value`

**Constraint:** the `submit_done` message must list the **exact SCTransform** parameters you used (`vst.flavor` if any).

## Deliverables

- `output/hvg_top.tsv`

Then `submit_done(success=true)`.
