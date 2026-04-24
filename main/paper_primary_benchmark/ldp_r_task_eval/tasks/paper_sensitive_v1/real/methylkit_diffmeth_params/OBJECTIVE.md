# Paper-sensitive R-task: methylkit_diffmeth_params

**Design intent:** **methylKit** differential methylation has tunable **test** and **overdispersion** settings; defaults may not match the simulation. The benchmark uses **TSV outputs** (not RDS) for scoring stability.

> **Paper hygiene:** replace any MethPat-only PDF with the **methylKit** methods paper / vignette in the PDF pipeline before running experiments.

**Conceptual source:** `fritjoflammers-snakemake-methylanalysis-finish`.

## Your goal

You are given **region-level methylation** summaries in `input/`:

- `input/regions.tsv` — columns `chr,start,end,sample_id,meth,unmeth,coverage` (long format) **or** a path to per-sample bedGraph-style files listed in `input/manifest.txt`.

Compute **region-level differential methylation** using **methylKit**-compatible objects:

- You must document `calculateDiffMeth`-style inference with explicit choices for **`test`** (e.g. Fisher vs Chisq) and **overdispersion** (`"MN"` vs `"shrinkMN"` vs none) appropriate for the **coverage distribution** in the data.

Export:

- `output/diff_meth.tsv` with columns at minimum: `chr,start,end,meth.diff,pvalue,qvalue`

## Deliverables

- `output/diff_meth.tsv`

Then `submit_done(success=true)`.
