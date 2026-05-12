# Paper-sensitive R-task: seurat_integration_method

**Design intent:** **batch integration** in Seurat — **CCA** vs **RPCA** (reciprocal PCA) anchors. The default integration path is not always best for **large** or **dense** datasets; the Seurat paper discusses integration strategies.

**Conceptual source:** `epigen-scrnaseq_processing_seurat-finish`.

## Your goal

You are given **two** count matrices in `input/` (batch1 / batch2) with shared genes — see `input/README.md`.

- Build a **merged Seurat** object, split by batch, **normalize** with **LogNormalize** for integration prep (or SCT per batch if you document a coherent pipeline).
- Run `FindIntegrationAnchors` with **`reduction = "rpca"`** (not the default CCA) **unless** you document a convincing reason; the **intended** solution is RPCA anchors.
- **IntegrateData** / downstream must yield a non-empty embedding.

Export a **summary table** of integration quality (lightweight, deterministic):

- `output/integration_metrics.tsv` with at least:  
  `k_anchor, reduction_used, n_cells_batch1, n_cells_batch2, k.nn`  
  and two numeric scores you compute in-R (e.g. **Silhouette** on a quick PCA of batch label — implement anything reproducible; reference run will match).

> Note: the benchmark will not pixel-match UMAP; it scores TSVs.

## Deliverables

- `output/integration_metrics.tsv`

Then `submit_done(success=true)`.
