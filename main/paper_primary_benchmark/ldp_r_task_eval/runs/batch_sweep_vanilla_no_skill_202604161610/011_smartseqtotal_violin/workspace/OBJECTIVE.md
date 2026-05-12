# Real R-task: smartseqtotal_violin

**Pipeline provenance:** `gersteinlab-ASTRO` (family: `scrna`).
This workspace is derived from a real R script in the source workflow. The ground-truth
reference output used for offline scoring lives outside this workspace and is not
accessible to you during execution.

## Your goal

You are given three per-metric TSVs under `cache/` (relative to the working dir):
  - `cache/df_silhouette1012.tsv`
  - `cache/df_calinski1012.tsv`
  - `cache/df_davies1012.tsv`
Each has columns `down, data_type, value` with `data_type` in {`astro`,
`spaceranger`} and `down == 0.5`.

Render the benchmark figure at `output/violin_scores.png` (2400x1200 px) with a
three-panel violin (Silhouette, Calinski-Harabasz, Davies-Bouldin), one panel per
metric, showing ASTRO vs spaceranger side by side. Include the Wilcoxon
`stat_compare_means` p-value bracket, Set3 fill palette, and `theme_pubclean`.

## Deliverables

- At least `output/violin_scores.png` must exist when you submit.
- Full output set expected: violin_scores.png under `output/`.

When the deliverables are in `output/`, call `submit_done(success=true)` with a short
summary of how you solved it.
